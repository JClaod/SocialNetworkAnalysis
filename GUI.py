import tkinter as tk
from tkinter import ttk
from tkinter import font
import networkx as nx
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from Graph import Graph
from Graph import GraphTraversal

class GraphApp:
    def __init__(self, window, graph):
        self.window = window
        self.graph = graph
        self.traversal = {}
        self.G = nx.Graph()

        custom_font = font.Font(family="Helvetica", size=20, weight="bold")
        header = tk.Label(self.window, text="Social Network Analysis", height=2, font=custom_font)
        header.pack()

        self.text_widget = tk.Text(window, height=30, width=40)
        self.text_widget.pack()

        self.source_target_options = []
        for id in self.graph.adjacencyList.keys():
            name = self.graph.id_to_names[id]
            self.source_target_options.append(name)

        path_header = tk.Label(self.window, text="Find Path", height=2)
        path_header.pack()

        self.source_label = tk.Label(self.window, text="Source:", height=2)
        self.source_label.place(x=150, y=580)
        self.source_path = ttk.Combobox(window, values=self.source_target_options, width=10)
        self.source_path.place(x=200, y=587)

        self.target_label = tk.Label(self.window, text="Target:", height=2)
        self.target_label.place(x=150, y=610)
        self.target_path = ttk.Combobox(window, values=self.source_target_options, width=10)
        self.target_path.place(x=200, y=617)

        self.path_button = tk.Button(self.window, text="Submit", width=5, height=1, font=5, command=self.showPathTo)
        self.path_button.pack(pady=60)

        self.figure = self.visualize()
        self.canvas = FigureCanvasTkAgg(self.figure, master=window)
        self.canvas.get_tk_widget().pack()

    def showPathTo(self):
        self.deleteText()

        source = self.source_path.get()
        target = self.target_path.get()

        if int(source[0]) not in self.traversal:
            traversal = GraphTraversal(self.graph, int(source[0]))
            self.traversal[int(source[0])] = traversal
        
        traversal = self.traversal[int(source[0])]

        if traversal.hasPathTo(int(target[0])):
            path = traversal.pathToTarget(int(target[0]))  # Get the path
            self.text_widget.insert("end", "Path to target: " + str(path))
        else:
            self.text_widget.insert("end", "No Path to " + target)

    def updateText(self, node, community_id):
        if node not in self.traversal:
            traversal = GraphTraversal(self.graph, node)
            self.traversal[node] = traversal

        traversal = self.traversal[node]      
        information = self.graph.id_to_names[node]

        newText = f"Name: {information[1]}\n\nID: {node}\n\nCommunity ID: {community_id}\n\nNeighbors: \n{self.idToNames(node)}\nLocal Degree: {self.graph.localDegree(node)}\n\nCloseness Centrality: \n{traversal.closenessCentrality()}"
        self.text_widget.insert("end", newText)

    def idToNames(self, node):
        names = ""
        for id in self.graph.adjacencyList[node]:
            name = self.graph.id_to_names[id]
            names += "-" + name[1] + "\n"
        
        return names

    def deleteText(self):
        self.text_widget.delete("1.0", "end")

    def visualize(self):
        for id, name in self.graph.id_to_names:
            self.G.add_node(id, label=name)

        for fromID, neighbors in self.graph.adjacencyList.items():
            for toID in neighbors:
                self.G.add_edge(fromID, toID)

        pos = nx.spring_layout(self.G)
        node_labels = nx.get_node_attributes(self.G, 'label')

        # Use Louvain community detection
        communities = nx.algorithms.community.greedy_modularity_communities(self.G)

        cmap = plt.get_cmap('tab20')
        node_colors = []
        node_community_ids = {}

        for node in self.G.nodes():
            for i, community in enumerate(communities):
                if node in community:
                    node_community_ids[node] = i + 1
                    node_colors.append(cmap(i % len(communities)))
                    break

        def on_node_click(event):
            self.deleteText()

            if event.inaxes is not None:
                plt.clf()  # Clear the current figure

                clicked_node = None
                for node, (x, y) in pos.items():
                    dx = event.xdata - x
                    dy = event.ydata - y
                    if dx**2 + dy**2 < 0.02:
                        clicked_node = node
                        self.updateText(clicked_node, node_community_ids[clicked_node])

                if clicked_node is not None:
                    highlighted_edges = [(clicked_node, adj_node) for adj_node in self.G.adj[clicked_node]]

                    nx.draw(self.G, pos, labels=node_labels, with_labels=True, node_size=1000, font_size=10, ax=plt.gca(), node_color=node_colors)

                    if all(highlighted_edges):
                        nx.draw(self.G, pos, labels=node_labels, with_labels=True, node_size=1000, font_size=10, ax=plt.gca(), node_color=node_colors)
                        nx.draw_networkx_edges(self.G, pos, edgelist=highlighted_edges, ax=plt.gca(), edge_color='red', width=2)
                        plt.title("Social Network Graph")
                        plt.text(0.5, -0.1, f"Total Edges: {self.graph.edges}\n Average Global Degree: {self.graph.avgGlobalDegree()}", transform=plt.gca().transAxes, ha="center")
                        plt.draw()

                        legend_labels = []
                        for i, community in enumerate(communities):
                            legend_labels.append(f'Community {i+1}')
                        plt.legend(handles=[plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=cmap(i % len(communities)), label=label) for i, label in enumerate(legend_labels)])

        def on_release(event):
            if event.inaxes is None:
                self.deleteText()
                plt.clf()
                nx.draw(self.G, pos, labels=node_labels, with_labels=True, node_size=1000, font_size=10, ax=plt.gca(), node_color=node_colors)
                plt.title("Social Network Graph")
                plt.text(0.5, -0.1, f"Total Edges: {self.graph.edges}\n Average Global Degree: {self.graph.avgGlobalDegree()}", transform=plt.gca().transAxes, ha="center")
                plt.draw()

                legend_labels = []
                for i, community in enumerate(communities):
                    legend_labels.append(f'Community {i+1}')
                plt.legend(handles=[plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=cmap(i % len(communities)), label=label) for i, label in enumerate(legend_labels)])

        fig = plt.figure(figsize=(10, 6))
        nx.draw(self.G, pos, labels=node_labels, with_labels=True, node_size=1000, font_size=10, ax=plt.gca(), node_color=node_colors)

        legend_labels = []
        for i, community in enumerate(communities):
            legend_labels.append(f'Community {i+1}')
        plt.legend(handles=[plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=cmap(i % len(communities)), label=label) for i, label in enumerate(legend_labels)])


        nx.draw(self.G, pos, labels=node_labels, with_labels=True, node_size=1000, font_size=10, ax=plt.gca(), node_color=node_colors)
        plt.title("Social Network Graph")
        plt.text(0.5, -0.1, f"Total Edges: {self.graph.edges}\n Average Global Degree: {self.graph.avgGlobalDegree()}", transform=plt.gca().transAxes, ha="center")

        fig.canvas.mpl_connect('button_press_event', on_node_click)
        fig.canvas.mpl_connect('button_release_event', on_release)

        plt.tight_layout()
        plt.show()

def main():
    window = tk.Tk()
    window.title("Social Network Analysis")
    window.geometry("400x750")

    graph = Graph()
    
    graph.createNode("Charlie")  # 0
    graph.createNode("Charles")  # 1
    graph.createNode("Bob")      # 2
    graph.createNode("Ally")     # 3
    graph.createNode("James")    # 4
    graph.createNode("Holly")    # 5
    graph.createNode("Worth")    # 6
    graph.createNode("Jerry")    # 7

    # Add edges
    graph.addEdge(0, 1)
    graph.addEdge(0, 2)
    graph.addEdge(0, 3)
    graph.addEdge(1, 2)
    graph.addEdge(1, 4)
    graph.addEdge(2, 4)
    graph.addEdge(3, 5)
    graph.addEdge(5, 6)
    graph.addEdge(2, 7)

    GraphApp(window, graph)

    window.mainloop()

if __name__ == "__main__":
    main()