from User import User
from Course import Course
from Review import Review


class Student(User):

    def __init__(self, username="", password="", id=-1, title="", image_50x50="", initials="", review_id=-1):
        '''
        Student constructor
        :param id: int, default value -1
        :param username: str, default value "" (empty string)
        :param password: str, default value "" (empty string)
        :param title: str, default value "" (empty string)
        :param image_50x50: str, default value "" (empty string)
        :param initials: str, default value "" (empty string)
        :param review_id: int, default value -1
        '''
        self.id = id
        self.username = username
        self.password = password
        self.title = title
        self.image_50x50 = image_50x50
        self.initials = initials
        self.review_id = review_id

    def view_courses(self, *args):
        '''Prints out the course the student registered'''
        
        # read course.txt
        with open('data/course_data/course.txt','r',encoding='utf-8') as f:
            raw_courses = f.read().strip().split('\n')
            courses = []
            for raw in raw_courses:
                course = Course(
                    id=raw.split(';;;')[0],
                    title=raw.split(';;;')[1],
                    image_100x100=raw.split(';;;')[2],
                    headline=raw.split(';;;')[3],
                    num_subscribers=raw.split(';;;')[4],
                    avg_rating=raw.split(';;;')[5],
                    content_length=raw.split(';;;')[6]
                )
                courses.append(course)
        
        # read review.txt
        with open('data/course_data/review.txt','r',encoding='utf-8') as f:
            raw_reviews = f.read().strip().split('\n')
            reviews = []
            for raw in raw_reviews:
                review = Review(
                    id=str(raw.split(';;;')[0]),
                    content=raw.split(';;;')[1],
                    rating=str(raw.split(';;;')[2]),
                    course_id=str(raw.split(';;;')[3])
                )
                reviews.append(review)

        # filtered review(s) id
        filtered = []
        for review in reviews:
            if review.id == self.review_id:
                filtered.append(review.course_id)
        filtered = list(dict.fromkeys(filtered))

        # filtered course(s) id
        limit = 1
        for course in courses:
            if course.id in filtered:
                print(course)
                if limit > 9:
                    break
                else:
                    limit += 1
        
        # print total returned course
        print(f'total returned course: {len(filtered)}\n')

    def view_reviews(self, *args):
        '''Prints out the review the student wrote'''
        
        # read review.txt
        with open('data/course_data/review.txt','r',encoding='utf-8') as f:
            raw_reviews = f.read().strip().split('\n')
            reviews = []
            for raw in raw_reviews:
                review = Review(
                    id=str(raw.split(';;;')[0]),
                    content=raw.split(';;;')[1],
                    rating=str(raw.split(';;;')[2]),
                    course_id=str(raw.split(';;;')[3])
                )
                reviews.append(review)

        # filtered review(s) id
        filtered = []
        for review in reviews:
            if review.id == self.review_id:
                filtered.append(review)

        # filtered course(s) id
        limit = 1
        for review in filtered:
            print(review)
            if limit > 9:
                break
            else:
                limit += 1

        # print total returned course
        print(f'total returned course: {len(filtered)}\n')

    def __str__(self):
        '''Object in string format'''

        return ";;;".join([
            self.id,
            self.username,
            self.password,
            self.title,
            self.image_50x50,
            self.initials,
            self.review_id
        ])