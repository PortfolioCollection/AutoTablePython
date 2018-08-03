import requests
from bs4 import BeautifulSoup
from Course import*
from Session import*

class Scraper:

    def __init__(self, AutoTable):
        self.AutoTable = AutoTable
        self.AutoTable.year = Session("Year")
        self.AutoTable.fall = Session("Fall")
        self.AutoTable.winter = Session("Winter")

    def access_site(self,url):
        with requests.Session() as c:
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
            c.encoding = 'UTF-8'
            page = c.get(url, verify=False,headers=headers)
            html = page.content
            #print(html)
            soup = BeautifulSoup(html, "html5lib")
            return soup
            


    def scrape_course(self,url,season):
        soup = self.access_site(url)
        title = soup.find_all("span", {"class": "uif-headerText-span"})[0].get_text()
        course_name = title[:6]
        section = title[6:7]
        table = soup.find_all('table')[0]
        course = Course(course_name,section)
        for tr in table.find_all("tr"):
            tds = tr.find_all("td")
            if len(tds)>0:
                timeslot_name,code = tds[0].get_text().strip().split(" ")
                times = tds[1].get_text().strip().split(" ")
                #print(timeslot_name)
                #print(code)
                days = []
                periods = []
                for i in range(len(times)):
                    if i % 2 == 0:
                        days.append(times[i][:3])
                    else:
                        periods.append((int(times[i][:2]),int(times[i][6:8])))
                #print(days)
                #print(periods)

                slot = None
                if timeslot_name[:3] == "Lec":
                    slot = Lecture(code,days,periods)
                elif timeslot_name[:3] == "Tut":
                    slot = Tutorial(code,days,periods)
                elif timeslot_name[:3] == "Pra":
                    slot = Practical(code,days,periods)
                else:
                    print("Missed something")

                if slot != None:
                    course.add_section(slot)
        if section == "H":
            if season == "Fall":
                self.AutoTable.fall.add_course(course)
            elif season == "Winter":
                self.AutoTable.winter.add_course(course)


    def build_table(self):
        self.scrape_course("http://coursefinder.utoronto.ca/course-search/search/courseInquiry?methodToCall=start&viewId=CourseDetails-InquiryView&courseId=CSC324H5F20189#.W2SlJu-nHIU","Fall") #CSC324
        self.scrape_course("http://coursefinder.utoronto.ca/course-search/search/courseInquiry?methodToCall=start&viewId=CourseDetails-InquiryView&courseId=CSC347H5F20189#.W2Slju-nHIU","Fall") #CSC347
        #self.scrape_course("http://coursefinder.utoronto.ca/course-search/search/courseInquiry?methodToCall=start&viewId=CourseDetails-InquiryView&courseId=CSC369H5F20189#.W2Sloe-nHIU","Fall") #CSC369
        self.scrape_course(" http://coursefinder.utoronto.ca/course-search/search/courseInquiry?methodToCall=start&viewId=CourseDetails-InquiryView&courseId=MAT135H1F20189","Fall") #MAT135
        self.scrape_course("http://coursefinder.utoronto.ca/course-search/search/courseInquiry?methodToCall=start&viewId=CourseDetails-InquiryView&courseId=MAT301H5F20189#.W2SfUO-nHIU","Fall") #MAT301


        self.scrape_course("http://coursefinder.utoronto.ca/course-search/search/courseInquiry?methodToCall=start&viewId=CourseDetails-InquiryView&courseId=CSC338H5S20191#.W2Sl9--nHIU","Winter") #CSC338
        self.scrape_course("http://coursefinder.utoronto.ca/course-search/search/courseInquiry?methodToCall=start&viewId=CourseDetails-InquiryView&courseId=CSC343H5S20191#.W2SmE--nHIU","Winter") #CSC343
        self.scrape_course("http://coursefinder.utoronto.ca/course-search/search/courseInquiry?methodToCall=start&viewId=CourseDetails-InquiryView&courseId=CSC363H5S20191#.W2SmLu-nHIU","Winter") #CSC363
        self.scrape_course("http://coursefinder.utoronto.ca/course-search/search/courseInquiry?methodToCall=start&viewId=CourseDetails-InquiryView&courseId=CSC384H5S20191#.W2SmTO-nHIU","Winter") #CSC384
        return self.AutoTable
    
if __name__ == "__main__":
    from timetable import*
    autotable = AutoTable()
    scraper = Scraper(autotable)
    autotable = scraper.build_table()
    print(scraper.AutoTable)
    
