from bs4 import BeautifulSoup as bs
from requests import get
from Course import*
from Session import*

class Scraper:

    def __init__(self, AutoTable):
        self.AutoTable = AutoTable
        self.AutoTable.year = Session("Year")
        self.AutoTable.fall = Session("Fall")
        self.AutoTable.winter = Session("Winter")
    
    def scrape_course(self,course, session):
        if 'fall' in session.lower():
            if course[6].lower() == 'y':
                session = 'Y20189' #changes depending on year
            else:
                session = 'F20189'
        elif 'winter' in session.lower():
            session = 'S20191'
        elif 'summer' in session.lower():
            session = 'Y20189'
        else:
            print('Not a valid session')
            return
        
        url = 'http://coursefinder.utoronto.ca/course-search/search/courseInquiry?methodToCall=start&viewId=CourseDetails-InquiryView&courseId='+course.upper()+session
        response = get(url)
        if 'The course you are trying to access does not exist' in response.text:
            print('Sorry nothing!')
            return
        soup = bs(response.text, 'html.parser')

        course = Course(course[:6], session[0]) #
        time_td = soup.find_all('td')
        for i in range(0, len(time_td), 8):
            section = time_td[i].text.split() #0 = type, 1 = number
            times = time_td[i+1].text.split() #comes in 2s! i = day, i+1 = time
            days = [] #just so i can append
            hours = []
            for j in range(0, len(times), 2):
                days.append(times[j][:3])
                hours.append((int(times[j+1][:2]),int(times[j+1][6:8])))
            if 'Lec' in section[0]: #its bound to be one of these ifs
                sec = Lecture(section[1], days, hours)
            if 'Tut' in section[0]:
                sec = Tutorial(section[1], days, hours)
            if 'Pra' in section[0]:
                sec = Practical(section[1], days, hours)
            course.add_section(sec)
        if session[0].lower() == 'y':
            self.AutoTable.year.add_course(course)
        elif session[0].lower() == 'f':
            self.AutoTable.fall.add_course(course)
        elif session[0].lower() == 's':
            self.AutoTable.winter.add_course(course)
        else:
            print('Not a valid session')
            return

    def build_table(self):
        
        self.scrape_course("SPA100Y1","Fall")
        self.scrape_course("VIC172Y1","Fall")
        self.scrape_course("VIC173Y1","Fall")
        #self.scrape_course("VIC001Y1","Fall")

        self.scrape_course("SOC100H1","Fall")
        self.scrape_course("MAT135H1","Fall")

        self.scrape_course("CHM136H1","Winter")
        self.scrape_course("MAT136H1","Winter")
        """
        self.scrape_course("CSC324H5","Fall")
        self.scrape_course("CSC343H5","Fall")
        self.scrape_course("CSC347H5","Fall")
        self.scrape_course("CSC369H5","Fall")
        self.scrape_course("MAT301H5","Fall") 

        self.scrape_course("CSC338H5","Winter")
        self.scrape_course("CSC363H5","Winter")
        self.scrape_course("CSC384H5","Winter")
        self.scrape_course("MAT302H5","Winter")
        """
        return self.AutoTable
