__author__ = "ALEX-CHUN-YU (P76064538@mail.ncku.edu.tw)"
from classification import Classification
from sklearn.model_selection import train_test_split
import sklearn.datasets as ds
import MySQLdb
import numpy as np

# 主要將資料進行分析，選擇出適合的演算法，以及儲存每個演算法 model 和使用到的參數(Parameter)與它的精確性
def main():
	data = []
	target = []
	db = MySQLdb.connect(host = "localhost", user = "root", passwd = "wmmkscsie", db = "recommender_system", charset = "utf8")
	cursor = db.cursor()
	cursor.execute("SELECT id, type FROM articles Where id >= 1 and id < 1000 and type !=''")
	articles = cursor.fetchall()
	for article in articles:
		# Access Articles Vector
		cursor.execute("SELECT id, relation_content_add_vec, relation_content_hadamard_vec FROM articles_vector Where id =" + str(article[0]))
		vectors = cursor.fetchall()
		exist = False
		for vector in vectors:
			add_vec = []
			hadamard_vec = []
			article_id = vector[0]
			relation_content_add_vec = vector[1]
			relation_content_hadamard_vec = vector[2]
			for s in relation_content_add_vec[1:-1].split(' '):
				try:
					if s != "":
						add_vec.append(float(s))
				except:
					pass
			for s in relation_content_hadamard_vec[1:-1].split(' '):
				try:
					if s != "":
						hadamard_vec.append(float(s))
				except:
					pass

			relation_content_add_vec = np.array(add_vec).astype(np.float32)
			relation_content_hadamard_vec = np.array(hadamard_vec).astype(np.float32)
			# print(relation_content_add_vec)
			# print(relation_content_hadamard_vec)
			# print(relation_content_concatenate_vec)
			# print(1 - t.vectors_similarity(relation_content_add_vec, relation_content_hadamard_vec))
			data.append(relation_content_add_vec)
			exist = True
		if exist:
			# Label
			if article[1] == '1':
				target.append(0)
			elif article[1] == '2':
				target.append(1)
			elif article[1] == '3':
				target.append(2)
			elif article[1] == '4':
				target.append(3)
			elif article[1] == '5':
				target.append(4)
			elif article[1] == '6':
				target.append(5)
			elif article[1] == '7':
				target.append(6)
	data = np.array(data)
	target = np.array(target).astype(np.float32)
	# 如果是 4 筆資料，1 筆測試，3 筆訓練
	# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25)
	clf = Classification(data, target)
	# # 已有 Model 可以註解掉(model test data dimension and train data dimension must same!)
	clf.knn()
	# clf.svm()
	clf.nb()
	clf.mnb()
	# clf.rfc()
	# clf.find_best_estimator(X_test, y_test)

if __name__ == "__main__":
    main()
