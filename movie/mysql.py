# -*- coding: utf-8 -*-
import json
import MySQLdb
import parsing
from hanziconv import HanziConv
import re
import time

# Movie and parser result insert mysql
class Movie():
	def __init__(self):
		# 連接 MySQL 資料庫
		self.db = MySQLdb.connect(host = "localhost", user = "root", passwd = "wmmkscsie", db = "recommender_system", charset = "utf8")
		self.cursor = self.db.cursor()
		self.sleep = 1

	def movies_insert_mysql(self):
		# # 執行 MySQL 查詢指令
		# self.cursor.execute("SELECT * FROM movies Where 1")
		# # 取回所有查詢結果
		# results = self.cursor.fetchall()
		# # 輸出結果
		# for record in results:
		# 	col1 = record[0]
		# 	col2 = record[1]
		# 	col3 = record[2]
		# 	col4 = record[3]
		# 	col5 = record[4]
		# 	print("%s, %s, %s, %s, %s" % (col1, col2, col3, col4, col5))

		sql = "INSERT INTO movies (id, url, name, storyline, link) VALUES (%s, %s, %s, %s, %s)"# mysql syntatic
		count = 150 # mysql movies id
		for index in range(1, 359):
			movies = self.read_json("movies_yahoo_" + str(index))
			for movie in movies:
				print(movie['url'])
				print(movie['name'])
				print(movie['storyline'])
				print(movie['link'])
				val = (str(count), movie['url'], movie['name'], movie['storyline'], movie['link'])
				self.cursor.execute(sql, val)
				self.db.commit()
				print(self.cursor.rowcount, "record inserted.")
				print('*'*30)
				count += 1
		# 關閉連線
		self.db.close()

	def movies_parser_insert_mysql(self):
		self.cursor.execute("SELECT id, storyline FROM movies Where id >= 823")
		sql = "INSERT INTO movies_parser (id, storyline_parser_result) VALUES (%s, %s)"
		results = self.cursor.fetchall()
		for record in results:
			movie_id = record[0]
			movie_storyline = record[1]
			print(movie_id)
			print(movie_storyline)
			movie_storyline = re.sub(r'\、|\，|\。|\?|\？|\;|\；|\:|\~|\：|\⋯|\!', '\n', movie_storyline)
			storyline_parser_result = ""
			for line in movie_storyline.split("\n"):
				line = re.sub(r"[\s+\.\【\】\‧\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+", "", line)
				if len(line) >= 4 and '★' not in line and '◆' not in line:
					print(line)
					parser_result = parsing.Parser(line)
				else:
					continue
				if line == "" or len(parser_result) is not 1 or parser_result[0] == 'error':
					continue
				storyline_parser_result += parser_result[0]
				storyline_parser_result += "@"
			time.sleep(self.sleep)
			val = (movie_id, storyline_parser_result)
			print(storyline_parser_result)
			self.cursor.execute(sql, val)
			self.db.commit()
		self.db.close()

	def read_json(self, name):
		with open("Movie_Crawl_Result/" + name + ".json", encoding='utf-8') as json_data:
			movies = json.load(json_data)
		return movies
		
if __name__ == '__main__':
	movie_mysql = Movie()
	# movie_mysql.movies_insert_mysql()
	movie_mysql.movies_parser_insert_mysql()
