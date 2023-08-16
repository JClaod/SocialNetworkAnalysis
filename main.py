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
        self.adjacencyList[toNode].extend(fromNode)
        self.adjacencyList[fromNode].extend(toNode)