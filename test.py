from Model import *
from SolutionDrawer import *

class Route:
    def __init__(self, x):
        self.profit = 0
        self.sequence = []
        self.time_left = 200
        self.supply_left = 150
        self.x = x
        self.y = 1-x

class Solution:
    def __init__(self, x):
        self.profit = 0
        self.routes = []
        self.time_left = 200
        self.supply_left = 150
        self.x = x
        self.y = 1-x
def test(model, route):
    time = 0
    demand = 0
    profit = 0
    print(route)
    for i in range (0, len(route)-1):
        current = route[i]
        dest = route[i+1]
        print("Going from ", current,"to ", dest)
        rtime, rdemand, rprofit = going(model, current, dest)
        print("costs ", rtime)
        time = time + rtime
        print("Total time: ", time)
        demand = demand + rdemand
        profit = profit + rprofit
    print("Time:", time, " Demand:", demand, " Profit:", profit)
def going(model, current, dest):
    time = model.matrix[current][dest] + model.nodes[dest].stime
    demand = model.nodes[dest].demand
    profit = model.nodes[dest].profit
    return time, demand, profit

m = Model()
m.BuildModel()
route = [0, 307, 17, 69, 0]
test(m, route)