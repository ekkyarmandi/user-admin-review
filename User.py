import base64

class User:

	def __init__(self, username="", password="", user_id=-1):
		'''
		User constructor
		:param user_id: int, default value -1
		:param username: str, default value "" (empty string)
		:param password: str, default value "" (empty string)
		:return: None
		'''
		self.user_id = user_id
		self.username = username
		self.password = self.encryption(password)

	def generate_unique_user_id(self):
		'''Generate unique id for new registered user'''

		# collect id from all registered users
		content = []
		text_files = ['user_admin.txt','user_student.txt','user_instructor.txt']
		for file in text_files:
			with open(file,'r') as f:
				text = f.read().split('\n')
				content.extend(text)
		ids = []
		for c in content:
			if c.strip() != "":
				existing_id = c.strip().split('|')[0]
				ids.append(existing_id.strip('0'))
		ids = [int(id) for id in ids]
		ids = sorted(ids)
		
		# find a new unique id for new user
		i = 1
		while True:
			
			# return if find a unique one
			if i not in ids:
				return '{:010d}'.format(i)

	def encryption(self,password):
		'''
		User password encryption before saved into user_admin.txt, user_student.txt, or user_instructor.txt
		:param password: str
		:return:
		'''
		return base64.b64encode(bytes(password,encoding='utf-8')).decode()

	def login(self):
		pass

	def extract_info(self):
		'''Default user extract info message'''
		print('You have no premission to extract information.')

	def view_courses(self,**args):
		'''Default user view courses message'''
		print('You have no permission to view courses')

	def view_users(self):
		'''Default user view users message'''
		print('You have no permission to view users')

	def view_reviews(self,**args):
		'''Default user view reviews message'''
		print('You have no permission to view reviews')

	def remove_data(self):
		'''Default user remove data message'''
		print('You have no permission to remove data')

	def __str__(self):
		'''Object in string format'''
		return ";;;".join([str(self.user_id),self.username,self.password])