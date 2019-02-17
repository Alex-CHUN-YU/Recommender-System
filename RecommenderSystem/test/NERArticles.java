import constant_field.DatabaseConstant;
import database.MysqlDatabaseController;
import database.SqlObject;
import dictionary.ReadRoleDictionary;
import nlp.GeneralFeaturesExtractor;
import nlp.RelationFeaturesExtractor;

import java.io.IOException;
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
        // 讀取資料庫資料
        MysqlDatabaseController mysqlDatabaseController = new MysqlDatabaseController();
        GeneralFeaturesExtractor generalFeaturesExtractor = new GeneralFeaturesExtractor();
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
                String emotions = generalFeaturesExtractor.getEmotionsResult();
                String events = generalFeaturesExtractor.getEventsResult();
                String personObject = generalFeaturesExtractor.getPersonObjectsResult();
                String time = generalFeaturesExtractor.getTimeResult();
                String location = generalFeaturesExtractor.getLocationResult();
                System.out.println("Title NER:" + titleNER);
                generalFeaturesExtractor.produceGenerationFeatures(contentParser);
                String contentNER = generalFeaturesExtractor.getNERResult();
                emotions += generalFeaturesExtractor.getEmotionsResult();
                events += generalFeaturesExtractor.getEventsResult();
                personObject += generalFeaturesExtractor.getPersonObjectsResult();
                time += generalFeaturesExtractor.getTimeResult();
                location += generalFeaturesExtractor.getLocationResult();
                System.out.println("Content NER:" + contentNER);
                // Relation Features Generation.
                String relationTitleNER = "";
                int min = 6;
                String relationContentNER = "";
                try {
                    RelationFeaturesExtractor relationFeaturesExtractor = new RelationFeaturesExtractor();
                    relationFeaturesExtractor.produceTitleType(titleParser);
                    HashMap<String, Integer> relationshipCandidate = relationFeaturesExtractor.getTitleTypeResult();
                    if (relationshipCandidate != null) {
                        for (String relationship : relationshipCandidate.keySet()) {
                            System.out.println("Relation Title NER:" + relationship + ":" + relationshipCandidate.get(relationship));
                            relationTitleNER += relationship + " ";
                            if (relationshipCandidate.get(relationship) < min) {
                                min = relationshipCandidate.get(relationship);
                            }
                        }
                    }
                    relationFeaturesExtractor.produceRelationFeatures(contentParser);
                    relationContentNER = relationFeaturesExtractor.getNERResult();
                    System.out.println("Relation Content NER:" + relationContentNER);
                } catch (IOException e){
                    e.printStackTrace();
                }
                // Import MYSQL Data
                SqlObject NERSQLObject = new SqlObject();
                NERSQLObject.addSqlObject(DatabaseConstant.ID, id);
                NERSQLObject.addSqlObject(DatabaseConstant.TITLE_NER, titleNER);
                NERSQLObject.addSqlObject(DatabaseConstant.CONTENT_NER, contentNER);
                NERSQLObject.addSqlObject(DatabaseConstant.ARTICLE_EMOTIONS, emotions);
                NERSQLObject.addSqlObject(DatabaseConstant.ARTICLE_EVENTS, events);
                NERSQLObject.addSqlObject(DatabaseConstant.ARTICLE_PERSON_OBJECT, personObject);
                NERSQLObject.addSqlObject(DatabaseConstant.ARTICLE_TIME, time);
                NERSQLObject.addSqlObject(DatabaseConstant.ARTICLE_LOCATION, location);
                NERSQLObject.addSqlObject(DatabaseConstant.RELATION_TITLE_NER, relationTitleNER);
                NERSQLObject.addSqlObject(DatabaseConstant.RELATION_CONTENT_NER, relationContentNER);
                mysqlDatabaseController.execInsert(DatabaseConstant.ARTICLES_NER, NERSQLObject);
                SqlObject typeSQLObject = new SqlObject();
                // 1~5 label standard
                if (min != 6) {
                    typeSQLObject.addSqlObject(DatabaseConstant.TYPE, min);
                    mysqlDatabaseController.execUpdate(DatabaseConstant.ARTICLES, typeSQLObject,
                            DatabaseConstant.ID + "=" + id);
                }
            } else {
                continue;
            }
            System.out.print(id + " finished");
            System.out.println("-----------------------------------");
        }
//        // 印出統計結果
//        generalFeaturesExtractor.printStatisticResult();
    }
}
