package controllers;

import ckip.MonmouthCKIPParserClient;
import ckip.ParserClient;
import com.fasterxml.jackson.databind.JsonNode;

import dictionary.ReadRoleDictionary;
import json.JSONArray;
import json.JSONObject;
import ml_model_client.SocketClient;
import nlp.GeneralFeaturesExtractor;
import nlp.ScenarioFeaturesExtractor;
import play.libs.Json;
import play.mvc.*;
import scala.collection.immutable.List;

import java.util.ArrayList;


/**
 * Main Controller.
 *
 * @version 1.0 2018年8月14日
 * @author Alex
 *
 */
public class MainController extends Controller {


    public Result HelloWorld() {
        return ok("HelloWorld");
    }

    /**
     * Main Controller.
     */
    public Result getRecommendSystemResult(String article) {
//        JsonNode request = request().body().asJson();
//        JSONObject userDataJsonObject = new JSONObject(request.toString());
//        String article = userDataJsonObject.getString("article");
//        int value = userDataJsonObject.getInt("value");
//        System.out.println(text + ":" + value);
        System.out.println("Origin:"+ article);
        // Parser
        ParserClient monmouthCKIP = new MonmouthCKIPParserClient();
        article = article.replaceAll("\\b(https?|ftp|file)://[-a-zA-Z0-9+&@#/%?=~_|!:,.;]*[-a-zA-Z0-9+&@#/%=~_|]", "");
        // Remain import Punctuation(對於有以下符號所分開的斷句本身就會被 CKIP 認為不同句子，即使當同一個句子進去，也是一樣視為不同)
        article = article.replaceAll("。|\\.|\\?|？|!|;|,|，|；|:|~|：", "\n");
        article = article.replaceAll( "[\\pP+~$`^=|<>～｀＄＾＋＝｜＜＞￥×]" , "");
        String[] sentences = article.split("\n");
        String contentParserResult = "";
        // 本來想去掉空白，但考慮到某些文章存在重要的詞彙，例:這是測試\n               測試!
        for (String sentence : sentences) {
            if (sentence.length() >= 4) {
//                    System.out.println(sentence);
                ArrayList<String> list1 = (ArrayList<String>) monmouthCKIP.parse(sentence);
                for (String s : list1) {
                    contentParserResult += s;
                    contentParserResult += "@";
                    // System.out.println(s);
                }
            }
        }
        System.out.println(contentParserResult);
        // NER
        ReadRoleDictionary readThematicRolePOSPairDictionary = new ReadRoleDictionary();
        readThematicRolePOSPairDictionary.setRoleDictionary();
        GeneralFeaturesExtractor generalFeaturesExtractor = new GeneralFeaturesExtractor();
        generalFeaturesExtractor.produceGenerationFeatures(contentParserResult);
        String emotions = generalFeaturesExtractor.getEmotionsResult();
        String events = generalFeaturesExtractor.getEventsResult();
        String personObject = generalFeaturesExtractor.getPersonObjectsResult();
        String time = generalFeaturesExtractor.getTimeResult();
        String location = generalFeaturesExtractor.getLocationResult();
        ScenarioFeaturesExtractor scenarioFeaturesExtractor = new ScenarioFeaturesExtractor();
        scenarioFeaturesExtractor.produceScenarioFeatures(contentParserResult);
        String scenarioNER = scenarioFeaturesExtractor.getNERResult();
        String relationshipResult = emotions + "@" + events + "@" + personObject + "@" + time + "@" + location;
        String result = relationshipResult + "&" + scenarioNER;
        System.out.println(result);
        SocketClient socketClient = new SocketClient();
        String test = socketClient.connecting(result);
        System.out.println("Result:" + test);
        /*DatabaseController databaseController = new DatabaseController();
        JsonNode request = request().body().asJson();
        int id = Integer.parseInt(request.findPath(ConstantField.userAndArticleID).toString());
        int systemType = Integer.parseInt(request.findPath(ConstantField.userAndArticleSystemType).textValue());
        JsonNode result = Json.newObject();
        ResultSet resultSet = databaseController.execSelect(sqlCommandComposer.getUserDataSqlByIdAndSystemType(id, systemType));
        try {
            ResultSetMetaData resultSetMetaData = resultSet.getMetaData();
            JSONObject resultJsonObject = new JSONObject();
            if (resultSet.next()) {
                for (int i = 1; i <= resultSetMetaData.getColumnCount(); i++) {
                    Object columnValue = resultSet.getObject(i);
                    if (resultSetMetaData.getColumnTypeName(i).equals(ConstantField.databaseStringType)) {
                        resultJsonObject.put(resultSetMetaData.getColumnName(i), columnValue.toString());
                    } else if (resultSetMetaData.getColumnTypeName(i).equals(ConstantField.databaseIntType)) {
                        resultJsonObject.put(resultSetMetaData.getColumnName(i), Integer.parseInt(columnValue.toString()));
                    }
                }
            }
            result = Json.parse(resultJsonObject.toString());
        } catch (SQLException e) {
            e.printStackTrace();
        }*/
        try {
            response().setHeader("Access-Control-Allow-Origin", "*");
            response().setHeader("Allow", "*");
            response().setHeader("Access-Control-Allow-Methods", "POST, GET, PUT, DELETE, OPTIONS");
            response().setHeader("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept, Referer, User-Agent");
        } catch (Exception e) {
            return ok("Connecting Error");
        }

        JSONObject trailer = new JSONObject();
        trailer.put("artist", 0);
        trailer.put("trailer_name", "陰兒房第4章：鎖命亡靈");
        trailer.put("link", "https://www.youtube.com/embed/2Yht__fMpxA");
        trailer.put("storyline", "All videos on my channel are only used for commentary.\n" +
                "Copyright Disclaimer Under Section 107 of the Copyright Act 1976, allowance is made for \"fair use\" for purposes such as criticism, comment, news reporting, teaching, scholarship, and research. Fair use is a use permitted by copyright statute that might otherwise be infringing. Non-profit, educational or personal use tips the balance in favor of fair use.");
        JSONObject trailer1 = new JSONObject();
        trailer1.put("artist", 1);
        trailer1.put("trailer_name", "真愛挑日子 One Day");
        trailer1.put("link", "https://www.youtube.com/embed/GSeeFgsqUxU");
        trailer1.put("storyline", "喬和凱瑟琳是生意上的競爭對手。凱瑟琳經營著母親留下來的小書店，那裡溫馨宜人，已有40年曆史，為街坊所熟知。喬卻是同街一間大書店的老闆，憑著自身優勢，一開業就搞低折扣、服務佳的策略。凱瑟琳十分排斥他的入侵，白天二人展開鬥法。不料晚上卻透過電子郵件結為好友，不知道彼此身份的夜談，讓他們感情迅速升溫。");

        ArrayList<JSONObject> trailers = new ArrayList<>();
        trailers.add(trailer);
        trailers.add(trailer1);
        JsonNode results = Json.parse(trailers.toString());
        return ok(results);
    }
}
