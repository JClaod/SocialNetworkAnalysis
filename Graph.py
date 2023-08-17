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

    def addEdge(self, toNode, fromNode):
        self.adjacencyList[toNode].append(fromNode)
        self.adjacencyList[fromNode].append(toNode)
    
    def localDegree(self, node):
        return len(self.adjacencyList[node])
    
    def avgGlobalDegree(self):
        total_participants = len(self.adjacencyList)
        total_degree = 0

        for item in self.adjacencyList:
            total_degree += self.localDegree(item)

        return total_degree/total_participants
