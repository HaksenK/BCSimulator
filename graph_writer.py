import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv("./simulation_results.csv")

# グラフのプロパティ
fig, ax = plt.subplots()
ax.set_xlabel('Poolsize(α)')
ax.set_ylabel('Income Rate(R_pool)')
ax.set_title('Selfish Mining')

ax.set_xlim([0, 0.5])
ax.set_ylim([0, 1])

t = data["alpha"]
for (name, item), color in zip(data.iloc[:, 3:].iteritems(), ['red', 'green', 'blue']):
  ax.plot(t, item, color=color, label=f"γ={name}")

# Selfishノードがhonestと同じ動きをした場合の結果
ax.plot(t, data["honest"], color="gold", label="honest")

# プロット
ax.legend(loc=0)
fig.tight_layout()
plt.show()
