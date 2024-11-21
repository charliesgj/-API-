import datetime
import re


import numpy as np
from iFinDPy import THS_iFinDLogout, THS_iFinDLogin, THS_HQ, THS_DS, THS_BD, THS_RQ

from get_contracts_list import *


def extract_strike_price(contract_name):
    # 使用正则表达式匹配数字部分，即行权价
    strike_price = re.findall(r'(\d+).CFE', contract_name)
    strike_price = int(strike_price[0])
    return strike_price


def login():
    THS_iFinDLogout()
    # 输入用户的账号和密码
    thsLogin = THS_iFinDLogin("cjfco2002", "yjzxb1")
    if thsLogin != 0:
        print('登录失败')
    else:
        print('登录成功')


def getindex(ts_code, num):  # ts_code='000001.SH'

    #    import time
    StartDate = datetime.datetime.strftime(datetime.datetime.today()
                                           - datetime.timedelta(days=500), "%Y-%m-%d")
    price_df = THS_HQ(ts_code, 'close', '', StartDate,
                      datetime.datetime.today().strftime('%Y-%m-%d')).data
    print(ts_code)
    price_df = price_df.rename(columns={'thscode': 'ts_code',
                                        'time': 'Date'})
    price_df = price_df.sort_values(by=['Date'], ascending=True).dropna().reset_index(drop=True)
    price_df['trade_date'] = price_df.Date.str.replace('-', '')
    price_df['Date'] = price_df['Date'].astype('datetime64[ns]')
    price_df = price_df.tail(num).reset_index(drop=True)
    price_df.set_index("Date", inplace=True)
    return price_df


def get_index_preclose(ts_code):  # ts_code='000001.SH'
    #防止有公休假期 我们把数据提取到两周前
    StartDate = datetime.datetime.strftime(datetime.datetime.today()
                                           - datetime.timedelta(weeks=2), "%Y-%m-%d")
    preClose = THS_HQ(ts_code, 'preClose', '', StartDate,
                      datetime.datetime.today().strftime("%Y-%m-%d")).data.iloc[-1, -1]

    return preClose


def get_data_for_contract(contract_name):
    EndDate = datetime.datetime.today().strftime("%Y-%m-%d")
    StartDate = datetime.datetime.strftime(datetime.datetime.today()
                                           - datetime.timedelta(days=500), "%Y-%m-%d")
    data_structure = {
        '成交量': [],
        '持仓量': []
    }
    all_data = THS_DS(contract_name, 'ths_vol_option;ths_open_interest_option',
                      ';', '', StartDate, EndDate).data.dropna()
    #倒序保存 让最新的数据在第一条 因为数据长度不同，原始数据的第一条并不一定是同一天
    volume_data = all_data["ths_vol_option"].values.tolist().reverse()
    open_interest_data = all_data["ths_open_interest_option"].values.tolist().reverse()
    data_structure['成交量'] = volume_data
    data_structure['持仓量'] = open_interest_data
    return data_structure


def get_volume_open_interest_lists(variety_data, dom=None, subdom=None):
    if dom is None and subdom is None:
        dom, subdom = get_current_dom_subdom_month()

    volume_lists = {variety: {
        contract_type: {
            option_type: [] for option_type in ["call", "put"]
        } for contract_type in [dom, subdom]
    } for variety in ["上证50", "沪深300", "中证1000"]
    }
    open_interest_lists = {variety: {
        contract_type: {
            option_type: [] for option_type in ["call", "put"]
        } for contract_type in [dom, subdom]
    } for variety in ["上证50", "沪深300", "中证1000"]
    }
    #把contract拆散 分别将成交量和持仓量归结到相应的词典中，
    # 数据颗粒度从“上证50-主力-call-HO2406-C-2450.CFE-成交量”还原到如“成交量-上证50-主力-call”
    for variety, value1 in variety_data.items():
        for contract_type, value2 in value1.items():
            for option_type, value3 in value2.items():
                for contract, value4 in value3.items():
                    for name, value_list in value4.items():
                        if name == "成交量":
                            volume_lists[variety][contract_type][option_type].append(value_list)
                        else:
                            open_interest_lists[variety][contract_type][option_type].append(value_list)

    for variety, value1 in variety_data.items():
        for contract_type, value2 in value1.items():
            for option_type, value3 in value2.items():
                #为了加速运算转换为np.array 同时保持维度一致才能转换为array 故padding
                max_length = max(len(row) for row in volume_lists[variety][contract_type][option_type])
                padded_volume = [row + [0] * (max_length - len(row))
                                 for row in volume_lists[variety][contract_type][option_type]]
                volume_lists[variety][contract_type][option_type] = np.array(
                    padded_volume).sum()
                max_length = max(len(row) for row in open_interest_lists[variety][contract_type][option_type])
                padded_open_interest = [row + [0] * (max_length - len(row))
                                        for row in open_interest_lists[variety][contract_type][option_type]]
                open_interest_lists[variety][contract_type][option_type] = np.array(
                    padded_open_interest).sum()
    print(open_interest_lists)
    print(volume_lists)


def get_implied_volatility(index):
    data = THS_RQ(index, 'pre_implied_volatility').data.iloc[0, -1]
    return data


def get_greek_letter(letter, index):
    letter_to_code = {"delta": "ths_delta_option", "theta": "ths_theta_option",
                      "gamma": "ths_gamma_option", "vega": "ths_vega_option",
                      "rho": "ths_rho_option"}
    today = datetime.datetime.strftime(datetime.datetime.today() - datetime.timedelta(days=1), "%Y-%m-%d")
    data = THS_BD(index, letter_to_code[letter],
                  today).data.iloc[-1, -1]
    return data


def get_greek_letter_chg_ratio(letter, index):
    letter_to_code = {"delta": "ths_delta_option", "theta": "ths_theta_option",
                      "gamma": "ths_gamma_option", "vega": "ths_vega_option",
                      "rho": "ths_rho_option"}
    today = datetime.datetime.today() - datetime.timedelta(days=1)
    last_day_data = None
    # 向前取10天的数据，直到取到上一个交易日为止
    for i in range(1, 14):
        last_day = datetime.datetime.strftime(today - datetime.timedelta(days=i), "%Y-%m-%d")
        last_day_data = THS_BD(index, letter_to_code[letter], last_day).data
        if last_day_data is None:
            continue
        else:
            break
    last_day_data = last_day_data.iloc[-1, -1]
    today = today.strftime("%Y-%m-%d")
    today_data = THS_BD(index, letter_to_code[letter], today).data.iloc[-1, -1]
    if last_day_data != 0 and last_day_data is not None and today_data is not None:
        chg_ratio = today_data / last_day_data - 1
    else:
        chg_ratio = np.nan
    return chg_ratio


def get_volume_oi_data(contract_list: list):
    #输入合约名称列表
    #输出两个分别包含其最新成交量和持仓量的df
    #取出的值个数
    num_contracts = len(contract_list)
    contracts = ",".join(contract_list)
    today = datetime.datetime.today()
    startDate = datetime.datetime.strftime(today - datetime.timedelta(days=10), "%Y-%m-%d")
    today = today.strftime("%Y-%m-%d")
    openInterest_df = THS_HQ(contracts, 'openInterest', '', startDate, today).data
    interval = openInterest_df.shape[0] / num_contracts
    newest_records = [-1 + i * interval for i in range(1, num_contracts + 1)]
    openInterest_df = openInterest_df.iloc[newest_records, [1, 2]]
    volume_df = THS_HQ(contracts, "volume", "", startDate, today).data.iloc[newest_records, [1, 2]]
    return volume_df, openInterest_df
