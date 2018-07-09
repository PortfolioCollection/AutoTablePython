from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException
import time as t

current_folder = 'C:\\Users\\Joshua\\Desktop\\bolder\\chromedriver' #must be changed to path of chromedriver.exe
course_database = {}
times = {}

def list_courses(criteria, session):
    #figures out which session it is (probably should make better kind of sucks right now)
    if('fall' in session.lower() or 'winter' in session.lower()):
        session = '20189'
    elif('summer' in session.lower()):
        session = '20185'
    else:
        print("No valid session found within text");
        return

    #options that will make the browser invisible
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  
    options.add_argument("--window-size=%s" % '1920,1080')
    browser = webdriver.Chrome(executable_path=current_folder, chrome_options=options)
    browser.get('https://student.utm.utoronto.ca/timetable/index.php?session='+session+'&course='+criteria)
    t.sleep(5) #waits for page to load, theres a wait until func but the page will load different elements depending on if the criteria exists or not and i am too
    #lazy to figure a way for that right now

    #in case criteria meets nothing
    if 'No matching courses' in browser.page_source:
        print("No courses found")
        browser.quit()
        return

    courses = browser.find_elements_by_xpath('//div[contains(@id, \''+criteria.upper()+'\')]/span') #find div id that contains the criteria
    course_descs = browser.find_elements_by_xpath('//div[@class=\'alert alert-info infoCourseDetails infoCourse\']') #gives the descs

    for course, desc in zip(courses,course_descs): #each title and desc is obtained in the same order
        print(course.text)
        rows = browser.find_elements_by_xpath('//tr[contains(@id, \''+course.text[:9].upper()+'\')]') #gets the rows for this specific course

        for row in rows:
            cells = row.find_elements_by_tag_name("td") #get the cells of this row
            print('    ',cells[1].text, cells[7].text, cells[8].text, cells[9].text) #1 title, 7 day, 8 start time, 9 end time
            times[course.text[:9].upper()] = times.get(course.text[:9].upper(), []) + [[cells[1].text, cells[7].text, cells[8].text, cells[9].text]] #record for time function
        
        course_database[course.text[:6].upper()] = course.text[:6] + course.text[9:] + '\n\n' + desc.text #record the course & desc for easier course_desc

    browser.quit() #:)

def course_desc(course):
    if(len(course) != 6 and len(course) != 9):
        print('Course must be in XXX999 or XXX999X9X order')
        return
    if(course.upper() in course_database.keys()): #sees if we have the course data already else do above but for one course
        print(course_database[course.upper()])
    else:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  
        options.add_argument("--window-size=%s" % '1920,1080')
        browser = webdriver.Chrome(executable_path='C:\\Users\\Joshua\\Desktop\\bolder\\chromedriver', chrome_options=options)
        browser.get('https://student.utm.utoronto.ca/timetable/index.php?session=20189&course='+course) #session should be changed to be dependent
        t.sleep(5)

        if 'No matching courses' in browser.page_source:
            print("No course found")
            browser.quit()
            return

        courses = browser.find_elements_by_xpath('//div[contains(@id, \''+course.upper()+'\')]/span')
        course_descs = browser.find_elements_by_xpath('//div[@class=\'alert alert-info infoCourseDetails infoCourse\']')

        course_database[courses[0].text[:6].lower()] = courses[0].text[:6] + courses[0].text[9:] + '\n\n' + course_descs[0].text
        print(course_database[course])

        browser.quit()
