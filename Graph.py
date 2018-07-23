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
        print(tup)
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
        #print("Here")
        #print(cast2)
        for i in range(len(cast1.verticies)):
            for j in range(i,len(cast2.verticies)):
                #if cast1.verticies[i].name + " " + cast1.verticies[i].code == "csc347 pra0101":
                #    if cast2.verticies[j].name + " " + cast2.verticies[j].code == "mat301 lec0101":
                        #print(cast1.verticies[i].name + " " + cast1.verticies[i].code)
                        #print(cast2.verticies[j].name + " " + cast2.verticies[j].code)
                        #print((cast1.verticies[i].start,cast2.verticies[j].end))
                        #print((cast2.verticies[j].start,cast1.verticies[i].end))
                        #print(self.has_overlap(cast1.verticies[i].start,cast1.verticies[i].end,
                        #                   cast2.verticies[j].start,cast2.verticies[j].end))
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
        

    def add_edge(self,cast1,cast2,v1,v2):
        edge = Edge(v1,v2)
        v1.edges.append(edge)
        v2.edges.append(edge)
        cast1.add_edge(v1,v2)
        cast2.add_edge(v1,v2)
            


    def __str__(self):
        string = ""
        i=0
        permutations = 1
        for cast in self.casts:
            print(cast)
            for vertex in cast.verticies:
                i+=1
                permutations *= vertex.combinations
        print("Permutations: "+str(permutations))
        return string
