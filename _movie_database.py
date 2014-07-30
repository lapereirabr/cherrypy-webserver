# Mike Creehan #
# CherryPy 2   #

class _movie_database:
	def __init__(self):
		self.movie_names = dict()
		self.movie_genres = dict()
		self.user_gender = dict()
		self.user_age = dict()
		self.user_job = dict()
		self.user_zip = dict()
		self.ratings = dict()
		self.posters = dict()
		self.favorites = dict()

	def load_posters(self, posters_file):
		f = open(posters_file)
		for line in f:
			line = line.rstrip()
			components = line.split("::")
			mid = int(components[0])
			mimg = components[2]
			self.posters[mid] = mimg
		f.close()

	def load_movies(self, movie_file):
		f = open(movie_file)
		for line in f:
			line = line.rstrip()
			components = line.split("::")
			mid = components[0]
			mname = components[1]
			mgenre = components[2]
			mid = int(mid)
			self.movie_names[mid] = mname
			self.movie_genres[mid] = mgenre
		f.close()

	def load_favorites(self, favorites_file):
		f = open(favorites_file)
		for line in f:
			list = []
			line = line.rstrip()
			components = line.split("::")
			uid = int(components[0])
			mid = int(components[1])
			list.append(mid)
			if uid not in self.favorites:
				self.favorites[uid] = list
			else:
				self.favorites[uid].append(mid)
		f.close()
		
	def get_favorites(self, uid):
		uid = int(uid)
		mids = []
		if uid in self.favorites:
			for mid in self.favorites[uid]:
				mids.append(mid)
		else:
			mids.append(0)
		return mids
	
	def set_favorite(self, uid, mid):
		uid = int(uid)
		if uid in self.favorites:
			if mid not in self.favorites[uid]:
				self.favorites[uid].append(mid)
		else:
			list = []
			list.append(mid)
			self.favorites[uid] = list

	def delete_favorites(self, user_id):
		uid = int(user_id)
	#	mid = int(movie_id)
		if uid in self.favorites:
			del self.favorites[uid]


	def delete_all_favorites(self):
		self.favorites.clear()

	def save_favorites(self, favorites_file):
		f = open(favorites_file, "w")
#		f.write("I WROTE DIS\n")
		for uid in self.favorites:
			for mid in self.favorites[uid]:
				f.write(str(uid) + "::" + str(mid))
				f.write("\n")
		f.close()

	def get_favorite_counts(self):
		counts = {}
		for uid in self.favorites:
			for movie in self.favorites[uid]:
				if movie not in counts:
					counts[movie] = 1
				else:
					counts[movie] = counts[movie] + 1

		return counts


	def get_movie(self, mid):
		movie = []
		mid = int(mid)
		try:
			mname = self.movie_names[mid]
			mgenre = self.movie_genres[mid]
			if mid in self.posters:
				mimg = self.posters[mid]
			else:
				mimg = '/default.jpg'
			movie.append(mname)
			movie.append(mgenre)
			movie.append(mimg)
		except Exception as ex:
			movie = None
		return movie

	def get_movies(self):
		movies = []
		for key in self.movie_names:
			movies.append(key)
		return movies

	def set_movie(self, mid, (title, genres)):	
		mid = int(mid)
		self.movie_names[mid] = title
		self.movie_genres[mid] = genres
		self.posters[mid] = '/default.jpg'
		print self.movie_names[mid]
		print mid

	def delete_movie(self, mid):
		mid = int(mid)
		self.movie_names.pop(mid, None)
		self.movie_genres.pop(mid, None)

	def load_users(self, users_file):
		f = open(users_file)
		for line in f:
			line = line.rstrip()
			components = line.split("::")
			uid = components[0]
			gender = components[1]
			age = components[2]
			job = components[3]
			zip = components[4]
			uid = int(uid)
			age = int(age)
			job = int(job)
			self.user_gender[uid] = gender
			self.user_age[uid] = age
			self.user_job[uid] = job
			self.user_zip[uid] = zip

	def get_user(self, uid):
		user = []
		uid = int(uid)
		try:
			gender = self.user_gender[uid]
			age = self.user_age[uid]
			job = self.user_job[uid]
			zip = self.user_zip[uid]
			user.append(gender)
			user.append(age)
			user.append(job)
			user.append(zip)
		except Exception as ex:
			user = None
		return user
	
	def get_users(self):
		users = []
		for key in self.user_age:
			users.append(key)
		return users

	def set_user(self, uid, (gender, age, job, zip)):
		uid = int(uid)
		self.user_gender[uid] = gender
		self.user_age[uid] = age
		self.user_job[uid] = job
		self.user_zip[uid] = zip

	def delete_user(self, uid):
		uid = int(uid)
		self.user_gender.pop(uid, None)
		self.user_age.pop(uid, None)
		self.user_job.pop(uid, None)
		self.user_zip.pop(uid, None)

	def load_ratings(self, ratings_file):
		f = open(ratings_file)
		for line in f:
			line = line.rstrip()
			components = line.split("::")
			uid = components[0]
			mid = components[1]
			rating = components[2]
			mid = int(mid)
			uid = int(uid)
			rating = int(rating)
			if not mid in self.ratings:
				self.ratings[mid] = {}
			self.ratings[mid][uid] = rating

	def get_rating(self, mid):
		rating = 0
		for uid in self.ratings[mid]:
			rating += self.ratings[mid][uid]
		avg = (float(rating)/float(len(self.ratings[mid])))
		return avg
	
	def get_highest_rated_movie(self):
		id_avg = [0, 0]
		for mid in self.ratings:
			avg_rating = self.get_rating(mid)
			if avg_rating > id_avg[1]:
				id_avg[0] = int(mid)
				id_avg[1] = float(avg_rating)

			if avg_rating == id_avg[1]:
				if id_avg[0] > mid:
					id_avg[0] = int(mid)
					id_avg[1] = float(avg_rating)
		
		return id_avg[0]

	def get_highest_rated_unvoted_movie(self, user_id):
		user_id = int(user_id)
		id_avg = [0, 0]
		rating = 0
		avg = 0
		for mid in self.ratings:
			rating = 0
			avg = 0
			if user_id not in self.ratings[mid]:
				for uid in self.ratings[mid]:
					rating += self.ratings[mid][uid]
					avg = (float(rating)/float(len(self.ratings[mid])))
				if avg > id_avg[1]:
					id_avg[0] = int(mid)
					id_avg[1] = float(avg)
			
				if avg == id_avg[0]:
					if id_avg[0] > mid:
						id_avg[0] = int(mid)
						id_avg[1] = float(avg)
		return id_avg[0]
	
	def set_user_movie_rating(self, uid, mid, rating):
		self.ratings[mid][uid] = rating

	def get_user_movie_rating(self, uid, mid):
		try:
			rating = self.ratings[mid][uid]
		except Exception as ex:
			rating = None
		return rating
	
	def get_poster_by_mid(self, mid):
		if mid in self.posters.keys():
			return self.posters[mid]
		else:
			return '/default.jpg'	

	def delete_all_ratings(self):
		self.ratings.clear()
