# -*- coding: utf-8 -*
from word2vec import Word2Vec as w2v
import codecs
import matplotlib.pyplot as plt
import os

# 判斷是否有此資料夾, 沒有的話就建立它吧
def createFolder(directory):
	try:
		if not os.path.exists(directory):
			os.makedirs(directory)
	except OSError:
		print ('Error: Creating directory. ' +  directory)

thresholds = [0.8, 0.825, 0.85, 0.875, 0.9, 0.925, 0.95, 0.975]
# thresholds = [0.95]
# load entity2vec model
t = w2v()
t.train_file_setting("segmentation.txt", "result")
t.load_model()

# 判斷 character_object 與 event, time 和 location candidate 的 similarity > 0.5 在取出成正式辭典
# 1. 只跑 this word not in vocabulary 表示 character_object 不在 corpus 中
# 2. 只跑  not in storyline_event candidates! 表示 character_object 有在 corpus 中但 event_candidate 不在 storyline_event 中
# 3. 如果在加 this word not in vocabulary 表示 event_candidate 不在 corpus 中
# 用來將分數儲存起來
scores = []
experiment_base = []
storyline_event_candidate = []
with codecs.open('experiment_base.txt', 'r', encoding = 'utf-8') as experiment_file:
	for line in experiment_file.readlines():
		experiment_base.append(line.replace('\r\n', ''))
with codecs.open('dict_observation/storyline_event.txt', 'r', encoding = 'utf-8') as storyline_event_file:
	for line in storyline_event_file.readlines():
		storyline_event_candidate.append(line.replace('\r\n', ''))
for threshold in thresholds:
	# 將 event, time 和 location candidate 辭典詞彙取出
	event_candidates = []
	time_candidates = []
	location_candidates = []
	with codecs.open('dict_observation/event.txt', 'r', encoding = 'utf-8') as event_file:
		for line in event_file.readlines():
			event_candidates.append(line.replace('\r\n', ''))
	with codecs.open('dict_observation/time.txt', 'r', encoding = 'utf-8') as time_file:
		for line in time_file.readlines():
			time_candidates.append(line.replace('\r\n', ''))
	with codecs.open('dict_observation/location.txt', 'r', encoding = 'utf-8') as location_file:
		for line in location_file.readlines():
			location_candidates.append(line.replace('\r\n', ''))
	event = set()
	time = set()
	location = set()
	with codecs.open('ehownet/character_object.list', 'r', encoding = 'utf-8') as character_object_file:
		for character_object in character_object_file.readlines():
			character_object = character_object.replace('\r\n', '')
			print('#'*50)
			print(character_object)
			for event_candidate in event_candidates:
				print(event_candidate)
				try:
					# 用來判斷是否有與 storyline event candidates 中任何一個大於 threshold 詞彙
					flag = False
					if t.terms_similarity(character_object, event_candidate) >= threshold:
						for storyline_event in storyline_event_candidate:
							try:
								if t.terms_similarity(event_candidate, storyline_event) >= threshold:
									flag = True
									break
							except:
								print(storyline_event + " word(storyline_event) not in vocabulary!")
						if flag:
							event.add(event_candidate)
				except:
					print(character_object + "or" + event_candidate + " word(character_object or event_candidate) not in vocabulary!")
			# 增加效率用
			event_candidates = [event_candidate for event_candidate in event_candidates if event_candidate not in event]
			print('-'*50)
			for time_candidate in time_candidates:
				print(time_candidate)
				try:
					if t.terms_similarity(character_object, time_candidate) >= threshold:
						time.add(time_candidate)
				except:
					print(character_object + "or" + time_candidate + " word(character_object or time_candidate) not in vocabulary!")
			# 增加效率用
			time_candidates = [time_candidate for time_candidate in time_candidates if time_candidate not in time]
			print('-'*50)
			for location_candidate in location_candidates:
				print(location_candidate)
				try:
					if t.terms_similarity(character_object, location_candidate) >= threshold:
						location.add(location_candidate)
				except:
					print(character_object + "or" + location_candidate + " word(character_object or location_candidate) not in vocabulary!")
			# 增加效率用
			location_candidates = [location_candidate for location_candidate in location_candidates if location_candidate not in location]
			print('-'*50)
	count = 0
	for experiment in experiment_base:
		if experiment in event or experiment in time or experiment in location:
			count += 1
	scores.append(count/len(experiment_base))
	# 將正式辭典存起來
	with codecs.open('event.list', 'w', encoding='utf8') as event_file:
		event_file.write('\n'.join(event))

	with codecs.open('time.list', 'w', encoding='utf8') as time_file:
		time_file.write('\n'.join(time))

	with codecs.open('location.list', 'w', encoding='utf8') as location_file:
		location_file.write('\n'.join(location))

print(scores)
plt.title("Experiment of Knowledge Base Threshold")
plt.xlabel("The value of threshold")
plt.ylabel("score")	   
plt.plot(thresholds, scores, "-o", color = 'g', label = "basic knowledge")# 畫出平均數值	
plt.legend(loc = "best")
# save image
createFolder('./image/')
plt.savefig('image/knowledge_base_threshold_experiment.png')
plt.close()