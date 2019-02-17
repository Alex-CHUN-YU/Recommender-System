# -*- coding: utf-8 -*-
import json
import MySQLdb
import parsing
from hanziconv import HanziConv
import re
import time

# Article and parser result insert mysql
class Article():
	def __init__(self):
		# 連接 MySQL 資料庫
		self.db = MySQLdb.connect(host = "localhost", user = "root", passwd = "wmmkscsie", db = "recommender_system", charset = "utf8")
		self.cursor = self.db.cursor()
		self.sleep = 2

	def articles_parser_insert_mysql(self):#74218
		self.cursor.execute("SELECT id, title, content FROM articles where id >= 198886 and id <= 200000")
		sql = "INSERT INTO articles_parser (id, title_parser_result, content_parser_result) VALUES (%s, %s, %s)"
		results = self.cursor.fetchall()
		for record in results:
			index = record[0]
			title = record[1]
			content = record[2]
			print(index)
			print(title, end = "\n\n")
			print(content)
			if title != "":
				title_parser_result = parsing.Parser(re.sub(r"[\s+\.\【\】\‧\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+", "", title))
				if len(title_parser_result) != 0:
					if title_parser_result[0] == "error":
						title = HanziConv.toTraditional(title)
						title_parser_result = parsing.Parser(re.sub(r"[\s+\.\【\】\‧\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+", "", title))
				else:
					continue
			else:	
				continue
			content = re.sub(r'\、|\，|\。|\?|\？|\;|\；|\:|\~|\：|\⋯|\!', '\n', content)
			content_parser_result = ""
			for line in content.split("\n"):
				line = re.sub(r"[\s+\.\【\】\‧\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+", "", line)
				if len(line) >= 4 and '★' not in line and '◆' not in line:
					print(line)
					parser_result = parsing.Parser(line)
				else:
					continue
				if line == "" or len(parser_result) is not 1 or parser_result[0] == 'error':
					continue
				content_parser_result += parser_result[0]
				content_parser_result += "@"
			time.sleep(self.sleep)
			val = (index, title_parser_result[0], content_parser_result)
			print(title_parser_result[0], end = "\n\n")
			print(content_parser_result)
			self.cursor.execute(sql, val)
			self.db.commit()
		self.db.close()
		
if __name__ == '__main__':
	article_mysql = Article()
	article_mysql.articles_parser_insert_mysql()
