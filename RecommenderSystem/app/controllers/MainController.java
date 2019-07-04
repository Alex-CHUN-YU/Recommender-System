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
import read_write_file.ReadMovieDetailer;
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
        /* String emotions = generalFeaturesExtractor.getEmotionsResult();
        String events = generalFeaturesExtractor.getEventsResult();
        String personObject = generalFeaturesExtractor.getPersonObjectsResult();
        String time = generalFeaturesExtractor.getTimeResult();
        String location = generalFeaturesExtractor.getLocationResult();*/
        String contentNERTag = generalFeaturesExtractor.getNERResultTag();
        /* String relationshipResult = emotions + "@" + events + "@" + personObject + "@" + time + "@" + location;
        String nerResult = contentNERTag + "&" + sentenceInArticle;
        System.out.println(nerResult);*/
        JSONObject trailers = new JSONObject();
        try {
            SocketClient socketClient = new SocketClient();
            String movieIDs = socketClient.connecting(contentNERTag);
            String[] movieIDList = movieIDs.split(",");
            System.out.println("Result:" + movieIDs);
            if (movieIDs.contains(",")) {
                for (int id = 0; id < movieIDList.length ; id++) {
                    ReadMovieDetailer readMovieDetailer = new ReadMovieDetailer(movieIDList[id]);
                    JSONObject trailer = new JSONObject();
                    trailer.put("artist", id + 1);
                    trailer.put("trailer_name", readMovieDetailer.getName());
                    trailer.put("link", readMovieDetailer.getLink());
                    trailer.put("storyline", readMovieDetailer.getStoryline());
                    trailers.put(Integer.toString(id + 1), trailer);
                }
            }
        } catch (Exception e) {
            System.out.println("socket server error!!!!!");
        }
        try {
            response().setHeader("Access-Control-Allow-Origin", "*");
            response().setHeader("Allow", "*");
            response().setHeader("Access-Control-Allow-Methods", "POST, GET, PUT, DELETE, OPTIONS");
            response().setHeader("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept, Referer, User-Agent");
        } catch (Exception e) {
            return ok("Connecting Error");
        }
        /* JSONObject trailer1 = new JSONObject();
        trailer1.put("artist", 1);
        trailer1.put("trailer_name", "陰兒房第4章：鎖命亡靈");
        trailer1.put("link", "https://www.youtube.com/embed/F56NfDUjn5o");
        trailer1.put("storyline", "All videos on my channel are only used for commentary.\n" +
        "Copyright Disclaimer Under Section 107 of the Copyright Act 1976, allowance is made for \"fair use\" for purposes such as criticism, comment, news reporting, teaching, scholarship, and research. Fair use is a use permitted by copyright statute that might otherwise be infringing. Non-profit, educational or personal use tips the balance in favor of fair use.");
        JSONObject trailer2 = new JSONObject();
        trailer2.put("artist", 2);
        trailer2.put("trailer_name", "真愛挑日子 One Day");
        trailer2.put("link", "https://www.youtube.com/embed/0yC1B33J7SI");
        trailer2.put("storyline", "艾瑪和達斯兩人家庭背景天差地別，大學四年彼此互不相識，卻在畢業舞會當晚蹦出火花！兩人約定好每年這一天都要見面，不論任何困難、不論在那裡；一段20年前就開始的奇緣，到這一天才開花結果？當各自悲歡離合時，心裡都知道，他、她就那裡");
        JSONObject trailer3 = new JSONObject();
        trailer3.put("artist", 3);
        trailer3.put("trailer_name", "電子情書 You've Got Mail");
        trailer3.put("link", "https://www.youtube.com/embed/GSeeFgsqUxU");
        trailer3.put("storyline", "喬和凱瑟琳是生意上的競爭對手。凱瑟琳經營著母親留下來的小書店，那裡溫馨宜人，已有40年曆史，為街坊所熟知。喬卻是同街一間大書店的老闆，憑著自身優勢，一開業就搞低折扣、服務佳的策略。凱瑟琳十分排斥他的入侵，白天二人展開鬥法。不料晚上卻透過電子郵件結為好友，不知道彼此身份的夜談，讓他們感情迅速升溫。");
        trailers.put("1", trailer1);
        trailers.put("2", trailer2);
        trailers.put("3", trailer3);*/
        System.out.println(trailers.toString());
        JsonNode results = Json.parse(trailers.toString());
        return ok(results);
    }
}
