from collections import deque

class Graph:
    def __init__(self):
        self.id_to_names = []
        self.adjacencyList = {}
        self.userKeys = 0
    
    def createNode(self, name):
        id = self.userKeys
        self.adjacencyList[id] = []
        self.id_to_names.append([id, name])
        self.userKeys += 1

    def addEdge(self, toID, fromID):
        self.adjacencyList[toID].append(fromID)
        self.adjacencyList[fromID].append(toID)
    
    def localDegree(self, id):
        return len(self.adjacencyList[id])
    
    def avgGlobalDegree(self):
        total_participants = len(self.adjacencyList)
        total_degree = 0

        for id in self.adjacencyList:
            total_degree += self.localDegree(id)

        return total_degree/total_participants
    
class GraphTraversal:
    def __init__(self, g, source):
        self.listOfPath = []
        self.edgeTo = {id: float('inf') for id in self.g.adjacencyList}
        self.distTo = {id: None for id in self.g.adjacencyList}
        self.g = g
        self.source = source
    
    def shortestPath(self):
        self.distTo[self.source] = 0
        queue = deque([self.source])

        while queue:
            current = queue.popleft()

            for friend in self.g.adjacencyList[current]:
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