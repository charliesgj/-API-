from getiFind import getindex_pe_pb, login
import matplotlib.pyplot as plt
import datetime

def plot7():
    # 获取当日日期
    today = datetime.datetime.today().date()

    df = getindex_pe_pb()
    plt.rcParams["font.family"] = "Microsoft YaHei"
    fig, ax = plt.subplots()
    ax.axis('off')
    table = ax.table(cellText=df.values, colLabels=df.columns, rowLabels=df.index, loc='center', cellLoc='center')

    # 在第一行第一列（索引为(0, 0)）添加当日日期
    table.add_cell(0, -1, width=0.05, height=0.045, text=today, loc='left')

    # 调整表格的布局
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.2)

    # 添加标题
    plt.title("表1：主要指数估值", pad=20)
    plt.tight_layout()
    plt.savefig('plot7.png', bbox_inches='tight', pad_inches=0.05)
