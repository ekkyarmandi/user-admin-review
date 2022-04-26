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
            items = find(text[u.end():],keyword='items')
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
                                    content = re.sub('\s+',' ',result['content']).strip()
                                    review = Review(
                                        id=str(result['id']),
                                        content=content,
                                        rating=str(result['rating']),
                                        course_id=str(course_id)
                                    )
                                    reviews.append(review)

        # write out reviews into review.txt
        with open('data/course_data/review.txt','w',encoding='utf-8') as f:
            for review in reviews:
                print(review,file=f)

    def extract_student_info(self):
        '''Extract reviewers aka student from review_data folder'''

        def user_password(user):
            '''
            Convert user initials and id as an combination of password
            :param user: User class
            :return password: str
            '''
            return user.initials.lower() + user.id + user.initials.lower()
        
        # crawl for json files
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
                                        except: user_id = None
                                        student = Student(
                                            id=str(user_id),
                                            username=user['display_name'].replace('.','').replace(' ','_').lower(),
                                            title=user['title'],
                                            image_50x50=user['image_50x50'],
                                            initials=user['initials'],
                                            review_id=str(result['id'])
                                        )
                                        student.password = user_password(student)
                                        students.append(student)

        # write out reviews into review.txt
        with open('data/user_student.txt','w',encoding='utf-8') as f:
            for student in students:
                if student.id != 'None':
                    print(student,file=f)

        # generate new id
        new_students = []
        for student in students:
            if student.id == 'None':
                student.id = self.generate_unique_user_id()
                student.password = user_password(student)
                new_students.append(student)

        # append new generated user id into text file
        with open('data/user_student.txt','a',encoding='utf-8') as f:
            for student in new_students:
                print(student,file=f)


    def extract_instructor_info(self):
        '''Extract instructor list from raw_data.txt and write it out to user_instructor.txt'''
        
        # read raw_data.txt
        with open('data/course_data/raw_data.txt',encoding='utf-8') as f:
            text = f.read()

        # find units keyword in raw_data.txt
        instructors = []
        uniques = []
        units = re.finditer('\"unit\"',text)
        for u in units:

            # find items keyword including it's courses
            items = find(text[u.end():],keyword='items')
            for i in items:

                # collect instructor data
                if i['_class'] == "course":
                    for k in i['visible_instructors']:
                        if k['_class'] == 'user':
                            user_id = k['id']
                            if user_id not in uniques:
                                instructor = Instructor(
                                    id=k['id'],
                                    username=k['display_name'].replace(" ","_").replace(".","").lower(),
                                    password="".join(["***"+p+"---" for p in str(k['id'])]),
                                    display_name=k['display_name'],
                                    job_title=k['job_title'],
                                    image_100x100=k['image_100x100'],
                                    course_id_list=[str(i['id'])]
                                )
                                instructors.append(instructor)
                                uniques.append(user_id)
                            elif user_id in uniques:
                                for instructor in instructors:
                                    if user_id == instructor.id:
                                        instructor.course_id_list.append(str(i['id']))
                                        break

        # write out instructor data
        with open('data/user_instructor.txt','w',encoding='utf-8') as f:
            for instructor in instructors:
                instructor.course_id_list = list(dict.fromkeys(instructor.course_id_list))
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

    def view_courses(self, *args):
        '''
        Returned requested course

        usage: args=[command,value]
        i.e. ['TITLE_KEYWORD','web']
        allowed commands = TITLE_KEYWORD, ID, or INSTRUCTOR_ID

        :param args: list, [command,value]
        '''

        
        # count args
        trues = [True if p != "" else False for p in args]

        # filtered by input
        if sum(trues) == 2:

            if args[0] in ['TITLE_KEYWORD','ID','INSTRUCTOR_ID']:

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
                
                # read review.txt
                with open('data/user_instructor.txt','r',encoding='utf-8') as f:
                    raw_instructors = f.read().strip().split('\n')
                    instructors = []
                    for raw in raw_instructors:
                        instructor = Instructor(
                            id=raw.split(';;;')[0],
                            username=raw.split(';;;')[1],
                            password='***',
                            display_name=raw.split(';;;')[3],
                            job_title=raw.split(';;;')[4],
                            image_100x100=raw.split(';;;')[5],
                            course_id_list=raw.split(';;;')[6].split('--')
                        )
                        instructors.append(instructor)

                # returned course and it's count based on query
                count = 0
                if args[0] == 'TITLE_KEYWORD':
                    for course in courses:
                        if args[1].lower() in course.title.lower():
                            count += 1
                            print(course)

                elif args[0] == 'ID':
                    for course in courses:
                        if args[1] == course.id:
                            count += 1
                            print(course)

                elif args[0] == 'INSTRUCTOR_ID':
                    for instructor in instructors:
                        if args[1] == instructor.id:
                            selected_courses = instructor.course_id_list
                            for course in courses:
                                if course.id in selected_courses:
                                    count += 1
                                    print(course)
                            break
                
                # printout total numbers
                print('total returned course: ' + str(count) + '\n')

            else:
                # error message if user didn't type any command
                print('Please type the proper command 2 [TITLE_KEYWORD/ID/INSTRUCTOR_ID] [value]\n')

        # error message if user didn't type any command or value
        elif sum(trues) == 1:
            print('Make sure you also include command/value on the input\n')

        # error message if user didn't type anything and return course overview instead
        elif sum(trues) == 0:
            course = Course()
            course.course_overview()

    def view_reviews(self, *args):
        '''
        Returned requested reviews

        usage: args=[command,value]
        i.e. ['KEYWORD','nice']
        allowed commands = ID, KEYWORD, or COURSE_ID

        :param args: list, [command,value]
        '''

        # count args
        trues = [True if p != "" else False for p in args]

        # filtered by input
        if sum(trues) == 2:

            if args[0] in ['ID','KEYWORD','COURSE_ID']:

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
                
                # returned course and it's count based on query
                count = 0
                if args[0] == 'ID':
                    for review in reviews:
                        if args[1] in review.id:
                            count += 1
                            print(review)

                elif args[0] == 'KEYWORD':
                    for review in reviews:
                        if args[1].lower() in review.content.lower():
                            count += 1
                            print(review)

                elif args[0] == 'COURSE_ID':
                    for review in reviews:
                        if args[1] in review.course_id:
                            count += 1
                            print(review)
                
                # printout counted reviews
                print('total returned review: ' + str(count) + '\n')

            else:
                # error message if user didn't type any command
                print('Please type the proper command 4 [ID, KEYWORD, or COURSE_ID] [value]\n')

        # error message if user didn't input any value
        elif sum(trues) == 1:
            print('Make sure you also include value on the input\n')

        # error message if user didn't type anything and return course overview instead
        elif sum(trues) == 0:
            review = Review()
            review.reviews_overview()

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
        print()