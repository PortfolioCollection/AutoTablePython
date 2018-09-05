from Builder import*
from Graph import*
from Scraper import*
from Timeblock import*
from GUI import*
from tkinter import Tk, Label, Button
from tkinter import W
import time
import math
import copy

timeblocks = [[],[],[],[],[]]
for day in timeblocks:
    morning = Timeblock(8,12,lambda x: (12-8)-x-1)
    evening = Timeblock(17,22,lambda x: x)
    day.append(morning)
    day.append(evening)
    
class AutoTable:
    def __init__(self):
        self.fall = None
        self.winter = None
        self.year = None

def has_overlap(x1,x2,y1,y2):
        return x1 < y2 and y1 < x2

def check_section_overlap(section1,section2):
    for time1 in section1.times:
        for time2 in section2.times:
            if has_overlap(time1[0],time1[1],time2[0],time2[1]):
                return True
    return False

def solution_vertex_conflict(solution,vertex):
    for i in range(len(vertex.days)):
        day = vertex.days[i][1]
        time = vertex.times[i]
        for timeslot in solution[day]:
            if has_overlap(time[0],time[1],timeslot.start,timeslot.end):
                return True
    return False

def update_distance(solution,vertex,distance):
    found = False
    for i in range(len(vertex.days)):
        day = vertex.days[i][1]
        if len(solution[day]) == 0:
            distance += 0
        elif len(solution[day]) >= 1:
            if vertex.times[i][0] >= solution[day][-1].end:
                distance += vertex.times[i][0] - solution[day][-1].end
            elif vertex.times[i][1] <= solution[day][0].start:
                distance += solution[day][0].start - vertex.times[i][1]
            else:
                distance -= (vertex.times[i][1]-vertex.times[i][0])
    return distance


def timeblocking(vertex,distance):
    global timeblocks
    addition = 0
    for i in range(len(vertex.days)):
        day = vertex.days[i][1]
        for block in timeblocks[day]:
            # time is inside the block
            if block.start <= vertex.times[i][0] and block.end >= vertex.times[i][1]:
                index = int(vertex.times[i][0]-block.start)
                length = int(vertex.times[i][1] - vertex.times[i][0])
                for i in range(index,index+length):
                    addition += block.interval[i]
                break
            # block is inside the time
            if vertex.times[i][0] <= block.start and vertex.times[i][1] >= block.end:
                addition += block.end - block.start
                break
            # time is clipping bottom of block
            elif vertex.times[i][0] < block.end and vertex.times[i][1] > block.end:
                addition += 2**(block.end-vertex.times[i][0])
            # time is clipping top of block
            elif vertex.times[i][0] < block.start and vertex.times[i][1] > block.start:
                addition += 2**(vertex.times[i][1]-block.start)
    return int(distance + addition)
                    
def combine_casts(cast1,cast2):
    solutions = []
    for vertex1 in cast1.verticies:
        for vertex2 in cast2.verticies:
            if check_section_overlap(vertex1,vertex2) == False:
                solution = [[],[],[],[],[]]
                vertex_to_solution(solution,vertex1)
                distance = update_distance(solution,vertex2,0)
                #distance = timeblocking(vertex1,0)
                #distance = timeblocking(vertex2,distance)
                vertex_to_solution(solution,vertex2)
                solutions.append([solution,distance])
    return solutions

def vertex_to_solution(solution,vertex):
    for i in range(len(vertex.days)):
        timeslot = Timeslot(vertex.name+" "+vertex.type+vertex.code,vertex.days[i],vertex.times[i])
        day = vertex.days[i][1]
        if len(solution[day]) == 0:
            solution[day].append(timeslot)
        elif timeslot.end <= solution[day][0].start:
            solution[day].insert(0,timeslot)
        else:
            for j in range(len(solution[day])-1,-1,-1):
                if timeslot.start >= solution[day][j].end:
                    solution[day].insert(j+1,timeslot)
                    break
    return solution
        
def grow_solution(cast,solutions):
    new_solutions = []
    for vertex in cast.verticies:
        for solution in solutions:
            combination = [x[:] for x in solution[0]]
            if solution_vertex_conflict(combination,vertex) == False:
                distance = update_distance(combination,vertex,solution[1])
                #distance = timeblocking(vertex,solution[1])
                vertex_to_solution(combination,vertex)
                new_solutions.append([combination,distance])
    return new_solutions

