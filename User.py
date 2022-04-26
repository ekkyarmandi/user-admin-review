import base64
import random

class User:

	def __init__(self, username="", password="", id=-1):
		'''
		User constructor
		:param user_id: int, default value -1
		:param username: str, default value "" (empty string)
		:param password: str, default value "" (empty string)
		:return: None
		'''
		self.id = id
		self.username = username
		self.password = password

	def generate_unique_user_id(self):
		'''Generate unique id for new registered user'''

		# collect id from all registered users
		content = []
		text_files = [
			'data/user_admin.txt',
			'data/user_student.txt',
			'data/user_instructor.txt'
		]
		for file in text_files:
			with open(file,'r',encoding='utf-8') as f:
				text = f.read().split('\n')
				content.extend(text)
		ids = []
		for c in content:
			if c.strip() != "":
				existing_id = c.strip().split(';;;')[0]
				ids.append(existing_id)
		
		# find a new unique id
		new_id = random.choice(ids)
		while new_id in ids:
			new_id = "".join([str(random.randint(0,9)) for _ in range(10)])
		return new_id

	def encryption(self,password):
		'''
		User password encryption before saved into user_admin.txt, user_student.txt, or user_instructor.txt
		:param password: str
		:return:
		'''
		return base64.b64encode(bytes(password,encoding='utf-8')).decode()

	def login(self, username, password):
		'''
		Pass application authenticantion		
		:param username: str
		:param password: str
		:return login_result, login_user_role, login_user_info: tuple
		'''
		
		# read all user text file
		text_files = {
			'Admin': {
				'path': 'data/user_admin.txt'
			},
			'Instructor': {
				'path': 'data/user_instructor.txt'
			},
			'Student': {
				'path': 'data/user_student.txt'
			}
		}

		# look for the right user
		for role in text_files:
			with open(text_files[role]['path'],'r',encoding='utf-8') as f:
				registered_user = f.read().strip().split('\n')
				
				if role == 'Admin':
					password = self.encryption(password)
					for reg in registered_user:
						user = {
							"username": reg.split(';;;')[1],
							"password": reg.split(';;;')[2],
						}
						if user['username'] == username and user['password'] == password:
							return True, role, reg

				elif role in ['Instructor','Student']:
					for reg in registered_user:
						user = {
							"username": reg.split(';;;')[1],
							"password": reg.split(';;;')[0],
						}
						if user['username'] == username and user['password'] == password:
							return True, role, reg

		return False, None, None

	def extract_info(self):
		'''Default user extract info message'''
		print('You have no premission to extract information.')

	def view_courses(self, *args):
		'''Default user view courses message'''
		print('You have no permission to view courses')

	def view_users(self):
		'''Default user view users message'''
		print('You have no permission to view users')

	def view_reviews(self, *args):
		'''Default user view reviews message'''
		print('You have no permission to view reviews')

	def remove_data(self):
		'''Default user remove data message'''
		print('You have no permission to remove data')

	def __str__(self):
		'''Object in string format'''
		return ";;;".join([
			str(self.id),
			self.username,
			self.encryption(self.password)
		])