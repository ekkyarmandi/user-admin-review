from User import User
from Admin import Admin
from Student import Student
from Instructor import Instructor

def show_menu():
    msg = [
        '1. EXTRACT_DATA',
        '2. VIEW_COURSES',
        '3. VIEW_USERS',
        '4. VIEW_REVIEWS',
        '5. REMOVE_DATA\n'
    ]
    for m in msg:
        print(m)

def process_operations(user, header):

    def get_commands(user_input):
        inputs = user_input.split(" ")
        if len(inputs) >= 3:
            command = inputs[1]
            value = inputs[2]
            return command, value
        elif len(inputs) == 2:
            return inputs[1], ""
        elif len(inputs) == 1:
            return "", ""

    while True:

        # show menu options to user
        print(header)
        show_menu()

        # do user input
        user_input = input()
        if user_input.lower() == 'exit':
            return "exit"
        elif user_input.lower() == 'logout':
            return "logout"
        elif len(user_input) > 0:
            idx = user_input[0]
            if idx == '1':
                user.extract_info()
            elif idx == '2':
                command, value = get_commands(user_input)
                user.view_courses(command,value)
            elif idx == '3':
                user.view_users()
            elif idx == '4':
                command, value = get_commands(user_input)
                user.view_reviews(command,value)
            elif idx == '5':
                user.remove_data()
            else:
                print('Incorrect command\n')

        else:
            print('Incorrect command\n')
            

def main():

    while True:

        while True:
        
            # assign temporary user object
            user = User()

            # ask user to login
            raw_input = input('Please input username and password to login: (format username password)\n').strip().split(" ")
            if len(raw_input) > 1:
                username = raw_input[0]
                password = raw_input[1]
            elif len(raw_input) <= 1:
                username = raw_input[0]
                password = ""
            result = user.login(username,password)

            # identify username and password
            if result[1] == 'Admin':
                user = Admin(
                    id=result[2].split(";;;")[0],
                    username=result[2].split(";;;")[1],
                    password=password
                )
                break
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
                break
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
                break
            else:
                # show incorrect username and password message
                print('\nUsername and password incorrect\n')

        # process user input
        print('\n{} logged in succesfully'.format(result[1]))
        print('Welcome {}. Your role is {}.'.format(user.username,result[1]))
        message = 'Please enter {} command for further service:'.format(result[1])
        logic = process_operations(user, message)
        if logic == 'logout':
            print("\nThank you for using our system\n")
            continue
        elif logic == 'exit':
            print("\nBye")
            break
        

if __name__ == "__main__":

    # print a welcome message
    print('Welcome to our system\n')

    # manually registered admin
    main()