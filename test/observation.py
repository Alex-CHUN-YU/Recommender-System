import MySQLdb

db = MySQLdb.connect(host = "localhost", user = "root", passwd = "wmmkscsie", db = "recommender_system", charset = "utf8")
cursor = db.cursor()
while(True):
	id = input("enter the id:\n") 
	print(id)
	cursor.execute("SELECT a.storyline, a.relationship_type, a.scenario_type, b.emotion, b.event FROM movies as a, movies_ner as b Where a.id = b.id and a.id = '" + id + "'")
	entitys = cursor.fetchone()
	article = entitys[0]
	relationship_type = entitys[1]
	scenario_type = entitys[2]
	emotion = entitys[3]
	event = entitys[4]
	print("article:")
	print(article)
	print("relationship_type & scenario_type:" + relationship_type + "-" + scenario_type)
	print("emotion:")
	print(emotion)
	print("event:")
	print(event)