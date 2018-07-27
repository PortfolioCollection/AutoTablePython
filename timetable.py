from Builder import*
from Graph import*


class AutoTable:
    def __init__(self):
        self.fall = None
        self.winter = None
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
        global checks
        global distribution
        global solutions
        checks = 0
        distribution = {}
        solutions = []
        
        graph = input_graph
        visited = []
        restricted = []
        optimal = ([],10000)
        restricted.append(initial_cast)
        for timeslot in initial_cast.verticies:
            visited.append(timeslot)
            path = self.recursive_path(timeslot,visited[:],restricted[:],1,0)
            if optimal[1] > path[1] and path[1] >= 0:
                optimal = path
            visited = []
        global solutions
        return (optimal,solutions)
    
    def recursive_path(self,timeslot,visited,restricted,depth,distance):
        global graph
        
        if len(visited) == len(graph.casts):
            global checks
            global solutions
            global distribution
            if distance in distribution:
                distribution[distance] = distribution[distance]+1
            else:
                distribution[distance] = 1
            checks += 1
            solutions.append((visited,distance))
            return (visited,distance)

        if len(restricted) > len(visited):
            return (visited,100000)

        else:
            optimal = ([],100000)
            for cast in graph.casts:
                if cast not in restricted:
                    restricted.append(cast)
                    for timeslot in cast.verticies:
                        additional = self.get_closest_distance(visited,timeslot,distance)
                        if additional < 100000:
                            visited.append(timeslot)
                            path = self.recursive_path(timeslot,visited[:],restricted[:],depth+1,additional)
                            if optimal[1] > path[1]:
                                optimal = path
                            visited.remove(timeslot)
            return optimal


    def get_closest_distance(self,visited,timeslot,distance):
        found = False
        for vertex in visited:
            for tup1 in vertex.times:
                for tup2 in timeslot.times:
                    overlap = self.has_overlap(tup1[0],tup1[1],tup2[0],tup2[1])
                    if overlap == True:
                        return 100000
        for tup in timeslot.times:
            day = self.sort_by_day(visited,tup[0],tup[1])
            if len(day) == 0:
                distance += 0
            elif len(day) == 1:
                if tup[0] > day[0][0]:
                    distance += tup[0]-day[0][1]
                else:
                    distance += day[0][0]-tup[1]
                    
            
            elif len(day) > 1:
                for i in range(len(day)):
                    if tup[1] <= day[i][0]:
                        if i == 0:
                            distance += day[i][0]-tup[1]
                            found = True
                            break
                        elif i < len(day):
                            distance -= (tup[1]-tup[0])
                            found = True
                            break
                if found == False:
                    distance += tup[0]-day[-1][1]
        return distance

    def sort_by_day(self,visited,start,end):
        lst = []
        end = int(end)
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
        for vertex in visited:
            for tup1 in vertex.times:
                if self.has_overlap(day[0],day[1],tup1[0],tup1[1])==True:
                    lst.append(tup1)
        lst.sort(key=lambda tup: tup[0])
        return lst        

    def has_overlap(self,x1,x2,y1,y2):
        return x1 < y2 and y1 < x2

    def solution_space(self,session):
        graph = Graph()
        for course in session:
            graph.add_course(course)
        path,all_paths = self.best_path(graph)
        print("Optimal distance: "+str(path[1]))
        courses = self.organize_by_course(path[0])
        for course in courses:
            print(course+":")
            for section in courses[course]:
                print(section)
        print("Num Possible Solutions: "+str(checks))
        print("Permutations: "+str(graph.num_combinations()))
        print("--------------")
        for key in distribution:
            print(str(key)+" gaps: "+" "*(3-len(str(key)))+str(distribution[key])+" sols")
        return all_paths

    def organize_by_course(self,solution):
        courses = {}
        for vertex in solution:
            name = vertex.name+vertex.session
            if name in courses:
                courses[name].append(vertex)
            else:
                courses[name] = [vertex]
        return courses

    def construct_year(self,fall,winter):
        compatible = {}
        print("--------------")
        ordered1 = self.by_year_courses(fall)
        print("--------------")
        ordered2 = self.by_year_courses(winter)
        
        for key in ordered1:
            if key in ordered2:
                compatible[key] = []
                for solution in ordered1[key]:
                    compatible[key].append(solution)
                for solution in ordered2[key]:
                    compatible[key].append(solution)
        return compatible
        

    def by_year_courses(self,session):
        all_possible = {}
        for solution in session:
            courses = self.organize_by_course(solution[0])
            for course in courses:
                if course[-1] == "Y":
                    key = course
                    for section in courses[course]:
                        key += " "+section.type+section.code
                    if key in all_possible:
                        all_possible[key].append(solution)
                    else:
                        all_possible[key] = [solution]
        for key in all_possible:
            print(key)
        return all_possible
                    
        

if __name__ == "__main__":
    autotable = AutoTable()
    builder = Builder(autotable)
    autotable = builder.build_table()
    print("\n")
    print("Fall:")
    space1 = autotable.solution_space(autotable.fall.courses)
    print("\n")
    print("Winter:")
    space2 = autotable.solution_space(autotable.winter.courses)
    compatible = autotable.construct_year(space1,space2)
    optimal = 100000
    optimal_solution = []
    for key in compatible:
        for solution in compatible[key]:
            if solution[1] < optimal:
                optimal_solution = solution

    for section in optimal_solution[0]:
        print(section.name)
        print(section)

    
    
