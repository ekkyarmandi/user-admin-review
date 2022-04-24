from User import User

class Student(User):

    def __init__(self, username="", password="", user_id=-1, user_title="", user_image_50x50="", user_initials="", review_id=-1):
        '''
        Student constructor
        :param user_id: int, default value -1
        :param username: str, default value "" (empty string)
        :param password: str, default value "" (empty string)
        :param user_title: str, default value "" (empty string)
        :param user_image_50x50: str, default value "" (empty string)
        :param user_initials: str, default value "" (empty string)
        :param review_id: int, default value -1
        '''
        self.user_id = user_id
        self.username = username
        self.password = password
        self.user_title = user_title
        self.user_image_50x50 = user_image_50x50
        self.user_initials = user_initials
        self.review_id = review_id

    def view_courses(self, **args):
        pass

    def view_reviews(self, **args):
        pass

    def __str__(self):
        '''Object in string format'''
        return ";;;".join([
            str(self.user_id),
            self.username,
            self.password,
            self.user_title,
            self.user_image_50x50,
            self.user_initials,
            str(self.review_id)
        ])