from Admin import Admin
from User import User
from Course import Course
from Instructor import Instructor
from Student import Student
from Review import Review

def show_menu():
    msg = [
        'Please enter {} command for further service:',
        '1. EXTRACT_DATA',
        '2. VIEW_COURSES',
        '3. VIEW_USERS',
        '4. VIEW_REVIEWS',
        '5. REMOVE_DATA\n'
    ]
    for m in msg:
        print(m)

def process_operations():
    pass

def main():
    pass


if __name__ == "__main__":

    # print a welcome message
    print('Welcome to our system')

    # ask user to login
    raw_input = input('Pleaes input username and password to login: (format username password)\n').strip().split(" ")
    if len(raw_input) > 1:
        username = raw_input[0]
        password = raw_input[1]
    elif len(raw_input) <= 1:
        username = raw_input[0]
        password = ""

    user = User()
    result = user.login(username,password)
    print(result)

    if result[1] == 'Admin':
        user = Admin(
            id=result[2].split(";;;")[0],
            username=result[2].split(";;;")[1],
            password=result[2].split(";;;")[2]
        )

    elif result[1] == 'Instructor':
        user = Instructor(
            id=result[2].split(";;;")[0],
            username=result[2].split(";;;")[1],
            password=result[2].split(";;;")[2],
            display_name=result[2].split(";;;")[3],
            job_title=result[2].split(";;;")[4],
            image_100x100=result[2].split(";;;")[5],
            course_id_list=result[2].split(";;;")[6].split('--')
        )

    elif result[1] == 'Student':
        user = Student(
            id=result[2].split(";;;")[0],
            username=result[2].split(";;;")[1],
            password=result[2].split(";;;")[2],
            title=result[2].split(";;;")[3],
            image_50x50=result[2].split(";;;")[4],
            initials=result[2].split(";;;")[5],
            review_id=result[2].split(";;;")[6]
        )

    print(user)