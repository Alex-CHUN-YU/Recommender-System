import ckip.*;
import constant_field.NERDictionaryConstant;
import dictionary.ReadRoleDictionaryTest;
import generictree.Node;
import generictree.Tree;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

/**
 * Parser BasicNERTest Function.
 */
public class ParserServerTest {

    public static void main(String[] args) {
        // 將 rule 寫入
        ReadRoleDictionaryTest readThematicRolePOSPairDictionary = new ReadRoleDictionaryTest();
        readThematicRolePOSPairDictionary.setRoleDictionary();
        String sentence = "周杰倫是帥哥，可以:fdsfasfdds；告訴我嗎? 可是我覺得我比較帥! 我感覺到 sad嗎? ";
        // CKIP Parser
        ParserClient ckip = new CKIPParserClient();
        List list = ckip.parse(sentence);
        ParserResult parserResult = (ParserResult)list.get(0);
        for (String s : parserResult.getSentence()) {
            candidateWordList = new ArrayList<>();
            System.out.println(s);
            Tree<Term> rootNode = ParserUtil.taggedTextToTermTree(s);
            findCandidateWords(rootNode.getRoot());
            for (CKIPParserClient.Triple r : candidateWordList) {
                System.out.println(r.getSegmentWord() + ":" + r.getTagging() + ":" + r.getThematicRole());
            }
            System.out.println("-----");
        }
        System.out.println("\n\n");
        // Monmouth CKIP Parser
        ParserClient monmouthCKIP = new MonmouthCKIPParserClient();
        ArrayList<String> list1 = (ArrayList<String>) monmouthCKIP.parse(sentence);
        for (String s : list1) {
            candidateWordList = new ArrayList<>();
            System.out.println(s);
            Tree<Term> rootNode = ParserUtil.taggedTextToTermTree(s);
            findCandidateWords(rootNode.getRoot());
            for (CKIPParserClient.Triple r : candidateWordList) {
                System.out.println(r.getSegmentWord() + ":" + r.getTagging() + ":" + r.getThematicRole());
            }
            System.out.println("----------");
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
