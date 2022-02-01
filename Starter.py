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
def solve (model):
    x = 0.8
    solution = Solution(x)
    for node in model.nodes:
        node.isRouted = False
    colors = ['black', 'green', 'yellow', 'orange', 'grey', 'purple']
    firstStops = [10, 25, 77, 211, 273, 322]
    for i in range(0, 6):
        route = Route(x)
        depot = model.nodes[0]
        route.sequence.append(depot)
        y = 1 - x
        customStart = False
        firstStop = model.nodes[firstStops[i]]
        next_customer(model, route, depot, route.x, route.y, True, customStart, firstStop)
        testTime, testDemand, testProfit = test(model, route)
        testRoute(model, route, testTime, testDemand, testProfit)
        solution.routes.append(route)
    for r in solution.routes:
        formatted_x = "{:.2f}".format(r.x)
        formatted_y = "{:.2f}".format(r.y)
        formatted_time = "{:.2f}".format(r.time_left)
        r.x = float(formatted_x)
        r.y = float(formatted_y)
        r.time_left = float(formatted_time)
        solution.profit = solution.profit + r.profit
    SolDrawer.draw(0, solution, model.nodes, model.uselessNodes, colors)
    firstSolution = solution
    txt = "Total Profit\n" + str(firstSolution.profit) + "\n"
    counter = 1
    for route in firstSolution.routes:
        txt = txt + "Route " + str(counter) + " timeleft:" + str(route.time_left) + "\n"
        rt = ' '.join(str(n) for n in route.sequence)
        txt = txt + rt + "\n"
        counter = counter + 1
    with open('solution0.txt', 'w') as g:
        g.write(txt)
        g.close()
    for tr in range(0, 10):
        for r in range(0, len(solution.routes)):
            addition, new_route = addNode(model, solution.routes[r], r)
            if addition:
                solution.routes[r] = new_route
        SolDrawer.draw(1, solution, model.nodes, model.uselessNodes, colors)
        bestSolution = solution
        bestSolution.profit = 0
    for route in bestSolution.routes:
        bestSolution.profit = bestSolution.profit + route.profit
    txt = "Total Profit\n" + str(bestSolution.profit) + "\n"
    counter = 1
    for route in bestSolution.routes:
        txt = txt + "Route " + str(counter) + "\n"
        rt = ' '.join(str(n) for n in route.sequence)
        txt = txt + rt + "\n"
        counter = counter + 1
    with open('solution1.txt', 'w') as g:
        g.write(txt)
        g.close()
def next_customer(model, route, current_node, x, y, running, customStart, firstStop):
    options_available = getOptionList(model, current_node, running, route)
    if running:
        if len(options_available) != 0:
            options_available.pop(0) #removes first option which is always the depot
        if len(options_available) == 0:
            next_node = model.nodes[0] #if you can afford to go nowhere else, get back to the depot
            running = False
        else:
            if customStart:
                next_node = firstStop
            else:
                next_node = optionsRating(options_available, x, y, model.max_duration, model.max_capacity)
        route.time_left = route.time_left - (model.matrix[current_node.id][next_node.id] + next_node.stime)
        route.supply_left = route.supply_left - next_node.demand
        route.sequence.append(next_node)
        model.nodes[next_node.id].isRouted = True
        route.profit = route.profit + next_node.profit
        next_customer(model, route, next_node, x, y, running, False, None)

def getOptionList(model, current_node, running, route):
    options_available = []
    if running:
        for i in range(0, len(model.neighbours_array[current_node.id])):
            candidate_id = model.neighbours_array[current_node.id][i]
            candidate = model.nodes[candidate_id]
            time_cost = model.matrix[current_node.id][candidate_id] + candidate.stime
            time_back = model.matrix[candidate_id][0]
            if ((time_cost + time_back) <= route.time_left) and (candidate.demand <= route.supply_left) and (
            not candidate.isRouted):
                candidate_info = [candidate, time_cost]
                options_available.append(candidate_info)
    return options_available

def optionsRating(options_available, x, y, max_duration, max_capacity):
    next_node = options_available[0][0]
    max_rating = 0
    for i in range(1, len(options_available)):
        candidate = options_available[i][0]
        pr_to_cost = candidate.profit / (options_available[i][1] / max_duration)
        pr_to_demand = candidate.profit / (candidate.demand / max_capacity)
        rating = x * pr_to_cost + y * pr_to_demand
        if rating > max_rating:
            max_rating = rating
            next_node = candidate
    return next_node

