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

if __name__ == "__main__":
    autotable = AutoTable()
    builder = Builder(autotable)
    autotable = builder.build_table()
    graph = Graph()
    for course in autotable.courses:
        graph.add_course(course)
    print(autotable)
    
    for course in autotable.courses:
        print(course.name)
        print(course.compress_times())
    graph.connect_graph()
    #print(graph)
    for edge in graph.edges:
        print(edge
    
    

    
