class Review:

    def __init__(self, username="", password="", user_id=-1, user_title="", user_image_50x50="", user_initials="", review_id=-1):
        '''
        Review constructor
        :param user_id: int, default value -1
        :param username: str, default value "" (empty string)
        :param password: str, default value "" (empty string)
        :param user_title: str, default value "" (empty string)
        :param user_image_50x50: str, default value "" (empty string)
        :param use_initials: str, default value "" (empty string)
        :param review_id: int, default value -1
        '''
        self.user_id = user_id
        self.username = username
        self.password = password
        self.user_title = user_title
        self.user_image_50x50 = user_image_50x50
        self.user_initials = user_initials
        self.review_id = review_id

    def find_review_by_id(self, review_id):
        pass

    def find_review_by_keywords(self, keyword):
        pass

    def find_review_by_course_id(self, course_id):
        pass

    def reviews_overview(self):
        pass # count the total number of reviews

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