from Builder import*
from Graph import*


checks = 0

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
            path = self.recursive_path(timeslot,visited[:],restricted[:],1,0)
            if optimal[1] > path[1]:
                optimal = path
            visited = []
        return optimal
    
    def recursive_path(self,timeslot,visited,restricted,depth,distance):
        global graph
        if len(visited) >= len(graph.casts):
            global checks
            checks += 1
            return (visited,distance)
        
        else:
            optimal = ([],10000)
            for cast in graph.casts:
                if cast not in restricted:
                    restricted.append(cast)
                    for timeslot in cast.verticies:
                        additional = self.get_closest_distance(visited,timeslot)
                        visited.append(timeslot)
                        #print(additional)
                        path = self.recursive_path(timeslot,visited[:],restricted[:],depth+1,distance+additional)
                        if optimal[1] > path[1]:
                            optimal = path
                        visited.remove(timeslot)
            return optimal


    def get_closest_distance(self,visited,timeslot):
        distance = 1000
        for vertex in visited:
            distance = min(distance,abs(int(timeslot.end)-int(vertex.start)))
            distance = min(distance,abs(int(timeslot.start)-int(vertex.end))) 
        return distance

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
    graph.connect_graph()
    #print(graph)
    path = autotable.best_path(graph)
    print("Optimal distance: "+str(path[1]))
    for vertex in path[0]:
        print(vertex)
    
    print(checks)
