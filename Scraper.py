from bs4 import BeautifulSoup as bs
from requests import get
from Course import*
from Session import*

def scrape_course(course, session):
    if 'fall' in session.lower():
        if course[5].lower() == 'y':
            session = 'Y20189' #changes depending on year
        else:
            session = 'F20189'
    elif 'winter' in session.lower():
        session = 'S20191'
    elif 'summer' in session.lower():
        session = 'Y20185'
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
            days.append(times[j][0] + times[j][1:3].lower())
            hours.append((int(times[j+1][:2]),int(times[j+1][6:8])))
        if 'Lec' in section[0]: #its bound to be one of these ifs
            sec = Lecture(section[1], days, hours)
        if 'Tut' in section[0]:
            sec = Tutorial(section[1], days, hours)
        if 'Pra' in section[0]:
            sec = Pratical(section[1], days, hours)
        course.add_section(sec)
    return course
