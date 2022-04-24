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

        # open raw_data.txt
        with open('data/course_data/raw_data.txt') as f:
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
                        course_id=i['id'],
                        course_title=i['title'],
                        course_image_100x100=i['image_100x100'],
                        course_headline=i['headline'],
                        course_num_subscribers=i['num_subscribers'],
                        course_avg_rating=round(i['avg_rating'],2),
                        course_content_length=re.search('[0-9.]+',i['content_info']).group()
                    )
                    courses.append(course)

        # write out courses into course.txt
        with open('data/course_data/course.txt','w',encoding='utf-8') as f:
            for course in courses:
                print(course,file=f)

    def extract_review_info(self):
        pass

    def extract_student_info(self):
        pass

    def extract_instructor_info(self):
        
        # open raw_data.txt
        with open('data/course_data/raw_data.txt') as f:
            text = f.read()

        # find units keyword in raw_data.txt
        instructors = []
        temp = {}
        units = re.finditer('\"unit\"',text)
        for u in units:

            # find items keyword including it's courses
            items = find(text[u.end():])
            for i in items:

                # find instructor
                if i['_class'] == "course":
                    for k in i['visible_instructors']:
                        if k['_class'] == 'user':

                            # collect unique instructor
                            users = [k for k in temp.keys()]
                            if k['id'] not in users:
                                temp.update({k['id']: [str(i['id'])]})
                            elif k['id'] in users:
                                temp[k['id']].append(str(i['id']))

                            # collect instructor data in more detail
                            instructor = Instructor(
                                user_id=k['id'],
                                username=k['display_name'].replace(" ","_").replace(".","").lower(),
                                password=self.encryption(k['id']),
                                display_name=k['display_name'],
                                job_title=k['job_title'],
                                image_100x100=k['image_100x100']
                            )
                            instructors.append(instructor)
            
        uniques = []
        for p in temp:
            for q in instructors:
                if p == q.user_id:
                    if q.user_id not in uniques:
                        q.course_id_list.extend(temp[p])
                        instructors.append(q)
                        uniques.append(q.user_id)

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
        '''
        Count for the number of users including admins, instructors, and students.
        '''
        root = 'sources'
        text_files = {
            'Admin': os.path.join(root,'user_admin.txt'),
            'Student': os.path.join(root,'user_student.txt'),
            'Instructor': os.path.join(root,'user_instructor.txt')
        }
        count = {
            'Admin': 0,
            'Student': 0,
            'Instructor': 0
        }
        for p,f in text_files.items():
            with open(f) as fr:
                lines = fr.read().split('\n')
                for c in lines:
                    if c != "":
                        count[p] += 1
        for j in count:
            print(f'Total number of {j.lower()}: {int(count[j])}')

    def view_reviews(self, **args):
        pass

if __name__ == '__main__':

    admin = Admin(username='admin', password='admin')
    admin.extract_instructor_info()