# グラフをプロットする。BitcoinNetworkSimulatorを様々な条件で呼び出して、R_poolを記録してプロット。
import numpy as np
import matplotlib.pyplot as plt
from node import *
from simulator import *

# 一つの条件で何回か繰り返す
ITERATION_NUM = 5

fig, ax = plt.subplots()
ax.set_xlabel('Poolsize(α)')
ax.set_ylabel('Income Rate(R_pool)')
ax.set_title('Selfish Mining')

ax.set_xlim([0, 0.5])
ax.set_ylim([0, 1])

for gamma, color in zip([0, 0.5, 1], ['red', 'green', 'blue']):
  R_pools = []
  for alpha in [a/1000 for a in range(500)]:
    simulator = BitcoinNetworkSimulator(SelfishNode, int(1000*(1-alpha)), int(1000*alpha), gamma)
    aver_sum = 0
    for i in range(ITERATION_NUM):
      simulator.execute_simulation()
      aver_sum += simulator.show_R_pool()
    R_pools.append(aver_sum / ITERATION_NUM)
  del simulator

  t = np.linspace(0, 0.5, 500)
  ax.plot(t, R_pools, color=color, label=f"γ={gamma}")

ax.legend(loc=0)
fig.tight_layout()
plt.show()
