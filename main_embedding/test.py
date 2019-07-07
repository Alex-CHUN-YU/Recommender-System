# -*- coding: utf-8 -*-
# import re
# import jieba
# content = "為了不要透漏那】個人的身份\n我叫他為㊙️?靠邀★★"
# sentences = re.sub(r'\、|\，|★|\。|\?|\？|\;|\；|\:|\~|\：|\⋯', '\n', content)
# sentence_list = sentences.split("\n")
# print(sentence_list)
# for sentence in sentence_list:
# 	if sentence != '':
# 		print(sentence)
# 		seg_list = jieba.cut(sentence,  cut_all = False)
# 		for seg in seg_list:
# 			print(seg, end = ' ')

# result = []
# test = [[0.6, 0.3, 0.1], [0.4, 0.3, 0.3]]
# for t in test:
# 	if max(t) >= 0.5:
# 		print(t)
# 		result.append()
test = "這是一個aa測試ccc"
for t in test:
	print(t)