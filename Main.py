from Admin import Admin
from User import User


def show_menu():
    pass


def process_operations():
    pass


def main():
    pass


if __name__ == "__main__":

    # print a welcome message
    print('Welcome to our system')

    # manually register admin
    while True:
        user_input = input('Please input username and password to login: (format username password)\n')
        if user_input == 'logout':
            print('Thank you for using our system')
        else:
            try:
                username = user_input.split(" ")[0]
                password = user_input.split(" ")[1]
                if username == 'admin' and password == 'admin':
                    admin = Admin(username=username,password=password)
                    admin.register_admin()
                    print(admin)
                    break
            except:
                print('username or password incorrect')