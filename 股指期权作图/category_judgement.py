##平值，实一，实二，虚一，虚二合约名称

from ths_data import *


def find_contract_categories(contracts, index_value):
    #给定一个包含某一具体种类全部合约的字典， 如dom_calls_dict
    #contracts = {'HO2406-C-1950.CFE': 1950, 'HO2406-C-2000.CFE': 2000, 'HO2406-C-2050.CFE': 2050...}
    #和index_value 也即该合约指数现价
    #返回平值，实一，实二，虚一，虚二合约名称
    # closest_contract, above_contract, above_contract_2, below_contract, below_contract_2
    #注意
    #对call合约来说，看涨，故above_contract为虚合约，below_contract为实合约
    #对put合约来说，看跌，故below_contract为虚合约， above_contract为实合约
    sorted_contracts = sorted(contracts.items(), key=lambda x: x[1])  # 按行权价排序
    closest_strike_price = None
    above_index, below_index = [], []
    for contract_name, strike_price in sorted_contracts:
        #找到与目前价格最接近的价格
        if (closest_strike_price is None or
                abs(strike_price - index_value) < abs(closest_strike_price - index_value)):
            closest_strike_price = strike_price
        #将所有高于目前价格的行权价加入列表中
        if strike_price > index_value:
            above_index.append((contract_name, strike_price))
        #将所有低于目前价格的行权价加入列表中
        if strike_price < index_value:
            below_index.append((contract_name, strike_price))

    closest_contract = [name for name, price in contracts.items()
                        if price == closest_strike_price][0]

    # 找到第一个和第二个高于目标价的合约
    above_contracts = [contract for contract, price in sorted_contracts
                       if price > index_value and contract != closest_contract]
    above_contract = above_contracts[0] if above_contracts else None
    above_contract_2 = above_contracts[1] if len(above_contracts) > 1 else None

    # 找到第一个低于目标价的合约
    below_contract = None
    for contract, price in reversed(sorted_contracts):
        if price < index_value and contract != closest_contract:
            below_contract = contract
            break

    # 找到第二个低于目标价的合约
    below_contract_2 = None
    for contract, price in reversed(sorted_contracts):
        if (price < index_value and contract != closest_contract
                and contract != below_contract):
            below_contract_2 = contract
            break

    return closest_contract, above_contract, above_contract_2, below_contract, below_contract_2


def get_index_contracts_categories_dict(variety_name):
    #对某个具体指数，例如中证50，输入它的期权编号，例如"HO"，获得一个包含20个名称的dict
    #dict中包括其主力合约和次主力合约的call和put合约的平值、实一、实二、虚一、虚二合约的名称
    dom, subdom = get_current_dom_subdom_month()
    dom_calls = get_contract_names(variety_name, dom, "call")
    sub_calls = get_contract_names(variety_name, subdom, "call")
    dom_puts = get_contract_names(variety_name, dom, "put")
    sub_puts = get_contract_names(variety_name, subdom, "put")
    temp_dict = {"HO": "IH8888.CFE", "IO": "IF8888.CFE", "MO": "IM8888.CFE"}
    dom_calls_dict = {}
    sub_calls_dict = {}
    dom_puts_dict = {}
    sub_puts_dict = {}
    #先取得平值合约
    index_value = get_index_preclose(temp_dict[variety_name])
    for dom_call in dom_calls:
        dom_calls_dict[dom_call] = extract_strike_price(dom_call)
    for sub_call in sub_calls:
        sub_calls_dict[sub_call] = extract_strike_price(sub_call)
    for dom_put in dom_puts:
        dom_puts_dict[dom_put] = extract_strike_price(dom_put)
    for sub_put in sub_puts:
        sub_puts_dict[sub_put] = extract_strike_price(sub_put)
    category_dict = \
        {dom:
            {"call": {
                ##对call合约来说，看涨，故above_contract为虚合约，below_contract为实合约
                #输出的5个值分别为 flat, above_contract, above_contract_2,
                # below_contract, below_contract_2
                "平值": find_contract_categories(dom_calls_dict, index_value)[0],
                "实一": find_contract_categories(dom_calls_dict, index_value)[3],
                "实二": find_contract_categories(dom_calls_dict, index_value)[4],
                "虚一": find_contract_categories(dom_calls_dict, index_value)[1],
                "虚二": find_contract_categories(dom_calls_dict, index_value)[2]
            },
                "put": {
                    "平值": find_contract_categories(dom_puts_dict, index_value)[0],
                    "实一": find_contract_categories(dom_puts_dict, index_value)[1],
                    "实二": find_contract_categories(dom_puts_dict, index_value)[2],
                    "虚一": find_contract_categories(dom_puts_dict, index_value)[3],
                    "虚二": find_contract_categories(dom_puts_dict, index_value)[4]}
            },
            subdom:
                {"call": {
                    ##对call合约来说，看涨，故above_contract为虚合约，below_contract为实合约
                    # 输出的5个值分别为 flat, above_contract, above_contract_2, below_contract, below_contract_2
                    "平值": find_contract_categories(sub_calls_dict, index_value)[0],
                    "实一": find_contract_categories(sub_calls_dict, index_value)[3],
                    "实二": find_contract_categories(sub_calls_dict, index_value)[4],
                    "虚一": find_contract_categories(sub_calls_dict, index_value)[1],
                    "虚二": find_contract_categories(sub_calls_dict, index_value)[2]},
                    "put": {
                        "平值": find_contract_categories(sub_puts_dict, index_value)[0],
                        "实一": find_contract_categories(sub_puts_dict, index_value)[1],
                        "实二": find_contract_categories(sub_puts_dict, index_value)[2],
                        "虚一": find_contract_categories(sub_puts_dict, index_value)[3],
                        "虚二": find_contract_categories(sub_puts_dict, index_value)[4]
                    }}}
    return category_dict
