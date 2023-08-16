class Graph:
    def __init__(self):
        self.adjacencyList = []
    
    def createNode(self, name):
        self.adjacencyList.append(name, [])
    
    def addEdge(self, toName, fromName):
        self.createNode(toName)
        self.createNode(fromName)
        self.adjacencyList
    

