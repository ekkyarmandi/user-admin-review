from User import User
import os

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
        pass

    def extract_review_info(self):
        pass

    def extract_student_info(self):
        pass

    def extract_instructor_info(self):
        pass

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
    admin.view_users()