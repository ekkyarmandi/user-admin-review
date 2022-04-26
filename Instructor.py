from User import User
from Course import Course
from Review import Review


class Instructor(User):

    def __init__(self, username="", password="", id=-1, display_name="", job_title="", image_100x100="", course_id_list=[]):
        '''
        Instructor constructor
        :param id: int, default value -1
        :param username: str, default value "" (empty string)
        :param password: str, default value "" (empty string)
        :param display_name: str, default value "" (empty string)
        :param job_title: str, default value "" (empty string)
        :param image_100x100: str, default value "" (empty string)
        :param course_id_list: list, default value [] (empty list)
        :return: None
        '''
        self.id = id
        self.username = username
        self.password = password
        self.display_name = display_name
        self.job_title = job_title
        self.image_100x100 = image_100x100
        self.course_id_list = course_id_list

    def view_courses(self, *args):
        '''Print out all the courses taught by this instructor.'''
        
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
                    content_length=raw.split(';;;')[6],
                )
                courses.append(course)

            # filtered the courses
            filtered = []
            for course in courses:
                if course.id in self.course_id_list:
                    filtered.append(course)

            # printout filtered course(s)
            limit = 1
            for course in filtered:
                print(course)
                if limit > 9:
                    break
                else:
                    limit += 1

            # print total returned course
            print(f'total returned course: {len(filtered)}\n')


    def view_reviews(self, *args):
        '''Print out all the reviews belong to the courses this instructor teaches.'''
        
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

        # filtered the reviews
        filtered = []
        for review in reviews:
            if review.course_id in self.course_id_list:
                filtered.append(review)

        # printout filtered review(s)
        limit = 1
        for review in filtered:
            print(review)
            if limit > 9:
                break
            else:
                limit += 1

        # print total returned course
        print(f'total returned review: {len(filtered)}\n')

    def __str__(self):
        '''Object in string format'''
        return ";;;".join([
            str(self.id),
            self.username,
            self.password,
            self.display_name,
            self.job_title,
            self.image_100x100,
            "--".join(self.course_id_list)
        ])