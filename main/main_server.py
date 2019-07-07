import socket
from sklearn import preprocessing
import numpy as np
import json
from sklearn.externals import joblib
import MySQLdb
from bert_embedding import BertEmbedding
import re
from scipy.spatial import distance
from cnn_e2v_bert import CNN_E2V_BERT
from cnn_e2v_w2v_sg import CNN_E2V_W2V_SG
from word2vec import Word2Vec
# 主要負責將判斷結果傳回去
class RecommenderSystem():
	def __init__(self):
		self.db = MySQLdb.connect(host = "localhost", user = "root", passwd = "wmmkscsie", db = "recommender_system", charset = "utf8")
		self.cursor = self.db.cursor()
		# sql = "SELECT a.relationship_type, a.scenario_type, b.id, b.scenario_e2v_bert FROM movies as a, movies_vector as b Where a.id=b.id and a.id >= 1 and a.id <= 1171 and b.scenario_e2v_bert !=''"
		sql = "SELECT a.relationship_type, a.scenario_type, b.id, b.scenario_e2v_w2v_sg FROM movies as a, movies_vector as b Where a.id=b.id and a.id >= 1 and a.id <= 1171 and b.scenario_e2v_w2v_sg !=''"
		print(sql)
		self.cursor.execute(sql)
		self.movies_information = self.cursor.fetchall()
		# Relationship Model
		#######################
		# self.model = CNN_E2V_BERT()
		# For Produce Vector
		# self.bert_embedding = BertEmbedding(model = 'bert_12_768_12', dataset_name='wiki_cn', max_seq_length = 50)
		# self.relationship_e2v_bert = []
		# self.scenario_e2v_bert = []
		#######################
		self.model = CNN_E2V_W2V_SG()
		# 產生一個 word2vec 物件
		self.t = Word2Vec()
		self.t.train_file_setting("segmentation.txt", "e2v_w2v_sg")
		self.t.load_model()
		self.dimension = self.t.size
		self.relationship_e2v_w2v_sg = []
		self.scenario_e2v_w2v_sg = []
	def main(self, content_ner_tag):
		self.w2v_vector_produce(content_ner_tag)
		print(self.relationship_e2v_w2v_sg.shape)
		print(self.scenario_e2v_w2v_sg.shape)
		relationship_type = self.relationship_model(self.relationship_e2v_w2v_sg)
		scenario_type = self.scenario_model(relationship_type, self.scenario_e2v_w2v_sg)
		candidates = self.relationship_scenario_based_trailer_recommendation(str(relationship_type), str(scenario_type), self.scenario_e2v_w2v_sg)
		return candidates

	def w2v_vector_produce(self, content_ner_tag):
		self.relationship_e2v_w2v_sg = []
		self.scenario_e2v_w2v_sg = []
		sentences_ner_tag = content_ner_tag
		po_vector = np.zeros(self.dimension)
		em_vector = np.zeros(self.dimension)
		ev_vector = np.zeros(self.dimension)
		lo_vector = np.zeros(self.dimension)
		ti_vector = np.zeros(self.dimension)
		po_count = 0
		em_count = 0
		ev_count = 0
		lo_count = 0
		ti_count = 0
		for sentence_ner_tag in sentences_ner_tag.split('@'):
			for term_ner_tag in sentence_ner_tag.split(' '):
				if " " not in term_ner_tag and term_ner_tag != "":
					term = term_ner_tag.split(':')[0]
					tag = term_ner_tag.split(':')[1]
					try:
						entity_vector = self.t.term_to_vector(term)
					except:
						continue;
					if tag == 'none':
						pass
					elif tag == 'po':
						po_vector += entity_vector
						po_count += 1
					elif tag == 'em':
						em_vector += entity_vector
						em_count += 1
					elif tag == 'ev':
						ev_vector += entity_vector
						ev_count += 1
					elif tag == 'lo':
						lo_vector += entity_vector
						lo_count += 1
					elif tag == 'ti':
						ti_vector += entity_vector
						ti_count += 1					
		if po_count == 0:
			po_count = 1
		if em_count == 0:
			em_count = 1
		if ev_count == 0:
			ev_count = 1
		if lo_count == 0:
			lo_count = 1
		if ti_count == 0:
			ti_count = 1
		self.relationship_e2v_w2v_sg = np.append(self.relationship_e2v_w2v_sg, po_vector/po_count)
		self.relationship_e2v_w2v_sg = np.append(self.relationship_e2v_w2v_sg, em_vector/em_count)
		self.relationship_e2v_w2v_sg = np.append(self.relationship_e2v_w2v_sg, ev_vector/ev_count)
		self.relationship_e2v_w2v_sg = np.append(self.relationship_e2v_w2v_sg, lo_vector/lo_count)
		self.relationship_e2v_w2v_sg = np.append(self.relationship_e2v_w2v_sg, ti_vector/ti_count)
		self.scenario_e2v_w2v_sg = np.append(self.scenario_e2v_w2v_sg, em_vector/em_count)
		self.scenario_e2v_w2v_sg = np.append(self.scenario_e2v_w2v_sg, ev_vector/ev_count)
		self.relationship_e2v_w2v_sg = np.array([self.relationship_e2v_w2v_sg]).astype(np.float32)
		self.scenario_e2v_w2v_sg = np.array([self.scenario_e2v_w2v_sg]).astype(np.float32)

	def bert_vector_produce(self, content_ner_tag):
		sentences_ner_tag = content_ner_tag
		dimension = 768
		self.relationship_e2v_bert = []
		self.scenario_e2v_bert = []
		sentences = []
		entity_type_position_length_in_sentences = []
		for sentence_ner_tag in sentences_ner_tag.split('@'):
			if sentences_ner_tag != "":
				sentence = ""
				entity_type_position_length_in_sentence = []
				for term_ner_tag in sentence_ner_tag.split(' '):
					if " " not in term_ner_tag and term_ner_tag != "":
						term_ner_tag = term_ner_tag.split(':')
						term = term_ner_tag[0]
						tag = term_ner_tag[1]
						position = int(term_ner_tag[2])
						length = int(term_ner_tag[3])
						entity_type_position_length_in_sentence.append([term, tag, position, length])
						sentence += term
				sentences.append(sentence)
				# print(len(entity_type_position_length_in_sentence))
				entity_type_position_length_in_sentences.append(entity_type_position_length_in_sentence)
		print(sentences)
		print(entity_type_position_length_in_sentences)
		results = self.bert_embedding(sentences)
		print("文章長度:", end = "")
		print(len(results))
		po_vector = np.zeros(dimension)
		em_vector = np.zeros(dimension)
		ev_vector = np.zeros(dimension)
		lo_vector = np.zeros(dimension)
		ti_vector = np.zeros(dimension)
		po_count = 0
		em_count = 0
		ev_count = 0
		lo_count = 0
		ti_count = 0
		for i, result in enumerate(results):
			print(sentences[i])
			print(entity_type_position_length_in_sentences[i])
			print(result[0])
			for i, entity in enumerate(entity_type_position_length_in_sentences[i]): 
				entity_vector = np.zeros(dimension)
				try:
					for i in range(entity[3]):
						entity_vector += result[1][entity[2] + 1 + i]
				except:
					print("some illegal characters")
					break
				if entity[1] == 'none':
					pass
				elif entity[1] == 'po':
					po_vector += entity_vector
					po_count += 1
				elif entity[1] == 'em':
					em_vector += entity_vector
					em_count += 1
				elif entity[1] == 'ev':
					ev_vector += entity_vector
					ev_count += 1
				elif entity[1] == 'lo':
					lo_vector += entity_vector
					lo_count += 1
				elif entity[1] == 'ti':
					ti_vector += entity_vector
					ti_count += 1
			print(po_vector[:5])
			print(em_vector[:5])
			print(ev_vector[:5])
			print(lo_vector[:5])
			print(ti_vector[:5])
		# print(po_count)
		# print(em_count)
		# print(ev_count)
		# print(lo_count)
		# print(ti_count)
		if po_count == 0:
			po_count = 1
		if em_count == 0:
			em_count = 1
		if ev_count == 0:
			ev_count = 1
		if lo_count == 0:
			lo_count = 1
		if ti_count == 0:
			ti_count = 1
		self.relationship_e2v_bert = np.append(self.relationship_e2v_bert, po_vector/po_count)
		self.relationship_e2v_bert = np.append(self.relationship_e2v_bert, em_vector/em_count)
		self.relationship_e2v_bert = np.append(self.relationship_e2v_bert, ev_vector/ev_count)
		self.relationship_e2v_bert = np.append(self.relationship_e2v_bert, lo_vector/lo_count)
		self.relationship_e2v_bert = np.append(self.relationship_e2v_bert, ti_vector/ti_count)
		self.scenario_e2v_bert = np.append(self.scenario_e2v_bert, em_vector/em_count)
		self.scenario_e2v_bert = np.append(self.scenario_e2v_bert, ev_vector/ev_count)

	def relationship_model(self, vector):
		# relationship_entity_add_concatenate_vec
		print('='*10 + "Relationship Model")
		# vector = np.array([[-2.066110805608332, 0.16115589439868927, -0.8212800249457359, 7.355080664157867, 9.313586361706257, 0.883366055553779, 6.991141228936613, -2.2308409749530256, -1.3047744808718562, -7.108685530722141, -1.2024109195917845, 6.555380880832672, -0.5627602450549603, -5.180419153533876, 0.5274344704230316, 4.247194541618228, -5.197871895506978, -1.237175827845931, 4.241049209609628, 3.1406697183847427, 0.5035639950074255, 1.6817689090967178, -7.45180681347847, 3.126457031816244, 3.5915335826575756, -9.678227704018354, 1.4218628755770624, 7.566162683069706, 3.2458093520253897, -3.8422005232423544, -3.356283213943243, -11.875780530273914, 6.592635054141283, 3.690986793488264, -6.072623967658728, -0.5265748184174299, 6.210876929573715, -3.5262628861237317, -4.939359355717897, -4.217223412822932, -12.06464770808816, -7.417452611029148, -2.8151860553771257, -2.463255364447832, 0.9488655244931579, 2.0972471833229065, 0.07497748360037804, 9.059335336089134, -1.269356465432793, 2.8366426760330796, -0.7607279606163502, -5.594993252307177, 10.486049368977547, -2.3894655955955386, 1.7127534877508879, 1.855499284574762, -2.2778221322223544, -4.163902197033167, -1.9953488856554031, 0.8825333677232265, -5.951648209244013, 0.27176723908632994, 1.353278107009828, -3.312895404174924, 0.00261036679148674, -8.193300642073154, 1.850490316748619, -2.564398480579257, -9.076481387019157, -3.1498620414640754, -3.944758715108037, 3.5526213217526674, -1.7255649091675878, 1.9109152611345053, -4.548103146145877, 2.2381230439059436, 2.3029133956879377, 2.8645118242129683, 6.299119411036372, -0.6312925415113568, -0.9389064232818782, -2.375913670286536, -4.646331590192858, -8.77202619984746, 3.09520710259676, -0.6554593443870544, 7.8337350487709045, -3.2521730340085924, -8.64602156355977, 6.859105922281742, 1.3730081748217344, -0.01938602328300476, 5.231854770332575, -9.71850349009037, 8.566046990454197, -7.628184090252034, 3.021138161420822, 9.87629371881485, -7.370002392679453, -4.719617136579473, 13.384277313947678, -5.6560634933412075, -10.55622497573495, 0.9211312211700715, 7.307594787329435, -0.6405862374231219, 5.65233389288187, 2.7332590892910957, -8.621868310961872, -1.4247712520882487, 12.216730996966362, -11.871873466297984, 3.977166708558798, -5.167338028550148, 1.8449608515948057, 1.2210508366115391, -1.2492095660418272, 1.2548218425363302, 5.1677048135316, -3.1401315443217754, -7.912353068590164, -4.129932567477226, 4.824684917926788, 9.184399716556072, -0.694231097586453, -2.3665229454636574, 5.252724005491473, 7.471400173380971, 0.8004886601120234, 3.275064706802368, -1.1984233539551497, 1.2957793108653277, -2.0097766146063805, -7.031285271048546, 8.040803417563438, -4.22169547341764, 12.477146476507187, 1.4345265924930573, 10.488350048661232, 1.7328325621783733, -12.81810461729765, -1.6819983564782888, -6.021992594003677, -5.478453643620014, 6.266745634377003, -7.144069686532021, -3.3898362796753645, -0.901844322681427, 1.0522630596533418, 1.4229730409570038, -1.3622867974918336, -1.7566761918715201, -0.7775809622835368, 5.409112347057089, 8.459109397605062, -1.0421071638702415, 2.415369793307036, -2.6276072841137648, -3.244689887855202, -6.406068034470081, 0.43607304408214986, 3.946493566967547, 1.2968847488518804, -1.250881565734744, -2.9850157076725736, 0.4237996246665716, -2.2478050589561462, -2.11603326338809, 0.30041580367833376, 0.12742933133267798, -1.8531031869351864, 0.7372045367956161, -1.9777050884440541, 2.6355860559269786, 2.9488389464095235, -5.291839499026537, 0.8065057042986155, 5.2197140753269196, 2.4962507225573063, -3.673188158776611, -3.182041609659791, -11.00412462465465, 6.586144924163818, 0.7927808412350714, -2.3961436464451253, -0.41050696559250355, 5.413942236453295, -3.1470601754263043, 0.6664996850304306, -4.888255646452308, -11.226139485836029, -2.610705205646809, -3.2844694573432207, -4.803120758384466, -1.3944403833302204, 6.083473160862923, 3.0916060061572352, 6.000555995851755, 4.676511040976038, -0.6585877165198326, -0.9755883268080652, -3.837522093206644, 7.4124216781929135, -4.313151413574815, 0.356202261056751, 2.8681854885071516, 0.08767313696444035, -2.733600841485895, -1.5783623596653342, 0.8027703128755093, -4.827803282998502, 0.9441597936674953, -0.0732387364259921, -0.6941389999119565, -1.221462706103921, -7.3489547111094, 3.8834445290267467, 0.16769123077392578, -6.914329591207206, -2.7971799727529287, 2.444386974675581, 0.45903875096701086, -2.2807575612096116, 2.5778212659060955, 0.2553887264803052, 0.1199934961841791, 0.13296812094631605, 4.2503963224589825, 5.28116776618117, 1.0391911696642637, 1.761561068939045, -2.7903470881283283, -4.674146605655551, -8.715219444944523, 2.60592063004151, -3.15032362844795, 8.326966300606728, -4.502989804372191, -3.3313056211918592, 4.429901668801904, -0.2328520230948925, 1.9217834908049554, 4.647498352918774, -8.774816360324621, 6.236015729606152, -6.485844768583775, 6.481980320066214, 7.307716980576515, -7.768629290163517, -3.646297875791788, 8.942306742072105, -6.194041540831677, -12.111823961138725, 0.47389703686349094, 8.287271559238434, 0.027343424037098885, 4.903520950116217, -0.446960482862778, -7.304315077140927, -2.126269797096029, 8.90249446593225, -7.396514328662306, 3.537413904443383, -8.149640936404467, -1.6993623896269128, 5.3228392312303185, -0.6333336047828197, 2.558341591968201, 2.6250321628176607, -1.253831862937659, -7.504875340498984, -2.413521676324308, 3.540472883731127, 4.826454630121589, 0.5283674655947834, -3.3068663366138935, 3.7459033601917326, 4.030286066234112, 1.0522729165386409, 4.2872846979880705, 1.3551377415424213, 2.5173666765913367, 0.1663997732102871, -3.1994992457330227, 5.0380625682882965, -1.3658358692191541, 10.827426016330719, 2.3478439030004665, 10.465065814554691, 2.151220729574561, -7.880378361791372, -4.276638119481504, -6.812701473012567, -4.387942299712449, 5.528798753395677, -5.181164860725403, -4.101220800541341, -2.9554961542598903, -0.6735558211803436, -3.1012318518478423, 0.4613134544342756, -1.0217744391411543, -1.1332262023352087, 4.714989019092172, 4.584322616457939, -1.299859999679029, 3.2993552633561194, -1.2760014825034887, -3.3137903612223454, -8.400650952011347, 2.5873046973720193, 5.90872510522604, -2.5127272363752127, -4.9474510829895735, -0.027258528396487236, 0.28195299953222275, -4.394729640334845, -0.63094323547557, -0.14223328232765198, 1.0244826152920723, -1.8839732831693254, 0.7800494146067649, -3.486956935375929, 2.4582354156300426, 2.0934998840093613, -6.661864381283522, 0.9247164037078619, 4.701536297798157, -0.5024042916484177, -3.8008312359452248, -2.6984294913709164, -10.608423235360533, 10.77097389230039, 2.336896028195042, -2.2927761938190088, -0.5603948291391134, 5.41568709211424, -7.19297587312758, -1.2455416703596711, -7.528297398239374, -9.709450609982014, -2.2941218498162925, -2.4056133590638638, -5.577835243195295, -3.451240688562393, 8.804942347109318, 0.41033406648784876, 7.70054067671299, 2.933702440932393, -0.29523202596465126, -1.284063845872879, -2.6755026979371905, 7.233851621858776, -2.9489388428628445, 1.2113225725479424, 1.4815757237374783, -0.22577004134655, -4.670327360741794, -1.7407872015610337, 2.0877276295796037, -5.8973917830735445, -1.2026252339128405, 1.0034352699294686, 0.21852132119238377, -1.3581159822642803, -6.694963403046131, 3.396074239164591, -0.7166257528588176, -3.429538344964385, -1.4860957637429237, 3.7870422780833906, -1.1247864094912075, -2.5774328077677637, 6.92059263214469, 2.329966662451625, -0.007602648343890905, 0.4304218194447458, 5.424539508298039, 4.370711257681251, 1.7706177309155464, 0.563650427851826, -4.253673784900457, -2.11350916326046, -8.991372741758823, 2.04699479136616, -5.963554989546537, 6.407083411235362, -2.844026267528534, -1.478282656520605, 3.037665940821171, -0.8178062224760652, 0.7287878780625761, 4.606010633055121, -11.361196875572205, 6.62005452811718, -3.989517719950527, 1.5475015183910728, 6.635305635631084, -5.8960674945265055, -3.0003331848420203, 10.251452416181564, -6.825238795019686, -8.809514552354813, -0.6862915772944689, 5.426880185957998, 2.2379916179925203, 7.7398531883955, 1.2278626407496631, -4.858941558748484, -0.8527997839264572, 10.491980209946632, -6.538483217358589, 2.0433748699724674, -7.074902940541506, 0.5198068635363597, 2.9550550831481814, -0.7177549321204424, 1.528885536827147, 2.941592833958566, -0.7723639812320471, -5.939199328422546, -3.6782302940264344, 6.008641377091408, 7.525129094719887, -0.24704481125809252, -2.036923013627529, 7.122870311141014, 4.066739859525114, 2.376695226877928, 3.2163343019783497, -0.34854072774760425, 3.449339509010315, 0.927513369359076, -4.634804844856262, 5.151644669473171, -2.2632339517585933, 8.636745177209377, -0.8766012415289879, 10.58003424713388, 2.746479067951441, -8.794460849836469, -2.9834252558648586, -4.187422346323729, -5.083394678775221, 5.347401097416878, -4.647329514846206, -2.9456684729084373, -5.515949439257383, 0.3587173279374838, -2.064152616309002, -0.02237321436405182, -1.0231781899929047, 0.022591400891542435, 0.7663705460727215, 2.2946889400482178, 0.027567874640226364, 0.7560110725462437, -0.1767941117286682, -0.48105698823928833, -0.5369076561182737, 0.2962241694331169, 0.7843970395624638, -0.07941846549510956, -1.5834220945835114, -0.12700189650058746, 1.1348189264535904, -0.3536022324115038, -0.7375196730718017, -0.590878427028656, -0.4773779958486557, -0.35154083697125316, -0.3705187663435936, -0.6775448173284531, 0.1366031914949417, 0.3918406367301941, -0.8881963565945625, 0.02498922497034073, 0.6709226844832301, 0.5886747390031815, 0.13851622119545937, -1.0554892122745514, -1.6507534980773926, 0.9110579937696457, 0.8487408757209778, -0.19375299662351608, -0.48130910098552704, 0.6187785267829895, 0.3090984523296356, 0.31550149619579315, -0.7951957285404205, -1.6292847394943237, -1.606433741748333, -0.7028935551643372, -0.5268277376890182, 0.16949550062417984, 0.6238332502543926, -0.5656673610210419, 1.163374975323677, -0.33300521969795227, 0.4531899355351925, 0.6174423918128014, -1.2220894694328308, 2.090583026409149, 0.33033744990825653, -0.622660681605339, 0.8420846462249756, -0.23904043436050415, -1.668164111673832, 0.01293976604938507, -0.06014237739145756, -0.9566419124603271, 0.4796907603740692, 0.4253878518939018, -0.18998099491000175, -0.5966575145721436, -1.0209780931472778, -0.0776431611739099, 0.043612141627818346, -1.222432078793645, 0.059869736433029175, 0.11381275951862335, 0.7855478674173355, -0.3338439092040062, -0.04314526543021202, 0.06641635624691844, 0.31880880519747734, 0.6319205239415169, 0.8672215491533279, 0.08889221027493477, -0.03558824211359024, 0.7259387895464897, -0.933734305202961, -0.7875963002443314, -0.5559269338846207, 1.05672818236053, -0.7479253336787224, 1.931088924407959, -2.09170401096344, -0.6273876056075096, 1.0050660073757172, 0.9341623794753104, 0.8833081126213074, 0.827135756611824, -1.2380013465881348, 2.0690156519412994, -0.26956881675869226, 2.1024726927280426, 1.6563076674938202, -2.049911320209503, -0.3532300293445587, 0.7390681132674217, -0.881852313876152, -1.9458013474941254, 0.5116352513432503, 0.5846329513005912, -0.845678212121129, 0.5019644647836685, -0.28568226657807827, -1.3299775123596191, 0.13351456820964813, 0.9976958483457565, -1.1326252035796642, 0.581440195441246, -2.215947240591049, -0.6550364978611469, 0.9486387968063354, -0.6312316879630089, -0.08989167213439941, 0.3526955097913742, 0.062254488468170166, -0.7923866659402847, 0.1047690361738205, 0.34445904940366745, 1.3821646347641945, 0.17229551076889038, -0.4698857753537595, 1.2308078110218048, 0.057523252442479134, 0.2804228598251939, 1.534933291375637, 0.41592239774763584, 0.0777411088347435, -1.052711844444275, -0.963726133108139, 1.26722913980484, -0.6228322684764862, 1.5780211985111237, 0.4774792566895485, 2.190441459417343, 1.6329608038067818, -1.182456135749817, -1.0119654089212418, -0.5745962113142014, -1.1535235047340393, 1.207232628017664, 0.023364678025245667, -0.8615301009267569, -0.337090440094471, -0.5499313233885914, -0.4198428988456726, -0.07478811591863632, -0.8354338556528091, -0.7992463856935501, 0.7605002149939537, 0.9896327555179596, 0.08777801832184196, 0.21013402612879872, 0.04984780587255955, -1.0010175108909607, -1.1539928913116455, 0.24474776908755302, -0.15811879187822342, -0.34097202122211456, -0.5026487708091736, -0.0017850399017333984, 0.03726679086685181, -0.49836988747119904, -0.5436718463897705, -0.13171638548374176, -0.2381463646888733, -0.2148088961839676, -0.004217715933918953, -1.055863544344902, 0.17784008383750916, 0.3633468672633171, -0.9661596491932869, -0.5670819878578186, 0.4346912354230881, -0.11198863387107849, -0.7100928872823715, -0.41908933967351913, -1.480366736650467, 1.7677760422229767, 0.7720776498317719, -0.3420986654236913, -0.10374898836016655, 0.8447530046105385, -0.6414093375205994, 0.3885188698768616, -1.2689768075942993, -2.0131545662879944, -0.14888936653733253, -0.49848319590091705, -0.6274251046124846, -0.433972992002964, 0.5170707553625107, -0.4740992709994316, 1.0385462790727615, 0.5381012000143528, 0.3948468565940857, 0.5837043039500713, 0.0688488781452179, 0.8898871410638094, -0.1843617558479309, -0.8211786821484566, 0.1371673196554184, -0.320256270468235, -0.48983401246368885, 0.12109804898500443, 1.0018230080604553, 0.12052507698535919, -0.28415926173329353, 0.06458622962236404, -0.5138764968141913, -0.9549810737371445, -1.3093583285808563, 0.5690342783927917, 0.281949020922184, -0.7436752766370773, 0.4288229439407587, 0.46042523346841335, 0.15991246327757835, -0.6204444503528066, 0.6380452178418636, 0.3217952996492386, -0.4583030752837658, 0.4492829516530037, 0.8567532151937485, 0.7335707135498524, -0.9531793966889381, -0.47532933205366135, 0.07036768645048141, -0.5449253767728806, -1.0676311999559402, -0.40469594299793243, -0.22891013324260712, 0.3361979308538139, 0.3390146642923355, 0.08820633962750435, -0.628567012026906, 1.0129808336496353, 0.591758769005537, 0.19915846083313227, -0.4818510264158249, 0.4808281138539314, -1.1318305432796478, 0.30035195499658585, 0.6268359571695328, -1.274775356054306, -0.9606710337102413, 0.7504455074667931, -0.5006858482956886, -1.2608012855052948, 0.04682363569736481, 0.8280471712350845, 0.12595904245972633, 1.1536374986171722, -0.06134992092847824, -0.2996862381696701, 0.09475208818912506, 1.1204302608966827, -0.5949244610965252, 0.28687557578086853, -1.0610337406396866, -0.6009781546890736, 0.682308591902256, 0.2991427779197693, -0.14735287800431252, 0.7295128256082535, -0.3475244492292404, -0.6077383607625961, -0.17784017627127469, 0.565036004409194, 0.10590744577348232, 0.02292618900537491, 0.1847716518677771, 0.21496532845776528, 0.16006054356694221, 0.5734389759600163, 0.0733613595366478, -0.09323807433247566, 0.3125750496983528, -0.5271374806761742, -0.5322702527046204, 1.2288738191127777, -0.6482347324490547, 1.8263351023197174, -0.3161086328327656, 0.85243359208107, -0.30992551520466805, -0.9132879376411438, -0.5217241551727057, -0.9503904618322849, -0.5832918882369995, 0.9081718772649765, -1.2898404598236084, -0.6885523796081543, -0.2546490617096424, -0.35693840961903334, 0.03823630511760712]]).astype(np.float32)
		print(vector.shape)
		# 載入參數並顯示出來
		filter_n1 = ''
		neural_node = ''
		with open(self.model.model_hyperparameter_path) as json_file:
			parameters = json.load(json_file)
			for p in parameters['hyperparameter']:
				filter_n1 = str(p['filter_n1'])
				neural_node = str(p['neural_node'])
		# Result:
		# print(filter_n1)
		# print(neural_node)
		# print(vector)
		# y_test = np.array([[0, 1, 0, 0, 0, 0, 0]]).astype(np.float32) 代表愛情(2, index = 1)
		result = int(self.model.predict(vector, filter_n1 + '_' + neural_node)[0])
		print("predictive result:", end = '')
		# 由於 Relationship LSTM Model Predict 的結果必須加一才有辦法對應到資料庫
		result = result + 1
		print(result)
		return result

	def kinship(self, data_vec):
		# 載入參數並顯示出來
		with open('model/kinship_svm_parameters') as json_file:  
			data = json.load(json_file)
			for p in data['parameters']:
				print('C: ' + str(p['C']))
				print('kernel: ' + p['kernel'])
				print('gamma: ' + str(p['gamma']))
			# 不同的評分標準 key 要做更改
			for s in data['scoring']:
				print('valid_score: ' + str(s['valid_score']))
			for p in data['preprocessing']:
				print('normalization: ' + str(p['normalization']))
				normalization = p['normalization']
		# 載入 model 並去預測
		if normalization == True:
			data_vec = preprocessing.scale(data_vec)
		else:
			data_vec = data_vec
		model = joblib.load('model/kinship_svm.pkl')	
		result = int(model.predict(data_vec[:1])[0])
		return result

	def romantic_relationship(self, data_vec):
		# 載入參數並顯示出來
		with open('model/romantic_relationship_svm_parameters') as json_file:  
			data = json.load(json_file)
			for p in data['parameters']:
				print('C: ' + str(p['C']))
				print('kernel: ' + p['kernel'])
				print('gamma: ' + str(p['gamma']))
			# 不同的評分標準 key 要做更改
			for s in data['scoring']:
				print('valid_score: ' + str(s['valid_score']))
			for p in data['preprocessing']:
				print('normalization: ' + str(p['normalization']))
				normalization = p['normalization']
		# 載入 model 並去預測
		if normalization == True:
			data_vec = preprocessing.scale(data_vec)
		else:
			data_vec = data_vec
		model = joblib.load('model/romantic_relationship_svm.pkl')	
		result = int(model.predict(data_vec[:1])[0])
		return result

	def friendship(self, data_vec):
		# 載入參數並顯示出來
		with open('model/friendship_svm_parameters') as json_file:  
			data = json.load(json_file)
			for p in data['parameters']:
				print('C: ' + str(p['C']))
				print('kernel: ' + p['kernel'])
				print('gamma: ' + str(p['gamma']))
			# 不同的評分標準 key 要做更改
			for s in data['scoring']:
				print('valid_score: ' + str(s['valid_score']))
			for p in data['preprocessing']:
				print('normalization: ' + str(p['normalization']))
				normalization = p['normalization']
		# 載入 model 並去預測
		if normalization == True:
			data_vec = preprocessing.scale(data_vec)
		else:
			data_vec = data_vec
		model = joblib.load('model/friendship_svm.pkl')	
		result = int(model.predict(data_vec[:1])[0])
		return result

	def business_relationship(self, data_vec):
		# 載入參數並顯示出來
		with open('model/business_relationship_rfc_parameters') as json_file:  
			data = json.load(json_file)
			for p in data['parameters']:
				print('n_estimators: ' + str(p['n_estimators']))
				print('criterion: ' + p['criterion'])
				print('max_features: ' + p['max_features'])
			# 不同的評分標準 key 要做更改
			for s in data['scoring']:
				print('valid_score: ' + str(s['valid_score']))
			for p in data['preprocessing']:
				print('normalization: ' + str(p['normalization']))
				normalization = p['normalization']
		# 載入 model 並去預測
		if normalization == True:
			X = preprocessing.scale(X_test)
		else:
			X = X_test
		model = joblib.load('model/business_relationship_rfc.pkl')	
		result = int(model.predict(data_vec[:1])[0])
		return result

	def others(self, data_vec):
		# 載入參數並顯示出來
		with open('model/others_svm_parameters') as json_file:  
			data = json.load(json_file)
			for p in data['parameters']:
				print('C: ' + str(p['C']))
				print('kernel: ' + p['kernel'])
				print('gamma: ' + str(p['gamma']))
			# 不同的評分標準 key 要做更改
			for s in data['scoring']:
				print('valid_score: ' + str(s['valid_score']))
			for p in data['preprocessing']:
				print('normalization: ' + str(p['normalization']))
				normalization = p['normalization']
		# 載入 model 並去預測
		if normalization == True:
			data_vec = preprocessing.scale(data_vec)
		else:
			data_vec = data_vec
		model = joblib.load('model/others_svm.pkl')	
		result = int(model.predict(data_vec[:1])[0])
		return result

	def scenario_model(self, relationship, vector):
		# scenario_add_vec
		print('='*10 + "Scenario Model")
		# Kinship
		if relationship == 1:
			result = self.kinship(vector)
			print("predictive result:", end = '')
			print(result)
		# Romantic Relationship
		elif relationship == 2:
			result = self.romantic_relationship(vector)
			print("predictive result:", end = '')
			print(result)
		# Friendship
		elif relationship == 3:
			result = self.friendship(vector)
			print("predictive result:", end = '')
			print(result)
		# Teacher Student Relationship
		elif relationship == 4:
			result = 1
		# Business Relationship
		elif relationship == 5:
			result = self.business_relationship(vector)
			print("predictive result:", end = '')
			print(result)
		# Others
		elif relationship == 6:
			result = self.others(vector)
			print("predictive result:", end = '')
			print(result)
		else:
			result = 10
		return result

	def relationship_scenario_based_trailer_recommendation(self, relationship_type_result, scenario_type_result, vector):
		candidates = {}
		for movie_information in self.movies_information:
			relationship_type = movie_information[0]
			scenario_type = movie_information[1]
			movie_id = movie_information[2]
			movie_vector = movie_information[3]
			relationship_type_list = relationship_type.split(',')
			# print("relationship_type:" + relationship_type)
			scenario_type_list = scenario_type.split(',')
			# print("scenario_type:" + scenario_type)
			for idx, rt in enumerate(relationship_type_list):
				if rt == relationship_type_result and scenario_type_list[idx] == scenario_type_result:
					vec = []
					for s in movie_vector[1:-1].split(', '):
						try:
							if s != "":
								vec.append(float(s))
						except:
							pass
					vec = np.array(vec).astype(np.float32)
					# print(vector.shape)
					# print(vec.shape)
					similarity = 1 - distance.cosine(vec, vector)
					print(str(movie_id) + ":" + str(similarity))
					candidates[str(movie_id)] = similarity
		candidates = sorted(candidates, key = candidates.get, reverse = True)
		print(candidates)
		try:
			return candidates[0] + "," + candidates[1] + "," + candidates[2];
		except:
			return ""

if __name__ == '__main__':
	recommender_system = RecommenderSystem()
	soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a socket object
	# # host = "140.116.245.146" # Get local machine name
	host = "127.0.0.1"
	port = 1994 # Reserve a port for your service.
	soc.bind((host, port))   # Bind to the port
	soc.listen(5) # Now wait for client connection.
	print("server running..")
	while True:
		conn, addr = soc.accept() # Establish connection with client.
		print ("Got connection from", addr)
		questions = conn.recv(1024)
		answers = recommender_system.main(questions.decode("utf-8"))
		conn.send((answers + "\n").encode('utf-8'))