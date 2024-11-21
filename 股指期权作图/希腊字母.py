from category_judgement import *
from ths_data import *
from df_to_png import df_to_png
from copy import deepcopy as dc
import pandas as pd

#每个品种的主力和次主力合约 平值，虚一，虚二，实一，实二的delta, gamma, vega, theta 并计算各自的涨幅
#3个品种，每个有主力和次主力合约，每个主力分为call和put 每个call和put有这五个合约 每个合约有这四个字母 所以要提出3*2*2*5*4个值

def get_greek_letter_df(contract_list, contract_type: str):
    """输入合约名称列表，输出一个df， 是该合约列表的delta,gamma, theta, vega 和rho
    contract_type填写这是call合约还是put合约 用于美化df"""
    delta = [get_greek_letter("delta", i) for i in contract_list]
    delta_chg_ratio = [get_greek_letter_chg_ratio("delta", i) for i in contract_list]
    gamma = [get_greek_letter("gamma", i) for i in contract_list]
    gamma_chg_ratio = [get_greek_letter_chg_ratio("gamma", i) for i in contract_list]
    theta = [get_greek_letter("theta", i) for i in contract_list]
    theta_chg_ratio = [get_greek_letter_chg_ratio("theta", i) for i in contract_list]
    vega = [get_greek_letter("vega", i) for i in contract_list]
    vega_chg_ratio = [get_greek_letter_chg_ratio("vega", i) for i in contract_list]
    rho = [get_greek_letter("rho", i) for i in contract_list]
    rho_chg_ratio = [get_greek_letter_chg_ratio("rho", i) for i in contract_list]
    indexes = [contract_type + i for i in ["平值", "实一", "实二", "虚一", "虚二"]]
    columns = ["delta", "delta涨幅", "gamma", "gamma涨幅", "theta", "theta涨幅", "vega", "vega涨幅", "rho", "rho涨幅"]
    df = pd.DataFrame(
        [delta, delta_chg_ratio, gamma, gamma_chg_ratio, theta, theta_chg_ratio, vega, vega_chg_ratio, rho,
         rho_chg_ratio]).T
    df.index = indexes
    df.columns = columns
    return df


def format_columns(df):
    formatted_df = dc(df)
    formatted_df.iloc[:, [0, 2, 4, 6, 8]] = formatted_df.iloc[:, [0, 2, 4, 6, 8]].astype(float).applymap(lambda x: f"{x:.2f}")
    formatted_df.iloc[:, [1, 3, 5, 7, 9]] = formatted_df.iloc[:, [1, 3, 5, 7, 9]].astype(float).applymap(lambda x: f"{x:.2%}")
    return formatted_df


def plot_greek_letter():
    print("####################################################正在绘制希腊字母表格####################################################")
    dom, subdom = get_current_dom_subdom_month()
    index_dict = {"上证50": "HO", "沪深300": "IO", "中证1000": "MO"}
    for name, index in index_dict.items():
        #对主力
        dom_dict = get_index_contracts_categories_dict(index)[dom]
        dom_call_dict = dom_dict["call"]
        dom_put_dict = dom_dict["put"]
        #按要求顺序排列的合约名称
        dom_call_list = [dom_call_dict["平值"], dom_call_dict["实一"], dom_call_dict["实二"], dom_call_dict["虚一"],
                         dom_call_dict["虚二"]]
        dom_put_list = [dom_put_dict["平值"], dom_put_dict["实一"], dom_put_dict["实二"], dom_put_dict["虚一"],
                        dom_put_dict["虚二"]]
        #获取greek letters
        dom_call_df = get_greek_letter_df(dom_call_list, "call")
        dom_put_df = get_greek_letter_df(dom_put_list, "put")

        #拼接为一个df
        dom_df = pd.concat([dom_call_df, dom_put_df], axis=0)

        #对次主力
        #call
        subdom_dict = get_index_contracts_categories_dict(index)[subdom]
        subdom_call_dict = subdom_dict["call"]
        subdom_put_dict = subdom_dict["put"]

        #按顺序要求排序的合约名称
        subdom_call_list = [subdom_call_dict["平值"], subdom_call_dict["实一"], subdom_call_dict["实二"],
                            subdom_call_dict["虚一"], subdom_call_dict["虚二"]]
        subdom_put_list = [subdom_put_dict["平值"], subdom_put_dict["实一"], subdom_put_dict["实二"],
                           subdom_put_dict["虚一"], subdom_put_dict["虚二"]]
        #获取greek letters
        subdom_call_df = get_greek_letter_df(subdom_call_list, "call")
        subdom_put_df = get_greek_letter_df(subdom_put_list, "put")

        #拼接为一个df
        subdom_df = pd.concat([subdom_call_df, subdom_put_df], axis=0)
        formatted_dom_df = format_columns(dom_df)
        formatted_subdom_df = format_columns(subdom_df)

        print(f"{index}:")
        print("主力合约为:")
        print(dom_df)
        print("次主力合约为")
        print(subdom_df)
        df_to_png(dom_df, formatted_df=formatted_dom_df, filename=f"{name}主力合约希腊字母.png", color_column=True, color_column_num_list=[1, 3, 5, 7, 9])
        df_to_png(subdom_df, formatted_df=formatted_subdom_df, filename=f"{name}次主力合约希腊字母.png", color_column=True,
                  color_column_num_list=[1, 3, 5, 7, 9])
