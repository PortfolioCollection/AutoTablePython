class Vertex:
    def __init__(self,name,code,start,end):
        self.name = name
        self.code = code
        self.start = start
        self.end = end
        self.edges = []
        self.combinations = 1

    def __str__(self):
        return "Vertex: "+self.name+" "+self.code+" "+self.start+" "+self.end

class Edge:
    def __init__(self, v1,v2):
        self.v1 = v1
        self.v2 = v2
        self.distance = 1000

    def set_distance(self,distance):
        self.distance = distance

    def __str__(self):
        return str((str(self.v1),str(self.v2),self.distance))


class Cast:
    def __init__(self,name):
        self.name = name
        self.verticies = []
        self.edges = []

    def add_vertex(self,vertex):
        vertecies.append(vertex)

    def connect_graph(self):
        for i in range(len(self.verticies)):
            for j in range(i+1,len(self.verticies)):
                self.add_edge(self.verticies[i],self.verticies[j])

    def add_edge(self,v1,v2):
        edge = Edge(v1,v2)
        v1.edges.append(edge)
        v2.edges.append(edge)
        self.edges.append(edge)

class Graph:
    def __init__(self):
        self.casts = []
        self.edges = []

    def add_course(self,course):
        course_vertex = []
        tup = course.compress_times()
        i = 0
        name = course.name+" lectures"
        cast = Cast(name)
        for lecture in tup[0]:
            time = lecture.split()
            vertex = Vertex(course.name,"lec"+tup[0][lecture][0],time[0],time[1])
            cast.verticies.append(vertex)
            i+= 1
        if i > 0:
            self.casts.append(cast)
            vertex.combinations *= i
        i = 0
        name = course.name+" tutorials"
        cast = Cast(name)
        for tutorial in tup[1]:
            time = tutorial.split()
            vertex = Vertex(course.name,"tut"+tup[1][tutorial][0],time[0],time[1])
            cast.verticies.append(vertex)
            i+= 1
        
        if i > 0:
            self.casts.append(cast)
            vertex.combinations *= i
        i = 0
        name = course.name+" practicals"
        cast = Cast(name)
        for practical in tup[2]:
            time = practical.split()
            vertex = Vertex(course.name,"pra"+tup[2][practical][0],time[0],time[1])
            cast.verticies.append(vertex)
            i+= 1
        if i > 0:
            self.casts.append(cast)
            vertex.combinations *= i

    def connect_graph(self):
        index = 0
        for i in range(len(self.casts)):
            for j in range(i+1,len(self.casts)):
                #index += 1
                #print "#"+str(index)+": "+str((str(self.verticies[i]),str(self.verticies[j])))
                #self.add_edge(self.verticies[i],self.verticies[j])
                self.connect_casts(self.casts[i],self.casts[j])

    def connect_casts(self,cast1,cast2):
        for i in range(len(cast1.verticies)):
            for j in range(i+1,len(cast2.verticies)):
                self.add_edge(cast1.verticies[i], cast2.verticies[j])
        
        

    def add_edge(self,v1,v2):
        edge = Edge(v1,v2)
        v1.edges.append(edge)
        v2.edges.append(edge)
        self.edges.append(edge)
            


    def __str__(self):
        string = ""
        i=0
        permutations = 1
        for cast in self.casts:
            for vertex in cast.verticies:
                i+=1
                permutations *= vertex.combinations
                string += str(i)+": "+str(vertex) + "\n"
        print("Permutations: "+str(permutations))
        return string
