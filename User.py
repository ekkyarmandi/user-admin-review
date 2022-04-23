import base64

class User:

	def __init__(self):
		self.user_id = -1
		self.username = ""
		self.password = ""
		self.encryption(self.password)

	def generate_unique_user_id(self):
		pass

	def encryption(self,password):
		self.password = base64.b64encode(bytes(password,encoding='utf-8')).decode()

	def login(self):
		pass

	def extract_info(self):
		pass

	def view_courses(self):
		pass

	def view_users(self):
		pass

	def view_reviews(self):
		pass

	def remove_data(self):
		pass

	def __str__(self):
		user_str = ";;;".join([str(self.user_id),self.username,self.password])
		print(user_str)