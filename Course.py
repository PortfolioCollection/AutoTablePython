day_list = ["MON","TUE","WED","THU","FRI"]

class Course:
    def __init__(self,name,session):
        self.name = name
        self.session = session
        self.lectures = []
        self.tutorials = []
        self.practicals = []

    def add_section(self,section):
        section.name = self.name
        section.session = self.session
        if type(section) is Lecture:
            self.lectures.append(section)
        elif type(section) is Tutorial:
            self.tutorials.append(section)
        elif type(section) is Practical:
            self.practicals.append(section)

    def compress_times(self):
        for i in range(len(self.lectures)):
            for j in range(i):
                if self.lectures[i].times == self.lectures[j].times:
                    self.lectures[j].simmilar_times.append(self.lectures[i])
                    self.lectures[i].simmilar_times = -1
                    break
        i = 0
        while i < len(self.lectures):
            if self.lectures[i].simmilar_times == -1:
                self.lectures.remove(self.lectures[i])
                i -= 1
            i+=1

        for i in range(len(self.tutorials)):
            for j in range(i):
                if self.tutorials[i].times == self.tutorials[j].times:
                    self.tutorials[j].simmilar_times.append(self.tutorials[i])
                    self.tutorials[i].simmilar_times = -1
                    break
        i = 0
        while i < len(self.tutorials):
            if self.tutorials[i].simmilar_times == -1:
                self.tutorials.remove(self.tutorials[i])
                i -= 1
            i+=1

        for i in range(len(self.practicals)):
            for j in range(i):
                if self.practicals[i].times == self.practicals[j].times:
                    self.practicals[j].simmilar_times.append(self.practicals[i])
                    self.practicals[i].simmilar_times = -1
                    break
        i = 0
        while i < len(self.practicals):
            if self.practicals[i].simmilar_times == -1:
                self.practicals.remove(self.practicals[i])
                i -= 1
            i+=1
        casts = []
        casts.append(self.lectures)
        casts.append(self.tutorials)
        casts.append(self.practicals)
        return casts


    def __str__(self):
        string = "--------------\n"
        for lec in self.lectures:
            string += str(lec)+"\n"
        string += "\n--------------\n"
        for tut in self.tutorials:
            string += str(tut)+"\n"
        string += "--------------\n"
        for pra in self.practicals:
            string += str(pra)+"\n"
        string += "\n--------------\n"
        return string
        
        
class Section(object):
    def __init__(self,code,days,times):
        global day_list
        for i in range(len(days)):
            for j in range(len(day_list)):
                if day_list[j] == days[i]:
                    break
            times[i] = (times[i][0] + 24*j,times[i][1] + 24*j)
        self.type = None
        self.name = None
        self.session = None
        self.code = code
        self.days = days
        self.times = times
        self.simmilar_times = []

    def __str__(self):
        string = ""
        for i in range(len(self.times)):
            string += self.days[i]+" start: "+str(self.times[i][0]%24)+" end: "+str(self.times[i][1]%24)+"\n"
            string+="\t"
        #print(self.simmilar_times)
        return string[:-1] 

class Lecture(Section):
    def __init__(self,code,days,times):
        Section.__init__(self,code,days,times)
        self.type = "Lec"

    def __str__(self):
        return self.type+self.code+":"+super(Lecture,self).__str__().strip()
        

class Tutorial(Section):
    def __init__(self,code,days,times):
        Section.__init__(self,code,days,times)
        self.type = "Tut"

    def __str__(self):
        return self.type+self.code+":"+super(Tutorial,self).__str__().strip()

class Practical(Section):
    def __init__(self,code,days,times):
        Section.__init__(self,code,days,times)
        self.type = "Pra"

    def __str__(self):
        return self.type+self.code+":"+super(Practical,self).__str__().strip()
