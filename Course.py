days = ["Mon","Tue","Wed","Thu","Fri"]

class Course:
    def __init__(self,name):
        self.name = name
        self.lectures = []
        self.tutorials = []
        self.practicals = []

    def add_section(self,section):
        if type(section) is Lecture:
            self.lectures.append(section)
        elif type(section) is Tutorial:
            self.tutorials.append(section)
        elif type(section) is Practical:
            self.practicals.append(section)

    def compress_times(self):
        dictionary1 = {}
        for section in self.lectures:
            term = str(section.start)+" "+str(section.end) 
            if term in dictionary1:
                new = dictionary1[term]
                new.append(section.code)
                dictionary1[term] = new
            else:
                dictionary1[term] = [section.code]
        dictionary2 = {}
        for section in self.tutorials:
            term = str(section.start)+" "+str(section.end) 
            if term in dictionary2:
                new = dictionary2[term]
                new.append(section.code)
                dictionary2[term] = new
            else:
                dictionary2[term] = [section.code]
        dictionary3 = {}
        for section in self.practicals:
            term = str(section.start)+" "+str(section.end) 
            if term in dictionary3:
                new = dictionary3[term]
                new.append(section.code)
                dictionary3[term] = new
            else:
                dictionary3[term] = [section.code]

        return (dictionary1,dictionary2,dictionary3)


    def __str__(self):
        string = "--------------\n"
        for lec in self.lectures:
            string += str(lec)
        string += "--------------\n"
        for tut in self.tutorials:
            string += str(tut)
        string += "--------------\n"
        for pra in self.practicals:
            string += str(pra)
        string += "--------------\n"
        return string
        
        
class Section(object):
    def __init__(self,code,day,start,end):
        global days
        i = 0
        for index in days:
            if index != day:
                i+= 1
            else:
                break
        self.code = code
        self.day = day
        self.start = start + 24*i
        self.end = end + 24*i
        #print(day)
        #print((self.start,self.end))

    def __str__(self):
        string = self.day+" start: "+str(self.start)+" end: "+str(self.end)
        return string

class Lecture(Section):
    def __init__(self,code,day,start,end):
        Section.__init__(self,code,day,start,end)

    def __str__(self):
        string = "Lec: "
        return string+ super(Lecture,self).__str__()+"\n"
        

class Tutorial(Section):
    def __init__(self,code,day,start,end):
        Section.__init__(self,code,day,start,end)

    def __str__(self):
        string = "Tut: "
        return string+ super(Tutorial,self).__str__()+"\n"

class Practical(Section):
    def __init__(self,code,day,start,end):
        Section.__init__(self,code,day,start,end)

    def __str__(self):
        string = "Pra: "
        return string+ super(Practical,self).__str__()+"\n"
