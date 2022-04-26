
class Course:
    
    def __init__(self, id=-1, title="", image_100x100="", headline="", num_subscribers=-1, avg_rating=-1, content_length=-1.0):
        '''
        Course constructor
        :param id: int, default value -1
        :param title: str, defaul value "" (empty string)
        :param image_100x100: str, defaul value "" (empty string)
        :param headline: str, defaul value "" (empty string)
        :param num_subscribers: int, default value -1
        :param avg_rating: int, default value -1
        :param content_length: float, default value -1.0
        '''
        self.id = id
        self.title = title
        self.image_100x100 = image_100x100
        self.headline = headline
        self.num_subscribers = num_subscribers
        self.avg_rating = avg_rating
        self.content_length = content_length
    
    def find_course_by_title_keyword(self, keyword):
        pass
    
    def find_course_by_id(self, course_id):
        pass
    
    def find_course_by_instructor_id(self, instructor_id):
        pass
    
    def course_overview(self):
        '''Read course.txt and count it'''
        with open('data/course_data/course.txt',encoding='utf-8') as f:
            courses = f.read().split("\n")
            print('The total number of course is ' + str(len(courses)) + '\n')
    
    def __str__(self):
        '''Object in string format'''
        return ";;;".join([
            str(self.id),
            self.title,
            self.image_100x100,
            self.headline,
            str(self.num_subscribers),
            str(self.avg_rating),
            self.content_length,
        ])