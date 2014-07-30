# Mike Creehan #
# CherryPy 2   #

import cherrypy
import re, json
from _movie_database import _movie_database

class UserController(object):
	def __init__(self, mdb=None):
		if mdb is None:
			self.mdb = _movie_database()
		else:
			self.mdb = mdb
		self.mdb.load_users('ml-1m/users.dat')

	def GET(self, user_id):
		output = {'result':'success'}
		user_id = int(user_id)

		user = self.mdb.get_user(user_id)
		try:
			output['id'] = user_id
			output['gender'] = user[0]
			output['age'] = user[1]
			output['occupation'] = user[2]
			output['zipcode'] = user[3]
		except Exception as ex:
			output['result'] = 'error'
			output['message'] = str(ex)

		return json.dumps(output, encoding='latin-1')

	def GET_INDEX(self):
		output = {'result':'success'}
		list = []
		try:
			uids = self.mdb.get_users()
			for uid in uids:
				user = self.mdb.get_user(uid)
				if user is not None:
					list.append({'zipcode':user[3], 'age':user[1], 'gender':user[0], 'id':uid, 'occupation':user[2]})
			output['users'] = list
		except Exception as ex:
			output['result'] = 'error'
			output['message'] = str(ex)
			print str(ex)

		return json.dumps(output, encoding='latin-1')	

	def PUT(self, user_id):
		output = {'result':'success'}
		user_id = int(user_id)
		data = json.loads(cherrypy.request.body.read())

		try:
			gender = data['gender']
			age = data['age']
			job = data['occupation']
			zip = data['zipcode']
			self.mdb.set_user(user_id, (gender, age, job, zip))
		except Exception as ex:
			output['result'] = 'error'
			output['message'] = str(ex)

		return json.dumps(output, encoding='latin-1')

	def POST_INDEX(self):
		output = {'result':'success'}
		data = json.loads(cherrypy.request.body.read())
		try:
			users = self.mdb.get_users()
			key = max(users)
			key = int(key)
			key = key + 1
			gender = data['gender']
			age = data['age']
			zip = data['zipcode']
			job = data['occupation']
			key = int(key)
			self.mdb.set_user(key, (gender, age, job, zip))
			output['id'] = key
		except Exception as ex:
			output['result'] = 'error'
			output['message'] = str(ex)
			print str(ex)

		return json.dumps(output, encoding='latin-1')


	def DELETE(self, user_id):
		output = {'result':'success'}
		user_id = int(user_id)
		try:	
			data = json.loads(cherrypy.request.body.fp.read())
			self.mdb.delete_user(user_id)
		except Exception as ex:
			output['result'] = 'error'
			output['message'] = str(ex)
			print str(ex)
		return json.dumps(output, encoding='latin-1')

	def DELETE_INDEX(self):
		output = {'result':'success'}	
		try:
			uids = self.mdb.get_users()
			for uid in uids:
				self.mdb.delete_user(int(uid))
		except Exception as ex:
			output['result'] = 'error'
			output['message'] = str(ex)
			print str(ex)
		return json.dumps(output, encoding='latin-1')
			
