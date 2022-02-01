import csv, sys, pprint, math


class Node:
    def __init__(self, idd, xx, yy, demand, stime, profit):
        self.x = xx
        self.y = yy
        self.id = idd
        self.isRouted = False
        self.demand = demand
        self.stime = stime
        self.profit = profit

    def __repr__(self):
        return str(self.id)

class Truck:
    def __init__(self, idd, qq):
        self.capacity = qq
        self.id = idd

class Model:
    def __init__(self):
        self.nodes = []
        self.customers = []
        self.matrix = []
        self.trucks = []
        self.neighbours_array = []
        self.hoodSize = 0
        self.uselessNodes = []
        self.max_capacity = 0
        self.max_duration = 0

    def BuildModel(self):
        csvfile = sys.argv[1]
        with open(csvfile, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            line = 1
            for row in csv_reader:
                if line == 1:
                    temp = row[1]
                    k = int(temp)
                    line = line + 1
                elif line == 2:
                    for i in range(0, k):
                        temp = row[1]
                        capacity = float(temp)
                        truck = Truck(i, row[1])
                        self.trucks.append(truck)
                        self.max_capacity = capacity
                    line = line + 1
                elif line == 3:
                    temp = row[1]
                    t = float(temp)
                    self.max_duration = t
                    line = line + 1
                elif line == 6:
                    t1 = row[1]
                    t2 = row[2]
                    r1 = float(t1)
                    r2 = float(t2)
                    depot = Node(0, r1, r2, 0, 0, 0)
                    self.nodes.append(depot)
                    line = line + 1
                elif line == 8:
                    temp = row[1]
                    n = int(temp)
                    line = line + 1
                elif line > 11 and line <= 11 + n:
                    t1 = row[1]
                    t2 = row[2]
                    t0 = row[0]
                    t3 = row[3]
                    t4 = row[4]
                    t5 = row[5]
                    id = int(t0)
                    x = float(t1)
                    y = float(t2)
                    demand = int(t3)
                    stime = int(t4)
                    profit = int(t5)
                    node = Node(id, x, y, demand, stime, profit)
                    self.nodes.append(node)
                    line = line + 1
                else:
                    line = line + 1
        rows = len(self.nodes)
        self.matrix = [[0.0 for x in range(rows)] for y in range(rows)]
        self.customers = self.nodes[1:]
        for i in range(0, len(self.nodes)):
            for j in range(0, len(self.nodes)):
                a = self.nodes[i]
                b = self.nodes[j]
                dist = math.sqrt(math.pow(a.x - b.x, 2) + math.pow(a.y - b.y, 2))
                self.matrix[i][j] = dist
        # We create a neighbourhood list for each node of the problem. This allows us to limit the nodes we examine when
        # looking for our next move.A node is a neighbour to another node if the distance between them is smaller than
        # (or equal to) the the average distance for all nodes.
        s = 0
        for i in range(0, len(self.matrix)):
            s = s + sum(self.matrix[i])
        average_dist = s / (len(self.matrix) * len(self.matrix))
        self.hoodSize = average_dist
        for i in range(0, len(self.matrix)):
            hood = []
            for j in range(0, len(self.matrix)):
                if i != j:
                    if self.matrix[i][j] <= self.hoodSize:
                        hood.append(j)
            self.neighbours_array.append(hood)
        for i in range (0, len(self.matrix)):
            if (2 * self.matrix[0][i] + self.nodes[i].stime + 20) >= 200:
                self.uselessNodes.append(self.nodes[i])
