from ths_data import *
import numpy as np
from df_to_png import df_to_png
import matplotlib.pyplot as plt
import datetime
import pandas as pd
#标的指数的30日历史波动率 60日历史波动率 90日历史波动率
#标的指数共4个 故共计算12个值 表格输出到word文档中

today = datetime.datetime.today().date()
def calculate_rolling_volatility(df, window):
    df['log_return'] = np.log(df['close'] / (df['close'].shift(1)))
    df['volatility'] = df['log_return'].rolling(window=window).std() * np.sqrt(252)
    df = df.drop(columns=['log_return'])
    return df


def cal_wrt_index_volatility():
    indexes = ['IC', 'IF', 'IH', 'IM']
    dfs = {}
    for index in indexes:
        dfs[index] = getindex(f"{index}8888.CFE", num=100)
        dfs[index] = dfs[index][["close"]]

    days = [30, 60, 90]
    volatility = {index: {} for index in indexes}
    for index in indexes:
        for day in days:
            volatility[index][day] = calculate_rolling_volatility(dfs[index], day).iloc[-1, -1]

    volatility = pd.DataFrame.from_dict(volatility, orient="index")
    volatility = volatility.rename(
        index={"IC": "中证500指数", "IF": "沪深300指数", "IH": "上证50指数", "IM": "中证1000指数"},
        columns={30: "30日历史波动率", 60: "60日历史波动率", 90: "90日历史波动率"})
    volatility = volatility.map(lambda x: f"{x:.2%}")
    return volatility


def plot_index_his_volatility():
    print("####################################################正在绘制标的指数历史波动率表格####################################################")
    df = cal_wrt_index_volatility()
    print(df)
    plt.rcParams["font.family"] = "Microsoft YaHei"
    fig, ax = plt.subplots(figsize=(15, 10))
    ax.axis('off')
    table = ax.table(cellText=df.values, colLabels=df.columns, rowLabels=df.index, loc='center', cellLoc='center')

    # 在第一行第一列（索引为(0, 0)）添加当日日期
    table.add_cell(0, -1, width=0.05, height=0.0215, text=today, loc='left')

    # 调整表格的布局
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1, 2)
    # 添加标题
    plt.title("表3：指数历史波动率")
    plt.tight_layout()
    plt.savefig('标的指数历史波动率.png', bbox_inches='tight')
