from User import User


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
        pass

    def view_reviews(self, *args):
        pass

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