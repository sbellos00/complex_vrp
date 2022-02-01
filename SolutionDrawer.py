import matplotlib.pyplot as plt
class SolDrawer:
    @staticmethod
    def draw(it, solution, nodes, useless, colors):
        plt.clf()
        SolDrawer.drawPoints(nodes)
        SolDrawer.drawUseless(useless)
        SolDrawer.drawRoutes(solution, colors)
        plt.savefig(str(it))

    @staticmethod
    def drawPoints(nodes:list):
        x = []
        y = []
        for i in range(len(nodes)):
            n = nodes[i]
            x.append(n.x)
            y.append(n.y)
        plt.scatter(x, y, c="blue")

    @staticmethod
    def drawUseless(nodes:list):
        x = []
        y = []
        for i in range(len(nodes)):
            n = nodes[i]
            x.append(n.x)
            y.append(n.y)
        plt.scatter(x, y, c="red")

    @staticmethod
    def drawRoutes(solution, colors):
        ind = 0
        for route in solution.routes:
            if route is not None:
                for i in range(0, len(route.sequence) - 1):
                    c0 = route.sequence[i]
                    c1 = route.sequence[i + 1]
                    plt.plot([c0.x, c1.x], [c0.y, c1.y], c=colors[ind])
            ind = ind + 1
