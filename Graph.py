class Cast:
    def __init__(self,name):
        self.name = name
        self.verticies = []
        self.edges = []
        self.combinations = 1

    def add_vertex(self,vertex):
        vertecies.append(vertex)

    def __str__(self):
        string = self.name+":\n"
        for vertex in self.verticies:
            string += str(vertex) + "\n"
        return string

class Graph:
    def __init__(self):
        self.casts = []
        self.edges = []

    def add_course(self,course):
        course_vertex = []
        tup = course.compress_times()
        #print(tup)
        i = 0
        name = course.name+" lectures"
        cast = Cast(name)
        for lecture in tup[0]:
            cast.verticies.append(lecture)
            i+= 1
        if i > 0:
            cast.combinations *= i
            self.casts.append(cast)
        i = 0
        name = course.name+" tutorials"
        cast = Cast(name)
        for tutorial in tup[1]:
            cast.verticies.append(tutorial)
            i+= 1
        
        if i > 0:
            cast.combinations *= i
            self.casts.append(cast)
            
        i = 0
        name = course.name+" practicals"
        cast = Cast(name)
        for practical in tup[2]:
            cast.verticies.append(practical)
            i+= 1
        if i > 0:
            cast.combinations *= i
            self.casts.append(cast)

    def connect_casts(self,cast1,cast2):
        for i in range(len(cast1.verticies)):
            for j in range(len(cast2.verticies)):
                overlap = self.has_overlap(cast1.verticies[i].start,cast1.verticies[i].end,
                                           cast2.verticies[j].start,cast2.verticies[j].end)
                if overlap == False:
                    self.add_edge(cast1,cast2,
                                  cast1.verticies[i], cast2.verticies[j])
                else:
                    print(cast1.verticies[i].name + " " + cast1.verticies[i].code)
                    print(cast2.verticies[j].name + " " + cast2.verticies[j].code)


    def has_overlap(self,x1,x2,y1,y2):
        return x1 < y2 and y1 < x2

    def num_combinations(self):
        permutations = 1
        for cast in self.casts:
            permutations *= cast.combinations
        return permutations
            
    def __str__(self):
        string = ""
        for cast in self.casts:
            string += str(cast) + "\n"
        return string
