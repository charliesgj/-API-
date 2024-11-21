from category_judgement import *
from ths_data import *
import matplotlib.pyplot as plt


#每个品种的主力和次主力合约 平值，虚一，虚二，实一，实二的隐含波动率
#3个品种，每个有主力和次主力合约，每个主力分为call和put 每个call和put有这五个合约 也就是共有 3*2*2*5个数要取

def plot_volatility_curve():
    print("####################################################正在绘制波动率微笑曲线####################################################")
    dom, subdom = get_current_dom_subdom_month()
    index_dict = {"上证50": "HO", "沪深300": "IO", "中证1000": "MO"}
    for name, index in index_dict.items():
        print(name)
        #波动率微笑曲线中，x周为行权价 对call合约来说，行权价从小到大排列为 实二，实一，平值，虚一，虚二；对put合约来说，行权价从小到大排列为虚一，虚二，平值，实一，实二
        #对主力
        #call
        dom_dict = get_index_contracts_categories_dict(index)[dom]
        print("主力合约为：")
        print(dom_dict)
        dom_call_dict = dom_dict["call"]
        #按要求顺序排列的合约名称
        dom_call_list = [dom_call_dict["实二"], dom_call_dict["实一"], dom_call_dict["平值"], dom_call_dict["虚一"],
                         dom_call_dict["虚二"]]
        #获取x，y
        dom_call_strike_price = [extract_strike_price(i) for i in dom_call_list]
        dom_call_implied_volatility = [get_implied_volatility(i) for i in dom_call_list]
        #put
        dom_put_dict = dom_dict["put"]
        dom_put_list = [dom_put_dict["虚二"], dom_put_dict["虚一"], dom_put_dict["平值"], dom_put_dict["实一"],
                        dom_put_dict["实二"]]
        #获取x，y
        dom_put_strike_price = [extract_strike_price(i) for i in dom_put_list]
        dom_put_implied_volatility = [get_implied_volatility(i) for i in dom_put_list]

        #对次主力
        #call
        subdom_dict = get_index_contracts_categories_dict(index)[subdom]
        print("次主力合约为：")
        print(subdom_dict)
        subdom_call_dict = subdom_dict["call"]
        #按顺序要求排序的合约名称
        subdom_call_list = [subdom_call_dict["实二"], subdom_call_dict["实一"], subdom_call_dict["平值"],
                            subdom_call_dict["虚一"], subdom_call_dict["虚二"]]
        #获取x，y
        subdom_call_strike_price = [extract_strike_price(i) for i in subdom_call_list]
        subdom_call_implied_volatility = [get_implied_volatility(i) for i in subdom_call_list]
        #put
        subdom_put_dict = subdom_dict["put"]
        subdom_put_list = [subdom_put_dict["虚二"], subdom_put_dict["虚一"], subdom_put_dict["平值"],
                           subdom_put_dict["实一"], subdom_put_dict["实二"]]
        #获取x，y
        subdom_put_strike_price = [extract_strike_price(i) for i in subdom_put_list]
        subdom_put_implied_volatility = [get_implied_volatility(i) for i in subdom_put_list]

        strike_prices_list = [dom_call_strike_price,
                              dom_put_strike_price,
                              subdom_call_strike_price,
                              subdom_put_strike_price]
        implied_volatilities_list = [dom_call_implied_volatility,
                                     dom_put_implied_volatility,
                                     subdom_call_implied_volatility,
                                     subdom_put_implied_volatility]
        plt.rcParams["font.family"] = "Microsoft YaHei"
#####################################################################################################################################################
        #fig, axs = plt.subplots(2, 2, figsize=(12, 8))
        #plot_names = ["主力call", "主力put", "次主力call", "次主力put"]
        # 绘制四个波动率微笑曲线
        #for i, (strike_prices, implied_volatilities) in enumerate(zip(strike_prices_list, implied_volatilities_list)):
        #    row = i // 2
        #    col = i % 2
        #    ax = axs[row, col]
        #    ax.plot(strike_prices, implied_volatilities, marker='o', linestyle='-')
        #    ax.set_title(f'{plot_names[i]}')
        #    ax.set_xlabel('Strike Price')
        #    ax.set_ylabel('Implied Volatility')
        #    ax.grid(True)
#######################################################################################################################################################
        fig, axs = plt.subplots(1, 2, figsize=(12, 8))
        plot_names = ["Call Options", "Put Options"]
        # 绘制两个波动率微笑曲线
        for i in range(0,2):
            ax = axs[i]
            ax.plot(strike_prices_list[i*2], implied_volatilities_list[i*2], label="主力合约", color = "blue",marker='o', linestyle='-')
            ax.plot(strike_prices_list[i*2+1], implied_volatilities_list[i*2+1], label = "次主力合约", color = "red",marker='o', linestyle='-')
            ax.set_title(f'{plot_names[i]}')
            ax.set_xlabel('Strike Price')
            ax.set_ylabel('Implied Volatility')
            ax.grid(True)

        fig.suptitle(f"{name}波动率曲线")
        # 调整子图布局
        plt.tight_layout()
        plt.savefig(f"{name}波动率曲线.png")
