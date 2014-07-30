# Mike Creehan #
# CherryPy2    #

import cherrypy
import re, json
from _movie_database import _movie_database

class RatingController(object):
	def __init__(self, mdb=None):
		if mdb is None:
			self.mdb = _movie_database()
		else:
			self.mdb = mdb
		self.mdb.load_ratings('ml-1m/ratings.dat')

	def GET(self, movie_id):
		output = {'result':'success'}
		movie_id = int(movie_id)

		try:
			rating = self.mdb.get_rating(movie_id)
			output['movie_id'] = movie_id
			output['rating'] = rating
		except Exception as ex:
			output['result'] = 'error'
			output['message'] = str(ex)
			print str(ex)

		return json.dumps(output, encoding='latin-1')
