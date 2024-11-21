import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 创建数据
data = {
    'Contract': ['合约1', '合约2', '合约3'],
    'Volume': [1000, 1500, 1200],
    'Open Interest': [800, 1300, 900]
}

df = pd.DataFrame(data)

# 设置柱形图的宽度和位置
bar_width = 0.2
num_contracts = len(df['Contract'])
x = np.arange(2)  # 两个大类别

# 创建柱形图
fig, ax = plt.subplots()

# 成交量和持仓量的位置
x_volume = x[0] + np.arange(num_contracts) * bar_width
x_interest = x[1] + np.arange(num_contracts) * bar_width

# 绘制所有合约的成交量
for i in range(num_contracts):
    ax.bar(x_volume[i], df.loc[i, 'Volume'], bar_width, label=f'{df.loc[i, "Contract"]} 成交量')
# 绘制所有合约的持仓量
for i in range(num_contracts):
    ax.bar(x_interest[i], df.loc[i, 'Open Interest'], bar_width, label=f'{df.loc[i, "Contract"]} 持仓量' if i == 0 else "")

# 添加图例
ax.legend()

# 设置X轴标签位置和标签
ax.set_xticks([x_volume.mean(), x_interest.mean()])
ax.set_xticklabels(['成交量', '持仓量'])

# 添加标题和轴标签
ax.set_ylabel('数量')
ax.set_title('各合约的成交量和持仓量')

# 展示图形
plt.show()


