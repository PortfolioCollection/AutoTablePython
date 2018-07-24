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
            #print(path[1])
            #for vertex in path[0]:
            #    print(vertex)
            #print("done")
            if optimal[1] > path[1] and path[1] >= 0:
                optimal = path
            visited = []
        return optimal
    
    def recursive_path(self,timeslot,visited,restricted,depth,distance):
        global graph
        if len(visited) >= len(graph.casts):
            global checks
            checks += 1
            """
            print("Distance: "+str(distance))
            for v in visited:
                print(v)
            print("------------------------")
            """
            return (visited,distance)
        
        if len(restricted) >= len(graph.casts):
            return (visited,100000)

        else:
            optimal = ([],10000)
            for cast in graph.casts:
                if cast not in restricted:
                    restricted.append(cast)
                    for timeslot in cast.verticies:
                        additional = self.get_closest_distance(visited,timeslot,distance)
                        if additional < 100000:
                            visited.append(timeslot)
                            #print(additional)
                            path = self.recursive_path(timeslot,visited[:],restricted[:],depth+1,additional)
                            if optimal[1] > path[1]:
                                optimal = path
                            visited.remove(timeslot)
            return optimal


    def get_closest_distance(self,visited,timeslot,distance):
        for vertex in visited:
            overlap = self.has_overlap(vertex.start,vertex.end,timeslot.start,timeslot.end)
            if overlap == True:
                return 100000
        day = self.sort_by_day(visited,timeslot)
        found = False
        if len(day) == 0:
            distance += 0
        elif len(day) == 1:
            if timeslot.start > day[0].start:
                distance += timeslot.start-day[0].end
            else:
                distance += day[0].start-timeslot.end
                
        
        elif len(day) > 1:
            for i in range(len(day)):
                if timeslot.end <= day[i].start:
                    if i == 0:
                        distance += day[i].start-timeslot.end
                        found = True
                        break
                    elif i < len(day):
                        distance -= (timeslot.end-timeslot.start)
                        found = True
                        break
            if found == False:
                distance += timeslot.start-day[-1].end
        return distance
        #if distanceb >= distance:
        """print("-------")
        print(timeslot)
        print(distanceb)
        print(distance)
        print("-------------")
        for vertex in day:
            print(vertex)
        print("-------------")
        """

    def sort_by_day(self,visited,timeslot):
        lst = []
        end = int(timeslot.end)
        if end < 24:
            day = (0,24)
        elif end < 48:
            day = (24,48)
        elif end < 72:
            day = (48,72)
        elif end < 96:
            day = (72,96)
        elif end < 120:
            day = (96,120)
        else:
            day = (0,120)
        #print(day)
        for vertex in visited:
            if self.has_overlap(day[0],day[1],vertex.start,vertex.end)==True:
                lst.append(vertex)
        lst.sort(key=lambda vertex: vertex.start)
        """print("--------")
        for a in lst:
            print(a)
        print("-----")
        """
        return lst        

    def has_overlap(self,x1,x2,y1,y2):
        return x1 < y2 and y1 < x2

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
