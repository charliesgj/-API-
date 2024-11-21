import iFinDPy
import datetime

import numpy as np
import pandas as pd


def login():
    iFinDPy.THS_iFinDLogout()
    # 输入用户的帐号和密码
    thsLogin = iFinDPy.THS_iFinDLogin("cjfco2002", "yjzxb1")
    if thsLogin != 0:
        print('登录失败')
    else:
        print('登录成功')


def getindex(ts_code, num):  # ts_code='000001.SH'

    #    import time
    StartDate = datetime.datetime.strftime(datetime.datetime.today()
                                           - datetime.timedelta(days=500), "%Y-%m-%d")
    price_df = iFinDPy.THS_HQ(ts_code, 'close', '', StartDate,
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


def getindex_season(ts_code):  # ts_code='000001.SH'
    """先取前1000天数据，这其中肯定有不止500个交易日，所以我们取最新500个有基差数据的日期"""
    StartDate = datetime.datetime.strftime(datetime.datetime.today()
                                           - datetime.timedelta(days=1000), "%Y-%m-%d")
    price_df = iFinDPy.THS_HQ(ts_code, 'close', '', StartDate,
                              datetime.datetime.today().strftime('%Y-%m-%d')).data
    print(ts_code)
    price_df = price_df.rename(columns={'thscode': 'ts_code',
                                        'time': 'Date'})
    price_df = price_df.sort_values(by=['Date'], ascending=True).dropna().reset_index(drop=True)
    price_df['trade_date'] = price_df.Date.str.replace('-', '')
    price_df['Date'] = price_df['Date'].astype('datetime64[ns]')
    price_df = price_df.dropna().tail(250)
    price_df.set_index("Date", inplace=True)
    return price_df


def getindex_pe_pb():
    #上证指数,创业板指,深证成指,上证50,沪深300,中证500,中证1000
    #000001.SH,399006.SZ,399001.SZ,000016.SH,000300.SH,,000905.SH,000852.SH
    today = datetime.datetime.today()
    startDate = datetime.datetime.strftime(today - datetime.timedelta(weeks=2), "%Y-%m-%d")
    today = datetime.datetime.today().strftime("%Y-%m-%d")
    szzs = iFinDPy.THS_DS('000001.SH', 'ths_pe_ttm_index;ths_pe_ttm_quantile_index;ths_pb_index;ths_pb_quantile_index',
                          '100,100;100,100;107,100;107', 'Fill:Blank, block:history', startDate, today).data.iloc[-1, :]
    cybz = iFinDPy.THS_DS('399006.SZ', 'ths_pe_ttm_index;ths_pe_ttm_quantile_index;ths_pb_index;ths_pb_quantile_index',
                          '100,100;100,100;107,100;107', 'Fill:Blank, block:history', startDate, today).data.iloc[-1, :]
    szcz = iFinDPy.THS_DS('399001.SZ', 'ths_pe_ttm_index;ths_pe_ttm_quantile_index;ths_pb_index;ths_pb_quantile_index',
                          '100,100;100,100;107,100;107', 'Fill:Blank, block:history', startDate, today).data.iloc[-1, :]
    sz50 = iFinDPy.THS_DS('000016.SH', 'ths_pe_ttm_index;ths_pe_ttm_quantile_index;ths_pb_index;ths_pb_quantile_index',
                          '100,100;100,100;107,100;107', 'Fill:Blank, block:history', startDate, today).data.iloc[-1, :]
    hs300 = iFinDPy.THS_DS('000300.SH', 'ths_pe_ttm_index;ths_pe_ttm_quantile_index;ths_pb_index;ths_pb_quantile_index',
                           '100,100;100,100;107,100;107', 'Fill:Blank, block:history', startDate, today).data.iloc[-1,
            :]
    zz500 = iFinDPy.THS_DS('000905.SH', 'ths_pe_ttm_index;ths_pe_ttm_quantile_index;ths_pb_index;ths_pb_quantile_index',
                           '100,100;100,100;107,100;107', 'Fill:Blank, block:history', startDate, today).data.iloc[-1,
            :]
    zz1000 = iFinDPy.THS_DS('000852.SH',
                            'ths_pe_ttm_index;ths_pe_ttm_quantile_index;ths_pb_index;ths_pb_quantile_index',
                            '100,100;100,100;107,100;107', 'Fill:Blank, block:history', startDate, today).data.iloc[-1,
             :]
    df = pd.concat([szzs, sz50, hs300, zz1000, zz500, szcz, cybz], axis=1).T
    df.drop(columns=["time", "thscode"], inplace=True)
    df.columns = ["PE", "分位数", "PB", "分位数"]
    df.index = ["上证指数", "创业板指", "深证成指", "上证50", "沪深300", "中证500", "中证1000"]
    df= df.astype(float).round(2)
    return df

def getindex_change_vol(index, startDate, today):
    df = iFinDPy.THS_DS(index,'ths_close_price_index;ths_chg_ratio_index;ths_vol_index;ths_trans_amt_index', ';;;', 'block:history',
                          startDate, today).data.iloc[-2:,:]
    df["成交量变化"] = ((df["ths_vol_index"]/df["ths_vol_index"].shift(1)-1) * 100).round(2).astype(str) + '%'
    df = df.rename(columns = {"ths_close_price_index":"收盘价",
                        "ths_chg_ratio_index":"日涨跌幅",
                        "ths_vol_index":"日成交量",
                         "ths_trans_amt_index":"日成交额"})
    df["结算价"] = np.nan
    df["持仓量"] = np.nan
    df["持仓变化"] = np.nan
    df["基差"] = np.nan
    df = df.loc[:,["结算价","收盘价","日涨跌幅","日成交量","成交量变化","日成交额","持仓量","持仓变化","基差"]]
    df = df.iloc[-1,:]
    return df

def getfutures_change_vol_oi(index, startDate, today):
    df = iFinDPy.THS_DS(index,'ths_settle_future;ths_close_price_future;ths_chg_ratio_future;ths_vol_future;ths_amt_future;ths_open_interest_future;ths_basis_future',
                        ';;;;;;', '', startDate, today).data.iloc[-2:,:]
    df["成交量变化"] = ((df["ths_vol_future"]/df["ths_vol_future"].shift(1)-1) * 100).round(2).astype(str) + '%'
    df["持仓变化"] = ((df["ths_open_interest_future"]/df["ths_open_interest_future"].shift(1)-1) * 100).round(2).astype(str) + '%'
    #结算价，收盘价，涨跌幅，成交量，成交额，持仓量，基差
    df = df.rename(columns = {"ths_settle_future":"结算价",
                        "ths_close_price_future":"收盘价",
                        "ths_chg_ratio_future":"日涨跌幅",
                         "ths_vol_future":"日成交量",
                         "ths_amt_future":"日成交额",
                         "ths_open_interest_future":"持仓量",
                         "ths_basis_future":"基差"})
    df = df.loc[:,["结算价","收盘价","日涨跌幅","日成交量","成交量变化","日成交额","持仓量","持仓变化","基差"]]
    df = df.iloc[-1,:]
    return df
def getindex_futures_performance():
    #针对上证50、沪深300、中证500、中证1000，我们有收盘价，日涨跌幅，日成交量，日成交金额，还需要再成交量后面加上成交量变化，
    #所以每个种类我们取最新两天数据来计算成交量变化
    today = datetime.datetime.today()
    startDate = datetime.datetime.strftime(today - datetime.timedelta(weeks = 2),"%Y-%m-%d")
    today =  datetime.datetime.today().strftime("%Y-%m-%d")
    sz50 = getindex_change_vol("000016.SH", startDate, today)
    hs300 = getindex_change_vol('000300.SH', startDate, today)
    zz500 = getindex_change_vol('000905.SH', startDate, today)
    zz1000 = getindex_change_vol('000852.SH', startDate, today)
    #针对IH，IF，IC，IC，我们有结算价，收盘价，涨跌幅，成交量，成交额，持仓量，基差，还需要在成交量后面加上成交量变化，在持仓量后面加上持仓量变化
    IC = getfutures_change_vol_oi("IC8888.CFE", startDate, today)
    IF = getfutures_change_vol_oi("IF8888.CFE", startDate, today)
    IH = getfutures_change_vol_oi("IH8888.CFE", startDate, today)
    IM = getfutures_change_vol_oi("IM8888.CFE", startDate, today)
    df = pd.concat([sz50, IH, hs300, IF, zz500, IC, zz1000, IM], axis = 1).T
    df.index = ["上证50","IH", "沪深300", "IF", "中证500", "IC", "中证1000","IM"]
    df.loc[:,["结算价","收盘价","日涨跌幅","基差"]] = df.loc[:,["结算价","收盘价","日涨跌幅","基差"]].astype(float).round(2)
    df.loc[:, ["日成交量", "日成交额"]] = df.loc[:,["日成交量","日成交额"]].astype(float).round(0)
    df = df.replace(np.nan, "")
    return df

