# -*- coding: utf-8 -*-
__author__ = "ALEX-CHUN-YU (P76064538@mail.ncku.edu.tw)"
import warnings
warnings.filterwarnings(action = 'ignore', category = UserWarning, module = 'gensim')
from gensim.models import word2vec
import codecs
from gensim.models.keyedvectors import KeyedVectors
from scipy.spatial import distance
import multiprocessing

# 主要透過 gensim 訓練成 model 並供使用
class Word2Vec(object):
	def __init__(self):
		self.sg = 1 # 1 for skip-gram; otherwise CBOW.
		self.size = 150 # default
		self.window = 6
		self.min_count = 1
		self.sample = 1e-3 # 越高會越受到高頻詞影響越重
		self.workers = multiprocessing.cpu_count()
		self.input_file = None
		self.output_file = None
		self.word_vectors = None

	def hyperparameter(self, dimension = 150, window = 6, min_count = 1, sample = 1e-3):
		self.size = dimension
		self.window = window
		self.min_count = min_count
		self.sample = sample

	def train_file_setting(self, input_file = None, output_file = None):
		self.input_file = input_file
		self.output_file = output_file

	def write_file(self, train_data = None, append = False):
		mode = "a" if append == True else "w"
		with codecs.open(self.input_file, mode = mode, encoding = 'utf8') as f:
			f.write(train_data)
			f.close()

	# 可參考 https://radimrehurek.com/gensim/models/word2vec.html 更多運用
	def train(self):
		print("訓練中...(喝個咖啡吧^0^)")
		# Load file
		sentence = word2vec.Text8Corpus(self.input_file)
		# Setting degree and Produce Model(Train)
		model = word2vec.Word2Vec(sentence, size = self.size , window = self.window, min_count = self.min_count, workers = self.workers, sg = self.sg, sample = self.sample)
		# Save model 
		model.wv.save_word2vec_format(self.output_file + "_" + str(self.size) + u".model.bin", binary = True)
		print("model 已儲存完畢")

	def load_model(self):
		self.word_vectors = KeyedVectors.load_word2vec_format(self.output_file + "_" + str(self.size) + u".model.bin", binary = True)

	def term_ranking_in_corpus(self, term, number):
		return self.word_vectors.most_similar(term, topn = number)

	def term_to_vector(self, term):
		return self.word_vectors[term]

	def terms_similarity(self, term1, term2):
		return self.word_vectors.similarity(term1, term2)

	def vectors_similarity(self, vec1, vec2):
		return distance.cosine(vec1, vec2)

if __name__ == "__main__":
	# 產生一個 word2vec 物件
	t = Word2Vec()
	# 設定訓練檔案名與輸出模型檔案名
	t.train_file_setting("segmentation.txt", "result")
	# 餵資料給訓練模型，argument: 資料是否要延伸下去
	t.write_file("cat say meow dog say woof", append = True)
	# 訓練(shallow semantic space)
	t.train()
	# 載入模型
	t.load_model()
	# 找出詞彙在語料庫中相似詞彙排名
	print(t.term_ranking_in_corpus("cat", 5))
	# 產生詞彙向量
	print(t.term_to_vector("cat"))
	# 詞彙計算相似度
	print(t.terms_similarity("cat", "dog"))
	# 向量計算相似度
	print(1 - t.vectors_similarity(t.term_to_vector("cat"), t.term_to_vector("dog")))
