from User import User
from Course import Course
from Instructor import Instructor
import re
import os

from pprint import pprint

def find(text):
    c = re.search('\"items\"',text).end()
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
            items = find(text[u.end():])
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
        pass

    def extract_student_info(self):
        pass

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
            items = find(text[u.end():])
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
        pass

    def remove_data(self):
        pass

    def view_courses(self, **args):
        pass

    def view_users(self):
        ''' Count admins, instructors, and students users account. '''

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
    admin.view_users()