def generate_semester(courses):
    if len(courses) == 0:
        return []
    graph = Graph()
    for course in courses:
        graph.add_course(course)
    graph.casts.sort(key=lambda x: x.combinations)
    cast1 = graph.casts[0]
    cast2 = graph.casts[1]
    solutions = combine_casts(cast1,cast2)
    print(len(solutions))
    for i in range(2,len(graph.casts)):
        solutions = grow_solution(graph.casts[i],solutions)
        print(len(solutions))
    print("----------------")
    return solutions

def optimal(solutions):
    optimal = 10000
    optimal_soltution = [] 
    for solution in solutions:
        if solution[1] < optimal:
            optimal = solution[1]
            optimal_soltution = solution[0]
    return (optimal_soltution,optimal)



def year_fall_winter_merge(year_solutions,fall_courses, winter_courses):
    fall = Graph()
    for course in fall_courses:
        fall.add_course(course)
    fall.casts.sort(key=lambda x: x.combinations)

    winter = Graph()
    for course in winter_courses:
        winter.add_course(course)
    winter.casts.sort(key=lambda x: x.combinations)

    year = []
    for solution in year_solutions:
        "Do Fall"
        fall_version = [solution[:]]
        for i in range(len(fall.casts)):
            fall_version = grow_solution(fall.casts[i],fall_version)
        "Do Winter"
        winter_version = [solution[:]]
        for i in range(len(winter.casts)):
            winter_version = grow_solution(winter.casts[i],winter_version)


        fall_optimal, fall_distance = optimal(fall_version)
        winter_optimal, winter_distance = optimal(winter_version)
                
        total_solution = [fall_optimal,winter_optimal]
        year.append((total_solution,fall_distance,winter_distance))

    optimal1 = 100000
    optimal2 = 100000
    optimal_solution = None
    for entry in year:
        if entry[1]+entry[2] < optimal1+optimal2:
            optimal1 = entry[1]
            optimal2 = entry[2]
            optimal_solution = entry[0][:]
            
    return (optimal_solution,optimal1,optimal2)
    
def fall_winter_merge(fall_courses, winter_courses):
    
    print("Fall Space")
    fall_optimal = []
    fall_version = generate_semester(fall_courses)
    if(len(fall_courses) > 0):
        fall_optimal, fall_distance = optimal(fall_version)
    print("Winter Space")
    winter_optimal = []
    winter_version = generate_semester(winter_courses)
    if(len(winter_courses) > 0):
        winter_optimal, winter_distance = optimal(winter_version)
        
    optimal_solution = [fall_optimal,winter_optimal]
        
    return (optimal_solution,fall_distance,winter_distance)

def solution_selection(solution,selector):
    if selector == "timeblocking":
        print("timeblocking")
    elif selector == "min_gap":
        print("min_gap")
    
        
def generate():
    "----------Start up the course times------------"
    autotable = AutoTable()
    scraper = Scraper(autotable)
    autotable = scraper.build_table()
    #builder = Builder(autotable)
    #autotable = builder.build_table()
    start_time = time.time()
    print("Year Space")
    year_solutions = generate_semester(autotable.year.courses)
    if len(year_solutions) == 0:
        optimal_solution = fall_winter_merge(autotable.fall.courses, autotable.winter.courses)
    else:
        optimal_solution = year_fall_winter_merge(year_solutions, autotable.fall.courses, autotable.winter.courses)
    
    print("Fall")
    for day in optimal_solution[0][0]:
        for timeslot in day:
            print(timeslot)
    print("Winter")
    for day in optimal_solution[0][1]:
        for timeslot in day:
            print(timeslot)
    print("Fall Distance: "+str(optimal_solution[1])+
          "    Winter Distance: "+str(optimal_solution[2]))
    print("--- Full algorithm %s seconds ---" % (time.time() - start_time))
    root = Tk()
    gui1 = MyFirstGUI(optimal_solution[0][0],"Fall",root)
    root.mainloop()
    root = Tk()
    gui2 = MyFirstGUI(optimal_solution[0][1],"Winter",root)
    root.mainloop()
    
    
if __name__ == "__main__":
    generate()
