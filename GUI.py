import tkinter as tk
import networkx as nx
import matplotlib.pyplot as plt
from Graph import Graph

class GraphApp:
    def __init__(self, window, graph):
        self.window = window
        self.graph = graph

        self.graph_visualization_frame = tk.Frame(self.window)
        self.graph_visualization_frame.pack()

        self.text_widget = tk.Text(window, height=10, width=40)
        self.text_widget.pack()

        self.visualize()
    
    def updateText(self, node):
        newText = f"ID: {node}\nLocal Degree: {self.graph.localDegree(node)}"
        self.text_widget.insert("end", newText)


    def deleteText(self):
        self.text_widget.delete("1.0", "end")
    
    def visualize(self):
        G = nx.Graph()

        for id, name in self.graph.id_to_names:
            G.add_node(id, label=name)

        for fromID, neighbors in self.graph.adjacencyList.items():
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
            self.deleteText()

            if event.inaxes is not None:
                plt.clf()  # Clear the current figure

                clicked_node = None
                for node, (x, y) in pos.items():
                    dx = event.xdata - x
                    dy = event.ydata - y
                    if dx**2 + dy**2 < 0.02:
                        clicked_node = node
                        self.updateText(clicked_node)
                        plt.text(x, y, f"ID: {node}\nLocal Degree: {self.graph.localDegree(node)}", fontsize=10, bbox=dict(facecolor='white', alpha=0.5))

                if clicked_node is not None:
                    highlighted_edges = [(clicked_node, adj_node) for adj_node in G.adj[clicked_node]]

                    nx.draw(G, pos, labels=node_labels, with_labels=True, node_size=1000, font_size=10, ax=plt.gca(), node_color=node_colors)
                    nx.draw_networkx_edges(G, pos, edgelist=highlighted_edges, ax=plt.gca(), edge_color='red', width=2)
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
                plt.clf()  # Clear the current figure
                nx.draw(G, pos, labels=node_labels, with_labels=True, node_size=1000, font_size=10, ax=plt.gca(), node_color=node_colors)
                plt.title("Social Network Graph")
                plt.text(0.5, -0.1, f"Total Edges: {self.graph.edges}\n Average Global Degree: {self.graph.avgGlobalDegree()}", transform=plt.gca().transAxes, ha="center")
                plt.draw()

                legend_labels = []
                for i, community in enumerate(communities):
                    legend_labels.append(f'Community {i+1}')
                plt.legend(handles=[plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=cmap(i % len(communities)), label=label) for i, label in enumerate(legend_labels)])

        fig = plt.figure(figsize=(10, 6))
        nx.draw(G, pos, labels=node_labels, with_labels=True, node_size=1000, font_size=10, ax=plt.gca(), node_color=node_colors)

        legend_labels = []
        for i, community in enumerate(communities):
            legend_labels.append(f'Community {i+1}')
        plt.legend(handles=[plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=cmap(i % len(communities)), label=label) for i, label in enumerate(legend_labels)])


        nx.draw(G, pos, labels=node_labels, with_labels=True, node_size=1000, font_size=10, ax=plt.gca(), node_color=node_colors)
        plt.title("Social Network Graph")
        plt.text(0.5, -0.1, f"Total Edges: {self.graph.edges}\n Average Global Degree: {self.graph.avgGlobalDegree()}", transform=plt.gca().transAxes, ha="center")

        fig.canvas.mpl_connect('button_press_event', on_node_click)
        fig.canvas.mpl_connect('button_release_event', on_release)

        plt.tight_layout()
        plt.show()

def main():
    window = tk.Tk()
    window.title("Social Network Analysis")
    window.geometry("400x400")

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