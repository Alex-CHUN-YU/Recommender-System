



with open("business_relationship_betray_emotion_dic.txt", 'r', encoding = 'UTF-8') as fp:
	entitys = fp.readlines()
	entitys = [entity.strip('\n') for entity in entitys]
	print(entitys)
	entitys = list(set(entitys))
	print(entitys)
with open("business_relationship_betray_emotion_dic.txt", "w", encoding = 'UTF-8') as file:
	for entity in entitys:
		file.write(entity)
		file.write('\n')