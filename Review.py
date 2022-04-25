class Review:

    def __init__(self, id=-1, content="", rating=-1.0, course_id=-1):
        '''
        Review constructor
        :param id: int, default value -1
        :param content: str, default value "" (empty string)
        :param rating: float, default value -1.0
        :param course_id: int, default value -1
        '''
        self.id = id
        self.content = content
        self.rating = rating
        self.course_id = course_id

    def find_review_by_id(self, review_id):
        pass

    def find_review_by_keywords(self, keyword):
        pass

    def find_review_by_course_id(self, course_id):
        pass

    def reviews_overview(self):
        '''Read review.txt and count it'''
        with open('data/course_data/review.txt',encoding='utf-8') as f:
            courses = f.read().split("\n")
            print('The total number of review is',len(courses))

    def __str__(self):
        '''Object in string format'''
        return ";;;".join([
            self.id,
            self.content,
            self.rating,
            self.course_id
        ])