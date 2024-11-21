from getiFind import getindex_futures_performance, login
import matplotlib.pyplot as plt
import datetime

def plot8():
    today = datetime.datetime.today().date()
    df = getindex_futures_performance()
    plt.rcParams["font.family"] = "Microsoft YaHei"
    fig, ax = plt.subplots(figsize=(15, 10))
    ax.axis('off')
    table = ax.table(cellText=df.values, colLabels=df.columns, rowLabels=df.index, loc='center', cellLoc='center')

    # 在第一行第一列（索引为(0, 0)）添加当日日期
    table.add_cell(0, -1, width=0.05, height=0.0215, text=today, loc='left')

    # 调整表格的布局
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.2)
    # 添加标题
    plt.title("表2：股指期货日表现")
    plt.tight_layout()
    plt.savefig('plot8.png', bbox_inches='tight')
