package constant_field;

import java.util.HashSet;
import java.util.Set;

/**
 * 主要提供 Name Entity Recognition 辭典所利用到的變數或常數.
 *
 * @version 1.0 2017年7月18日
 * @author Alex
 *
 */
public class NERDictionaryConstant {
    // Person and Object and Location and Time and Event and State
    /**
     * Person or Object Rule Set.
     */
    public static final Set PERSON_OBJECT_RULE_SET = new HashSet();
    /**
     * Person or Object Rule.
     */
    public static final String PERSON_OBJECT_RULE = "parser_rule/PERSON_OBJECT_RULE";
    /**
     * Location Rule Set.
     */
    public static final Set LOCATION_RULE_SET = new HashSet();
    /**
     * Location Rule.
     */
    public static final String LOCATION_RULE = "parser_rule/LOCATION_RULE";
    /**
     * Time Rule Set.
     */
    public static final Set TIME_RULE_SET = new HashSet();
    /**
     * Time Rule.
     */
    public static final String TIME_RULE = "parser_rule/TIME_RULE";
    /**
     * Event Rule Set.
     */
    public static final Set EVENT_RULE_SET = new HashSet();
    /**
     * Event Rule.
     */
    public static final String EVENT_RULE = "parser_rule/EVENT_RULE";
    /**
     * Complex Event Rule Set.
     */
    public static final Set COMPLEX_EVENT_RULE_SET = new HashSet();
    /**
     * Complex Event Rule.
     */
    public static final String COMPLEX_EVENT_RULE = "parser_rule/COMPLEX_EVENT_RULE";
    /**
     * State Rule Set.
     */
    public static final Set STATE_RULE_SET = new HashSet();
    /**
     * State Rule.
     */
    public static final String STATE_RULE = "parser_rule/STATE_RULE";
    // Test
    /**
     * Parser Storage TEST Rule.
     */
    public static final Set PARSER_RULE_TEST_SET = new HashSet();
    /**
     * 詞典檔名.
     */
    public static final String PARSER_DICTIONARY_TEST = "parser_rule/NER_TEST";
    /**
     * POS Tagging Storage TEST Role.
     */
    public static final Set POS_TAGGING_RULE_TEST_SET = new HashSet();
    /**
     * 詞典檔名.
     */
    public static final String POS_TAGGING_DICTIONARY_TEST = "pos_tagging_rule/NER_TEST";
    /**
     * Who Rule SET.
     */
    public static final Set WHO_POS_TAGGING_RULE = new HashSet();
    /**
     * 詞典檔名.
     */
    public static final String WHO_DICTIONARY = "pos_tagging_rule/who";
    /**
     * Action Rule SET.
     */
    public static final Set ACTION_POS_TAGGING_RULE = new HashSet();
    /**
     * 詞典檔名.
     */
    public static final String ACTION_DICTIONARY = "pos_tagging_rule/action";
    /**
     * Object Rule SET.
     */
    public static final Set OBJECT_POS_TAGGING_RULE = new HashSet();
    /**
     * 詞典檔名.
     */
    public static final String OBJECT_DICTIONARY = "pos_tagging_rule/object";
    /**
     * When Rule SET.
     */
    public static final Set WHEN_POS_TAGGING_RULE = new HashSet();
    /**
     * 詞典檔名.
     */
    public static final String WHEN_DICTIONARY = "pos_tagging_rule/when";
    /**
     * Where Rule SET.
     */
    public static final Set WHERE_POS_TAGGING_RULE = new HashSet();
    /**
     * 詞典檔名.
     */
    public static final String WHERE_DICTIONARY = "pos_tagging_rule/where";
    /**
     * 詞典檔延伸名.
     */
    public static final String FILE_EXTENSION = ".txt";
}
