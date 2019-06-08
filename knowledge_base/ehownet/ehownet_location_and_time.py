# -*- coding: utf-8 -*-
import codecs
# Extract ehownet Specific domain terms!
class Extract:
	def __init__(self):
		self.ehownet = codecs.open('resultSimple.csv', 'r', encoding = 'utf-8')
		self.location_set = set()
		self.location = ["世界", "省", "區", "市", "國都", "縣", "縣", "居民區", "鄉", "ChinaTown", "大陸", "非洲", "美洲", "亞洲",
		 "國家", "paradise", "ScenicSpot", "address", "hell", "berth", "corner", "StrategicPlace", "hometown", "seat", "territory",
		 "OppositeSide", "BreedingFarm", "battlefield", "ruins", "mines", "場所", "地方"]
		self.time_set = set()
		self.time = ["時段", "period", "朝代", "終生", "century", "年", "季", "月", "旬", "周", "日", "白晝", "夜", "時", "day",
		 "分鐘", "秒", "millisecond", "vacation", "leisure", "childhood", "generations", "SchoolTerm", "opportunity", "時段"]

	def extract(self):
		for line in self.ehownet.readlines():
			line = line.split("|")
			if len(line) >= 3:
				for l in self.location:
					if l in line[2]:
						self.location_set.add(line[1].split("	")[0].strip(" "))
				for t in self.time:
					if t in line[2]:
						self.time_set.add(line[1].split("	")[0].strip(" "))
						
	def save_model(self):
		out_file = open('location.list','w',encoding = 'utf-8')
		out_file.write('\n'.join(self.location_set))
		out_file = open('time.list','w',encoding = 'utf-8')
		out_file.write('\n'.join(self.time_set))

if __name__ == '__main__':
	e = Extract()
	e.extract()
	e.save_model()