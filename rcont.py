# Mike Creehan #
# CherryPy 2   #

import cherrypy
import re, json
from _movie_database import _movie_database

class ResetController(object):
	def __init__(self, mdb=None):
		if mdb is None:
			self.mdb = _movie_database()
		else:
			self.mdb = mdb
				

	def PUT(self):
		output = {'result':'success'}

		try:
			self.mdb.__init__()
			self.mdb.load_movies('ml-1m/movies.dat')
			self.mdb.load_users('ml-1m/users.dat')
			self.mdb.load_ratings('ml-1m/ratings.dat')
			self.mdb.load_posters('/afs/nd.edu/user37/cmc/Public/cse332_sp14/cherrypy/data/images.dat')	
		except Exception as ex:
			output['result'] = 'error'
			output['message'] = str(ex)		

		return json.dumps(output, encoding='latin-1')
