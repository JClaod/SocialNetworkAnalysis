from collections import deque
import networkx as nx
import matplotlib.pyplot as plt

class Graph:
    def __init__(self):
        self.id_to_names = []
        self.adjacencyList = {}
        self.userKeys = 0
        self.edges = 0
    
    def createNode(self, name):
        id = self.userKeys
        self.adjacencyList[id] = []
        self.id_to_names.append([id, name])
        self.userKeys += 1

    def addEdge(self, toID, fromID):
        self.adjacencyList[toID].append(fromID)
        self.adjacencyList[fromID].append(toID)
        self.edges += 1
    
    def totalEdges(self):
        return self.edges
    
    def localDegree(self, id):
        return len(self.adjacencyList[id])
    
    def avgGlobalDegree(self):
        total_participants = len(self.adjacencyList)
        total_degree = 0

        for id in self.adjacencyList:
            total_degree += self.localDegree(id)

        return total_degree/total_participants
    
    def visualize(self):
        G = nx.Graph()

        for id, name in self.id_to_names:
            G.add_node(id, label=name)

        for fromID, neighbors in self.adjacencyList.items():
            for toID in neighbors:
                G.add_edge(fromID, toID)

        pos = nx.spring_layout(G)
        node_labels = nx.get_node_attributes(G, 'label')

        # Use Louvain community detection
        communities = nx.algorithms.community.greedy_modularity_communities(G)

        cmap = plt.get_cmap('tab20')
        node_colors = []
        for node in G.nodes():
            for i, community in enumerate(communities):
                if node in community:
                    node_colors.append(cmap(i % len(communities)))
                    break

        def on_node_click(event):
            if event.inaxes is not None:
                plt.clf()  # Clear the current figure

                clicked_node = None
                for node, (x, y) in pos.items():
                    dx = event.xdata - x
                    dy = event.ydata - y
                    if dx**2 + dy**2 < 0.02:
                        clicked_node = node
                        plt.text(x, y, f"ID: {node}\nLocal Degree: {self.localDegree(node)}", fontsize=10, bbox=dict(facecolor='white', alpha=0.5))

                if clicked_node is not None:
                    highlighted_edges = [(clicked_node, adj_node) for adj_node in G.adj[clicked_node]]

                    nx.draw(G, pos, labels=node_labels, with_labels=True, node_size=1000, font_size=10, ax=plt.gca(), node_color=node_colors)
                    nx.draw_networkx_edges(G, pos, edgelist=highlighted_edges, ax=plt.gca(), edge_color='red', width=2)
                    plt.title("Social Network Graph")
                    plt.text(0.5, -0.1, f"Total Edges: {self.edges}", transform=plt.gca().transAxes, ha="center")
                    plt.draw()

        def on_release(event):
            if event.inaxes is None:
                plt.clf()  # Clear the current figure
                nx.draw(G, pos, labels=node_labels, with_labels=True, node_size=1000, font_size=10, ax=plt.gca(), node_color=node_colors)
                plt.title("Social Network Graph")
                plt.text(0.5, -0.1, f"Total Edges: {self.edges}", transform=plt.gca().transAxes, ha="center")
                plt.draw()

        fig = plt.figure(figsize=(10, 6))
        nx.draw(G, pos, labels=node_labels, with_labels=True, node_size=1000, font_size=10, ax=plt.gca(), node_color=node_colors)

        legend_labels = []
        for i, community in enumerate(communities):
            legend_labels.append(f'Community {i+1}')
        plt.legend(handles=[plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=cmap(i % len(communities)), label=label) for i, label in enumerate(legend_labels)])


        nx.draw(G, pos, labels=node_labels, with_labels=True, node_size=1000, font_size=10, ax=plt.gca(), node_color=node_colors)
        plt.title("Social Network Graph")
        plt.text(0.5, -0.1, f"Total Edges: {self.edges}", transform=plt.gca().transAxes, ha="center")

        fig.canvas.mpl_connect('button_press_event', on_node_click)
        fig.canvas.mpl_connect('button_release_event', on_release)

        plt.tight_layout()
        plt.show()

class GraphTraversal:
    def __init__(self, graph, source):
        self.listOfPath = []
        self.edgeTo = {id: float('inf') for id in graph.adjacencyList}
        self.distTo = {id: None for id in graph.adjacencyList}
        self.graph = graph
        self.source = source
    
    def shortestPath(self):
        self.distTo[self.source] = 0
        queue = deque([self.source])

        while queue:
            current = queue.popleft()

            for friend in self.graph.adjacencyList[current]:
                if self.distTo[friend] == float('inf'):
                    self.distTo[friend] = self.distTo[current] + 1
                    self.edgeTo[friend] = current
                    queue.append(friend)

    def pathToTarget(self, target):
        listOfPath = []

        while self.edgeTo[target] != None:
            listOfPath.append(self.edgeTo[target])
            target = self.edgeTo[target]
        
        print("Distance to target: " + str(len(listOfPath)) + ", Path to target: " + str(listOfPath))
    
    def hasPathTo(self, target):
        if self.distTo[target] != float('inf'):
            return True
        return False

    def distanceToNode(self):
        return self.distTo