import unittest
import requests
import json

class TestMovies(unittest.TestCase):

	#@classmethod
	#def setUpClass(self):
	SITE_URL = 'http://student00.cse.nd.edu:40009'
	MOVIES_URL = SITE_URL + '/movies/'
	RESET_URL = SITE_URL + '/reset/'

	def reset_data(self):
		m = {}
		m['apikey'] = 'AAAAAAAB'
		r = requests.put(self.RESET_URL, data = json.dumps(m))

	def is_json(self, resp):
		try:
			json.loads(resp)
			return True
		except ValueError:
			return False

	def test_movies_get(self):
		self.reset_data()
		movie_id = 32
		r = requests.get(self.MOVIES_URL + str(movie_id))
		self.assertTrue(self.is_json(r.content))
		resp = json.loads(r.content)
		self.assertEquals(resp['title'], 'Twelve Monkeys (1995)')
		self.assertEquals(resp['genres'], 'Drama|Sci-Fi')
		self.assertEquals(resp['img'], '/vxiIABQhiFlfODwamoevrzXvowU.jpg')

	def test_movies_put(self):
		self.reset_data()
		movie_id = 95

		r = requests.get(self.MOVIES_URL + str(movie_id))
		self.assertTrue(self.is_json(r.content))
		resp = json.loads(r.content)
		self.assertEquals(resp['title'], 'Broken Arrow (1996)')
		self.assertEquals(resp['genres'], 'Action|Thriller')

		m = {}
		m['title'] = 'ABC'
		m['genres'] = 'Sci-Fi|Fantasy'
		m['apikey'] = 'AAAAAAAB'
		r = requests.put(self.MOVIES_URL + str(movie_id), data = json.dumps(m))
		self.assertTrue(self.is_json(r.content))
		resp = json.loads(r.content)
		self.assertEquals(resp['result'], 'success')

		r = requests.get(self.MOVIES_URL + str(movie_id))
		self.assertTrue(self.is_json(r.content))
		resp = json.loads(r.content)
		self.assertEquals(resp['title'], m['title'])
		self.assertEquals(resp['genres'], m['genres'])

	def test_movies_delete(self):
		self.reset_data()
		movie_id = 95

		m = {}
		m['apikey'] = 'AAAAAAAB'
		r = requests.delete(self.MOVIES_URL + str(movie_id), data = json.dumps(m))
		self.assertTrue(self.is_json(r.content))
		resp = json.loads(r.content)
		self.assertEquals(resp['result'], 'success')

		r = requests.get(self.MOVIES_URL + str(movie_id))
		self.assertTrue(self.is_json(r.content))
		resp = json.loads(r.content)
		self.assertEquals(resp['result'], 'error')
		#self.assertEquals(resp['message'], 'movie not found')

if __name__ == "__main__":
	unittest.main()

