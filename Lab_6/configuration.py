"""Довірча ймовірність p = 0.95 (критерій значимості 0.05)"""
variant = {"n": 114, "x1min": -25, "x1max": 75, "x2min": 25, "x2max": 65, "x3min": 25, "x3max": 40}

x1_average = (variant["x1min"] + variant["x1max"]) / 2
x2_average = (variant["x2min"] + variant["x2max"]) / 2
x3_average = (variant["x3min"] + variant["x3max"]) / 2

del_x1 = variant["x1max"] - x1_average
del_x2 = variant["x2max"] - x2_average
del_x3 = variant["x3max"] - x3_average

x0 = [1, 1, 1, 1]
x1 = [-1, -1, 1, 1]
x2 = [-1, 1, -1, 1]
x3 = [1, -1, -1, 1]

nx0 = [1, 1, 1, 1]
nx1 = [variant["x1min"] if x1[i] == -1 else variant["x1max"] for i in range(4)]
nx2 = [variant["x2min"] if x2[i] == -1 else variant["x2max"] for i in range(4)]
nx3 = [variant["x3min"] if x3[i] == -1 else variant["x3max"] for i in range(4)]

sp_x0 = [1, 1, 1, 1]
sp_x1 = [-1, -1, 1, 1]
sp_x2 = [-1, 1, -1, 1]
sp_x3 = [-1, 1, 1, -1]

sp_nx0 = [1, 1, 1, 1]
sp_nx1 = [variant["x1min"] if sp_x1[i] == -1 else variant["x1max"] for i in range(4)]
sp_nx2 = [variant["x2min"] if sp_x2[i] == -1 else variant["x2max"] for i in range(4)]
sp_nx3 = [variant["x3min"] if sp_x3[i] == -1 else variant["x3max"] for i in range(4)]

tp_count = 6
tp_x0 = [1 for _ in range(tp_count)]
tp_x1 = [-1.73, 1.73, 0, 0, 0, 0]
tp_x2 = [0, 0, -1.73, 1.73, 0, 0]
tp_x3 = [0, 0, 0, 0, -1.73, 1.73]

tp_nx0 = [1 for _ in range(tp_count)]
tp_nx1 = [tp_x1[i] * del_x1 + x1_average for i in range(tp_count)]
tp_nx2 = [tp_x2[i] * del_x2 + x2_average for i in range(tp_count)]
tp_nx3 = [tp_x3[i] * del_x3 + x3_average for i in range(tp_count)]
