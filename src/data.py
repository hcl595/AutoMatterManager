import mysql.connector
from mysql.connector.locales.eng import client_error
from Setup import Settings
from sqlalchemy import *

sets = Settings()

class SQLManager(object):

	def __init__(self):
		self.conn = None
		self.cursor = None
		self.connect()

	def connect(self):
		DB_CONFIG = sets.database()
		self.conn = mysql.connector.connect(
			host=DB_CONFIG["host"],
			port=DB_CONFIG["port"],
			user=DB_CONFIG["user"],
			passwd=DB_CONFIG["passwd"],
			database=DB_CONFIG["db"]
		)
		self.cursor = self.conn.cursor()
		

	def get_list(self, sql, args=None):
		self.reconn()
		sqlcmd = sql + '"' + args + '"'
		print(sqlcmd)
		self.cursor.execute(sqlcmd)
		result = self.cursor.fetchall()
		return result

	def get_list2(self, sql1, sql2 ,args1=None ,args2=None):
		self.reconn()
		sqlcmd = sql1 + '"' + args1 + '"' + sql2 + '"' + args2 + '"'
		print(sqlcmd)
		self.cursor.execute(sqlcmd)
		result = self.cursor.fetchall()
		return result

	def get_list3(self, sql1, sql2 , sql3,args1=None ,args2=None, args3=None):
		self.reconn()
		sqlcmd = sql1 + '"' + args1 + '"' + sql2 + '"' + args2 + '"' + sql3 + '"' + args3 + '"'
		print(sqlcmd)
		self.cursor.execute(sqlcmd)
		result = self.cursor.fetchall()
		return result

	def get_list_order(self, sql1, sql2 ,args1=None):
		self.reconn()
		sqlcmd = sql1 + '"' + args1 + '" ' + sql2
		print(sqlcmd)
		self.cursor.execute(sqlcmd)
		result = self.cursor.fetchall()
		return result

	def get_one(self, sql, args=None):
		self.reconn()
		sqlcmd = sql + '"' + args + '"'
		print(sqlcmd)
		self.cursor.execute(sqlcmd)
		result = self.cursor.fetchone()
		return result

	def into(self, sql,args=None):
		self.reconn()
		sqlcmd = sql + args
		self.cursor.execute(sqlcmd)

	def into2(self, sql,args1=None,args2=None):
		self.reconn()
		sqlcmd = sql + "('" + args1 + "','" + args2 + "')"
		print(sqlcmd)
		self.cursor.execute(sqlcmd)

	def into3(self, sql,args1=None,args2=None,args3=None):
		self.reconn()
		sqlcmd = sql + "('" + args1 + "','" + args2 + "','" + args3 + "')"
		print(sqlcmd)
		self.cursor.execute(sqlcmd)

	def into4(self, sql,args1=None,args2=None,args3=None,args4=None):
		self.reconn()
		sqlcmd = sql + "('" + args1 + "','" + args2 + "','" + args3 + "','" + args4 + "')"
		print(sqlcmd)
		self.cursor.execute(sqlcmd)
		
	def into6(self, sql,args1=None,args2=None,args3=None,args4=None,args5=None,args6=None):
		self.reconn()
		sqlcmd = sql + "('" + args1 + "','" + args2 + "','" + args3 + "','" + args4 + "','" + args5 + "','" + args6 + "')"
		print(sqlcmd)
		self.cursor.execute(sqlcmd)

	def delete(self, sql, args=None):
		self.reconn()
		sqlcmd = sql + '"' + args + '"'
		self.cursor.execute(sqlcmd)

	def delete2(self, sql1, sql2, args1= None, args2=None):
		self.reconn()
		sqlcmd = sql1 + '"' + args1 + '"' + sql2 + '"' + args2 + '"'
		self.cursor.execute(sqlcmd)

	def update(self, sql1, sql2, sql3, sql4, sql5, sql6, args1= None, args2=None,args3= None, args4= None, args5= None, args6= None,):
		self.reconn()
		sqlcmd = sql1 + "'" + args1 + "'" + sql2 + "'" + args2 + "'" + sql3 + "'" + args3 + "'" + sql4 + "'" + args4 + "'" + sql5 + "'" + args5 + "'" + sql6 + "'" + args6 + "'"
		self.cursor.execute(sqlcmd)

	def moddify(self, sql, args=None):
		self.reconn()
		print(sql,args)
		sqlcmd = sql + '"' + args + '"'
		self.cursor.execute(sqlcmd)
		self.conn.commit()

	def multi_modify(self, sql, args=None):
		self.reconn()
		self.cursor.executemany(sql, args)
		self.conn.commit()

	def create(self, sql, args=None):
		self.reconn()
		sqlcmd = sql + '"' + args + '"'
		self.cursor.execute(sqlcmd)
		self.conn.commit()
		last_id = self.cursor.lastrowid
		return last_id

	def reconn(self):
		self.close()
		self.connect()
		print("reconnect complete")

	def close(self):
		self.conn.close()

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		self.close()