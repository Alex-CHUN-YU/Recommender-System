# Paper
## Overview flow
* Feature Generation</br>
Version1: </br>
Article NER 不經過辭典(RecommenderSystem) > 產生 person-object, emotion, event, time, location 辭典(algorithm_analysis and word_embedding) > 將 emotion, event 辭典移至(algorithm_analysis) 做觀察並將 filter 也加入 > Moview NER 不經過辭典(RecommenderSystem) > 統計 storyline 中的 emotion 和 event 並考慮存在在文章中且不在 filter 的詞彙 > 將 emotion 和 event 辭典加入 Article 和 Movie NER 辭典當中在執行 Article 和 Movie NER 經過辭典(RecommenderSystem), 記得刪掉資料庫資料 > 進行 Entity2Vec model 訓練(algorithm_analysis and word_embedding) > 訓練完後儲存 relationship feature 和 scenario feature 到資料庫中(algorithm_analysis and word_embedding) > Entity2Vec model 供給 server 存取(main)</br></br>
Version2: </br>
透過 Article, Storyline NER 不經過辭典(RecommenderSystem) 將資料存到資料庫 > 透過 (knowledge base) statistic_no_dic 產生 event.txt, time.txt, location.txt, storyline_event.txt candidate > 訓練 Entity2Vec Model > 透過 knowledge_base_producer 進行 ehownet character_object.list 與已經訓練好的 entity2vec model 找出所有 candidate 並透過 event, time 和 location 做區分(knowledge base) 挑選條件就是分別的 similarity >= 分別的 threshold(threshold tuning 訓練時間大約 1~2 天) > 將 event.list, time.list 和 location.list 辭典加入 Article 和 Movie NER 辭典當中在執行 Article 和 Movie NER 經過辭典(RecommenderSystem), 記得刪掉資料庫資料 > 將 relationship feature 和 scenario feature 存到資料庫中(algorithm_analysis and word_embedding) > Entity2Vec model 供給 server 存取(main)</br></br>
1. Person、Emotion: 透過 e-hownet 做抽取</br>
2. Time、Location、Event: 利用 person 到 entity2vec 找出分別的 similarity >= 分別的 threshold 詞彙並透過 Article time 和 location 和 Event 詞彙做區分及取出</br>

* Relationship Classifer</br>
relationship classifier 訓練(algorithm_analysis and word_embedding) > 供給 server 存取(main)
* Scenario Classifier</br>
scenario classifier 訓練(algorithm_analysis) > 供給 server 存取(main)

## Main
### RecommenderSystem
目的：NER 運用, Server 架設
### main
目的：存取模型結果, Server 架設

## Preprocess
### algorithm_analysis and word_embedding
目的：訓練 relationship 模型
### algorithm_analysis
目的：訓練 scenario 模型
### article(Dcard Mood)
目的：爬蟲, 存取資料庫, CKIP Parser
### movie(Pixnet and Yahoo)
目的：爬蟲, 存取資料庫, CKIP Parser
### knowledge base
目的：產生 relationship lexicon(person), emotion lexicon(emotion), time, location and event 辭典 
### test
目的：測試資料用

## View
### view
目的：推薦系統視覺化

