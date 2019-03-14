__author__ = "ALEX-CHUN-YU (P76064538@mail.ncku.edu.tw)"
import tensorflow as tf
import numpy as np
import matplotlib
# on the mac
# matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from tensorflow.examples.tutorials.mnist import input_data
from sklearn.model_selection import KFold
import json

class LSTM():
	# LSTM Initializer
	def __init__(self):
		# Hyperparameter
		self.sess = None
		self.input_size = 150
		self.time_step = 5
		self.n_hidden = 128
		self.n_class = 7
		self.xs = None
		self.ys = None
		self.weights = None
		self.biases = None
		self.prediction = None
		self.learning_rate = 1e-4
		self.optimizer = None
		self.train_epoch = 100000
		self.batch_size = 256
		# Cross Validation 最大平均正確率
		self.max_score = 0
		# self.val_accuracy = 0
		# Cross Validation 最大正確率
		self.max_accuracy = 0
		self.best_epoch = 0
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
			if epoch % 10000 == 0:
				batch_xs, batch_ys = self.next_batch(num = self.batch_size, data = train_X, labels = train_y)
				batch_xs = batch_xs.reshape([self.batch_size, self.time_step, self.input_size])
				train_accuracy = self.compute_accuracy(batch_xs, batch_ys)
				batch_xs, batch_ys = self.next_batch(num = self.batch_size, data = test_X, labels = test_y)
				batch_xs = batch_xs.reshape([self.batch_size, self.time_step, self.input_size])
				test_accuracy = self.compute_accuracy(batch_xs, batch_ys)
				epoch_range.append(epoch)
				train_scores.append(train_accuracy)
				test_scores.append(test_accuracy)
				if test_accuracy > max_accuracy:
					max_accuracy = test_accuracy
					best_epoch = epoch
					# Save model weights to disk
					if max_accuracy >= self.max_accuracy:
						best_result = True
						self.max_accuracy = max_accuracy
						self.best_epoch = best_epoch
						# Save model weights to disk
						save_path = self.saver.save(self.sess, self.model_path + hyperparameter + "/rnn.ckpt")
						print("Model saved in file: %s" % save_path)
				print(test_accuracy)
				print("Current Max accuracy:{0}, Current Best epoch:{1}".format(max_accuracy, best_epoch), end = "\n\n")
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
		print("\nFinal Max accuracy:{0}, Final Best epoch:{1}".format(self.max_accuracy, self.best_epoch))
		return max_accuracy

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

	# Cross Validation
	def cross_validation(self, data, target, n_split = 10):
		# 將不同 hyperparameter 每次 cross validation 平均 Accuracy 記錄下來(目前 lstm 只有一次)
		parameters_socre = []
		kf = KFold(n_splits = n_split)
		scores = []
		for train_index, test_index in kf.split(data):
			X_train, X_test = data[train_index], data[test_index]
			y_train, y_test = target[train_index], target[test_index]
			scores.append(self.train(X_train, y_train, X_test, y_test))
		average_score = np.mean(scores)
		print("Average:" + str(average_score))
		parameters_socre.append(average_score)
		self.max_score = average_score
		parameters = {}
		parameters['scoring'] = []
		parameters['scoring'].append({
			'average accuracy' : float(self.max_score),
			'max accuracy' : float(self.max_accuracy),
			'best epoch' : float(self.best_epoch)
			})
		with open('model/rnn_parameters', 'w', encoding = 'utf-8') as rnn:
			json.dump(parameters, rnn)
		print('RNN Save Parameters Finished')
		# Next train init(Cross Validation about Max Accuracy and Best Epoch)
		self.max_accuracy = 0
		self.best_epoch = 0
		print(parameters_socre)

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
	model = LSTM()
	X_test = np.array([[-2.066110805608332, 0.16115589439868927, -0.8212800249457359, 7.355080664157867, 9.313586361706257, 0.883366055553779, 6.991141228936613, -2.2308409749530256, -1.3047744808718562, -7.108685530722141, -1.2024109195917845, 6.555380880832672, -0.5627602450549603, -5.180419153533876, 0.5274344704230316, 4.247194541618228, -5.197871895506978, -1.237175827845931, 4.241049209609628, 3.1406697183847427, 0.5035639950074255, 1.6817689090967178, -7.45180681347847, 3.126457031816244, 3.5915335826575756, -9.678227704018354, 1.4218628755770624, 7.566162683069706, 3.2458093520253897, -3.8422005232423544, -3.356283213943243, -11.875780530273914, 6.592635054141283, 3.690986793488264, -6.072623967658728, -0.5265748184174299, 6.210876929573715, -3.5262628861237317, -4.939359355717897, -4.217223412822932, -12.06464770808816, -7.417452611029148, -2.8151860553771257, -2.463255364447832, 0.9488655244931579, 2.0972471833229065, 0.07497748360037804, 9.059335336089134, -1.269356465432793, 2.8366426760330796, -0.7607279606163502, -5.594993252307177, 10.486049368977547, -2.3894655955955386, 1.7127534877508879, 1.855499284574762, -2.2778221322223544, -4.163902197033167, -1.9953488856554031, 0.8825333677232265, -5.951648209244013, 0.27176723908632994, 1.353278107009828, -3.312895404174924, 0.00261036679148674, -8.193300642073154, 1.850490316748619, -2.564398480579257, -9.076481387019157, -3.1498620414640754, -3.944758715108037, 3.5526213217526674, -1.7255649091675878, 1.9109152611345053, -4.548103146145877, 2.2381230439059436, 2.3029133956879377, 2.8645118242129683, 6.299119411036372, -0.6312925415113568, -0.9389064232818782, -2.375913670286536, -4.646331590192858, -8.77202619984746, 3.09520710259676, -0.6554593443870544, 7.8337350487709045, -3.2521730340085924, -8.64602156355977, 6.859105922281742, 1.3730081748217344, -0.01938602328300476, 5.231854770332575, -9.71850349009037, 8.566046990454197, -7.628184090252034, 3.021138161420822, 9.87629371881485, -7.370002392679453, -4.719617136579473, 13.384277313947678, -5.6560634933412075, -10.55622497573495, 0.9211312211700715, 7.307594787329435, -0.6405862374231219, 5.65233389288187, 2.7332590892910957, -8.621868310961872, -1.4247712520882487, 12.216730996966362, -11.871873466297984, 3.977166708558798, -5.167338028550148, 1.8449608515948057, 1.2210508366115391, -1.2492095660418272, 1.2548218425363302, 5.1677048135316, -3.1401315443217754, -7.912353068590164, -4.129932567477226, 4.824684917926788, 9.184399716556072, -0.694231097586453, -2.3665229454636574, 5.252724005491473, 7.471400173380971, 0.8004886601120234, 3.275064706802368, -1.1984233539551497, 1.2957793108653277, -2.0097766146063805, -7.031285271048546, 8.040803417563438, -4.22169547341764, 12.477146476507187, 1.4345265924930573, 10.488350048661232, 1.7328325621783733, -12.81810461729765, -1.6819983564782888, -6.021992594003677, -5.478453643620014, 6.266745634377003, -7.144069686532021, -3.3898362796753645, -0.901844322681427, 1.0522630596533418, 1.4229730409570038, -1.3622867974918336, -1.7566761918715201, -0.7775809622835368, 5.409112347057089, 8.459109397605062, -1.0421071638702415, 2.415369793307036, -2.6276072841137648, -3.244689887855202, -6.406068034470081, 0.43607304408214986, 3.946493566967547, 1.2968847488518804, -1.250881565734744, -2.9850157076725736, 0.4237996246665716, -2.2478050589561462, -2.11603326338809, 0.30041580367833376, 0.12742933133267798, -1.8531031869351864, 0.7372045367956161, -1.9777050884440541, 2.6355860559269786, 2.9488389464095235, -5.291839499026537, 0.8065057042986155, 5.2197140753269196, 2.4962507225573063, -3.673188158776611, -3.182041609659791, -11.00412462465465, 6.586144924163818, 0.7927808412350714, -2.3961436464451253, -0.41050696559250355, 5.413942236453295, -3.1470601754263043, 0.6664996850304306, -4.888255646452308, -11.226139485836029, -2.610705205646809, -3.2844694573432207, -4.803120758384466, -1.3944403833302204, 6.083473160862923, 3.0916060061572352, 6.000555995851755, 4.676511040976038, -0.6585877165198326, -0.9755883268080652, -3.837522093206644, 7.4124216781929135, -4.313151413574815, 0.356202261056751, 2.8681854885071516, 0.08767313696444035, -2.733600841485895, -1.5783623596653342, 0.8027703128755093, -4.827803282998502, 0.9441597936674953, -0.0732387364259921, -0.6941389999119565, -1.221462706103921, -7.3489547111094, 3.8834445290267467, 0.16769123077392578, -6.914329591207206, -2.7971799727529287, 2.444386974675581, 0.45903875096701086, -2.2807575612096116, 2.5778212659060955, 0.2553887264803052, 0.1199934961841791, 0.13296812094631605, 4.2503963224589825, 5.28116776618117, 1.0391911696642637, 1.761561068939045, -2.7903470881283283, -4.674146605655551, -8.715219444944523, 2.60592063004151, -3.15032362844795, 8.326966300606728, -4.502989804372191, -3.3313056211918592, 4.429901668801904, -0.2328520230948925, 1.9217834908049554, 4.647498352918774, -8.774816360324621, 6.236015729606152, -6.485844768583775, 6.481980320066214, 7.307716980576515, -7.768629290163517, -3.646297875791788, 8.942306742072105, -6.194041540831677, -12.111823961138725, 0.47389703686349094, 8.287271559238434, 0.027343424037098885, 4.903520950116217, -0.446960482862778, -7.304315077140927, -2.126269797096029, 8.90249446593225, -7.396514328662306, 3.537413904443383, -8.149640936404467, -1.6993623896269128, 5.3228392312303185, -0.6333336047828197, 2.558341591968201, 2.6250321628176607, -1.253831862937659, -7.504875340498984, -2.413521676324308, 3.540472883731127, 4.826454630121589, 0.5283674655947834, -3.3068663366138935, 3.7459033601917326, 4.030286066234112, 1.0522729165386409, 4.2872846979880705, 1.3551377415424213, 2.5173666765913367, 0.1663997732102871, -3.1994992457330227, 5.0380625682882965, -1.3658358692191541, 10.827426016330719, 2.3478439030004665, 10.465065814554691, 2.151220729574561, -7.880378361791372, -4.276638119481504, -6.812701473012567, -4.387942299712449, 5.528798753395677, -5.181164860725403, -4.101220800541341, -2.9554961542598903, -0.6735558211803436, -3.1012318518478423, 0.4613134544342756, -1.0217744391411543, -1.1332262023352087, 4.714989019092172, 4.584322616457939, -1.299859999679029, 3.2993552633561194, -1.2760014825034887, -3.3137903612223454, -8.400650952011347, 2.5873046973720193, 5.90872510522604, -2.5127272363752127, -4.9474510829895735, -0.027258528396487236, 0.28195299953222275, -4.394729640334845, -0.63094323547557, -0.14223328232765198, 1.0244826152920723, -1.8839732831693254, 0.7800494146067649, -3.486956935375929, 2.4582354156300426, 2.0934998840093613, -6.661864381283522, 0.9247164037078619, 4.701536297798157, -0.5024042916484177, -3.8008312359452248, -2.6984294913709164, -10.608423235360533, 10.77097389230039, 2.336896028195042, -2.2927761938190088, -0.5603948291391134, 5.41568709211424, -7.19297587312758, -1.2455416703596711, -7.528297398239374, -9.709450609982014, -2.2941218498162925, -2.4056133590638638, -5.577835243195295, -3.451240688562393, 8.804942347109318, 0.41033406648784876, 7.70054067671299, 2.933702440932393, -0.29523202596465126, -1.284063845872879, -2.6755026979371905, 7.233851621858776, -2.9489388428628445, 1.2113225725479424, 1.4815757237374783, -0.22577004134655, -4.670327360741794, -1.7407872015610337, 2.0877276295796037, -5.8973917830735445, -1.2026252339128405, 1.0034352699294686, 0.21852132119238377, -1.3581159822642803, -6.694963403046131, 3.396074239164591, -0.7166257528588176, -3.429538344964385, -1.4860957637429237, 3.7870422780833906, -1.1247864094912075, -2.5774328077677637, 6.92059263214469, 2.329966662451625, -0.007602648343890905, 0.4304218194447458, 5.424539508298039, 4.370711257681251, 1.7706177309155464, 0.563650427851826, -4.253673784900457, -2.11350916326046, -8.991372741758823, 2.04699479136616, -5.963554989546537, 6.407083411235362, -2.844026267528534, -1.478282656520605, 3.037665940821171, -0.8178062224760652, 0.7287878780625761, 4.606010633055121, -11.361196875572205, 6.62005452811718, -3.989517719950527, 1.5475015183910728, 6.635305635631084, -5.8960674945265055, -3.0003331848420203, 10.251452416181564, -6.825238795019686, -8.809514552354813, -0.6862915772944689, 5.426880185957998, 2.2379916179925203, 7.7398531883955, 1.2278626407496631, -4.858941558748484, -0.8527997839264572, 10.491980209946632, -6.538483217358589, 2.0433748699724674, -7.074902940541506, 0.5198068635363597, 2.9550550831481814, -0.7177549321204424, 1.528885536827147, 2.941592833958566, -0.7723639812320471, -5.939199328422546, -3.6782302940264344, 6.008641377091408, 7.525129094719887, -0.24704481125809252, -2.036923013627529, 7.122870311141014, 4.066739859525114, 2.376695226877928, 3.2163343019783497, -0.34854072774760425, 3.449339509010315, 0.927513369359076, -4.634804844856262, 5.151644669473171, -2.2632339517585933, 8.636745177209377, -0.8766012415289879, 10.58003424713388, 2.746479067951441, -8.794460849836469, -2.9834252558648586, -4.187422346323729, -5.083394678775221, 5.347401097416878, -4.647329514846206, -2.9456684729084373, -5.515949439257383, 0.3587173279374838, -2.064152616309002, -0.02237321436405182, -1.0231781899929047, 0.022591400891542435, 0.7663705460727215, 2.2946889400482178, 0.027567874640226364, 0.7560110725462437, -0.1767941117286682, -0.48105698823928833, -0.5369076561182737, 0.2962241694331169, 0.7843970395624638, -0.07941846549510956, -1.5834220945835114, -0.12700189650058746, 1.1348189264535904, -0.3536022324115038, -0.7375196730718017, -0.590878427028656, -0.4773779958486557, -0.35154083697125316, -0.3705187663435936, -0.6775448173284531, 0.1366031914949417, 0.3918406367301941, -0.8881963565945625, 0.02498922497034073, 0.6709226844832301, 0.5886747390031815, 0.13851622119545937, -1.0554892122745514, -1.6507534980773926, 0.9110579937696457, 0.8487408757209778, -0.19375299662351608, -0.48130910098552704, 0.6187785267829895, 0.3090984523296356, 0.31550149619579315, -0.7951957285404205, -1.6292847394943237, -1.606433741748333, -0.7028935551643372, -0.5268277376890182, 0.16949550062417984, 0.6238332502543926, -0.5656673610210419, 1.163374975323677, -0.33300521969795227, 0.4531899355351925, 0.6174423918128014, -1.2220894694328308, 2.090583026409149, 0.33033744990825653, -0.622660681605339, 0.8420846462249756, -0.23904043436050415, -1.668164111673832, 0.01293976604938507, -0.06014237739145756, -0.9566419124603271, 0.4796907603740692, 0.4253878518939018, -0.18998099491000175, -0.5966575145721436, -1.0209780931472778, -0.0776431611739099, 0.043612141627818346, -1.222432078793645, 0.059869736433029175, 0.11381275951862335, 0.7855478674173355, -0.3338439092040062, -0.04314526543021202, 0.06641635624691844, 0.31880880519747734, 0.6319205239415169, 0.8672215491533279, 0.08889221027493477, -0.03558824211359024, 0.7259387895464897, -0.933734305202961, -0.7875963002443314, -0.5559269338846207, 1.05672818236053, -0.7479253336787224, 1.931088924407959, -2.09170401096344, -0.6273876056075096, 1.0050660073757172, 0.9341623794753104, 0.8833081126213074, 0.827135756611824, -1.2380013465881348, 2.0690156519412994, -0.26956881675869226, 2.1024726927280426, 1.6563076674938202, -2.049911320209503, -0.3532300293445587, 0.7390681132674217, -0.881852313876152, -1.9458013474941254, 0.5116352513432503, 0.5846329513005912, -0.845678212121129, 0.5019644647836685, -0.28568226657807827, -1.3299775123596191, 0.13351456820964813, 0.9976958483457565, -1.1326252035796642, 0.581440195441246, -2.215947240591049, -0.6550364978611469, 0.9486387968063354, -0.6312316879630089, -0.08989167213439941, 0.3526955097913742, 0.062254488468170166, -0.7923866659402847, 0.1047690361738205, 0.34445904940366745, 1.3821646347641945, 0.17229551076889038, -0.4698857753537595, 1.2308078110218048, 0.057523252442479134, 0.2804228598251939, 1.534933291375637, 0.41592239774763584, 0.0777411088347435, -1.052711844444275, -0.963726133108139, 1.26722913980484, -0.6228322684764862, 1.5780211985111237, 0.4774792566895485, 2.190441459417343, 1.6329608038067818, -1.182456135749817, -1.0119654089212418, -0.5745962113142014, -1.1535235047340393, 1.207232628017664, 0.023364678025245667, -0.8615301009267569, -0.337090440094471, -0.5499313233885914, -0.4198428988456726, -0.07478811591863632, -0.8354338556528091, -0.7992463856935501, 0.7605002149939537, 0.9896327555179596, 0.08777801832184196, 0.21013402612879872, 0.04984780587255955, -1.0010175108909607, -1.1539928913116455, 0.24474776908755302, -0.15811879187822342, -0.34097202122211456, -0.5026487708091736, -0.0017850399017333984, 0.03726679086685181, -0.49836988747119904, -0.5436718463897705, -0.13171638548374176, -0.2381463646888733, -0.2148088961839676, -0.004217715933918953, -1.055863544344902, 0.17784008383750916, 0.3633468672633171, -0.9661596491932869, -0.5670819878578186, 0.4346912354230881, -0.11198863387107849, -0.7100928872823715, -0.41908933967351913, -1.480366736650467, 1.7677760422229767, 0.7720776498317719, -0.3420986654236913, -0.10374898836016655, 0.8447530046105385, -0.6414093375205994, 0.3885188698768616, -1.2689768075942993, -2.0131545662879944, -0.14888936653733253, -0.49848319590091705, -0.6274251046124846, -0.433972992002964, 0.5170707553625107, -0.4740992709994316, 1.0385462790727615, 0.5381012000143528, 0.3948468565940857, 0.5837043039500713, 0.0688488781452179, 0.8898871410638094, -0.1843617558479309, -0.8211786821484566, 0.1371673196554184, -0.320256270468235, -0.48983401246368885, 0.12109804898500443, 1.0018230080604553, 0.12052507698535919, -0.28415926173329353, 0.06458622962236404, -0.5138764968141913, -0.9549810737371445, -1.3093583285808563, 0.5690342783927917, 0.281949020922184, -0.7436752766370773, 0.4288229439407587, 0.46042523346841335, 0.15991246327757835, -0.6204444503528066, 0.6380452178418636, 0.3217952996492386, -0.4583030752837658, 0.4492829516530037, 0.8567532151937485, 0.7335707135498524, -0.9531793966889381, -0.47532933205366135, 0.07036768645048141, -0.5449253767728806, -1.0676311999559402, -0.40469594299793243, -0.22891013324260712, 0.3361979308538139, 0.3390146642923355, 0.08820633962750435, -0.628567012026906, 1.0129808336496353, 0.591758769005537, 0.19915846083313227, -0.4818510264158249, 0.4808281138539314, -1.1318305432796478, 0.30035195499658585, 0.6268359571695328, -1.274775356054306, -0.9606710337102413, 0.7504455074667931, -0.5006858482956886, -1.2608012855052948, 0.04682363569736481, 0.8280471712350845, 0.12595904245972633, 1.1536374986171722, -0.06134992092847824, -0.2996862381696701, 0.09475208818912506, 1.1204302608966827, -0.5949244610965252, 0.28687557578086853, -1.0610337406396866, -0.6009781546890736, 0.682308591902256, 0.2991427779197693, -0.14735287800431252, 0.7295128256082535, -0.3475244492292404, -0.6077383607625961, -0.17784017627127469, 0.565036004409194, 0.10590744577348232, 0.02292618900537491, 0.1847716518677771, 0.21496532845776528, 0.16006054356694221, 0.5734389759600163, 0.0733613595366478, -0.09323807433247566, 0.3125750496983528, -0.5271374806761742, -0.5322702527046204, 1.2288738191127777, -0.6482347324490547, 1.8263351023197174, -0.3161086328327656, 0.85243359208107, -0.30992551520466805, -0.9132879376411438, -0.5217241551727057, -0.9503904618322849, -0.5832918882369995, 0.9081718772649765, -1.2898404598236084, -0.6885523796081543, -0.2546490617096424, -0.35693840961903334, 0.03823630511760712],
		[0.33450492937117815, -0.6536929830908775, -0.6560164093971252, 0.8703121393918991, 1.7896485328674316, -1.1579607464373112, 0.8238589689135551, -0.5300157996825874, -1.0445826100185513, -1.3582814037799835, 0.5807762891054153, 1.2275211960077286, -0.1740901106968522, -0.1639579888433218, 0.06760407239198685, 0.0665538227185607, -0.7280092425644398, -0.7399328947067261, -0.5046487711369991, -0.21168740838766098, 0.06100008450448513, 0.28357841074466705, -0.6092972680926323, 0.29347196966409683, -0.4598078802227974, -2.068903833627701, -0.9796636775135994, 0.9162738770246506, 1.4192296490073204, -0.4397946521639824, -0.8402365446090698, -1.488558828830719, 1.5146491825580597, 1.2984008640050888, -0.23145616799592972, -0.7000512853264809, 1.344981923699379, -0.6606523618102074, 1.2690928019583225, -1.9237837195396423, -3.2983900606632233, -0.23452409356832504, -0.8438811898231506, 1.197478260844946, -0.08241327106952667, 2.1008123606443405, -0.366106279194355, 1.5925399959087372, 0.5694187171757221, -0.2593386210501194, 0.10073967278003693, -1.2962083965539932, 1.3549837619066238, -1.6344999969005585, -0.1333350222557783, 0.3202465772628784, -0.7653435543179512, -0.2583387419581413, 0.06318517657928169, 0.31752099841833115, -0.5436697527766228, -0.27453256770968437, -0.5351800322532654, 0.4228320084512234, 0.3939066054299474, -2.1912307739257812, 1.076245634816587, 0.1868133693933487, -1.3830919489264488, 0.5222843158990145, -0.4539720742031932, 0.8121459037065506, -0.026133067905902863, 0.22364183515310287, -0.5948884794488549, 0.7056412347592413, 0.4650634787976742, 1.3146149814128876, -0.1157233938574791, -0.2714007034956012, 0.6120969206094742, -0.7356059923768044, -1.7370973527431488, -0.2879519898779108, -0.39136382937431335, -1.3929499089717865, 1.534731574356556, -2.130887560546398, -1.0134721025824547, 0.8634978830814362, 0.2979239150881767, 1.1313734240829945, -0.32807256653904915, -2.1301995366811752, 2.3191364854574203, -1.5002124160528183, 0.9195823334157467, 2.2111745476722717, -1.7232040021335706, 0.6932617165148258, 1.8305472433567047, -0.5990438312292099, -1.4820266119204462, -0.058664992451667786, 2.453404486179352, -0.09251303225755692, 0.8537569642066956, 0.5608238577842712, -1.9600147753953934, -0.08587039820849895, 1.4017063677310944, -0.9016023576259613, 0.7499665766954422, -1.5196576118469238, -1.0149523792788386, 1.449631541967392, 0.22450734674930573, 0.1505110440775752, 1.036516503605526, -0.05346441315487027, -1.2090369164943695, -1.8677562773227692, -0.13487428799271584, 0.7171706594526768, 0.4134133644402027, -0.1782414335757494, 0.6262491159141064, 1.3622219562530518, 0.3232424259185791, 0.9157937616109848, 1.2941980573814362, 0.28378673642873764, -1.696931540966034, -2.085102617740631, 1.1208148747682571, -1.9033069964498281, 1.165479987859726, 1.0494809299707413, 1.734537661075592, 0.1885854983702302, -0.966202437877655, -0.0718505991389975, -0.9384084455668926, -0.79993786662817, 1.9517553746700287, -1.3354970514774323, -1.0175452455878258, 0.6128004491329193, -0.32640399038791656, -1.0744186528027058, -1.217635948676616, -5.703218889422715, 0.7749398471787572, 1.8576182802207768, 10.874819593504071, -1.3913973327726126, 2.3729214929044247, -1.1553083937615156, -3.947796671593096, -7.467844936996698, 4.827623980119824, 4.200525190681219, -0.5446550850756466, 0.8644185949160601, 2.0124429035931826, 1.5090376790612936, -2.023827584576793, -1.393272414803505, -0.9678060128208017, -1.8071253634989262, -2.4271377688273787, -2.5871453462168574, -0.79162273183465, 3.7481898707337677, 1.659179880283773, -7.5444890931248665, -2.7503689136356115, 4.0074798204004765, 4.181593605258968, -0.25652822759002447, -0.4272065721452236, -5.933057303307578, 8.494590184418485, 2.911346822977066, -5.998671032488346, -1.3987827319651842, 4.721387739293277, -2.263312842696905, 4.22465642914176, -6.388332950882614, -7.1034316793084145, -1.6783803943544626, -1.5086398087441921, 2.034361381083727, -3.8295161197020207, 5.896589808166027, -1.0057803206145763, 3.541331097483635, 0.7278217934072018, -1.6023499127477407, -0.5417184941470623, -4.326843097805977, 5.228923828341067, 1.1729514356702566, -2.6629298562183976, 3.5632325038313866, 0.1678161493036896, -5.207248285412788, 2.0981042050989345, -1.126293231267482, -2.147978339344263, 3.4993449356406927, -1.2711206774692982, -0.7259177714586258, -1.5939812285359949, -7.444961037486792, 4.326150653883815, 0.38300828193314373, -4.882692217826843, 0.5621988759376109, 5.249989904463291, 2.911577582359314, -2.7488564867526293, 3.0572552513331175, -0.1472543142735958, 0.48451489210128784, 4.753136646933854, 2.626396559178829, 1.9522825004532933, 1.3825578354299068, -0.047525899950414896, -1.1549663986079395, -9.229904152452946, -3.732017781585455, 0.8120436089811847, -2.805741121992469, 6.925559367984533, -6.398871723562479, -5.36597615480423, 3.8987996191717684, -0.3128465712070465, 4.005209612194449, 0.9874495565891266, -7.8160604909062386, 4.76620352617465, -2.6620889641344547, 4.6355573842301965, 6.357405304908752, -9.957498744130135, -1.186335819773376, 9.832990992814302, -3.349500648211688, -9.1538697630167, -1.750039465725422, 6.334054231643677, -1.7623985698446631, 4.354496913962066, 1.1193121820688248, -5.874306283891201, -0.5860825246199965, 6.076604593545198, -5.633164444938302, 1.6870818808674812, -5.409230682998896, -4.200202986598015, 4.813703947234899, 1.1908929757773876, 7.077388729900122, 2.165287280222401, 1.024036714574322, -5.952560426667333, -7.1018828398082405, 0.9983610813505948, 3.443840879946947, 0.9172612132970244, -4.20610210718587, 0.6939122364856303, 6.159203248564154, 1.6912256027571857, 3.6422289945185184, 2.8297022823244333, -0.7893746979534626, -0.22600441612303257, -4.498730858787894, 4.142525929957628, -5.03685941407457, 9.136918641626835, 2.7641962121706456, 5.284365780651569, 0.602833328768611, -4.108134055510163, -0.2550935928011313, -8.180074710398912, -1.9491070751100779, 10.155785091221333, -2.6187226260080934, -4.721961829811335, 1.9101383984088898, -3.385631092824042, -1.2748128771781921, -0.052302610129117966, -0.693192258477211, 0.165610418189317, 3.685929451137781, 5.430708825588226, -0.6340840719640255, -0.1935313567519188, 2.0840655320789665, -1.8494710103841498, -6.500148266553879, 2.6977306096814573, 1.9032328352332115, -0.6119404947385192, 0.6287667034193873, 0.096970584243536, 1.325617560185492, -4.990774556994438, -1.3520981669425964, -1.2904670387506485, -3.386462604627013, -1.5541126802563667, -1.619484145194292, -2.2797184409573674, 0.2624647095799446, 0.10221615061163902, -5.487369932234287, -2.2039172500371933, 1.5458613261580467, 2.0306930877268314, -3.2670853435993195, 0.07836742326617241, -4.578297048807144, 6.796980142593384, -0.7186899520456791, -3.09060400351882, -2.3294034050777555, 3.531000602990389, -1.1684555986430496, 3.6955137364566326, -2.0186095191165805, -6.976761469617486, -0.5257948879152536, -2.2607222832739353, 2.3593321706866845, -0.8250623401254416, 5.023990586400032, -1.6761414539068937, -0.5301596131175756, 3.200537269935012, 0.21949469577521086, -0.009674444794654846, -3.0718725218903273, 4.045756250154227, 1.0949649140238762, -0.21830011904239655, 0.548020739108324, -0.458396608941257, -3.6406491082161665, 2.1534740570932627, 0.5715660157729872, -3.0999583187513053, 2.9084676182828844, -1.5035736607387662, 1.0508006568998098, -0.6834764704108238, -6.17900450527668, 0.3387509733438492, 0.025476891547441483, -1.440877835266292, 3.0374531131237745, 3.4414775408804417, 1.4411790743470192, 0.6206478103995323, 3.9519198834896088, -1.1629950068891048, -0.05250630248337984, 3.0445136008784175, 1.0080174580216408, 0.443067817017436, -1.561367653310299, 0.8302888600155711, 0.2864227965474129, -9.642177820205688, -0.9986444972455502, 1.7806331268511713, -3.5497411154210567, 2.2598811835050583, -4.926521105691791, -3.6539896838366985, 0.16795657202601433, 0.5257205367088318, -0.06587404664605856, -1.1415728107094765, -6.931670963764191, 2.0088180005550385, -3.8646450703963637, 2.636066857725382, 5.404421105980873, -7.422225579619408, 1.7889305017888546, 3.8464008420705795, -2.9722862718626857, -4.76807152479887, -3.178740030154586, 5.359947830438614, -0.9015211341902614, 4.204840764403343, 2.9297852674499154, -6.132800325751305, 0.16642095195129514, 4.352984800934792, -3.0502361729741096, 0.6757472647004761, -3.1193310134112835, -2.231557935476303, 3.8580150695052, -0.3641509674489498, 1.8886232040822506, 3.282147938385606, -0.5060120443813503, -5.287813551723957, -3.5635060779750347, 0.780216233804822, 4.242667265236378, 0.9334482904523611, -0.9144573025405407, 2.7055803686380386, 3.107417054474354, -1.1690182350575924, 1.818317231722176, 5.100033473223448, -1.173272605985403, -2.312708381563425, -4.456686746329069, 4.485179886221886, -3.6087033227086067, 5.6928820759058, 0.610473278502468, 4.278503127396107, -0.43517737835645676, -0.8662777375429869, -0.4240180738270283, -4.3182128965854645, -2.0498261358588934, 6.29375272244215, -2.4298496022820473, -4.604754813015461, 0.09469357877969742, -3.574358504265547, -2.2689624708145857, -0.12300215661525726, -0.8038528691977262, -0.7916112150996923, 1.1312234052456915, 3.7095394134521484, -0.8969735503196716, 1.0198033079504967, -0.2680364642292261, -0.19009236246347427, -1.0307624451816082, 1.9434937313199043, 1.9222115576267242, -0.25471553951501846, 0.47047345247119665, 0.8284863010048866, -0.41724663972854614, -1.1874780803918839, -1.6221209615468979, -0.5551628023386002, 0.03672904893755913, 0.05161705054342747, -0.08334150165319443, -0.21299175824970007, 0.9229146391153336, -0.5468975659459829, -2.0797503367066383, 0.446033189073205, 1.7624721825122833, 0.912761899176985, -0.5297277420759201, 0.28786100377328694, -1.6359117105603218, 2.21903408318758, 1.864206999540329, -1.5996438711881638, 0.5240643369033933, 1.1731948554515839, -0.9053554125130177, 1.5126923397183418, -2.317710801027715, -2.3635435551404953, -1.093770956620574, 0.062138402834534645, 0.3606219254434109, -0.8315789345651865, 1.7558938413858414, -1.7436741553246975, 1.756638154387474, 0.40139661356806755, -1.242635264992714, 0.09180627018213272, -1.7934488654136658, 1.3336860248818994, 0.4171573050552979, -0.22964861011132598, 1.6694653779268265, -1.0030872449278831, -2.3769304752349854, 1.2003230270929635, -0.9958367869257927, -1.2447200383176096, 1.1983884372748435, -0.025171742774546146, 0.6642971057444811, 0.46411067992448807, -2.040316343307495, 0.7630500122904778, 0.38701874017715454, -1.3539259005337954, -0.30285679548978806, -0.08939640130847692, 0.08809717744588852, -0.4507439322769642, 0.8434294611215591, -0.5145422592759132, -0.11502736434340477, 0.9709756318479776, 1.7355888485908508, 1.2342777326703072, 0.1707477536983788, -0.12206519115716219, -1.4711666256189346, -1.931718337815255, -1.7708115205168724, 0.36315537244081497, -1.2210586592555046, 2.36542309820652, -2.8317805975675583, -1.8387361094355583, 0.9034557491540909, 0.07594048231840134, 1.4888101341202855, 1.2135067069903016, -2.453768879175186, 2.4663488268852234, -1.6994526237249374, 1.5750536601990461, 3.0595312416553497, -3.177989214658737, -0.6955947875976562, 2.966718077659607, -1.4626542888581753, -3.1034676134586334, -1.2640923806466162, 2.6328278481960297, -1.111710015218705, 1.33661824837327, 0.03743536025285721, -1.7721422761678696, 0.7434481121599674, 1.9972405582666397, -1.6764303371310234, 1.2605595160275698, -2.922322243452072, -1.2345270439982414, 2.6226275116205215, -0.05337817966938019, 1.4267050698399544, 0.9000637494027615, 0.14079550467431545, -1.5818177871406078, -1.9139462485909462, 0.3382200598716736, 0.7538055554032326, 0.7036139033734798, -0.17676127329468727, 0.4868071631062776, 0.38761309906840324, 0.7782689618616132, 1.2999299094080925, 0.1869286485016346, -0.03435556683689356, -1.1492061503231525, -0.09796051681041718, 1.5531042665243149, -1.0376713769510388, 1.934093421092257, 2.4969714134931564, 2.8566537499427795, 0.9824632201343775, -2.0184580460190773, -0.09270814806222916, -1.7989778593182564, 0.48318529035896063, 1.7940110266208649, -1.305278591811657, -1.413164809346199, -0.14996101893484592, -0.40397655963897705, 0.06624373607337475, 0.17693008482456207, -0.03460787609219551, -0.5533201694488525, 0.2669876515865326, 0.5886672735214233, -0.19161023199558258, 0.03921634331345558, 0.036959465593099594, -0.23177827894687653, -0.2293352335691452, 0.3311308026313782, 0.2074737846851349, -0.2419663667678833, -0.0652032345533371, 0.2885884642601013, -0.0014448683941736817, -0.12570308148860931, -0.34307458996772766, -0.2581009864807129, -0.02490988001227379, -0.1410873532295227, 0.10136855393648148, -0.40754783153533936, 0.07179082185029984, -0.05896635726094246, -0.19606119394302368, 0.09514942765235901, 0.32177698612213135, 0.150193989276886, -0.4178846776485443, 0.3653261363506317, -0.16647757589817047, 0.6010639667510986, -0.11127233505249023, -0.2405129075050354, 0.34026244282722473, 0.44675132632255554, 0.0004452732973732054, -0.0123511403799057, -0.15652872622013092, -0.48216667771339417, -0.23763759434223175, 0.18541395664215088, 0.1130225658416748, -0.243548184633255, 0.02269386127591133, 0.10867871344089508, 0.03223419934511185, 0.09383480995893478, -0.40041419863700867, 0.016740119084715843, -0.363437294960022, -0.3569433093070984, -0.06124495714902878, -0.1479274183511734, 0.2488086074590683, 0.24818341434001923, -0.4108496904373169, -0.029197005555033684, 0.05089907720685005, -0.19225460290908813, -0.0037612521555274725, -0.7626669406890869, 0.0757230892777443, 0.0837029442191124, -0.7339184880256653, 0.12256681174039841, 0.18592189252376556, -0.11466500163078308, 0.6726919412612915, 0.3225133717060089, 0.11034230887889862, 0.3045516908168793, 0.2804548442363739, -0.2760155498981476, -0.05352504923939705, -0.2541753053665161, 0.2142874300479889, 0.30728453397750854, 0.3634836971759796, -0.054183319211006165, -0.2761833965778351, -0.02841806784272194, -0.2866213619709015, -0.1034747064113617, -0.24864442646503448, 0.15584316849708557, -0.2782966196537018, -0.4064479470252991, -0.23511725664138794, 0.30314573645591736, 0.46149390935897827, 0.028402799740433693, -0.3344908654689789, 0.3120556175708771, -0.12184760719537735, 0.42105570435523987, 0.6107463836669922, -0.3071797490119934, 0.4943375289440155, 0.46609681844711304, -0.22799134254455566, -0.5234137773513794, -0.23913133144378662, 0.5784447193145752, -0.04196364805102348, 0.30693426728248596, 0.14444772899150848, -0.844233512878418, 0.023292729631066322, 0.17494504153728485, -0.14968857169151306, -0.06102709099650383, -0.122182697057724, -0.03387349098920822, 0.12216059863567352, 0.7664976119995117, 0.34237679839134216, 0.16878056526184082, 0.14194735884666443, 0.08374553173780441, -0.21922674775123596, 0.42319875955581665, -0.5857028365135193, -0.1885833889245987, -0.2652585506439209, 0.20143991708755493, 0.18542718887329102, 0.4536927342414856, -0.3957229256629944, 0.21320533752441406, -0.2997978627681732, -0.37428799271583557, -0.05940720811486244, 0.22969910502433777, 0.4037386476993561, 0.3270714282989502, -0.008210795000195503, -0.07634427398443222, -0.07044419646263123, -0.29205313324928284, -0.3790713846683502, 0.05909197777509689, -0.06457304954528809, 0.4199115037918091, -0.3242582380771637, -0.331023246049881, -0.26972949504852295, -0.11752045154571533, -0.1484186053276062]]).astype(np.float32)
	print(X_test.shape)
	# Result:
	# y_test = np.array([[0, 1, 0, 0, 0, 0, 0]]).astype(np.float32) 代表愛情(2, index = 1)
	# y_test = np.array([[0, 0, 1, 0, 0, 0, 0]]).astype(np.float32) 代表友情(3, index = 2)			
	print(model.predict(X_test))
	


