import constant_field.DatabaseConstant;
import database.MysqlDatabaseController;
import database.SqlObject;
import dictionary.ReadRoleDictionary;
import nlp.GeneralFeaturesExtractor;
import nlp.ScenarioFeaturesExtractor;

import java.sql.ResultSet;
import java.sql.SQLException;

/**
 * Design for the movies_ner DB Column.
 * @version 1.0 2018年11月03日
 * @author Alex
 *
 */
public class NERMovies {
    public static void main(String[] args) {
        // 將 Rule 寫入
        ReadRoleDictionary readThematicRolePOSPairDictionary = new ReadRoleDictionary();
        readThematicRolePOSPairDictionary.setRoleDictionary();
        // 讀取資料庫資料 3722 = label 數量: 1171 目前只觀察到 195
        MysqlDatabaseController mysqlDatabaseController = new MysqlDatabaseController();
        GeneralFeaturesExtractor generalFeaturesExtractor = new GeneralFeaturesExtractor();
        for (int id = 1; id <= 1171; id++) {
            mysqlDatabaseController.execDelete(DatabaseConstant.MOVIES_NER, DatabaseConstant.ID + "=" + id);
            String storylineParser = "";
            ResultSet articleResult = mysqlDatabaseController.execSelect(
                    DatabaseConstant.STORYLINE_PARSER_RESULT, DatabaseConstant.MOVIES_PARSER + " as a, "
                            + DatabaseConstant.MOVIES + " as b ", "a.id=b.id and a.id=" + id + " and b.scenario_type != ''");
            try {
                if (articleResult.next()) {
                    storylineParser = articleResult.getString(DatabaseConstant.STORYLINE_PARSER_RESULT);
                }
            } catch (SQLException s) {
                System.out.println("Page " + id + " Extract ERROR!");
                s.printStackTrace();
                continue;
            }
            if (!storylineParser.equals("")) {
                // Named Entity Recognition.
                // General Features Generation.
                generalFeaturesExtractor.produceGenerationFeatures(storylineParser);
                String storylineNER = generalFeaturesExtractor.getNERResult();
                String storylineNERTag = generalFeaturesExtractor.getNERResultTag();
                String emotions = generalFeaturesExtractor.getEmotionsResult();
                String events = generalFeaturesExtractor.getEventsResult();
                System.out.println("Storyline NER:" + storylineNER);
                // Scenario Features Generation.
                ScenarioFeaturesExtractor scenarioFeaturesExtractor = new ScenarioFeaturesExtractor();
                scenarioFeaturesExtractor.produceScenarioFeatures(storylineParser);
                String scenarioNER = scenarioFeaturesExtractor.getNERResult();
                System.out.println("Scenario NER:" + scenarioNER);
                // Import MYSQL Data
                SqlObject NERSQLObject = new SqlObject();
                NERSQLObject.addSqlObject(DatabaseConstant.ID, id);
                // 不會經過辭典
                NERSQLObject.addSqlObject(DatabaseConstant.STORYLINE_NER, storylineNER);
                NERSQLObject.addSqlObject(DatabaseConstant.STORYLINE_NER_Tag, storylineNERTag);
                // 會經過辭典
                NERSQLObject.addSqlObject(DatabaseConstant.FILM_EMOTIONS, emotions);
                NERSQLObject.addSqlObject(DatabaseConstant.FILM_EVENTS, events);
                NERSQLObject.addSqlObject(DatabaseConstant.SCENARIO_NER, scenarioNER);
                mysqlDatabaseController.execInsert(DatabaseConstant.MOVIES_NER, NERSQLObject);
            } else {
                continue;
            }
            System.out.print(id + " finished");
            System.out.println("-----------------------------------");
        }
        System.out.print("總共長度:");
        System.out.println(generalFeaturesExtractor.getLength());
//        // 印出統計結果
//        generalFeaturesExtractor.printStatisticResult();
    }
}
