from User import User


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
        pass

    def view_reviews(self, *args):
        pass

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
