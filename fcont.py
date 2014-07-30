# Mike Creehan #
# CherryPy 2   #

import cherrypy
import re, json
from _movie_database import _movie_database

class FavoriteController(object):
	def __init__(self, mdb=None):
		if mdb is None:
			self.mdb = _movie_database()
		else:
			self.mdb = mdb
		self.mdb.load_favorites('ml-1m/favorites.dat')		

	def GET(self, user_id):
		output = {'result':'success'}
		user_id = int(user_id)
		try:
			favs = self.mdb.get_favorites(user_id)
			output['favorites'] = favs

		except Exception as ex:
			output['result'] = 'error'
			output['message'] = str(ex)
			print str(ex)

		return json.dumps(output, encoding='latin-1')

	def GET_INDEX(self):
		output = {'result':'success'}
		#data = json.loads(cherrypy.request.body.fp.read())
		try:
		#	mid = data['movie_id']
			counts = self.mdb.get_favorite_counts()
			output['counts'] = counts
		except Exception as ex:
			output['result'] = 'error'
			output['message'] = str(ex)
		return json.dumps(output, encoding='latin-1')


	def PUT(self, user_id):
		output = {'result':'success'}
		user_id = int(user_id)
	#	print "HURR"
		data = json.loads(cherrypy.request.body.read())
		try:
			mid = data['movie_id']
			self.mdb.set_favorite(user_id, mid)
		except Exception as ex:
			output['result'] = 'error'
			output['message'] = str(ex)
			print str(ex)
		return json.dumps(output, encoding='latin-1')
	
	def POST_INDEX(self):
		output = {'result':'success'}
		data = json.loads(cherrypy.request.body.read())	
	#	print "HEEEEEEEEEREEEEEEEE"

		self.mdb.save_favorites(data['path'])
		return json.dumps(output, encoding='latin-1')

	def DELETE(self, user_id):
		output = {'result':'success'}
		user_id = int(user_id)
#		data = json.loads(cherrypy.request.body.read())
		try:
#			mid = data['movie_id']
			self.mdb.delete_favorites(user_id)
		except Exception as ex:
			output['result'] = 'error'
			output['message'] = str(ex)
		return json.dumps(output, encoding='latin-1')

	def DELETE_INDEX(self):
		output = {'result':'success'}
		try:
			self.mdb.delete_all_favorites()
		except Exception as ex:
			output['result'] = 'error'
			output['message'] = str(ex)
			print str(ex)
		return json.dumps(output, encoding='latin-1')
