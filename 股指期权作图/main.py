from ths_data import *
from 希腊字母 import plot_greek_letter
from 波动率微笑曲线 import plot_volatility_curve
from 标的指数历史波动率 import plot_index_his_volatility
from 持仓量成交量排序行权价格 import plot_amt_strike_price
from writedoc import create_word_document


def main():
    login()
    plot_greek_letter()
    plot_volatility_curve()
    plot_index_his_volatility()
    plot_amt_strike_price()
    create_word_document()
main()
