from Builder import*
from Graph import*
from Scraper import*
import time


class AutoTable:
    def __init__(self):
        self.fall = None
        self.winter = None
        self.year = None
        self.graph = None
        self.checks = 0
        self.solutions = []
        self.distribution = {}
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
        self.checks = 0
        self.distribution = {}
        self.solutions = []
        
        self.graph = input_graph
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
        return (optimal,self.solutions)
    
    def recursive_path(self,timeslot,visited,restricted,depth,distance):
        if len(visited) == len(self.graph.casts):
            if distance in self.distribution:
                self.distribution[distance] = self.distribution[distance]+1
            else:
                self.distribution[distance] = 1
            self.checks += 1
            self.solutions.append((visited,distance))
            return (visited,distance)

        if len(restricted) > len(visited):
            return (visited,100000)

        else:
            optimal = ([],100000)
            for cast in self.graph.casts:
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

    def get_day(self,end):
        return math.floor(end/24)

        

    def sort_by_day(self,visited,start,end):
        """
        sort_by_day(self,visited,start,end) -> list of tuples
        """
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
        """
        (self,x1,x2,y1,y2) -> boolean

        @param x1: begining of interval 1
        @param x2: ending of interval 1
        @param y1: begining of interval 2
        @param y2: ending of interval 2

        Returns True if the intervals overlap
        Returns Fals otherwise
        """
        return x1 < y2 and y1 < x2

    def solution_space(self,session):
        """
        solution_space(session) -> list of strings

        @param session: a fall or winter session

        Returns a list of strings of all possible solutions
        """
        graph = Graph()
        for course in session:
            graph.add_course(course)
        path,all_paths = self.best_path(graph)
        courses = self.organize_by_course(path[0])
        print("Num Possible Solutions: "+str(self.checks))
        print("Permutations: "+str(graph.num_combinations()))
        print("--------------")
        return all_paths

    def organize_by_course(self,solution):
        """
        organize_by_course(self,solution) -> list of courses

        Returns a list of courses given a solution of strings
        """
        courses = {}
        for vertex in solution:
            name = vertex.name+vertex.session
            if name in courses:
                courses[name].append(vertex)
            else:
                courses[name] = [vertex]
        return courses

    def construct_year(self,fall,winter,listed):
        """
        construct_year(fall,winter,listed) -> tuple

        @param fall: fall solution space
        @param winter: winter solution space
        @param listed: list of yearly sections

        Returns a tuple of a smallest gap solution and the set of all possible solutions
        """
        compatible = {}
        print("--------------")
        ordered1 = self.by_year_courses(fall,listed)
        print("--------------")
        ordered2 = self.by_year_courses(winter,listed)
        print("---------------")
        lst = []
        
        for key in ordered1:
            if key in ordered2:
                optimal1 = 100000
                optimal2 = 100000
                optimal_solution = [None,None]
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
                lst.append((optimal_solution,optimal1,optimal2))
                
        optimal = 100000
        optimal1 = 100000
        optimal2 = 100000
        optimal_solution = []
        for item in lst:
            distance = item[1]+item[2]
            if distance<optimal:
                optimal = distance
                optimal_solution = item[0]
                optimal1 = item[1]
                optimal2 = item[2]
        optimal_solution.append((optimal1,optimal2))
        return (optimal_solution,compatible)


    def index_year_courses(self,year_courses):
        """
        index_year_courses(year_courses) -> list

        @param year_courses: a list of yearly courses

        Returns a list of all section strings for every yearly course
        """
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
        """
        by_year_courses(session,listed) -> dict

        @param session: fall or winter solution space
        @param listed: list of yearly sections

        Returns a dictionary for each yearly configuration with
        a best solution attached to it
        """
        all_possible = {}
        for solution in session:
            key = []
            courses = self.organize_by_course(solution[0])
            for course in courses:
                if course[-1] == "Y":
                    for section in courses[course]:
                        for i in range(len(listed)):
                            if str(section) == listed[i]:
                                key.append(i)
            key.sort()
            key = str(key)
            if key in all_possible:
                if all_possible[key][0][1] > solution[1]:
                    all_possible[key][0] = solution
            else:
                all_possible[key] = [solution]
        return all_possible

def generate():
    "----------Start up the course times------------"
    
    autotable = AutoTable()
    scraper = Scraper(autotable)
    autotable = scraper.build_table()
    #builder = Builder(autotable)
    #autotable = builder.build_table()
    start_time = time.time()
    "----------Get all Fall Timetables------------"
    courses = autotable.fall.courses
    courses.extend(autotable.year.courses)
    space1 = autotable.solution_space(courses)
    "----------Get all Winter Timetables------------"
    courses = autotable.winter.courses
    courses.extend(autotable.year.courses)
    space2 = autotable.solution_space(courses)
    "-----------Combine fall and winter-------------"
    
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
