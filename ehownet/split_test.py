extract = ["爸爸", "父", "母"]
sentence = "             | 小老婆	3571	{wife|妻子:qualification={informal|非正式}}"
print(sentence.split("|")[1])
print(sentence.split("|")[1].split("	")[0].strip(" "))
