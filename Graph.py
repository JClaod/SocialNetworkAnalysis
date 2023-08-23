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
    
    def neighbors(self, id):
        return self.adjacencyList[id]
    
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
        self.edgeTo = {id: None for id in graph.adjacencyList}
        self.distTo = {id: float('inf') for id in graph.adjacencyList}
        self.graph = graph
        self.source = source

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
        
        return listOfPath
    
    def hasPathTo(self, target):
        if self.distTo[target] != float('inf'):
            return True
        return False

    def distanceToNode(self):
        return self.distTo
    
    def closenessCentrality(self):
        closeness = ""

        for id in sorted(self.distTo):
            if id == self.source:
                continue
            information = self.graph.id_to_names[id]
            closeness += "-" + f'{information[1]}: {self.distTo[id]}' + "\n"
        
        return closeness