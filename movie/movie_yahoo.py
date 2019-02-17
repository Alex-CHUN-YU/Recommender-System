
from urllib.request import urlopen, Request
# https://www.crummy.com/software/BeautifulSoup/bs4/doc/
from bs4 import BeautifulSoup
import os
import json
import time

# Crawl https://remylovedrama5.blogspot.com/ movie url, name, storyline, link 
class Crawler():
	def __init__(self):
		self.root = "https://movies.yahoo.com.tw/moviegenre_result.html?genre_id=05&page="
		self.headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6' }
		# self.proxies=["101.53.101.172:9999","101.53.101.172:9999","171.117.93.229:8118","119.251.60.37:21387","58.246.194.70:8080"]
		# 1, 359
		self.pages_range = range(263, 359)
		self.sleep_time = 4
		
	def crawl(self):
		movies = []
		for movies_url in self.get_movies_url():
			print(movies_url)
			time.sleep(self.sleep_time)
			for movie_url in self.get_movie_url(movies_url):
				movies.append(self.movie_parser(movie_url))
			self.write_json(movies, movies_url.split("page=")[1])
			movies = []

	# https://movies.yahoo.com.tw/moviegenre_result.html?genre_id=05
	def get_movies_url(self):
		for page in self.pages_range:
			yield self.root + str(page)

	# https://movies.yahoo.com.tw/movieinfo_main/%E6%88%91%E7%9A%84%E7%88%B8%E7%88%B8%E6%98%AF%E5%A3%9E%E8%9B%8B%E5%86%A0%E8%BB%8D-my-dad-is-a-heel-wrestler-8919
	def get_movie_url(self, movies_url):
		req = Request(movies_url, headers = self.headers)
		html = urlopen(req).read().decode('utf-8')
		soup = BeautifulSoup(html, features = "lxml")
		for link in soup.select(".release_foto"):
			yield link.select('a')[0]['href']

	def movie_parser(self, movie_url):
		movie = {}
		movie['link'] = ""
		movie['storyline'] = ""
		req = Request(movie_url, headers = self.headers)
		html = urlopen(req).read().decode('utf-8')
		soup = BeautifulSoup(html, features = "lxml")
		movie['url'] = movie_url
		movie['name'] = soup.select('h1')[0].text
		movie['storyline'] = soup.find("div", {"class": "gray_infobox_inner"}).find("span").text
		try:
			movie['link'] = soup.find('ul', {'class': 'trailer_list tlist'}).find("a")['href']
		except:
			print("no link")
		print(movie)
		return movie

	# 輸出 JSON 格式
	def write_json(self, movies, page):
		if not os.path.exists("Movie_Crawl_Result"):
			os.makedirs("Movie_Crawl_Result")
		with open("Movie_Crawl_Result/" + "movies_yahoo_" + page + ".json" , 'wb') as f:
			f.write(json.dumps(movies, indent = 4, ensure_ascii = False).encode('utf-8'))

if __name__ == "__main__":
	crawler = Crawler()
	crawler.crawl()