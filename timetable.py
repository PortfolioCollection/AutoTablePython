from Builder import*
from Graph import*
from coursefinder import*
import time

class AutoTable:
    def __init__(self):
        self.fall = None
        self.winter = None
        self.year = None
        print("Initializing Table")

    def add_course(self,course):
        self.courses.append(course)

    def __str__(self):
        string = ""
        string+="Fall\n"
        for course in self.fall.courses:
            string += str(course) + "\n"
        string+="Winter:\n"
        for course in self.winter.courses:
            string += str(course) + "\n"
        string+="Year:\n"
        for course in self.year.courses:
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
        courses = self.organize_by_course(path[0])
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

    def construct_year(self,fall,winter,listed):
        compatible = {}
        print("--------------")
        ordered1 = self.by_year_courses(fall,listed)
        print("--------------")
        ordered2 = self.by_year_courses(winter,listed)
        optimal_solution = [None,None]
        optimal1 = 100000
        optimal2 = 100000
        print("---------------")
        for key in ordered1:
            if key in ordered2:
                #print(key)
                compatible[key] = []
                for solution in ordered1[key]:
                    compatible[key].append(solution)
                    if solution[1] < optimal1:
                        optimal1 = solution[1]
                        optimal_solution[0] = solution
                for solution in ordered2[key]:
                    compatible[key].append(solution)
                    if solution[1] < optimal2:
                        optimal2 = solution[1]
                        optimal_solution[1] = solution
        optimal_solution.append((optimal1,optimal2))
        return (optimal_solution,compatible)


    def index_year_courses(self,year_courses):
        listed = []
        for course in year_courses:
            for lecture in course.lectures:
                listed.append(str(lecture))
            for tutorial in course.tutorials:
                listed.append(str(tutorial))
            for practical in course.practicals:
                listed.append(str(practical))

        return listed

    def by_year_courses(self,session,listed):
        all_possible = {}
        for solution in session:
            key = ""
            courses = self.organize_by_course(solution[0])
            for course in courses:
                if course[-1] == "Y":
                    for section in courses[course]:
                        for i in range(len(listed)):
                            if str(section) == listed[i]:
                                key += str(i) + " " 
                    
            if key in all_possible:
                #print(all_possible[key][0])
                if all_possible[key][0][1] > solution[1]:
                    all_possible[key][0] = solution
            else:
                all_possible[key] = [solution]
        #for key in all_possible:
        #    print(key)
            #print(all_possible[key][0][1])
        return all_possible

def generate():
    start_time = time.time()
    autotable = AutoTable()
    #builder = Builder(autotable)
    #autotable = builder.build_table()
    scraper = Scraper(autotable)
    autotable = scraper.build_table()
    #print(autotable)
    
    print("\n")
    print("Fall:")
    courses = autotable.fall.courses
    courses.extend(autotable.year.courses)
    space1 = autotable.solution_space(courses)
    print("\n")
    print("Winter:")
    courses = autotable.winter.courses
    courses.extend(autotable.year.courses)
    space2 = autotable.solution_space(courses)
    listed = autotable.index_year_courses(autotable.year.courses)
    compatible = autotable.construct_year(space1,space2,listed)
    print("Fall:")
    for section in compatible[0][0][0]:
        print(section.name)
        print(section)
    print("Winter:")
    for section in compatible[0][1][0]:
        print(section.name)
        print(section)
    print("Distance: "+str(compatible[0][2]))
    print("--- %s seconds ---" % (time.time() - start_time))    

if __name__ == "__main__":
    generate()

    
    
