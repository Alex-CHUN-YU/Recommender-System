package ckip;

import net.sf.json.JSONArray;
import net.sf.json.JSONObject;

import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.URL;
import java.net.URLEncoder;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.TimeUnit;

/**
 * Connect Monmouth CKIP Parser Server.
 *
 * @version 1.0 2017年7月17日
 * @author Alex
 *
 */
public class MonmouthCKIPParserClient extends ParserClient {
    /**
     * 中研院Parser服務的基礎URL.
     */
    private String parserBaseUrl = "http://clifton.office.mt.com.tw/mtparser/parsing/";

    /**
     * Constructor.
     */
    public MonmouthCKIPParserClient() {
    }

    /**
     * Constructor.
     * @param parserBaseUrl parser base URL
     */
    public MonmouthCKIPParserClient(String parserBaseUrl) {
        this.parserBaseUrl = parserBaseUrl;
    }

    /**
     * 由孟華所提供之 parser 之結果.
     * @param parserQuestion user question
     * @return question 經 parser 後產生的結果
     */
    public List parse(String parserQuestion) {
        JSONObject json;
        try {
            String url = parserBaseUrl + URLEncoder.encode(parserQuestion, "UTF-8");
            InputStream is = new URL(url).openStream();
            BufferedReader rd = new BufferedReader(new InputStreamReader(is, "utf-8"));
            StringBuilder sb = new StringBuilder();
            int cp;
            while ((cp = rd.read()) != -1) {
                sb.append((char) cp);
            }
            json = JSONObject.fromObject(sb.toString());
            List<String> parserRes = new ArrayList<>();
            JSONArray jsonArray = json.getJSONArray("sentence");
            for (Object jsonElement : jsonArray) {
                parserRes.add(jsonElement.toString().replace("%", "S"));
            }
            is.close();
            //System.out.println(parserRes.toString());
            return parserRes;
        } catch (Exception e) {
            e.printStackTrace();
            // 休息一下吧!
            try {
                TimeUnit.SECONDS.sleep(1);
            } catch (InterruptedException e1) {
                e1.getCause();
            }
        }
        return new ArrayList<>();
    }
}
