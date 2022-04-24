from User import User
from Course import Course
from Instructor import Instructor
from Student import Student
from Review import Review
import re
import os


def find(text,keyword):
    c = re.search('\"'+keyword+'\"',text).end()
    brackets = re.finditer('\[|\]',text[c:])
    ob,cb,j = -1,-1,""
    for b in brackets:
        if b.group() == "[":
            ob += 1
            if j == "":
                j = b.start()
        elif b.group() == "]":
            cb += 1
        if ob == cb:
            items = text[c:][j:b.end()]
            items = items.replace('true','True')
            items = items.replace('false','False')
            items = items.replace('null','None')
            return eval(items)

class Admin(User):

    def register_admin(self):
        '''Register admin'''

        # read user_admin.txt file
        with open('sources/user_admin.txt','r') as f:
            text = f.read().split('\n')

        for t in text:

            # check if a user is exists or not
            if t != "":
                username = t.split('|')[1]
                password = t.split('|')[2]
                trues = [
                    username == self.username,
                    password == self.password
                ]
                if all(trues):
                    break

            # register new one if a user named admin does not exists
            elif self.username == 'admin' and self.password == 'YWRtaW4=':
                self.user_id = self.generate_unique_user_id()
                with open('sources/user_admin.txt','w') as f:
                    f.write('|'.join([self.user_id,self.username,self.password]))
                    break

    def extract_course_info(self):
        '''Extract course list from raw_data.txt and write it into course.txt'''

        # open raw_data.txt
        with open('data/course_data/raw_data.txt',encoding='utf-8') as f:
            text = f.read()

        # find units keyword in raw_data.txt
        courses = []
        units = re.finditer('\"unit\"',text)
        for u in units:

            # find items keyword including it's courses
            items = find(text[u.end():],keyword='item')
            for i in items:

                # find course
                if i['_class'] == "course":
                    course = Course(
                        id=i['id'],
                        title=i['title'],
                        image_100x100=i['image_100x100'],
                        headline=i['headline'],
                        num_subscribers=i['num_subscribers'],
                        avg_rating=round(i['avg_rating'],2),
                        content_length=re.search('[0-9.]+',i['content_info']).group()
                    )
                    courses.append(course)

        # write out courses into course.txt
        existing_course = []
        with open('data/course_data/course.txt','w',encoding='utf-8') as f:
            for course in courses:
                if course.id not in existing_course:
                    existing_course.append(course.id)
                    print(course,file=f)

    def extract_review_info(self):
        '''Extract all reviews from review_data folder'''
        
        # look for json files inside review_data folder
        reviews = []
        root = 'data/review_data/'
        for root,_,files in os.walk(root):
            for file in files:
                if file.endswith('json'):
                    file_path = root+file
                    course_id, _ = os.path.splitext(file)

                    # read the review json file
                    with open(file_path,encoding='utf-8') as f:
                        text = f.read()

                        # find course review
                        try: results = find(text,keyword='results')
                        except: results = None
                        if results != None:
                            for result in results:
                                if "course_review" == result['_class']:
                                    review = Review(
                                        id=str(result['id']),
                                        content=result['content'],
                                        rating=str(result['rating']),
                                        course_id=str(course_id)
                                    )
                                    reviews.append(review)

        # write out reviews into review.txt
        with open('data/course_data/review.txt','w',encoding='utf-8') as f:
            for review in reviews:
                print(review,file=f)

    def extract_student_info(self):
        
        students = []
        root = 'data/review_data/'
        for root,_,files in os.walk(root):
            for file in files:
                if file.endswith('json'):
                    file_path = root+file

                    # read the review json file
                    with open(file_path,encoding='utf-8') as f:
                        text = f.read()

                        # find student as reviewers
                        try: results = find(text,keyword='results')
                        except: results = None
                        if results != None:
                            for result in results:
                                if "course_review" == result['_class']:
                                    user = result['user']
                                    if 'user' == user['_class']:
                                        try: user_id = user['id']
                                        except: user_id = self.generate_unique_user_id()
                                        student = Student(
                                            id=str(user['id']),
                                            username=user['display_name'].replace('.','').replace(' ','_').lower(),
                                            password="".join(["***"+p+"---" for p in str(user['id'])]),
                                            title=user['title'],
                                            image_50x50=user['image_50x50'],
                                            initials=user['initials'],
                                            review_id=str(result['id'])
                                        )
                                        students.append(student)

        # write out reviews into review.txt
        with open('data/user_student.txt','w',encoding='utf-8') as f:
            for student in students:
                print(student,file=f)

    def extract_instructor_info(self):
        '''Extract instructor list from raw_data.txt and write it out to user_instructor.txt'''
        
        # open raw_data.txt
        with open('data/course_data/raw_data.txt',encoding='utf-8') as f:
            text = f.read()

        # find units keyword in raw_data.txt
        instructors = []
        uniques = []
        units = re.finditer('\"unit\"',text)
        for u in units:

            # find items keyword including it's courses
            items = find(text[u.end():],keyword='item')
            for i in items:

                # find instructor
                if i['_class'] == "course":
                    for k in i['visible_instructors']:
                        if k['_class'] == 'user':

                            # collect instructor data
                            instructor = Instructor(
                                id=k['id'],
                                username=k['display_name'].replace(" ","_").replace(".","").lower(),
                                password="".join(["***"+p+"---" for p in str(k['id'])]),
                                display_name=k['display_name'],
                                job_title=k['job_title'],
                                image_100x100=k['image_100x100'],
                                course_id_list=[str(i['id'])]
                            )

                            # check the unique instructor id
                            if instructor.id not in uniques:
                                uniques.append(instructor.id)
                                instructors.append(instructor)
                            elif instructor.id in uniques:

                                # append course id for which instructor take
                                for idx,q in enumerate(instructors):
                                    if q.id == instructors[idx].id and i['id'] not in q.course_id_list:
                                        instructors[idx].course_id_list.append(str(i['id']))

        # write out instructor data
        with open('data/user_instructor.txt','w',encoding='utf-8') as f:
            for instructor in instructors:
                print(instructor,file=f)

    def extract_info(self):
        '''Extract all information including course, instructors, student, and reviews data.'''
        self.extract_course_info()
        self.extract_instructor_info()
        self.extract_review_info()
        self.extract_student_info()

    def remove_data(self):
        '''Clear data for course.txt, review.txt, user_student.txt, and user_instructor.txt'''
        
        # define file's path
        text_files = [
            'data/course_data/course.txt',
            'data/course_data/review.txt',
            'data/user_student.txt',
            'data/user_instructor.txt',
        ]

        # write empty string into it
        for file in text_files:
            with open(file,'w') as f:
                f.write('')

    def view_courses(self, **args):
        pass

    def view_users(self):
        ''' Count numbers of admins, instructors, and students users account. '''

        # prepare users object
        root = 'data'
        text_files = {
            'Admin': {
                'path': os.path.join(root,'user_admin.txt'),
                'count': 0
            },
            'Student': {
                'path': os.path.join(root,'user_student.txt'),
                'count': 0
            },
            'Instructor': {
                'path': os.path.join(root,'user_instructor.txt'),
                'count': 0
            }
        }
        
        # count the lines for each text file
        for user in text_files:
            with open(text_files[user]['path'],encoding='utf-8') as fr:
                lines = fr.read().split('\n')
                for c in lines:
                    if c != "":
                        text_files[user]['count'] += 1
        
        # printout the results
        for user in text_files:
            count = text_files[user]['count']
            print(f'Total number of {user.lower()}: {int(count)}')

    def view_reviews(self, **args):
        pass

if __name__ == '__main__':

    admin = Admin(username='admin', password='admin')
    admin.extract_student_info()