from collections import deque

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

        while self.edgeTo(target) != None:
            listOfPath.append(self.edgeTo[target])
            target = self.edgeTo[target]
        
        print("Distance to target: " + str(len(listOfPath)) + ", Path to target: " + str(listOfPath))
    
    def distanceToNode(self):
        return self.distTo

class Louvain:
    def __init__(self, graph):
        self.graph = graph
        self.community_assignment = {id: id for id in graph.adjacencyList}
    
    def modularity_gain(self, node, community):
        degree_node = self.graph.localDegree(node)
        degree_community = sum(self.graph.localDegree(neighbor) for neighbor in self.graph.adjacencyList[community])
    
        edges_between_communities = sum(1 for neighbor in self.graph.adjacencyList[node] if self.community_assignment[neighbor] == community)
    
        modularity_gain = (2 * edges_between_communities - degree_community * degree_node / (2 * self.graph.edges)) / (2 * self.graph.edges)
    
        return modularity_gain
        
    def move_node(self, node, target_community):
        self.community_assignment[node] = target_community
        
    def find_best_community(self, node):
        best_community = self.community_assignment[node]
        best_gain = 0
        
        for neighbor in self.graph.adjacencyList[node]:
            if self.community_assignment[neighbor] != self.community_assignment[node]:
                gain = self.modularity_gain(node, self.community_assignment[neighbor])
                if gain > best_gain:
                    best_gain = gain
                    best_community = self.community_assignment[neighbor]
        
        return best_community
    
    def apply_algorithm(self):
        changed = True
        
        while changed:
            changed = False
            
            for node in self.graph.adjacencyList:
                current_community = self.community_assignment[node]
                best_community = self.find_best_community(node)
                
                if best_community != current_community:
                    self.move_node(node, best_community)
                    changed = True