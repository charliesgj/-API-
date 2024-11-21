import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import percentileofscore
from getiFind import getindex


def plot4(ts_codes=None, num=125, filename = "plot4.png"):
    """
    ts_codes: 四个主连合约的代码
    num:时间长短，125为半年
    T、TF、TL、TS两两主力合约之间价差
    时间跨度为半年 上下拼接为 6*1
    显示最新数据所在半年数据中的分位数
    """
    if ts_codes is None:
        ts_codes = ['TZL.CFE', 'TFZL.CFE', 'TLZL.CFE', 'TSZL.CFE']
    plt.rcParams['font.family'] = ['Microsoft YaHei']
    df_dict = {}
    for ts_code in ts_codes:
        df_dict[ts_code] = getindex(ts_code=ts_code, num=num)
    T_df = df_dict['TZL.CFE'].loc[:, 'close']
    TF_df = df_dict['TFZL.CFE'].loc[:, 'close']
    TL_df = df_dict['TLZL.CFE'].loc[:, 'close']
    TS_df = df_dict['TSZL.CFE'].loc[:, 'close']
    T_TF_df = pd.DataFrame(T_df - TF_df, index=df_dict['TZL.CFE'].index)
    T_TL_df = pd.DataFrame(T_df - TL_df, index=df_dict['TZL.CFE'].index)
    T_TS_df = pd.DataFrame(T_df - TS_df, index=df_dict['TZL.CFE'].index)
    TF_TL_df = pd.DataFrame(TF_df - TL_df, index=df_dict['TFZL.CFE'].index)
    TF_TS_df = pd.DataFrame(TF_df - TS_df, index=df_dict['TFZL.CFE'].index)
    TL_TS_df = pd.DataFrame(TL_df - TS_df, index=df_dict['TLZL.CFE'].index)
    dfs = [T_TF_df, T_TL_df, T_TS_df, TF_TL_df, TF_TS_df, TL_TS_df]
    fig, axes = plt.subplots(3, 2, figsize=(10, 10))
    name_dict = {1: "T-TF", 2: "T-TL", 3: "T-TS", 4: "TF-TL", 5: "TF-TS", 6: "TL-TS"}
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
