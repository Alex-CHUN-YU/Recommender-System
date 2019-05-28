# -*- coding: utf-8 -*
import re
import codecs
def is_uchar(uchar):
    """判断一个unicode是否是汉字"""
    if uchar >= u'\u4e00' and uchar<=u'\u9fa5':
            return True
    # """判断一个unicode是否是数字"""
    # if uchar >= u'\u0030' and uchar<=u'\u0039':
    #         return False        
    # """判断一个unicode是否是英文字母"""
    # if (uchar >= u'\u0041' and uchar<=u'\u005a') or (uchar >= u'\u0061' and uchar<=u'\u007a'):
    #         return False
    # if uchar in ('-',',','，','。','.','>','?'):
    #         return False
    return False
mental_act_set = set()
with codecs.open('lexicon_MentalAct.txt', 'r', encoding='utf8') as mental_act:
	for line in mental_act.readlines():
		temp_str = ''
		for i in range(len(line)):
			if is_uchar(line[i]):
				temp_str += line[i]
		if temp_str != "":
			mental_act_set.add(temp_str)
with codecs.open('mental_act.list', 'w', encoding='utf8') as mental_act:
    mental_act.write('\n'.join(mental_act_set))

mental_state_set = set()
with codecs.open('lexicon_MentalState.txt', 'r', encoding='utf8') as mental_state:
	for line in mental_state.readlines():
		temp_str = ''
		for i in range(len(line)):
			if is_uchar(line[i]):
				temp_str += line[i]
		if temp_str != "":
			mental_state_set.add(temp_str)
with codecs.open('mental_state.list', 'w', encoding='utf8') as mental_state:
    mental_state.write('\n'.join(mental_state_set))
