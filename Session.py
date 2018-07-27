class Session:
    def __init__(self,session):
        self.session = session
        self.courses = []
        
    def add_course(self,course):
        self.courses.append(course)
