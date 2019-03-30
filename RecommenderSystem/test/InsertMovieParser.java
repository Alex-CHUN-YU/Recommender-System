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
 * Insert Movie Content Parser into Mysql
 * @author ALEX-CHUN-YU
 */
public class InsertMovieParser {
    public static void main(String[] args) {
        String content = "";
        MysqlDatabaseController mysqlDatabaseController = new MysqlDatabaseController();
        ParserClient monmouthCKIP = new MonmouthCKIPParserClient();
        // 寫入電影個數 3722
        for (int i = 500; i <= 550 ; i++) {
            ResultSet result = mysqlDatabaseController.execSelect("storyline", DatabaseConstant.MOVIES, "id=" + i);
            try {
                if (result.next()) {
                    content = result.getString(DatabaseConstant.STORYLINE);
//                    System.out.println(title);
//                    System.out.println(content);
                } else {
                    System.out.println("this id " + i + " not occur!");
                    continue;
                }
            } catch (SQLException e) {
                System.out.println("Page " + i + " Extract ERROR!");
                System.out.print(e.getErrorCode());
                continue;
            }
                // https filter
                content = content.replaceAll("\\b(https?|ftp|file)://[-a-zA-Z0-9+&@#/%?=~_|!:,.;]*[-a-zA-Z0-9+&@#/%=~_|]", "");
                // Remain import Punctuation(對於有以下符號所分開的斷句本身就會被 CKIP 認為不同句子，即使當同一個句子進去，也是一樣視為不同)
                content = content.replaceAll("。|\\.|\\?|？|!|;|,|，|；|:|~|：", "\n");
                content = content.replaceAll( "[\\pP+~$`^=|<>～｀＄＾＋＝｜＜＞￥×]" , "");
                String[] sentences = content.split("\n");
                String contentParserResult = "";
                // 本來想去掉空白，但考慮到某些文章存在重要的詞彙，例:這是測試\n               測試!
                for (String sentence : sentences) {
                    if (sentence.length() >= 1) {
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
                System.out.println(contentParserResult);
                SqlObject sqlObject = new SqlObject();
                sqlObject.addSqlObject(DatabaseConstant.ID, i);
                sqlObject.addSqlObject(DatabaseConstant.STORYLINE_PARSER_RESULT, contentParserResult);
                mysqlDatabaseController.execInsert(DatabaseConstant.MOVIES_PARSER, sqlObject);
                System.out.println("movie " + i + " finished!");
                // 休息一下吧!
                try {
                    TimeUnit.SECONDS.sleep(2);
                } catch (InterruptedException e) {
                    e.getCause();
                }
        }
    }
}
