import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import percentileofscore
from getiFind import getindex


def plot2(ts_codes=None, num=125,filename = "plot2.png"):
    """
    IF、IC、IH、IM各自主力合约和对应指数之间期现基差
    时间跨度为半年 上下拼接为 4*1
    显示最新数据所在半年数据中的分位数
    """
    if ts_codes is None:
        ts_codes = ['ICZL.CFE', 'IFZL.CFE', 'IHZL.CFE', 'IMZL.CFE', 'IC8888.CFE', 'IF8888.CFE', 'IH8888.CFE',
                    'IM8888.CFE']
    plt.rcParams['font.family'] = ['Microsoft YaHei']
    df_dict = {}
    for ts_code in ts_codes:
        df_dict[ts_code] = getindex(ts_code=ts_code, num=num)
    IF_df = pd.DataFrame(df_dict['IF8888.CFE'].loc[:, 'close'] - df_dict['IFZL.CFE'].loc[:, 'close'],
                         index=df_dict['IFZL.CFE'].index)
    IH_df = pd.DataFrame(df_dict['IH8888.CFE'].loc[:, 'close'] - df_dict['IHZL.CFE'].loc[:, 'close'],
                         index=df_dict['IHZL.CFE'].index)
    IM_df = pd.DataFrame(df_dict['IM8888.CFE'].loc[:, 'close'] - df_dict['IMZL.CFE'].loc[:, 'close'],
                         index=df_dict['IMZL.CFE'].index)
    IC_df = pd.DataFrame(df_dict['IC8888.CFE'].loc[:, 'close'] - df_dict['ICZL.CFE'].loc[:, 'close'],
                         index=df_dict['IHZL.CFE'].index)

    dfs = [IF_df, IH_df, IM_df, IC_df]
    fig, axes = plt.subplots(2, 2, figsize=(10, 10))
    name_dict = {1: "IF基差", 2: "IH基差", 3: "IM基差", 4: "IC基差"}
    for i, ax in enumerate(axes.flatten()):
        df = dfs[i]
        ax.plot(df.index, df['close'], label='close')
        ax.set_title(f'{name_dict[i + 1]}')
        ax.set_xlabel('Date')
        ax.set_ylabel('Close Price')
        plt.xticks(rotation=45)

        plt.tight_layout()

        last_close = df['close'].iloc[-1]
        percentage = percentileofscore(df['close'], last_close)
        text = f'最新价差的分位占比: {percentage:.2f}%'
        ax.annotate(text, xy=(0.75, 0.1), xycoords='axes fraction', ha='center', va='bottom', fontsize=10)

    plt.suptitle("基差数据", fontsize=16)
    plt.subplots_adjust(top=0.9)
    plt.savefig(filename, bbox_inches='tight')
