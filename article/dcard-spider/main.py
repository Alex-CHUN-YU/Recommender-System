# -*- coding: utf-8 -*-
# Crawl mood board Data title and content
from dcard import Dcard
import os
import json

def main():
	dcard = Dcard()
	forums = dcard.forums.get()
	# forums = dcard.forums.get(no_school=True)
	# ariticle_metas = dcard.forums('mood').get_metas(num=20, sort='popular')
	ariticle_metas = dcard.forums('mood').get_metas(num=1000000, sort='new')
	# article length
	print(len(ariticle_metas))
	ids = [meta['id'] for meta in ariticle_metas]
	articles = dcard.posts(ids).get(comments=False, links=False)
	data = {}
	index = 0
	for article in articles.results:
		try:
			res = []
			data['title'] = article['title']
			data['content'] = article['content']
			res.append(data)
			ouput_board_page_articles_json(data['title'], res, index)
			print(str(index) + " page finish!")
			index+= 1
		except:
			print("this article no exist!")

# 輸出 JSON 格式
def ouput_board_page_articles_json(filename = None, res = None, start_page= None):
	if not os.path.exists("Dcard_Crawl_Result"):
		os.makedirs("Dcard_Crawl_Result")
	with open("Dcard_Crawl_Result/" + str(start_page) + "_" + remove_punctuation(filename) + ".json" , 'wb') as f:
		f.write(json.dumps(res, indent = 4, ensure_ascii = False).encode('utf-8'))

import re
# 只取中文英文與數字
def remove_punctuation(line):
	rule = re.compile(r"[^a-zA-Z0-9\u4e00-\u9fa5]")
	line = rule.sub('',line)
	return line

if __name__ == '__main__':
	main()