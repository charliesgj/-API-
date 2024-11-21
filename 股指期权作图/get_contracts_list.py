#每个第三周周五之后更新目前的合约列表，需要手动操作，从同花顺获取最新的合约列表，分别更新到txt中
#粘贴时注意事项：去除首尾的引号，只留下','分割的合约名，无需换行
from date_calculation import get_current_dom_subdom_month


#我们需要将目前的期权合约名称列表存储为：
#主力合约call+主力合约put+次主力合约call+次主力合约put
#并能比较方便的提取他们

def read_contracts_file(dom=None, subdom=None):
    #针对最新在txt中更新的合约列表，将他们分门别类存储到字典中，返回字典
    if dom is None and subdom is None:
        dom, subdom = get_current_dom_subdom_month()
    with open("HO_contracts.txt", 'r') as HO_contracts:
        HO_list = HO_contracts.read().split(',')
        HO_dict = list_to_dict(HO_list, dom, subdom)
        #print(HO_dict)

    with open("IO_contracts.txt", 'r') as IO_contracts:
        IO_list = IO_contracts.read().split(',')
        IO_dict = list_to_dict(IO_list, dom, subdom)
        #print(IO_dict)

    with open("MO_contracts.txt", 'r') as MO_contracts:
        MO_list = MO_contracts.read().split(',')
        MO_dict = list_to_dict(MO_list, dom, subdom)
        #print(MO_dict)

    index_to_dict = {"HO": HO_dict, "IO": IO_dict, "MO": MO_dict}
    return index_to_dict


def list_to_dict(index_list, dom, subdom):
    if dom is None and subdom is None:
        dom, subdom = get_current_dom_subdom_month()

    index_dict = {
        dom: {"put": [], "call": []},
        subdom: {"put": [], "call": []}
    }
    for contract in index_list:
        if dom in contract:
            if "P" in contract:
                index_dict[dom]["put"].append(contract)
            else:
                index_dict[dom]["call"].append(contract)
        if subdom in contract:
            if "P" in contract:
                index_dict[subdom]["put"].append(contract)
            else:
                index_dict[subdom]["call"].append(contract)
    return index_dict


def get_index_dom_now(index, index_to_dict, dom, subdom, dom_True: bool):
    """快捷获得某指数现在的全部 dom合约 or subdom合约, 不区分call or put
    例如要获取HO的全部dom合约， 则index = 'HO', dom =True"""
    if dom is None and subdom is None:
        dom, subdom = get_current_dom_subdom_month()

    dict_temp = index_to_dict[index]
    if dom_True:
        return dict_temp[dom]["put"] + dict_temp[dom]["call"]
    else:
        return dict_temp[subdom]["put"] + dict_temp[subdom]["call"]


def get_contract_names(variety_name, contract_type, option_type):
    """快捷获得某指数的dom合约 or subdom合约中的call or put, 只获得精确的某一小部分
    例如要获取HO的dom合约中的put， 则index = 'HO', dom =True, call = False"""
    dom, subdom = get_current_dom_subdom_month()
    index_to_dict = read_contracts_file(dom, subdom)
    dict_temp = index_to_dict[variety_name]
    if contract_type == dom:
        dict_temp = dict_temp[dom]
        if option_type == "call":
            return dict_temp["call"]
        else:
            return dict_temp["put"]
    else:
        dict_temp = dict_temp[subdom]
        if option_type == "call":
            return dict_temp["call"]
        else:
            return dict_temp["put"]
