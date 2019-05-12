# Paper
## Overview flow
* Feature Generation
Article NER 不經過辭典(RecommenderSystem) > 產生 person-object, emotion, event, time, location 辭典(algorithm_analysis and word_embedding) > 將 emotion, event 辭典移至(algorithm_analysis) 做觀察並將 filter 也加入 > Moview NER 不經過辭典(RecommenderSystem) > 統計 storyline 中的 emotion 和 event 並考慮存在在文章中且不在 filter 的詞彙 > 將 emotion 和 event 辭典加入 Article 和 Movie NER 辭典當中在執行 Article 和 Movie NER 經過辭典(RecommenderSystem), 記得刪掉資料庫資料 > 進行 Entity2Vec model 訓練(algorithm_analysis and word_embedding) > 訓練完後儲存 relationship feature 和 scenario feature 到資料庫中(algorithm_analysis and word_embedding) > Entity2Vec model 供給 server 存取(main)
* Relationship Classifer
relationship classifier 訓練(algorithm_analysis and word_embedding) > 供給 server 存取(main)
* Scenario Classifier
scenario classifier 訓練(algorithm_analysis) > 供給 server 存取(main)

## Main
### RecommenderSystem
目的：NER 運用, Server 架設
### main
目的：存取模型結果, Server 架設

## Test
### algorithm_analysis and word_embedding
目的：訓練 relationship 模型
### algorithm_analysis
目的：訓練 scenario 模型
### article(Dcard Mood)
目的：爬蟲, 存取資料庫, CKIP Parser
### movie(Pixnet and Yahoo)
目的：爬蟲, 存取資料庫, CKIP Parser
### ehownet
目的：產生 ehownet lexicon
### test
目的：測試資料用

## View
### view
目的：推薦系統視覺化

