#!/usr/bin/python
#-*- encoding: UTF-8 -*-

#from nltk.tree import *
#from nltk.draw.tree import TreeView
from collections import OrderedDict
from multiprocessing import Pool
import socket
import json
import time

token = ['，', ',', '。']

target_host = "140.116.245.147"
target_port = 9998

def Parser(sentence):
    # create socket
    # AF_INET 代表使用標準 IPv4 位址或主機名稱
    # SOCK_STREAM 代表這會是一個 TCP client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # client 建立連線
    client.connect((target_host, target_port))
    # 傳送資料給 target
    
    for tok in token:
        sentence = sentence.replace(tok, tok + '\n')

    sentence = sentence.strip()
    
    info = {}
    info['text'] = sentence
    
    response = []
    retry_limit = 3

    for i in range(retry_limit):

        try:
            client.send(json.dumps(info).encode("utf-8"))
            # 回收結果信息
            data = bytes()
            while True:
                request = client.recv(8)
                if request:
                    data += request
                    begin = time.time()
                else:
                    break
                    
            if(data is not None and data != ''):
                response = data.decode('utf-8').strip().replace('\r\n','\n').split('\n')
                break
            else:
                time.sleep(5 * (i + 1))
        except:
            time.sleep(5 * (i + 1))
        finally:
            client.close()
    
    return response

def TreeConsturct(sentence):
    ResultList = Parser(sentence)
    for result in ResultList:
        field = result.rstrip().split('#')
        sentence_parse_result = field[1].split('] ')[1]
        sentence_parse_result = "(" + sentence_parse_result + ")"
        sentence_parse_result = sentence_parse_result.replace("|",")(")
        syntax_tree = ParentedTree.fromstring(sentence_parse_result)
        TreeView(syntax_tree)._cframe.print_to_file('output.ps') #show structure

Sent = '不過，檢方勘驗劉喬安被拍的影片，及她與記者間LINE對話紀錄，認定劉去飯店賣酒的說法不實，以涉犯偽證罪查辦，後來將她起訴。台北地院日前判劉女3月徒刑，因她未提上訴而確定。劉喬安在台北地院判決結果出爐後表示說，對於這次的判決，不想上訴，會進去坐牢3個月、會服滿刑期。（中央社記者劉世怡台北26日電）「太陽花女王」劉喬安涉作偽證，遭台北地院判刑3月，因劉女未上訴而確定。台北地檢署將於28日傳喚她到案執行。'
TreeConsturct(Sent)
