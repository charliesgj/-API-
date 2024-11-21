import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import percentileofscore
from getiFind import getindex


def plot1(ts_codes=None, num=125, filename = "plot1.png"):
    """
    ts_codes: 四个主连合约的代码
    num:时间长短，125为半年
    IF、IC、IH、IM两两主力合约之间价差
    时间跨度为半年 上下拼接为 6*1
    显示最新数据所在半年数据中的分位数
    """
    if ts_codes is None:
        ts_codes = ['ICZL.CFE', 'IFZL.CFE', 'IHZL.CFE', 'IMZL.CFE']
    plt.rcParams['font.family'] = ['Microsoft YaHei']
    df_dict = {}
    for ts_code in ts_codes:
        df_dict[ts_code] = getindex(ts_code=ts_code, num=num)
    IF_IC_df = pd.DataFrame(df_dict['IFZL.CFE'].loc[:, 'close'] - df_dict['ICZL.CFE'].loc[:, 'close'],
                            index=df_dict['IFZL.CFE'].index)
    IF_IH_df = pd.DataFrame(df_dict['IFZL.CFE'].loc[:, 'close'] - df_dict['IHZL.CFE'].loc[:, 'close'],
                            index=df_dict['IFZL.CFE'].index)
    IF_IM_df = pd.DataFrame(df_dict['IFZL.CFE'].loc[:, 'close'] - df_dict['IMZL.CFE'].loc[:, 'close'],
                            index=df_dict['IFZL.CFE'].index)
    IC_IH_df = pd.DataFrame(df_dict['ICZL.CFE'].loc[:, 'close'] - df_dict['IHZL.CFE'].loc[:, 'close'],
                            index=df_dict['ICZL.CFE'].index)
    IC_IM_df = pd.DataFrame(df_dict['ICZL.CFE'].loc[:, 'close'] - df_dict['IMZL.CFE'].loc[:, 'close'],
                            index=df_dict['ICZL.CFE'].index)
    IH_IM_df = pd.DataFrame(df_dict['IHZL.CFE'].loc[:, 'close'] - df_dict['IMZL.CFE'].loc[:, 'close'],
                            index=df_dict['IHZL.CFE'].index)
    dfs = [IF_IC_df, IF_IH_df, IF_IM_df, IC_IH_df, IC_IM_df, IH_IM_df]
    fig, axes = plt.subplots(3, 2, figsize=(10, 10))
    name_dict = {1: "IF-IC", 2: "IF-IH", 3: "IF-IM", 4: "IC-IH", 5: "IC-IM", 6: "IH-IM"}
    for i, ax in enumerate(axes.flatten()):
        df = dfs[i]
        ax.plot(df.index, df['close'], label='close')
        ax.set_title(f'主力合约价差 {name_dict[i + 1]}')
        ax.set_xlabel('Date')
        ax.set_ylabel('Close Price')
        plt.xticks(rotation=45)
        plt.tight_layout()

        last_close = df['close'].iloc[-1]
        percentage = percentileofscore(df['close'], last_close)
        text = f'最新价差的分位占比: {percentage:.2f}%'
        ax.annotate(text, xy=(0.75, 0.1), xycoords='axes fraction', ha='center', va='bottom', fontsize=10)

    plt.suptitle("跨品种套利参考", fontsize=16)
    plt.subplots_adjust(top=0.9)
    plt.savefig(filename, bbox_inches='tight')
