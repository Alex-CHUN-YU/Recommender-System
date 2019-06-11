import re
import jieba
content = "為了不要透漏那】個人的身份\n我叫他為㊙️?靠邀★★"
sentences = re.sub(r'\、|\，|★|\。|\?|\？|\;|\；|\:|\~|\：|\⋯', '\n', content)
sentence_list = sentences.split("\n")
print(sentence_list)
for sentence in sentence_list:
	if sentence != '':
		print(sentence)
		seg_list = jieba.cut(sentence,  cut_all = False)
		for seg in seg_list:
			print(seg, end = ' ')