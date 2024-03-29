import constant_field.DatabaseConstant;
import database.MysqlDatabaseController;
import database.SqlObject;
import dictionary.ReadRoleDictionary;
import nlp.GeneralFeaturesExtractor;
import nlp.RelationFeaturesExtractor;
import nlp.ScenarioFeaturesExtractor;

import java.io.IOException;
import java.security.cert.TrustAnchor;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.HashMap;

/**
 * Design for the articles_ner DB Column.
 * @version 1.0 2018年11月03日
 * @author Alex
 *
 */
public class NERArticles {
    public static void main(String[] args) {
        // 將 Rule 寫入
        ReadRoleDictionary readThematicRolePOSPairDictionary = new ReadRoleDictionary();
        readThematicRolePOSPairDictionary.setRoleDictionary();
        // 讀取資料庫資料 221269
        MysqlDatabaseController mysqlDatabaseController = new MysqlDatabaseController();
        GeneralFeaturesExtractor generalFeaturesExtractor = new GeneralFeaturesExtractor();
        // 計算 title 有出現兩個以上的詞彙篇數
        int titleRelationshipSum = 0;
        int titleRelationshipCount;
        int titleLabelSum = 0;
        for (int id = 1; id <= 221269; id++) {
            String titleParser = "";
            String contentParser = "";
            ResultSet articleResult = mysqlDatabaseController.execSelect(
                    DatabaseConstant.TITLE_PARSER_RESULT + "," + DatabaseConstant.CONTENT_PARSER_RESULT,
                    DatabaseConstant.ARTICLES_PARSER, DatabaseConstant.ID + "=" + id);
            try {
                if (articleResult.next()) {
                    titleParser = articleResult.getString(DatabaseConstant.TITLE_PARSER_RESULT);
                    contentParser = articleResult.getString(DatabaseConstant.CONTENT_PARSER_RESULT);
                }
            } catch (SQLException s) {
                System.out.println("Page " + id + " Extract ERROR!");
                s.printStackTrace();
                continue;
            }
            if (!titleParser.equals("") && !contentParser.equals("")) {
                // Named Entity Recognition.
                // General Features Generation.
                generalFeaturesExtractor.produceGenerationFeatures(titleParser);
                String titleNER = generalFeaturesExtractor.getNERResult();
//                String emotions = generalFeaturesExtractor.getEmotionsResult();
//                String events = generalFeaturesExtractor.getEventsResult();
//                String personObject = generalFeaturesExtractor.getPersonObjectsResult();
//                String time = generalFeaturesExtractor.getTimeResult();
//                String location = generalFeaturesExtractor.getLocationResult();
                System.out.println("Title NER:" + titleNER);
                generalFeaturesExtractor.produceGenerationFeatures(contentParser);
                String contentNER = generalFeaturesExtractor.getNERResult();
                String contentNERTag = generalFeaturesExtractor.getNERResultTag();
                String emotions = generalFeaturesExtractor.getEmotionsResult();
                String events = generalFeaturesExtractor.getEventsResult();
                String personObject = generalFeaturesExtractor.getPersonObjectsResult();
                String time = generalFeaturesExtractor.getTimeResult();
                String location = generalFeaturesExtractor.getLocationResult();
                System.out.println("Content NER:" + contentNER);
                // Scenario Features Generation.
                ScenarioFeaturesExtractor scenarioFeaturesExtractor = new ScenarioFeaturesExtractor();
                scenarioFeaturesExtractor.produceScenarioFeatures(titleParser);
                String scenarioNER = scenarioFeaturesExtractor.getNERResult();
                scenarioFeaturesExtractor.produceScenarioFeatures(contentParser);
                scenarioNER += scenarioFeaturesExtractor.getNERResult();
                System.out.println("Scenario NER:" + scenarioNER);
                // Relation Features Generation.(主要透過 E-HowNet 來劃分)
                String relationTitleNER = "";
                int min = 6;
                String relationContentNER = "";
                try {
                    RelationFeaturesExtractor relationFeaturesExtractor = new RelationFeaturesExtractor();
                    relationFeaturesExtractor.produceTitleType(titleParser);
                    HashMap<String, Integer> relationshipCandidate = relationFeaturesExtractor.getTitleTypeResult();
                    if (relationshipCandidate != null) {
                        // 區分是否有不同的關係
                        boolean differentRelationship = false;
                        int relationshipTemp = 0;
                        titleRelationshipCount = 0;
                        for (String relationship : relationshipCandidate.keySet()) {
                            titleRelationshipCount++;
                            if (titleRelationshipCount == 1) {
                                relationshipTemp = relationshipCandidate.get(relationship);
                            } else {
                                if (relationshipTemp != relationshipCandidate.get(relationship)) {
                                    differentRelationship = true;
                                }
                            }
                            System.out.println("Relation Title NER:" + relationship + ":" + relationshipCandidate.get(relationship));
                            relationTitleNER += relationship + " ";
                            if (relationshipCandidate.get(relationship) < min) {
                                min = relationshipCandidate.get(relationship);
                            }
                        }

                        // title 關係詞彙出現超過 2 次
                        if (titleRelationshipCount >= 2 && differentRelationship) {
                            titleRelationshipSum++;
                        }
                        if(titleRelationshipCount >= 1) {
                            // 計算 透過 title 標記總數
                            titleLabelSum++;
                        }
                    }
                    relationFeaturesExtractor.produceRelationFeatures(contentParser);
                    relationContentNER = relationFeaturesExtractor.getNERResult();
                    System.out.println("Relation Content NER:" + relationContentNER);
                } catch (IOException e) {
                    e.printStackTrace();
                }
                // Import MYSQL Data
                SqlObject NERSQLObject = new SqlObject();
                NERSQLObject.addSqlObject(DatabaseConstant.ID, id);
                // 不會經過辭典(但會經過 stop word)
                NERSQLObject.addSqlObject(DatabaseConstant.TITLE_NER, titleNER);
                NERSQLObject.addSqlObject(DatabaseConstant.CONTENT_NER, contentNER);
                NERSQLObject.addSqlObject(DatabaseConstant.CONTENT_NER_TAG, contentNERTag);
                // 會經過辭典(也會經過 stop word)
                NERSQLObject.addSqlObject(DatabaseConstant.RELATION_TITLE_NER, relationTitleNER);
                NERSQLObject.addSqlObject(DatabaseConstant.RELATION_CONTENT_NER, relationContentNER);
                NERSQLObject.addSqlObject(DatabaseConstant.ARTICLE_EMOTIONS, emotions);
                NERSQLObject.addSqlObject(DatabaseConstant.ARTICLE_EVENTS, events);
                NERSQLObject.addSqlObject(DatabaseConstant.ARTICLE_PERSON_OBJECT, personObject);
                NERSQLObject.addSqlObject(DatabaseConstant.ARTICLE_TIME, time);
                NERSQLObject.addSqlObject(DatabaseConstant.ARTICLE_LOCATION, location);
                NERSQLObject.addSqlObject(DatabaseConstant.SCENARIO_NER, scenarioNER);
                mysqlDatabaseController.execInsert(DatabaseConstant.ARTICLES_NER, NERSQLObject);
                // 標記所判斷的 relationship feature 也就是 relationship type
                /*SqlObject typeSQLObject = new SqlObject();
                // 1~5 label standard
                if (min != 6) {
                    typeSQLObject.addSqlObject(DatabaseConstant.TYPE, min);
                    mysqlDatabaseController.execUpdate(DatabaseConstant.ARTICLES, typeSQLObject,
                            DatabaseConstant.ID + "=" + id);
                }*/
            } else {
                continue;
            }
            System.out.println(id + " finished");
            System.out.println("-----------------------------------");
        }
        System.out.print("總共長度:");
        System.out.println(generalFeaturesExtractor.getLength());
        System.out.print("總共 label 總數:");
        System.out.println(titleLabelSum);
        System.out.print("Title NER 出現兩個以上的 relationship 詞彙:");
        System.out.println(titleRelationshipSum);

//        // 印出統計結果
//        generalFeaturesExtractor.printStatisticResult();
    }

}
