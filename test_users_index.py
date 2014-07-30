import unittest
import requests
import json

class TestUsersIndex(unittest.TestCase):

	#@classmethod
	#def setUpClass(self):
	SITE_URL = 'http://student00.cse.nd.edu:40009'
	USERS_URL = SITE_URL + '/users/'
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

	def test_users_index_get(self):
		self.reset_data()
		r = requests.get(self.USERS_URL)
		self.assertTrue(self.is_json(r.content))
		resp = json.loads(r.content)

		testuser = {}
		testuser['gender'] = 'M'
		testuser['occupation'] = 4

		users = resp['users']
		for user in users:
			if user['id'] == 6029:
				testuser = user

		self.assertEquals(testuser['gender'], 'F')
		self.assertEquals(testuser['occupation'], 1)

	def test_users_index_post(self):
		self.reset_data()

		m = {}
		m['gender'] = 'F'
		m['occupation'] = 4000
		m['age'] = 34
		m['zipcode'] = '46556'
		m['apikey'] = 'AAAAAAAB'
		r = requests.post(self.USERS_URL, data = json.dumps(m))
		self.assertTrue(self.is_json(r.content))
		resp = json.loads(r.content)
		self.assertEquals(resp['result'], 'success')
		self.assertEquals(resp['id'], 6041)

		r = requests.get(self.USERS_URL + str(resp['id']))
		self.assertTrue(self.is_json(r.content))
		resp = json.loads(r.content)
		self.assertEquals(resp['gender'], m['gender'])
		self.assertEquals(resp['occupation'], m['occupation'])

	def test_users_index_delete(self):
		self.reset_data()

		m = {}
		m['apikey'] = 'AAAAAAAB'
		r = requests.delete(self.USERS_URL, data = json.dumps(m))
		self.assertTrue(self.is_json(r.content))
		resp = json.loads(r.content)
		self.assertEquals(resp['result'], 'success')

		r = requests.get(self.USERS_URL)
		self.assertTrue(self.is_json(r.content))
		resp = json.loads(r.content)
		users = resp['users']
		self.assertFalse(users)

if __name__ == "__main__":
	unittest.main()

