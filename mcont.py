# Mike Creehan #
# CherryPy 2   #

import cherrypy
import re, json
from _movie_database import _movie_database

class MovieController(object):
	def __init__(self, mdb=None):
		if mdb is None:
			self.mdb = _movie_database()
		else:
			self.mdb = mdb
		self.mdb.load_movies('ml-1m/movies.dat')
		self.mdb.load_posters('/afs/nd.edu/user37/cmc/Public/cse332_sp14/cherrypy/data/images.dat')

	def GET(self, movie_id):
		output = {'result':'success'}
		movie_id = int(movie_id)
		movie = self.mdb.get_movie(movie_id)
	#	print movie
		try:
	#		movie = self.mdb.get_movie(movie_id)
			output['id'] = movie_id
			output['title'] = movie[0]
			output['genres'] = movie[1]
			output['img'] = movie[2]
		except Exception as ex:
			output['result'] = 'error'
			output['message'] = str(ex)
#			print str(ex)

		return json.dumps(output, encoding='latin-1')

	def GET_INDEX(self):
		output = {'result':'success'}
		list = []
		try:
			mids = self.mdb.get_movies()
			for mid in mids:
				movie = self.mdb.get_movie(mid)
				if movie is not None:
					list.append({'genres':movie[1], 'title':movie[0], 'result':'success', 'id':mid, 'img':movie[2]})
			output['movies'] = list
		except Exception as ex:
			output['result'] = 'error'
			output['message'] = str(ex)
#			print str(ex)

		return json.dumps(output, encoding='latin-1')	

	def PUT(self, movie_id):
		output = {'result':'success'}
		movie_id = int(movie_id)
		data = json.loads(cherrypy.request.body.read())

		try:
			title = data['title']
			genres = data['genres']
			self.mdb.set_movie(movie_id, (title, genres))
		except Exception as ex:
			output['result'] = 'error'
			output['message'] = str(ex)

		return json.dumps(output, encoding='latin-1')

	def POST_INDEX(self):
		output = {'result':'success'}
		data = json.loads(cherrypy.request.body.read())
		
		try:
			movies = self.mdb.get_movies()
			key = max(movies)
			key = int(key)
			key = key + 1
			genres = data['genres']
			title = data['title']
			output['id'] = key
		#	print key
			self.mdb.set_movie(key, (title, genres))
		except Exception as ex:
			output['result'] = 'error'
			output['message'] = str(ex)
#			print str(ex)
		return json.dumps(output, encoding='latin-1')


	def DELETE(self, movie_id):
		output = {'result':'success'}
		movie_id = int(movie_id)
		data = json.loads(cherrypy.request.body.fp.read())

		try:
			self.mdb.delete_movie(movie_id)
		except Exception as ex:
			output['result'] = 'error'
			output['message'] = str(ex)

		return json.dumps(output, encoding='latin-1')

	def DELETE_INDEX(self):
		output = {'result':'success'}
		
		try:
			mids = self.mdb.get_movies()
			for key in mids:
				self.mdb.delete_movie(int(key))
		except Exception as ex:
			output['result'] = 'error'
			output['message'] = str(ex)
#			print str(ex)
		return json.dumps(output, encoding='latin-1')
			
