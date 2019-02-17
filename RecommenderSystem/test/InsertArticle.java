import constant_field.DatabaseConstant;
import constant_field.FileName;
import database.MysqlDatabaseController;
import database.SqlObject;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;

import java.io.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Insert Article Title and Content into Mysql
 * @author ALEX-CHUN-YU
 */

public class InsertArticle {

    public static void main(String[] args) {
        // Write to DB
        MysqlDatabaseController mysqlDatabaseController = new MysqlDatabaseController();
        SqlObject sqlObject;
        // Read from JSON
        JSONParser parser = new JSONParser();
        File folder = new File(FileName.RESOURCE + "dcard_mood/");
        String[] articles = folder.list();
        for (int article = 0; article < articles.length; article++) {
            try {
                Object obj1 = parser.parse(new BufferedReader(new InputStreamReader(new FileInputStream(FileName.RESOURCE + "dcard_mood/" + articles[article]), "UTF-8")));
                JSONArray jsonArray1 = (JSONArray) obj1;
                //System.out.println(jsonArray);
                for (int i = 0; i < jsonArray1.size(); i++) {
                    sqlObject = new SqlObject();
                    JSONObject jsonObject = (JSONObject) jsonArray1.get(i);
                    String title = (String) jsonObject.get(DatabaseConstant.TITLE);
                    String content = (String) jsonObject.get(DatabaseConstant.CONTENT);
                    System.out.println("title: " + title);
//                    System.out.println("content: " + content);
                    // Insert Data
                    sqlObject.addSqlObject(DatabaseConstant.TITLE, filter(title));
                    sqlObject.addSqlObject(DatabaseConstant.CONTENT, filter(content));
                    mysqlDatabaseController.execInsert(DatabaseConstant.ARTICLES, sqlObject);
//                    System.out.println("-----------------------------------------------------");
                }
                System.out.println("Article " + article + " Finish!~");
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }

    /**
     * 過濾表情符號
     * */
    public static String filter(String str) {
        if (str.trim().isEmpty()) {
            return str;
        }
        String pattern = "[\uD83E\uDD17]|[\ud83c\udc00-\ud83c\udfff]|[\ud83d\udc00-\ud83d\udfff]|[\u2600-\u27ff]";
        String reStr = "";
        Pattern emoji = Pattern.compile(pattern);
        Matcher emojiMatcher = emoji.matcher(str);
        str = emojiMatcher.replaceAll(reStr);
        return str;
    }
}