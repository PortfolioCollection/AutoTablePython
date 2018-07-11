# csc373

class Vertex:
    def __init__(self,index):
        self.index = index
        self.edges = []
        self.visited = False

    def __str__(self):
        return "Vertex: "+str(self.index)

class Edge:
    def __init__(self,v1,v2):
        self.v1 = v1
        self.v2 = v2
        
    def __str__(self):
        return "Edge: ("+str(self.v1.index)+")("+str(self.v2.index)+")"
        
class Graph:
    def __init__(self,V=[],E=[]):
        self.V = V
        self.E = E

    def add_vertex(self,vertex):
        flag = True
        for v in self.V:
            if vertex.index == v.index:
                print("Vertex already exists")
                flag = False
                break
        if(flag):
            self.V.append(vertex)

    def add_edge(self,e):
        self.E.append(e)
        e.v1.edges.append(e)
        e.v2.edges.append(e)

    def detect_cycles(self,path,v):
        i = 0
        if v.visited == True:
            print(len(path))
            for edge in path:
                print(edge)
        
        elif len(v.edges)==1:
            v.visited = True
            
        elif len(v.edges)>1:
            for edge in v.edges:
                if edge not in path:
                    p = path[:]
                    p.append(edge)
                    v.visited = True
                    if v == edge.v1:
                        self.detect_cycles(p,edge.v2)
                    else:
                        self.detect_cycles(p,edge.v1)

    def connect_MST(self):
        

    def __str__(self):
        print("----Verticies----")
        for v in self.V:
            print(v)
        print("------Edges------")
        for e in self.E:
            print(e)
        return ""

if __name__ == "__main__":
    graph = Graph()
    v1 = Vertex(1)
    v2 = Vertex(2)
    v3 = Vertex(3)
    v4 = Vertex(4)
    v5 = Vertex(5)
    v6 = Vertex(6)
    graph.add_vertex(v1)
    graph.add_vertex(v2)
    graph.add_vertex(v3)
    graph.add_vertex(v4)
    graph.add_vertex(v5)
    graph.add_vertex(v6)
    e1 = Edge(v1,v2)
    e2 = Edge(v2,v3)
    e3 = Edge(v3,v4)
    e4 = Edge(v4,v5)
    e5 = Edge(v5,v6)
    e6 = Edge(v1,v6)
    graph.add_edge(e1)
    graph.add_edge(e2)
    graph.add_edge(e3)
    graph.add_edge(e4)
    graph.add_edge(e5)
    graph.add_edge(e6)
    graph.detect_cycles([],v3)
    print(graph)




    
    


    
    
