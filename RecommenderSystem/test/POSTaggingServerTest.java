import ckip.POSTaggingClient;
import constant_field.NERDictionaryConstant;
import dictionary.ReadRoleDictionaryTest;

import java.util.ArrayList;
import java.util.Iterator;

/**
 * Part of Speech Tagging BasicNERTest Function.
 */
public class POSTaggingServerTest {

    public static void main(String[] args) {
        ReadRoleDictionaryTest readRoleDictionaryTest = new ReadRoleDictionaryTest();
        readRoleDictionaryTest.setRoleDictionary();
        POSTaggingClient posTagging = new POSTaggingClient();
        ArrayList<POSTaggingClient.Tuple<String, String>> result;
        result = posTagging.seg("我最近分手了，好不開心喔，好想跟周杰倫去美國，想玩玩具。");
        for (POSTaggingClient.Tuple s : result) {
            // System.out.println(s.getSegmentation() + ":" + s.getTagging());
            // 檢查詞性
            Iterator iterator = NERDictionaryConstant.POS_TAGGING_RULE_TEST_SET.iterator();
            while (iterator.hasNext()) {
                String testSet = (String) iterator.next();
                if (s.getTagging().equals(testSet)) {
                    System.out.println(s.getSegmentation() + ":" + s.getTagging());
                }
            }
        }
    }
}