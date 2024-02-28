from psycopg2 import connect
from config import FunctionConfig as conf

class DbClient:
	def __init__(self):
		db_name = conf.POSTGRES_DB
		db_username = conf.POSTGRES_USER
		db_password = conf.POSTGRES_PW
		db_host = conf.POSTGRES_URL
		connection = connect(database=db_name, user=db_username, password=db_password, host=db_host)
		self.cur = connection.cursor()
	
	def get(self, id):
		