import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.stats import percentileofscore
from getiFind import getindex_season


def plot3(ts_codes=None, filename="plot3.png"):
    """
    IF、IC、IH、IM各自季月期货合约（3，6，9，12）之间 03-06 06-09 09-12 03-12
    时间跨度为季度 每个标的为一个三维图 横向 2*2拼接"""
    scs = ["IF", "IH", "IM", "IC"]
    if ts_codes is None:
        ts_codes = []
        for sc in scs:
            for tm in ["03", "06", "09", "12"]:
                ts_codes.append(sc + tm + "M.CFE")
    plt.rcParams['font.family'] = ['Microsoft YaHei']
    # 单个标的的字典
    single_dict = {}
    for ts_code in ts_codes:
        single_dict[ts_code] = getindex_season(ts_code=ts_code)

    subtracts = {"03-06": ["03", "06"], "06-09": ["06", "09"], "09-12": ["09", "12"], "12-03": ["12", "03"]}
    # 相减标的的字典
    dfs = {sc: {} for sc in scs}
    for sc in scs:
        for subtract_name, years in subtracts.items():
            col1 = single_dict[sc + years[0] + "M.CFE"].loc[:, 'close']
            col2 = single_dict[sc + years[1] + "M.CFE"].loc[:, 'close']
            index = single_dict[sc + years[0] + "M.CFE"].index
            dfs[sc][subtract_name] = pd.DataFrame(col1 - col2, index=index).dropna().tail(100).reset_index()
            dfs[sc][subtract_name] = dfs[sc][subtract_name].drop(columns={"Date"})
            print(dfs[sc][subtract_name].shape)
            print(dfs[sc][subtract_name])

    fig, axes = plt.subplots(2, 2, figsize=(10, 10), subplot_kw={'projection': '3d'})
    axes = axes.flatten()
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']

    # 先画IF试试水
    for ax, sc in zip(axes, scs):
        percentiles = {}
        textstr = ''
        for i, subtract_name in enumerate(subtracts.keys()):
            percentiles[subtract_name] = percentileofscore(dfs[sc][subtract_name]['close'],
                                                           dfs[sc][subtract_name]['close'].iloc[-1])
            ax.plot(dfs[sc][subtract_name].index,
                    np.full_like(dfs[sc][subtract_name]['close'], i), dfs[sc][subtract_name]['close'],
                    label=subtract_name, color=colors[i])
            textstr += f'{subtract_name} 最新数据分位数: {percentiles[subtract_name]:.2f}%\n'

        ax.set_zlabel('Price')
        ax.set_title(sc, fontsize=12)
        ax.tick_params(axis='x', labelsize=8)  # 设置 x 轴标签字号
        ax.tick_params(axis='y', labelsize=8)  # 设置 y 轴标签字号
        ax.tick_params(axis='z', labelsize=8)
        ax.set_yticks(range(len(subtracts)))
        ax.set_yticklabels(subtracts.keys())
        # 添加文本到每个子图的右侧
        ax.text2D(0, 0.95, textstr, transform=ax.transAxes, fontsize=10, va='top', ha='left')

    # 调整布局以适应文本
    plt.subplots_adjust(right=0.85, top=0.9)
    fig.suptitle("跨月基差", fontsize=16)
    plt.savefig(filename, bbox_inches='tight')
