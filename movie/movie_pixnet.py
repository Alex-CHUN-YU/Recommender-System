
from urllib.request import urlopen
# https://www.crummy.com/software/BeautifulSoup/bs4/doc/
from bs4 import BeautifulSoup
import os
import json

# Crawl https://remylovedrama5.blogspot.com/ movie url, name, storyline, link 
class Crawler():
	def __init__(self):
		self.root = "https://remylovedrama5.blogspot.com/"
		self.years_range = range(2016, 2019)
		
	def crawl(self):
		movies = []
		for movies_url in self.get_movies_url():
			for movie_url in self.get_movie_url(movies_url):
				movies.append(self.movie_parser(movie_url))
		self.write_json(movies)

	# https://remylovedrama5.blogspot.com/2016/
	def get_movies_url(self):
		for year in self.years_range:
			yield self.root + str(year) + "/"

	# https://remylovedrama5.blogspot.com/2016/
	def get_movie_url(self, movies_url):
		html = urlopen(movies_url).read().decode('utf-8')
		soup = BeautifulSoup(html, features = "lxml")
		for link in soup.select(".jump-link"):
			yield link.select('a')[0]['href']

	def movie_parser(self, movie_url):
		movie = {}
		movie['link'] = ""
		movie['storyline'] = ""
		html = urlopen(movie_url).read().decode('utf-8')
		soup = BeautifulSoup(html, features = "lxml")
		movie['url'] = movie_url
		movie['name'] = soup.select('h3')[0].text
		for content in soup.find_all('span'):
			if content.string is not None and ("劇照" in content.string or "預告片" in content.string):
				break
			elif content.string is not None and len(content.string) > 20:
				movie['storyline'] = content.string
			elif content.string is not None and len(content.string) > 70:
				movie['storyline'] = content.string
				break
		if soup.find_all('iframe')[0]['src'] is not None and soup.find_all('iframe')[0]['src'] is not "":
			link_html = urlopen(soup.find_all('iframe')[0]['src']).read().decode('utf-8')
			link_soup = BeautifulSoup(link_html, features = "lxml")
			movie['link'] = link_soup.find_all('link')[1]['href']
		print(movie['url'])
		print(movie['name'])
		print(movie['storyline'])
		print(movie['link'])
		print('*'*30)
		return movie

	# 輸出 JSON 格式
	def write_json(self, movies):
		if not os.path.exists("Movie_Crawl_Result"):
			os.makedirs("Movie_Crawl_Result")
		with open("Movie_Crawl_Result/" + "movies_pixnet" + ".json" , 'wb') as f:
			f.write(json.dumps(movies, indent = 4, ensure_ascii = False).encode('utf-8'))

if __name__ == "__main__":
	crawler = Crawler()
	crawler.crawl()