# Mike Creehan #
# CherryPy 2   #

import cherrypy
import re, json
from _movie_database import _movie_database

class VoteController(object):
	def __init__(self, mdb=None):
		if mdb is None:
			self.mdb = _movie_database()
		else:
			self.mdb = mdb
		self.mdb.load_ratings('ml-1m/ratings.dat')		

	def GET(self, user_id):
		output = {'result':'success'}
		user_id = int(user_id)
		try:
			rec_id = self.mdb.get_highest_rated_unvoted_movie(user_id)
			output['movie_id'] = rec_id

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
			mid = data['movie_id']
			rating = data['rating']
			self.mdb.set_user_movie_rating(user_id, mid, rating)
		except Exception as ex:
			output['result'] = 'error'
			output['message'] = str(ex)
			print str(ex)
		return json.dumps(output, encoding='latin-1')
	
	def DELETE_INDEX(self):
		output = {'result':'success'}
		try:
			self.mdb.delete_all_ratings()
		except Exception as ex:
			output['result'] = 'error'
			output['message'] = str(ex)
			print str(ex)
		return json.dumps(output, encoding='latin-1')
