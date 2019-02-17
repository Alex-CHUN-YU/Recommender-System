# -*- coding: utf-8 -*-

# Extract ehownet Specific domain terms!
class Extract:
	def __init__(self):
		self.ehownet = open('resultSimple.csv', 'r', encoding = 'utf-8')
		self.kinship_set = set()
		self.kinship = ["父", "母", "父母", "兒子", "女兒", "後代", "兄弟", "兄", "弟", "姊妹", "姊", "妹", "丈夫", "妻子", "夫妻", "親戚"]
		self.love_set = set()
		self.love = ["boyfriend", "girlfriend"]
		self.friendship_set = set()
		self.friendship = ["朋友"]
		self.teacher_student_relationship_set = set()
		self.teacher_student_relationship = ["coach", "professor", "teacher"]
		self.business_relationship_set = set()
		self.business_relationship = ["ShopAssistant", "tenant", "customer", "shopkeeper"]

	def extract(self):
		for line in self.ehownet.readlines():
			line = line.split("|")
			if len(line) >= 3:
				for k in self.kinship:
					if k in line[2]:
						self.kinship_set.add(line[1].split("	")[0].strip(" "))
				for l in self.love:
					if l in line[2]:
						self.love_set.add(line[1].split("	")[0].strip(" "))
				for f in self.friendship:
					if f in line[2]:
						self.friendship_set.add(line[1].split("	")[0].strip(" "))
				for t in self.teacher_student_relationship:
					if t in line[2]:
						self.teacher_student_relationship_set.add(line[1].split("	")[0].strip(" "))
				for t in self.business_relationship:
					if t in line[2]:
						self.business_relationship_set.add(line[1].split("	")[0].strip(" "))
						
	def save_model(self):
		out_file = open('kinship.list','w',encoding = 'utf-8')
		out_file.write('\n'.join(self.kinship_set))
		out_file = open('love.list','w',encoding = 'utf-8')
		out_file.write('\n'.join(self.love_set))
		out_file = open('friendship.list','w',encoding = 'utf-8')
		out_file.write('\n'.join(self.friendship_set))
		out_file = open('teacher_student_relationship.list','w',encoding = 'utf-8')
		out_file.write('\n'.join(self.teacher_student_relationship_set))
		out_file = open('business_relationship.list','w',encoding = 'utf-8')
		out_file.write('\n'.join(self.business_relationship_set))

if __name__ == '__main__':
	e = Extract()
	e.extract()
	e.save_model()