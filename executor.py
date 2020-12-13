# グラフをプロットする。BitcoinNetworkSimulatorを様々な条件で呼び出して、R_poolを記録してプロット。
# 結果をcsv出力する。
import numpy as np
from tqdm import tqdm
import pandas as pd
from node import *
from simulator import *

data = pd.DataFrame()
data['alpha'] = [a/1000 for a in range(500)]

# 一つの条件で何回か繰り返す
ITERATION_NUM = 10

# Selfishノードがhonestと同じ動きをした場合の結果
R_pools_all_honest = []
for alpha in tqdm([a/1000 for a in range(500)], desc="honest"):
  simulator = BitcoinNetworkSimulator(Node, int(1000*(1-alpha)), int(1000*alpha), 0.5)
  aver_sum = 0
  # ITERATION_NUM回実験し、平均を取る
  for i in range(ITERATION_NUM):
    simulator.execute_simulation()
    aver_sum += simulator.show_R_pool()
  R_pools_all_honest.append(aver_sum / ITERATION_NUM)
  del simulator

data["honest"] = R_pools_all_honest

# Selfishノードでの実験。γは0, 0.5, 1の三種
for gamma in [0, 0.5, 1]:
  results = []
  # 1000ノードのうちselfishの割合は0から0.5まで0.01刻み。
  for alpha in tqdm([a/1000 for a in range(500)], desc=f"gamma = {gamma}"):
    simulator = BitcoinNetworkSimulator(SelfishNode, int(1000*(1-alpha)), int(1000*alpha), gamma)
    aver_sum = 0

    # ITERATION_NUM回実験し、平均を取る
    for _ in range(ITERATION_NUM):
      simulator.execute_simulation()
      aver_sum += simulator.show_R_pool()
    results.append(aver_sum / ITERATION_NUM)
    del simulator

  data[gamma] = results

data.to_csv("./simulation_results.csv")
