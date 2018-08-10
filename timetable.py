from Builder import*
from Graph import*
from Scraper import*
import time
import math


class AutoTable:
    def __init__(self):
        self.fall = None
        self.winter = None
        self.year = None
        print("Initializing Table")


def get_distance(time1,time2):
    if time1[0] < time2[0]:
        distance = time2[0] - time1[1]
    else:
        distance = time1[0] - time2[1]
    return distance

def update_distance(visited,timeslot,distance):
    found = False
    for tup in timeslot.times:
        day = sort_by_day(visited,tup[0],tup[1])
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

def sort_by_day(visited,start,end):
    """
    sort_by_day(self,visited,start,end) -> list of tuples
    """
    lst = []
    end = int(end)
    bottom = math.floor(end/24)
    day = (bottom*24,bottom*24+24)
    for vertex in visited:
        for tup1 in vertex.times:
            if has_overlap(day[0],day[1],tup1[0],tup1[1])==True:
                lst.append(tup1)
    lst.sort(key=lambda tup: tup[0])
    return lst       
    

def has_overlap(x1,x2,y1,y2):
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


def check_section_overlap(section1,section2):
    for time1 in section1.times:
        for time2 in section2.times:
            if has_overlap(time1[0],time1[1],time2[0],time2[1]):
                return True
    return False

def combine_casts(cast1,cast2):
    solutions = []
    for vertex1 in cast1.verticies:
        for vertex2 in cast2.verticies:
            if check_section_overlap(vertex1,vertex2) == False:
                solution = [vertex1,vertex2]
                distance = update_distance([vertex1],vertex2,0)
                
                solutions.append([solution,distance])
    return solutions

def combine_solutions(cast1,solutions):
    conflict = False
    new_solutions = []
    for vertex1 in cast1.verticies:
        for solution in solutions:
            for vertex in solution[0]:
                if check_section_overlap(vertex1,vertex) == True:
                    conflict = True
                    break
            if conflict == False:
                combination = solution[0][:]
                distance = update_distance(combination,vertex1,solution[1])
                
                combination.append(vertex1)
                new_solutions.append([combination,distance])
            else:
                conflict = False
    return new_solutions


def generate_semester(courses):
    graph = Graph()
    for course in courses:
        graph.add_course(course)

    cast1 = graph.casts[0]
    cast2 = graph.casts[1]
    solutions = combine_casts(cast1,cast2)
    
    for i in range(2,len(graph.casts)):
        solutions = combine_solutions(graph.casts[i],solutions)
    return solutions

def construct_year(fall,winter,listed,dictionary):
        """
        construct_year(fall,winter,listed) -> tuple

        @param fall: fall solution space
        @param winter: winter solution space
        @param listed: list of yearly sections

        Returns a tuple of a smallest gap solution and the set of all possible solutions
        """
        compatible = {}
        print("--------------")
        start_time = time.time()
        ordered1 = by_year_courses(fall,listed,dictionary)
        print("--- Fall by year %s seconds ---" % (time.time() - start_time)) 
        print("--------------")
        start_time = time.time()
        ordered2 = by_year_courses(winter,listed,dictionary)
        print("--- Winter by year %s seconds ---" % (time.time() - start_time)) 
        print("---------------")
        lst = []
        
        for key in ordered1:
            if key in ordered2:
                fall = ordered1[key]
                winter = ordered2[key]
                solution = (fall[0],winter[0],fall[1]+winter[1])
                lst.append(solution)
                
        optimal = 100000
        optimal_solution = []
        for item in lst:
            #print(item)
            if item[2]<optimal:
                optimal = item[2]
                optimal_solution = [item[0],item[1]]
        optimal_solution.append(optimal)
        return (optimal_solution)

def index_year_courses(year_courses):
    """
    index_year_courses(year_courses) -> list

    @param year_courses: a list of yearly courses

    Returns a list of all section strings for every yearly course
    """
    listed = []
    dictionary = {}
    counter = 0
    for course in year_courses:
        for lecture in course.lectures:
            string = str(lecture)
            listed.append(string)
            dictionary[string] = counter
            counter+=1
        for tutorial in course.tutorials:
            string = str(tutorial)
            listed.append(string)
            dictionary[string] = counter
            counter+=1
        for practical in course.practicals:
            string = str(practical)
            listed.append(string)
            dictionary[string] = counter
            counter+=1
    return (listed,dictionary)

def organize_by_course(solution):
        """
        organize_by_course(self,solution) -> list of courses

        Returns a list of courses given a solution of strings
        """
        courses = {}
        for vertex in solution:
            if vertex.session == "Y":
                name = vertex.name+vertex.session
                if name in courses:
                    courses[name].append(vertex)
                else:
                    courses[name] = [vertex]
        return courses


def by_year_courses(session,listed,dictionary):
    """
    by_year_courses(session,listed) -> dict

    @param session: fall or winter solution space
    @param listed: list of yearly sections

    Returns a dictionary for each yearly configuration with
    a best solution attached to it
    """
    all_possible = {}
    duration1 = 0
    duration2 = 0
    out_counter = 0
    for solution in session:
        start_time1 = time.time()
        key = []
        for section in solution[0]:
            out_counter+=1
            if section.session == "Y":
                string = str(section)
                if string in dictionary:
                    key.append(dictionary[string])
                        
        end_time1 = time.time()
        duration1 += end_time1-start_time1
        key.sort()
        key = str(key)
        start_time2 = time.time()
        if key in all_possible:
            if all_possible[key][1] > solution[1]:
                all_possible[key][0] = solution[0]
                all_possible[key][1] = solution[1]
        else:
            all_possible[key] = solution
        end_time2 = time.time()
        duration2 += end_time2-start_time2
    print("--- Part 1 %s seconds ---" % (duration1))
    print("--- Part 2 %s seconds ---" % (duration2))
    print("Out Counter: "+str(out_counter))
    return all_possible
    
def generate():
    "----------Start up the course times------------"
    start_time = time.time()
    autotable = AutoTable()
    scraper = Scraper(autotable)
    autotable = scraper.build_table()
    print("--- Scrapper time %s seconds ---" % (time.time() - start_time))  
    #builder = Builder(autotable)
    #autotable = builder.build_table()
    start_time = time.time()
    "Fall courses"
    start_time_half = time.time()
    courses = autotable.fall.courses
    courses.extend(autotable.year.courses)
    fall_space = generate_semester(courses)
    print(len(fall_space))
    print("--- Fall half year %s seconds ---" % (time.time() - start_time_half))  
    "Winter courses"
    start_time_half = time.time()
    courses = autotable.winter.courses
    courses.extend(autotable.year.courses)
    winter_space = generate_semester(courses)
    print(len(winter_space))
    print("--- Winter half year %s seconds ---" % (time.time() - start_time_half)) 
    "Year courses"
    start_time_year = time.time()
    listed,dictionary = index_year_courses(autotable.year.courses)
    print("--- List year courses %s seconds ---" % (time.time() - start_time_year)) 
    compatible = construct_year(fall_space,winter_space,listed,dictionary)
    print("Fall:")
    for section in compatible[0]:
        print(section.name)
        print(section)
    print("Winter:")
    for section in compatible[1]:
        print(section.name)
        print(section)
    print("Distance: "+str(compatible[2]))
    print("--- Full algorithm %s seconds ---" % (time.time() - start_time))   

if __name__ == "__main__":
    generate()
