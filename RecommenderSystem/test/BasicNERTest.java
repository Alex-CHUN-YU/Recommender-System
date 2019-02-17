import ckip.CKIPParserClient;
import ckip.POSTaggingClient;
import ckip.ParserUtil;
import ckip.Term;
import constant_field.NERDictionaryConstant;
import database.MysqlDatabaseController;
import dictionary.ReadRoleDictionaryTest;
import generictree.Node;
import generictree.Tree;
import nlp.BasicNER;

import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.Iterator;

/**
 * BasicNERTest Function.
 */
public class BasicNERTest {
    public static void main(String[] args) {
        // 將 rule 寫入
        ReadRoleDictionaryTest readThematicRolePOSPairDictionary = new ReadRoleDictionaryTest();
        readThematicRolePOSPairDictionary.setRoleDictionary();
        String parserResult = "";
        MysqlDatabaseController mysqlDatabaseController = new MysqlDatabaseController();
        ResultSet result = mysqlDatabaseController.execSelect("title_parser_result", "articles_parser", "id = 109259");
        try {
            if (result.next()) {
                parserResult = result.getString(1);
            }
        } catch (SQLException e) {
            System.out.print(e.getErrorCode());
        }
        String[] parsers = parserResult.split("@");
        for (String parser : parsers) {
            try {
                candidateWordList = new ArrayList<>();
                System.out.println(parser);
                Tree<Term> rootNode = ParserUtil.taggedTextToTermTree(parser);
                findCandidateWords(rootNode.getRoot());
                for (CKIPParserClient.Triple r : candidateWordList) {
                    System.out.println(r.getSegmentWord() + ":" + r.getTagging() + ":" + r.getThematicRole());
                }
                System.out.println("*********************************");
            } catch (Exception e) {
                System.out.print("this is a error analysis");
                e.getCause();
            }
        }
        // 將 rule 寫入
        readThematicRolePOSPairDictionary.setRoleDictionary();
        BasicNER basicNER = new BasicNER("劉德華在香港長得好像明星喔");
        System.out.println(basicNER.getSentence());
        System.out.println("------------");
        for (POSTaggingClient.Tuple t : basicNER.getWho()) {
            System.out.println(t.getSegmentation() + ":" + t.getTagging());
        }
        System.out.println("------------");
        for (POSTaggingClient.Tuple t : basicNER.getAction()) {
            System.out.println(t.getSegmentation() + ":" + t.getTagging());
        }
        System.out.println("------------");
        for (POSTaggingClient.Tuple t : basicNER.getObject()) {
            System.out.println(t.getSegmentation() + ":" + t.getTagging());
        }
        System.out.println("------------");
        for (POSTaggingClient.Tuple t : basicNER.getWhen()) {
            System.out.println(t.getSegmentation() + ":" + t.getTagging());
        }
        System.out.println("------------");
        for (POSTaggingClient.Tuple t : basicNER.getWhere()) {
            System.out.println(t.getSegmentation() + ":" + t.getTagging());
        }
    }

    /**
     * A List which represents the Candidate Words in a sentence.
     */
    private static ArrayList<CKIPParserClient.Triple<String, String, String>> candidateWordList;
    private static void findCandidateWords(Node<Term> rootNode) {
        if (rootNode.getChildren().size() != 0) {
            for (int i = 0; i < rootNode.getChildren().size(); i++) {
                findCandidateWords(rootNode.getChildAt(i));
            }
        } else {
            // 檢查語意腳色與詞性
            Iterator iterator = NERDictionaryConstant.PARSER_RULE_TEST_SET.iterator();
            while (iterator.hasNext()) {
                String testSet = (String) iterator.next();
                if ((rootNode.getData().getThematicRole() + " "
                        + rootNode.getData().getPos()).contains(testSet)) {
                    CKIPParserClient.Triple<String, String, String> r;
                    r = new CKIPParserClient.Triple<>(rootNode.getData().getText(), rootNode.getData().getPos(), rootNode.getData().getThematicRole());
                    candidateWordList.add(r);
                }
            } // while (NERDictionaryConstant.iterator.hasNext())
        }
    }
}
