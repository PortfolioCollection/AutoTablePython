from Course import*
from Session import*
class Builder:
    def __init__(self, AutoTable):
        self.AutoTable = AutoTable

    def build_table(self):
        csc324 = Course("csc324","Y")
        lec101 = Lecture("0101",["Wed"],      [(13,15)])
        lec102 = Lecture("0102",["Wed"],      [(17,19)])
        pra101 = Practical("0101",["Fri"],    [(11,12)])
        pra102 = Practical("0102",["Fri"],    [(11,12)])
        pra103 = Practical("0103",["Fri"],    [(12,13)])
        pra104 = Practical("0104",["Fri"],    [(12,13)])
        pra105 = Practical("0105",["Fri"],    [(13,14)])
        csc324.add_section(lec101)
        csc324.add_section(lec102)
        csc324.add_section(pra101)
        csc324.add_section(pra102)
        csc324.add_section(pra103)
        csc324.add_section(pra104)
        csc324.add_section(pra105)
        
        csc347 = Course("csc347","Y")
        lec101 = Lecture("0101",["Fri"],      [(15,17)])
        pra101 = Practical("0101",["Wed"],    [(11,12)])
        pra102 = Practical("0102",["Wed"],    [(15,16)])
        csc347.add_section(lec101)
        csc347.add_section(pra101)
        csc347.add_section(pra102)

        csc369 = Course("csc369","Y")
        lec101 = Lecture("0101",["Mon"],      [(9,11)])
        lec102 = Lecture("0102",["Mon"],      [(13,15)])
        pra101 = Practical("0101",["Thu"],    [(9,10)])
        pra102 = Practical("0102",["Thu"],    [(9,10)])
        pra103 = Practical("0103",["Thu"],    [(10,11)])
        pra104 = Practical("0104",["Thu"],    [(10,11)])
        csc369.add_section(lec101)
        csc369.add_section(lec102)
        csc369.add_section(pra101)
        csc369.add_section(pra102)
        csc369.add_section(pra103)
        csc369.add_section(pra104)

        mat301 = Course("mat301","Y")
        lec101 = Lecture("0101",["Wed","Fri"],  [(11,13),(9,10)])
        tut101 = Tutorial("0101",["Wed"],       [(9,10)])
        tut102 = Tutorial("0102",["Wed"],       [(10,11)])
        tut103 = Tutorial("0103",["Wed"],       [(13,14)])
        mat301.add_section(lec101)
        mat301.add_section(tut101)
        mat301.add_section(tut102)
        mat301.add_section(tut103)

        csc338 = Course("csc338","Y")
        lec101 = Lecture("0101",["Wed"],      [(15,17)])
        tut101 = Tutorial("0101",["Fri"],     [(13,14)])
        tut102 = Tutorial("0102",["Fri"],     [(14,15)])
        csc338.add_section(lec101)
        csc338.add_section(tut101)
        csc338.add_section(tut102)

        csc343 = Course("csc343","Y")
        lec101 = Lecture("0101",["Mon"],      [(9,11)])
        pra101 = Practical("0101",["Thu"],    [(13,14)])
        pra102 = Practical("0102",["Wed"],    [(14,15)])
        csc343.add_section(lec101)
        csc343.add_section(pra101)
        csc343.add_section(pra102)

        csc363 = Course("csc363","Y")
        lec101 = Lecture("0101",["Mon"],      [(11,13)])
        lec102 = Lecture("0102",["Thu"],      [(18,20)])
        tut101 = Tutorial("0101",["Wed"],     [(13,14)])
        tut102 = Tutorial("0102",["Wed"],     [(13,14)])
        tut103 = Tutorial("0103",["Wed"],     [(14,15)])
        tut104 = Tutorial("0104",["Wed"],     [(14,15)])
        csc363.add_section(lec101)
        csc363.add_section(lec102)
        csc363.add_section(tut101)
        csc363.add_section(tut102)
        csc363.add_section(tut103)
        csc363.add_section(tut104)

        csc384 = Course("csc384","Y")
        lec101 = Lecture("0101",["Thu"],      [(11,13)])
        tut101 = Tutorial("0101",["Tue"],     [(16,17)])
        tut102 = Tutorial("0102",["Tue"],     [(17,18)])
        tut103 = Tutorial("0103",["Tue"],     [(17,18)])
        csc384.add_section(lec101)
        csc384.add_section(tut101)
        csc384.add_section(tut102)
        csc384.add_section(tut103)


        self.AutoTable.year = Session("Year")
        self.AutoTable.fall = Session("Fall")
        self.AutoTable.winter = Session("Winter")


        self.AutoTable.year.add_course(csc324)

        self.AutoTable.fall.add_course(csc347)
        self.AutoTable.fall.add_course(csc369)
        self.AutoTable.fall.add_course(mat301)

        
        self.AutoTable.winter.add_course(csc338)
        self.AutoTable.winter.add_course(csc343)
        self.AutoTable.winter.add_course(csc363)
        self.AutoTable.winter.add_course(csc384)
        



        return self.AutoTable
