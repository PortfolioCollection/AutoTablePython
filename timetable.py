from Builder import*
from Graph import*

class AutoTable:
    def __init__(self):
        self.courses = []
        print("Initializing Table")

    def add_course(self,course):
        self.courses.append(course)

    def __str__(self):
        string = ""
        for course in self.courses:
            string += str(course) + "\n"
        return string

    def best_path(self,input_graph):
        initial_cast = input_graph.casts[0]
        global graph
        graph = input_graph
        visited = []
        restricted = []
        optimal = ([],10000)
        restricted.append(initial_cast)
        for timeslot in initial_cast.verticies:
            visited.append(timeslot)
            path = self.recursive_path(timeslot,visited[:],restricted[:],1)
            #for vertex in path[0]:
            #    print(vertex)
            #print("-------")
            if optimal[1] > path[1]:
                optimal = path
            visited = []

        return optimal
    
    def recursive_path(self,timeslot,visited,restricted,depth):
        
        global graph
        #print(len(restricted))
        #for cast in restricted:
            #print(cast.name)
        if len(visited) >= len(graph.casts):
            #print("Path at Depth: "+str(depth))
            #print("Restricted")
            #for cast in restricted:
            #    print(cast.name)
            #print(len(visited))
            #print("-------------")
            #print("Visited")
            #for vertex in visited:
            #    print(vertex)
            #print("-------------------------")
            return (visited,len(visited))
        else:
            optimal = ([],10000)
            for cast in graph.casts:
                if cast not in restricted:
                    restricted.append(cast)
                    for timeslot in cast.verticies:
                        visited.append(timeslot)
                        #print(str(len(restricted)-len(visited)))
                        path = self.recursive_path(timeslot,visited[:],restricted[:],depth+1)
                        #print((optimal,path))
                        if optimal[1] > path[1]:
                            optimal = path
                        visited.remove(timeslot)
                    #restricted.remove(cast)
            #print("Path at Depth: "+str(depth))
            #for vertex in visited:
            #    print(vertex)
            #print("-------------------------")
            return optimal
            
            

if __name__ == "__main__":
    autotable = AutoTable()
    builder = Builder(autotable)
    autotable = builder.build_table()
    graph = Graph()
    for course in autotable.courses:
        
        graph.add_course(course)
    #print(autotable)
    """
    for course in autotable.courses:
        print(course.name)
        print(course.compress_times())
    graph.connect_graph()
    for cast in graph.casts:
        print(cast.name)
        for vertex in cast.verticies:
            for edge in vertex.edges:
                print(edge)
        print("----------------")
    """
    print(graph)
    path = autotable.best_path(graph)
    print(path)
    for vertex in path[0]:
        print(vertex)
