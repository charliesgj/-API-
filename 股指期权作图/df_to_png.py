import matplotlib.pyplot as plt
import datetime


# 设置颜色
def get_text_color(val):
    if val > 0:
        return 'red'
    elif val < 0:
        return 'green'
    else:
        return 'black'


def df_to_png(df,filename:str, formatted_df=None,  color_column=False, color_column_num_list=None, have_index = False):
    today = datetime.datetime.today().date()
    plt.rcParams["font.family"] = "Microsoft YaHei"
    # 创建图形
    if formatted_df is None:
        formatted_df = df
    fig, ax = plt.subplots(figsize=(16, 8))  # 这里可以调整图表大小
    ax.axis('tight')
    ax.axis('off')

    # 创建表格

    if have_index is False:
        table = ax.table(cellText=formatted_df.values, colLabels=formatted_df.columns, rowLabels=formatted_df.index,
                         cellLoc='center', loc='center')
        cells = table.get_celld()
        cell_d = (cells[(0, 0)].get_height(), cells[(1, -1)].get_width())
        table.add_cell(0, -1, width=cell_d[1], height=cell_d[0], text=today, loc='left')
    else:
        table = ax.table(cellText=formatted_df.values, colLabels=formatted_df.columns,
                         cellLoc='center', loc='center')
    if color_column is True:
        # 设置单元格文本颜色
        for i in range(len(df)):
            for j in color_column_num_list:
                cell = table[(i + 1, j)]
                cell.get_text().set_color(get_text_color(df.iloc[i, j]))
    plt.title(filename)
    plt.tight_layout()
    # 保存为PNG文件
    plt.savefig(filename, bbox_inches='tight', pad_inches=0.1)
