# Paper
## Overview flow
* Feature Generation</br>
1. E2V-BERT 透過產生的斷詞進行辭典過濾並得到各個 entity 在進行 relationship feature 和 scenaio feature 的產生
2. E2V-W2V-SG 透過產生的斷詞進行辭典過濾並得到各個 entity 在進行 relationship feature 和 scenario feature 的產生
3. W2V-W2V-SG(relationship model baseline) 單純的斷詞未經過辭典產生 word 並做詞向量相加
* Relationship Classifer</br>
relationship classifier 訓練(relationship_algorithm_analysis) > 供給 server 存取(main)
* Scenario Classifier</br>
scenario classifier 訓練(scenario_algorithm_analysis) > 供給 server 存取(main)

## Main
### RecommenderSystem
目的：NER 運用, Server 架設
### main
目的：存取模型結果, Server 架設

## Preprocess
### relationship_algorithm_analysis
目的：訓練 relationship 模型(CNN)
### scenario_algorithm_analysis
目的：訓練 scenario 模型(KNN, NB, SVM, RFC)
### main_embedding
目的：針對 Entity2Vec-BERT, Entity2Vec-W2V-SG, Word2Vec-W2V-SG(baseline)
### rstr_evaluation
目的：給予評分項目，產生評估結果
### knowledge base
目的：產生 relationship lexicon(person), emotion lexicon(emotion), time lexicon(time), location lexicon(location)and event 辭典 
### article(Dcard Mood)
目的：爬蟲, 存取資料庫, CKIP Parser
### movie(Pixnet and Yahoo)
目的：爬蟲, 存取資料庫, CKIP Parser
### test
目的：測試資料用

## View
### rstr_view
目的：推薦系統視覺化
### rstr_view_evaluation
目的：評估系統