def test(model, route):
    time = 0
    demand = 0
    profit = 0
    for i in range(0, len(route.sequence)-1):
        current = route.sequence[i]
        dest = route.sequence[i+1]
        rtime, rdemand, rprofit = going(model, current, dest)
        time = time + rtime
        demand = demand + rdemand
        profit = profit + rprofit
    return time, demand, profit

def going(model, current, dest):
    time = model.matrix[current.id][dest.id] + model.nodes[dest.id].stime
    demand = model.nodes[dest.id].demand
    profit = model.nodes[dest.id].profit
    return time, demand, profit

def testRoute(model, route, testTime, testDemand, testProfit):
    formatted_demandT = "{:.2f}".format(model.max_capacity - testDemand)
    formatted_profitT = "{:.2f}".format(testProfit)
    formatted_timeT = "{:.2f}".format(model.max_duration - testTime)
    testDemand = float(formatted_demandT)
    testProfit = float(formatted_profitT)
    testTime = float(formatted_timeT)
    formatted_supplyr = "{:.2f}".format(route.supply_left)
    formatted_profitr = "{:.2f}".format(route.profit)
    formatted_timer = "{:.2f}".format(route.time_left)
    route.supply_left = float(formatted_supplyr)
    route.profit = float(formatted_profitr)
    route.time_left = float(formatted_timer)
    if testTime == route.time_left and testDemand == route.supply_left and testProfit == route.profit:
        print("Test passed successfully")
    else:
        print("Something is wrong")
        print("Time: ", testTime, " vs ", route.time_left)
        print("Supply: ", testDemand, " vs ", route.supply_left)
        print("Profit: ", testProfit, " vs ", route.profit)

def testAddition(route, node, model, ind):
    print("ATTENTION!")
    testTime, testDemand, testProfit = test(model, route)
    print(route.sequence)
    print(testTime, " ", testDemand, " ", testProfit)
    dummy = route
    dummy.sequence.insert(ind, node)
    testTime, testDemand, testProfit = test(model, dummy)
    print(dummy.sequence)
    print(testTime, " ", testDemand, " ", testProfit)

def addNode(model, route, route_id):
    candidates = []
    for node in model.customers:
        if node.stime < route.time_left and node.demand <= route.supply_left and not model.nodes[node.id].isRouted:
            #if the customer's service time and demands are not more than what we have left, maybe we can still service them (depends on the distance)
            candidates.append(node)
    if len(candidates) == 0:
        return False, route
    all_options = []
    foundOne = False
    for pointer in range(0, len(route.sequence)-1):
        index = pointer + 1
        spot_options = []
        original_distance_cost = model.matrix[route.sequence[pointer].id][route.sequence[index].id]
        for node in candidates:
            through_node_distance_cost = model.matrix[route.sequence[pointer].id][node.id] + node.stime + model.matrix[node.id][route.sequence[index].id]
            added_distance_cost = through_node_distance_cost - original_distance_cost
            if added_distance_cost <= route.time_left:
                spot_options.append(node)
                foundOne = True
        all_options.append(spot_options)
    if not foundOne:
        return False, route
    top_option = model.nodes[0]
    position = -12
    for i in range(0, len(all_options)):
        if len(all_options[i]) != 0:
            for j in range(0, len(all_options[i])):
                node = all_options[i][j]
                position = i + 1
                print("Trying node:", node.id, " in position ", position, "in route ", route_id+1)
                added, new_route = routeInsertNode(position, node, route, model)
                if added:
                    model.nodes[node.id].isRouted = True
                    print("Success!")
                else:
                    print("Nevermind")
                return added, new_route

def routeInsertNode(position, node, route, model):
    route.sequence.insert(position, node)
    added = True
    timeCost, demandCost, route.profit = test(model, route)
    route.time_left = model.max_duration - timeCost
    route.supply_left = model.max_capacity - demandCost
    route.profit = route.profit + node.profit
    if route.time_left < 0 or route.supply_left < 0:
        added = False
    return added, route

m = Model()
m.BuildModel()
solve(m)
