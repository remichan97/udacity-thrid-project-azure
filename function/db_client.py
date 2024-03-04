from psycopg2 import connect
from config import FunctionConfig as conf
from datetime import datetime

class DbClient:
	def __init__(self):
		db_name = conf.POSTGRES_DB
		db_username = conf.POSTGRES_USER
		db_password = conf.POSTGRES_PW
		db_host = conf.POSTGRES_URL
		self.connection = connect(database=db_name, user=db_username, password=db_password, host=db_host)
		self.cur = self.connection.cursor()
	
	def get_attendee(self): 
		self.cur.execute("select * from public.attendee")
		return self.cur.fetchall()
 
	def get_notification(self, notification_id) : 
		self.cur.execute("select * from public.notification where id = %s", (notification_id, ))
		return self.cur.fetchone()
 
	def update_notification(self, notification_id, complete_date : datetime, count): 
		self.cur.execute("update public.notification set completed_date = %s, status='Notified %s attendees' where id = %s", (complete_date,count,notification_id, ))
		self.connection.commit()
 
	def close_connection(self) : 
		self.cur.close()
		self.connection.close()