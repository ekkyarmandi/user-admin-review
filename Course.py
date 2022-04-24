
class Course:
    
    def __init__(self, course_id=-1, course_title="", course_image_100x100="", course_headline="", course_num_subscribers=-1, course_avg_rating=-1, course_content_length=-1.0):
        '''
        Course constructor
        :param course_id: int, default value -1
        :param course_title: str, defaul value "" (empty string)
        :param course_image_100x100: str, defaul value "" (empty string)
        :param course_headline: str, defaul value "" (empty string)
        :param course_num_subscribers: int, default value -1
        :param course_avg_rating: int, default value -1
        :param course_content_length: float, default value -1.0
        '''
        self.course_id = course_id
        self.course_title = course_title
        self.course_image_100x100 = course_image_100x100
        self.course_headline = course_headline
        self.course_num_subscribers = course_num_subscribers
        self.course_avg_rating = course_avg_rating
        self.course_content_length = course_content_length
    
    def find_course_by_title_keyword(self, keyword):
        pass
    
    def find_course_by_id(self, course_id):
        pass
    
    def find_course_by_instructor_id(self, instructor_id):
        pass
    
    def course_overview(self):
        pass # count the course
    
    def __str__(self):
        '''Object in string format'''
        return ";;;".join([
            str(self.course_id),
            self.course_title,
            self.course_image_100x100,
            self.course_headline,
            str(self.course_num_subscribers),
            str(self.course_avg_rating),
            str(round(self.course_content_length,2)),
        ])