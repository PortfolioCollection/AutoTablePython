from bs4 import BeautifulSoup as bs
from requests import get

times = {}

def course_time(course, session):
    if 'fall' in session.lower():
        if course[5] == 'y':
            session = 'Y20189' #changes depending on year
        else:
            session = 'F20189'
    elif 'winter' in session.lower():
        session = 'S20191'
    elif 'summer' in session.lower():
        'heh'
    else:
        print('Not a valid session')
        return
    
    url = 'http://coursefinder.utoronto.ca/course-search/search/courseInquiry?methodToCall=start&viewId=CourseDetails-InquiryView&courseId='+course.upper()+session

    response = get(url)
    if 'The course you are trying to access does not exist' in response.text:
        print('Sorry nothing!')
        return
    soup = bs(response.text, 'html.parser')

    times[course.upper()+session[0]] = [[],[],[]]
    time_td = soup.find_all('td')
    for i in range(0, len(time_td), 8):
        if 'Lec' in time_td[i].text.strip(): #0 = lec
            times[course.upper()+session[0]][0].append(time_td[i].text.strip() + ' ' + time_td[i+1].text.strip())
        if 'Tut' in time_td[i].text.strip(): #1 = tut
            times[course.upper()+session[0]][1].append(time_td[i].text.strip() + ' ' + time_td[i+1].text.strip())
        if 'Pra' in time_td[i].text.strip(): #2 = pra
            times[course.upper()+session[0]][2].append(time_td[i].text.strip() + ' ' + time_td[i+1].text.strip())
        print(time_td[i].text.strip(), time_td[i+1].text.strip())


def course_desc(course):
    'yap'
    
