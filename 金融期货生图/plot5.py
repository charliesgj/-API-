import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import percentileofscore
from getiFind import getindex


def plot5(ts_codes=None, num=125, filename="plot5.png"):
    """
    T、TF、TL、TS各自主力合约和对应指数之间期现基差
    时间跨度为半年 上下拼接为 4*1
    显示最新数据所在半年数据中的分位数
    """
    if ts_codes is None:
        ts_codes = ['TZL.CFE', 'TFZL.CFE', 'TLZL.CFE', 'TSZL.CFE', 'T8888.CFE', 'TF8888.CFE', 'TL8888.CFE',
                    'TS8888.CFE']
    plt.rcParams['font.family'] = ['Microsoft YaHei']
    df_dict = {}
    for ts_code in ts_codes:
        df_dict[ts_code] = getindex(ts_code=ts_code, num=num)
    T_df = pd.DataFrame(df_dict['T8888.CFE'].loc[:, 'close'] - df_dict['TZL.CFE'].loc[:, 'close'],
                        index=df_dict['TZL.CFE'].index)
    TF_df = pd.DataFrame(df_dict['TF8888.CFE'].loc[:, 'close'] - df_dict['TFZL.CFE'].loc[:, 'close'],
                         index=df_dict['TFZL.CFE'].index)
    TS_df = pd.DataFrame(df_dict['TS8888.CFE'].loc[:, 'close'] - df_dict['TSZL.CFE'].loc[:, 'close'],
                         index=df_dict['TSZL.CFE'].index)
    TL_df = pd.DataFrame(df_dict['TL8888.CFE'].loc[:, 'close'] - df_dict['TLZL.CFE'].loc[:, 'close'],
                         index=df_dict['TLZL.CFE'].index)

    dfs = [T_df, TF_df, TS_df, TL_df]
    fig, axes = plt.subplots(2, 2, figsize=(10, 10))
    name_dict = {1: "T基差", 2: "TF基差", 3: "TS基差", 4: "TL基差"}
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
