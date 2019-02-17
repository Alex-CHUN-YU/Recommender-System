__author__ = "ALEX-CHUN-YU (P76064538@mail.ncku.edu.tw)"
import tensorflow as tf
import numpy as np
import matplotlib
# on the mac
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from tensorflow.examples.tutorials.mnist import input_data

class LSTM():
	# LSTM Initializer
	def __init__(self):
		# Hyperparameter
		self.sess = None
		self.input_size = 28
		self.time_step = 28
		self.n_hidden = 128
		self.n_class = 10
		self.xs = None
		self.ys = None
		self.weights = None
		self.biases = None
		self.prediction = None
		self.learning_rate = 1e-4
		self.optimizer = None
		self.train_epoch = 10000
		self.batch_size = 256
		# Save or Restore
		self.saver = None
		self.model_path = "rnn_net/"

	# RNN Neural Structure
	def neural_structure(self):  
		# Resets the global default graph
		tf.reset_default_graph()
		# If you have GPU, it will be used
		config = tf.ConfigProto(log_device_placement = False)
		# config.gpu_options.per_process_gpu_memory_fraction = 0.85
		config.gpu_options.allow_growth = True
		# Create Session
		self.sess = tf.Session(config = config)
		self.xs = tf.placeholder(dtype = tf.float32, shape = [None, self.time_step, self.input_size])
		self.ys = tf.placeholder(dtype = tf.float32, shape = [None, self.n_class])
		self.weights = {
		'in': tf.Variable(tf.random_normal([self.input_size, self.n_hidden])),
		'out': tf.Variable(tf.random_normal([self.n_hidden, self.n_class])) 
		}
		self.biases = {
		'in': tf.Variable(tf.constant(0.1, shape = [self.n_hidden])),
		'out': tf.Variable(tf.constant(0.1, shape = [self.n_class]))
		}
		# LSTM Structure
		# Hidden Layer For Input
		# --> 128 batchs * 28 time_step, 28 inputs 
		xs = tf.reshape(self.xs, [-1, self.input_size])
		# --> 128 batchs * 28 time_step, 128 hidden 
		xs = tf.matmul(xs, self.weights['in']) + self.biases['in']
		# --> 128 batchs, 28 time_step, 128 hidden 
		xs = tf.reshape(xs, [-1,  self.time_step, self.n_hidden])
		# Cell
		rnn_cell = tf.contrib.rnn.BasicLSTMCell(self.n_hidden, forget_bias = 1.0, state_is_tuple = True)
		outputs, (h_c, h_n) = tf.nn.dynamic_rnn(
		rnn_cell,                   # cell you have chosen
	 	xs,                      # input
		initial_state = None,         # the initial hidden state
		dtype = tf.float32,           # must given if set initial_state = None
		time_major = False,           # False: (batch, time step, input); True: (time step, batch, input))
		)
		# outputs, final_state = tf.nn.dynamic_rnn(lstm_cell, xs, initial_state = init_state, time_major = False)
		# Hidden Layer For Output
		self.prediction = tf.layers.dense(outputs[:, -1, :], self.n_class)
		cross_entropy = tf.losses.softmax_cross_entropy(onehot_labels = self.ys, logits = self.prediction) 
		self.optimizer = tf.train.AdamOptimizer(self.learning_rate).minimize(cross_entropy)
		self.saver = tf.train.Saver()

	def train(self, train_X, train_y, test_X, test_y, hyperparameter = 'test'):
		# Goal: Draw Picture
		epoch_range = []
		train_scores = []
		test_scores = []
		best_result = False
		# Epoch about Max Accuracy and Best Epoch
		max_accuracy = 0
		best_epoch = 0
		# TF structure initialize
		self.neural_structure()
		self.sess.run(tf.global_variables_initializer())
		for epoch in range(self.train_epoch):
			batch_xs, batch_ys = self.next_batch(num = self.batch_size, data = train_X, labels = train_y)
			# print(batch_xs.shape)
			batch_xs = batch_xs.reshape([self.batch_size, self.time_step, self.input_size])
			# print(batch_xs.shape)
			self.sess.run(self.optimizer, feed_dict = {self.xs: batch_xs, self.ys: batch_ys})
			if epoch % 1000 == 0:
				batch_xs, batch_ys = self.next_batch(num = self.batch_size, data = train_X, labels = train_y)
				batch_xs = batch_xs.reshape([self.batch_size, self.time_step, self.input_size])
				train_accuracy = self.compute_accuracy(batch_xs, batch_ys)
				batch_xs, batch_ys = self.next_batch(num = self.batch_size, data = test_X, labels = test_y)
				batch_xs = batch_xs.reshape([self.batch_size, self.time_step, self.input_size])
				test_accuracy = self.compute_accuracy(batch_xs, batch_ys)
				epoch_range.append(epoch)
				train_scores.append(train_accuracy)
				test_scores.append(test_accuracy)
				print(test_accuracy)
				if test_accuracy > max_accuracy:
					max_accuracy = test_accuracy
					best_epoch = epoch
					# Save model weights to disk
					best_result = True
					save_path = self.saver.save(self.sess, self.model_path + hyperparameter + "/rnn.ckpt")
					print("Model saved in file: %s" % save_path)
		if best_result:
			# Draw the Picture
			plt.title("Accuracy with RNN Model")
			plt.xlabel("epoch")
			plt.ylabel("accuracy")
			plt.plot(epoch_range, train_scores, "-o", color = "y", label = "Training Score")
			plt.plot(epoch_range, test_scores, "-o", color = "b", label = "Testing Score")
			plt.legend(loc = "best")
			plt.savefig(self.model_path + hyperparameter + "/rnn.png")
			print("rnn.png is saved")
			plt.close()

	# Test
	def test(self, test_X, test_y, hyperparameter = "test"):
		self.batch_size = len(test_X)
		self.neural_structure()
		self.sess.run(tf.global_variables_initializer())
		self.saver.restore(self.sess, self.model_path + hyperparameter + "/rnn.ckpt")
		# batch_xs, batch_ys = self.next_batch(num = self.batch_size, data = test_X, labels = test_y)
		batch_xs = test_X.reshape([self.batch_size, self.time_step, self.input_size])
		print(self.compute_accuracy(batch_xs, test_y))
		self.sess.close()

	# Prediction
	def predict(self, test_X, hyperparameter = 'test'):
		self.batch_size = len(test_X)
		self.neural_structure()
		self.sess.run(tf.global_variables_initializer())
		self.saver.restore(self.sess, self.model_path + hyperparameter + "/rnn.ckpt")
		test_X = test_X.reshape([self.batch_size, self.time_step, self.input_size])
		y_pre = self.sess.run(self.prediction, feed_dict = {self.xs: test_X})
		result = self.sess.run(tf.argmax(y_pre, 1))
		self.sess.close()
		return result

	# 計算 accuracy 
	def compute_accuracy(self, v_xs, v_ys):
		# global prediction
		y_pre = self.sess.run(self.prediction, feed_dict = {self.xs: v_xs})
		# print(y_pre)
		# print(self.sess.run(tf.argmax(y_pre, 1)))
		correct_prediction = tf.equal(tf.argmax(y_pre, 1), tf.argmax(v_ys, 1))
		accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
		result = self.sess.run(accuracy, feed_dict = {self.xs:v_xs, self.ys:v_ys})
		# result = None
		return result

	# Data 隨機抽取, Return a total of `num` random samples and labels.
	def next_batch(self, num = 256, data = None, labels = None):
		idx = np.arange(0 , len(data))
		np.random.shuffle(idx)
		idx = idx[:num]
		data_shuffle = [data[i] for i in idx]
		labels_shuffle = [labels[i] for i in idx]
		return np.asarray(data_shuffle), np.asarray(labels_shuffle)

if __name__ == '__main__':
	lstm = LSTM()
	mnist = input_data.read_data_sets('MNIST_data', one_hot = 'True')
	x_train = mnist.train.images
	y_train = mnist.train.labels
	x_test = mnist.test.images
	y_test = mnist.test.labels
	lstm.train(x_train, y_train, x_test, y_test)
	lstm.test(x_test, y_test)
	print(lstm.predict(x_test[:1]))
	


