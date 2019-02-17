package nlp;

import ckip.POSTaggingClient;
import constant_field.NERDictionaryConstant;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.Set;

/**
 * 人--當主詞
 * 事--當動詞
 * 物--當受詞或副詞
 * 時--副詞
 * 地--副詞
 *
 * @version 1.0 2018年8月20日
 * @author Alex
 *
 */
public class BasicNER {
    /**
     * Sentence.
     */
    private String sentence = "";
    /**
     * POS Tagging Result.
     */
    private ArrayList<POSTaggingClient.Tuple<String, String>> result;
    /**
     * Who.
     */
    private ArrayList<POSTaggingClient.Tuple<String, String>> who;
    /**
     * Action.
     */
    private ArrayList<POSTaggingClient.Tuple<String, String>> action;
    /**
     * Object.
     */
    private ArrayList<POSTaggingClient.Tuple<String, String>> object;
    /**
     * When.
     */
    private ArrayList<POSTaggingClient.Tuple<String, String>> when;
    /**
     * Where.
     */
    private ArrayList<POSTaggingClient.Tuple<String, String>> where;

    /**
     * Constructor.
     */
    public BasicNER(String sentence) {
        this.sentence = sentence;
        // POS Tagging
        POSTaggingClient posTagging = new POSTaggingClient();
        result = posTagging.seg(this.sentence);
        // New Object
        who = new ArrayList<>();
        action = new ArrayList<>();
        object = new ArrayList<>();
        when = new ArrayList<>();
        where = new ArrayList<>();
        // Extract Entity
        whoExtraction();
        actionExtraction();
        objectExtraction();
        whenExtraction();
        whereExtraction();
    }

    /**
     * Get Sentence.
     */
    public String getSentence() {
        return this.sentence;
    }

    /**
     * Extract Who.
     */
    private void whoExtraction() {
        extraction(NERDictionaryConstant.WHO_POS_TAGGING_RULE, who);
    }

    /**
     * Get Who.
     */
    public ArrayList<POSTaggingClient.Tuple<String, String>> getWho() {
        return who;
    }

    /**
     * Extract Action.
     */
    private void actionExtraction() {
        extraction(NERDictionaryConstant.ACTION_POS_TAGGING_RULE, action);
    }

    /**
     * Get Action.
     */
    public ArrayList<POSTaggingClient.Tuple<String, String>> getAction() {
        return action;
    }

    /**
     * Extract Object.
     */
    private void objectExtraction() {
        extraction(NERDictionaryConstant.OBJECT_POS_TAGGING_RULE, object);
    }

    /**
     * Get Object.
     */
    public ArrayList<POSTaggingClient.Tuple<String, String>> getObject() {
        return object;
    }

    /**
     * Extract When.
     */
    private void whenExtraction() {
        extraction(NERDictionaryConstant.WHEN_POS_TAGGING_RULE, when);
    }

    /**
     * Get When.
     */
    public ArrayList<POSTaggingClient.Tuple<String, String>> getWhen() {
        return when;
    }

    /**
     * Extract Where.
     */
    private void whereExtraction() {
        extraction(NERDictionaryConstant.WHERE_POS_TAGGING_RULE, where);
    }

    /**
     * Get Where.
     */
    public ArrayList<POSTaggingClient.Tuple<String, String>> getWhere() {
        return where;
    }

    /**
     * Rule Analysis.
     */
    private void extraction(Set rule, ArrayList<POSTaggingClient.Tuple<String, String>> ruleResult) {
        for (POSTaggingClient.Tuple s : result) {
            // 檢查詞性
            Iterator iterator = rule.iterator();
            while (iterator.hasNext()) {
                String testSet = (String) iterator.next();
                if (s.getTagging().equals(testSet)) {
                    POSTaggingClient.Tuple<String, String> tuple =
                            new POSTaggingClient.Tuple(s.getSegmentation(), s.getTagging());
                    ruleResult.add(tuple);
                }
            }
        }
    }
}
