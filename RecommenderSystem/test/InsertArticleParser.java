import ckip.MonmouthCKIPParserClient;
import ckip.ParserClient;
import constant_field.DatabaseConstant;
import database.MysqlDatabaseController;
import database.SqlObject;

import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.concurrent.TimeUnit;

/**
 * Insert Article Title Parser and Content Parser into Mysql
 * @author ALEX-CHUN-YU
 */
public class InsertArticleParser {
    public static void main(String[] args) {
        String title = "", content = "";
        MysqlDatabaseController mysqlDatabaseController = new MysqlDatabaseController();
        ParserClient monmouthCKIP = new MonmouthCKIPParserClient();
        // 寫入文章個數 221269 int i = 71945; i <= 221269
        for (int i = 1; i <= 221269 ; i++) {
            ResultSet result = mysqlDatabaseController.execSelect("title, content", DatabaseConstant.ARTICLES, "id = " + i);
            try {
                if (result.next()) {
                    title = result.getString(DatabaseConstant.TITLE);
                    content = result.getString(DatabaseConstant.CONTENT);
//                    System.out.println(title);
//                    System.out.println(content);
                }
            } catch (SQLException e) {
                System.out.println("Page " + i + " Extract ERROR!");
                System.out.print(e.getErrorCode());
                continue;
            }
            // title not null
            title = title.replaceAll( "[\\pP+~$`^=|<>～｀＄＾＋＝｜＜＞￥×]" , "");
            if (!title.equals("")) {
                String titleParserResult = "";
                ArrayList<String> list = (ArrayList<String>) monmouthCKIP.parse(title);
                for (String s : list) {
                    titleParserResult = s;
                }
//            System.out.print("**********************\n");
                // https filter
                content = content.replaceAll("\\b(https?|ftp|file)://[-a-zA-Z0-9+&@#/%?=~_|!:,.;]*[-a-zA-Z0-9+&@#/%=~_|]", "");
                // Remain import Punctuation(對於有以下符號所分開的斷句本身就會被 CKIP 認為不同句子，即使當同一個句子進去，也是一樣視為不同)
                content = content.replaceAll("。|\\.|\\?|？|!|;|,|，|；|:|~|：", "\n");
                content = content.replaceAll( "[\\pP+~$`^=|<>～｀＄＾＋＝｜＜＞￥×]" , "");
                String[] sentences = content.split("\n");
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
//            System.out.print("======================================================\n");
                System.out.println(titleParserResult);
                System.out.println(contentParserResult);
                SqlObject sqlObject = new SqlObject();
                sqlObject.addSqlObject(DatabaseConstant.ID, i);
                sqlObject.addSqlObject(DatabaseConstant.TITLE_PARSER_RESULT, titleParserResult);
                sqlObject.addSqlObject(DatabaseConstant.CONTENT_PARSER_RESULT, contentParserResult);
                mysqlDatabaseController.execInsert(DatabaseConstant.ARTICLES_PARSER, sqlObject);
                System.out.println("article " + i + " finished!");
                // 休息一下吧!
                try {
                    TimeUnit.SECONDS.sleep(2);
                } catch (InterruptedException e) {
                    e.getCause();
                }
            }
        }
    }
}
