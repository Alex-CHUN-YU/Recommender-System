



with open("stopwords.txt", 'r', encoding = 'UTF-8') as fp:
	entitys = fp.readlines()
	entitys = [entity.strip('\n') for entity in entitys]
	print(entitys)
	entitys = list(set(entitys))
	print(entitys)
with open("stopwords.txt", "w", encoding = 'UTF-8') as file:
	for entity in entitys:
		file.write(entity)
		file.write('\n')