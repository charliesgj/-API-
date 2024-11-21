#股指期货 每个品种 的主力合约和次主力合约的call和put合约 中最大/次大成交量和最大/次大持仓量对应的期权行权价格  （以表格的形式展示）

from ths_data import *
from df_to_png import df_to_png
import matplotlib.pyplot as plt
import pandas as pd
import datetime


def plot_each_amt_strike(volume_df, oi_df, plotname, plottype, ax):
    df = pd.merge(volume_df, oi_df, on="thscode", how="left")
    df["index"] = df['thscode'].apply(lambda x: extract_strike_price(x))
    sorted_by_volume_df = df.sort_values(by="volume", ascending=False).reset_index().iloc[0:20, :]
    sorted_by_oi_df = df.sort_values(by="openInterest", ascending=False).reset_index().iloc[0:20, :]
    print(sorted_by_volume_df)
    top1_oi = sorted_by_oi_df.iloc[0, -1]
    top2_oi = sorted_by_oi_df.iloc[1, -1]
    top1_volume = sorted_by_volume_df.iloc[0, -1]
    top2_volume = sorted_by_volume_df.iloc[1, -1]
    top_values = (top1_oi, top2_oi, top1_volume, top2_volume)

    bar_width = 0.35
    index = range(len(df['thscode']))
    ax.bar([i - bar_width / 2 for i in index], df['volume'], bar_width, label='成交量', color="darkgrey")
    ax.bar([i + bar_width / 2 for i in index], df['openInterest'], bar_width, label='持仓量', color="darkred")
    ax.legend(loc="best")
    ax.set_title(f'{plotname}{plottype}')
    ax.set_xticks(index)
    ax.set_xticklabels(df['index'])
    ax.tick_params(axis='x', rotation=45)
    return ax, top_values


def plot_amt_strike_price():
    plt.rcParams["font.family"] = "Microsoft YaHei"
    print("####################################################正在绘制持仓量成交量排序行权价格"
          "####################################################")
    dom, subdom = get_current_dom_subdom_month()
    index_dict = {"上证50": "HO", "沪深300": "IO", "中证1000": "MO"}
    for name, index in index_dict.items():
        #对主力
        dom_call_list = get_contract_names(index, contract_type=dom, option_type="call")
        dom_call_volume, dom_call_oi = get_volume_oi_data(dom_call_list)

        dom_put_list = get_contract_names(index, contract_type=dom, option_type="put")
        dom_put_volume, dom_put_oi = get_volume_oi_data(dom_put_list)

        #对次主力
        subdom_call_list = get_contract_names(index, contract_type=subdom, option_type="call")
        subdom_call_volume, subdom_call_oi = get_volume_oi_data(subdom_call_list)
        subdom_put_list = get_contract_names(index, contract_type=subdom, option_type="put")
        subdom_put_volume, subdom_put_oi = get_volume_oi_data(subdom_put_list)

        fig, ax = plt.subplots(2, 2, figsize=(15, 10))
        _, top_values_dom_call = plot_each_amt_strike(dom_call_volume, dom_call_oi, name, "主力call", ax[0, 0])
        _, top_values_dom_put = plot_each_amt_strike(dom_put_volume, dom_put_oi, name, "主力put", ax[0, 1])
        _, top_values_subdom_call = plot_each_amt_strike(subdom_call_volume, subdom_call_oi, name, "次主力call",
                                                         ax[1, 0])
        _, top_values_subdom_put = plot_each_amt_strike(subdom_put_volume, subdom_put_oi, name, "次主力put", ax[1, 1])
        today = datetime.datetime.today().date()
        df = pd.DataFrame({
            f"{today} ": ["最大成交量行权价", "次大成交量行权价", "最大持仓量行权价", "次大持仓量行权价"],
            "主力call": [top_values_dom_call[0], top_values_dom_call[1],
                         top_values_dom_call[2], top_values_dom_call[3]],
            "主力put": [top_values_dom_put[0], top_values_dom_put[1], top_values_dom_put[2], top_values_dom_put[3]],
            "次主力call": [top_values_subdom_call[0], top_values_subdom_call[1], top_values_subdom_call[2],
                           top_values_subdom_call[3]],
            "次主力put": [top_values_subdom_put[0], top_values_subdom_put[1], top_values_subdom_put[2],
                          top_values_subdom_put[3]]
        })

        plt.tight_layout()
        plt.savefig(f"{name}持仓成交量.png")
        df_to_png(df, filename=f"{name}行权价数据统计", have_index=True)
