import datetime
import re
from collections import OrderedDict

import numpy as np
from iFinDPy import THS_iFinDLogout, THS_iFinDLogin, THS_HQ, THS_DS, THS_BD, THS_RQ

from get_contracts_list import *


def get_data_for_variety(variety_name, contract_type, option_type, dom=None, subdom=None):
    # 获取主力或次主力合约的全部call或put的名称列表
    #variety_name = ["HO","IO","MO" ]
    #HO为上证50，IO为沪深300， MO为中证1000
    if dom is None and subdom is None:
        dom, subdom = get_current_dom_subdom_month()
    contract_names = get_contract_names(variety_name, dom, subdom)
    # 遍历合约名称列表，获取对应的成交量和持仓量数据，并填充数据结构
    data_structure = {
        contract_name: {} for contract_name in contract_names
    }
    for contract_name in contract_names:
        data_structure[contract_name] = get_data_for_contract(contract_name)
    return data_structure


def generate_variety_data(dom=None, subdom=None):
    if dom is None and subdom is None:
        dom, subdom = get_current_dom_subdom_month()
    name_to_code = {"上证50": "HO", "沪深300": "IO", "中证1000": "MO"}
    #主力次主力合约为实时更新的
    data = {
        variety: {
            contract_type: {
                option_type: {} for option_type in ["call", "put"]
            } for contract_type in [dom, subdom]
        } for variety in ["上证50", "沪深300", "中证1000"]
    }

    for variety in name_to_code.keys():
        for contract_type in [dom, subdom]:
            for option_type in ["call", "put"]:
                data[variety][contract_type][option_type] = get_data_for_variety(name_to_code[variety],
                                                                                 contract_type, option_type)
    return data

#####待修改的 第一个pc画图########
def get_daily_pc(date_string):
    #取出每日三个品种，各自主力与次主力合约的成交量pc和持仓量pc，存入字典，共3*2*2 = 12个值
    #由于对所有该品种的主力/次主力合约取出的数值都是相同的，所以我们只需要一个主力合约/次主力合约的名字
    dom_HO = get_index_dom_now("HO", dom_True=True)[0]
    dom_IO = get_index_dom_now("IO", dom_True=True)[0]
    dom_MO = get_index_dom_now("MO", dom_True=True)[0]
    subdom_HO = get_index_dom_now("HO", dom_True=False)[0]
    subdom_IO = get_index_dom_now("IO", dom_True=False)[0]
    subdom_MO = get_index_dom_now("MO", dom_True=False)[0]
    pc_dict = {"沪深300": {
        "主力name": dom_IO,
        "次主力name": subdom_IO,
        "主力": {"成交量pc": None, "持仓量pc": None},
        "次主力": {"成交量pc": None, "持仓量pc": None}
    },
        "上证50": {
            "主力name": dom_HO,
            "次主力name": subdom_HO,
            "主力": {"成交量pc": None, "持仓量pc": None},
            "次主力": {"成交量pc": None,  "持仓量pc": None}
        },
        "中证1000": {
            "主力name": dom_MO, "次主力name": subdom_MO,
            "主力": {"成交量pc": None,  "持仓量pc": None},
            "次主力": {"成交量pc": None, "持仓量pc": None}
        }
    }

    for index in pc_dict.keys():
        dom_temp = THS_BD(pc_dict[index]["主力name"],
                          'ths_option_month_volume_pcr_option;ths_option_month_oi_pcr_option',
                          f"{date_string};{date_string}").data.iloc[0, :]
        pc_dict[index]["主力"]["成交量pc"] = dom_temp['ths_option_month_volume_pcr_option']
        pc_dict[index]["主力"]["持仓量pc"] = dom_temp['ths_option_month_oi_pcr_option']

        subdom_temp = THS_BD(pc_dict[index]["次主力name"],
                             'ths_option_month_volume_pcr_option;ths_option_month_oi_pcr_option',
                             f"{date_string};{date_string}").data.iloc[0, :]
        pc_dict[index]["次主力"]["成交量pc"] = subdom_temp['ths_option_month_volume_pcr_option']
        pc_dict[index]["次主力"]["持仓量pc"] = subdom_temp['ths_option_month_oi_pcr_option']
    return pc_dict


def get_monthly_pc():
    #使用get_daily_pc(),获取30个交易日数据列表
    pc_dict = {"沪深300": {
        "主力": {"成交量pc": None,
                 "持仓量pc": None},
        "次主力": {"成交量pc": None,
                   "持仓量pc": None}
    },
        "上证50": {
            "主力": {"成交量pc": None,
                     "持仓量pc": None},
            "次主力": {"成交量pc": None,
                       "持仓量pc": None}
        },
        "中证1000": {
            "主力": {"成交量pc": None,
                     "持仓量pc": None},
            "次主力": {"成交量pc": None,
                       "持仓量pc": None}
        }
    }
    today = datetime.datetime.today()
    date_list = []
    #获得一个一百日日期列表,直到今天,因为我们要的是30个交易日
    for i in range(70, -1, -1):
        date = today - datetime.timedelta(days=i)
        date = date.strftime("%Y-%m-%d")
        date_list.append(date)
    date_dict = OrderedDict()
    for date in date_list:
        date_dict[date] = get_daily_pc(date)
        #如果该日没有数据,删除这一天
        if date_dict[date]["沪深300"]["主力"]["成交量pc"] is None:
            del date_dict[date]
    return date_dict


#login()
#print(get_implied_volatility('HO2406-C-2500.CFE'))