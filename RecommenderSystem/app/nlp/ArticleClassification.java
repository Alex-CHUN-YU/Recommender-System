package nlp;

import ckip.CKIPParserClient;
import ckip.ParserUtil;
import ckip.Term;
import constant_field.DatabaseConstant;
import constant_field.FileName;
import constant_field.ModuleConstant;
import constant_field.NERDictionaryConstant;
import database.MysqlDatabaseController;
import dictionary.ReadRoleDictionary;

import generictree.Node;
import generictree.Tree;
import read_write_file.ReadFileController;

import java.io.IOException;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;

/**
 * Articles Classification.
 * @version 1.0 2018年10月28日
 * @author Alex
 *
 */
public class ArticleClassification {
    /**
     * Relationship.
     */
    private ReadFileController kinship, love, friendship, teacherStudentRelationship, businessRelationship;

    /**
     * Constructor.
     */
    public ArticleClassification() throws IOException {
        // 將 Rule 寫入
        ReadRoleDictionary readThematicRolePOSPairDictionary = new ReadRoleDictionary();
        readThematicRolePOSPairDictionary.setRoleDictionary();
        // Read Relation Dictionary(E-HowNet).
        kinship = new ReadFileController(FileName.RELATION + FileName.KINSHIP);
        love = new ReadFileController(FileName.RELATION + FileName.ROMANTIC_RELATIONSHIP);
        friendship = new ReadFileController(FileName.RELATION + FileName.FRIENDSHIP);
        teacherStudentRelationship = new ReadFileController(FileName.RELATION + FileName.TEACHER_STUDENT_RELATIONSHIP);
        businessRelationship = new ReadFileController(FileName.RELATION + FileName.BUSINESS_RELATIONSHIP);
        System.out.println(kinship.getLineList());
        System.out.println(love.getLineList());
        System.out.println(friendship.getLineList());
        System.out.println(teacherStudentRelationship.getLineList());
        System.out.println(businessRelationship.getLineList());
    }

    /**
     * Using Title Classification.
     */
    public void titleClassification() {
        MysqlDatabaseController mysqlDatabaseController = new MysqlDatabaseController();
        String titleParser = "";
        String contentParser = "";
        for (int id = 10; id <=10; id++) {
            ResultSet articleResult = mysqlDatabaseController.execSelect(
                    DatabaseConstant.TITLE_PARSER_RESULT + "," + DatabaseConstant.CONTENT_PARSER_RESULT,
                    DatabaseConstant.ARTICLES_PARSER, DatabaseConstant.ID + "=" + id);
            try {
                if (articleResult.next()) {
                    titleParser = articleResult.getString(DatabaseConstant.TITLE_PARSER_RESULT);
                    contentParser = articleResult.getString(DatabaseConstant.CONTENT_PARSER_RESULT);
                }
            } catch (SQLException s) {
                s.getErrorCode();
            }
            Tree<Term> rootNode;
            System.out.println(titleParser);
            rootNode = ParserUtil.taggedTextToTermTree(titleParser);
            relationshipCandidate = new HashMap<>();
            findRelationship(rootNode.getRoot());
            for (String relationship : relationshipCandidate.keySet()) {
                System.out.println(relationship + ":" + relationshipCandidate.get(relationship));
            }
//            for (CKIPParserClient.Triple<String, String, String> relation : candidateWordList) {
//                System.out.println(relation.getSegmentWord() + ":" + relation.getTagging() + ":" + relation.getThematicRole());
//            }
            System.out.println(contentParser + "\n");
            String[] parsers = contentParser.split("@");
            for (String parser : parsers) {
                try {
                    NERCandidateWordList = new ArrayList<>();
                    System.out.println(parser);
                    eventPresence = false;
                    rootNode = ParserUtil.taggedTextToTermTree(parser);
                    findNERCandidate(rootNode.getRoot());
                    for (CKIPParserClient.Triple r : NERCandidateWordList) {
                        System.out.println(r.getSegmentWord() + ":" + r.getTagging() + ":" + r.getThematicRole());
                    }
                    System.out.println("*********************************");
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        }
    }

    private HashMap<String, Integer> relationshipCandidate;
    /**
     * Through E-HowNet Find Relationship.
     * @param rootNode root
     */
    private void findRelationship(Node<Term> rootNode) {
        if (rootNode.getChildren().size() != 0) {
            for (int i = 0; i < rootNode.getChildren().size(); i++) {
                findRelationship(rootNode.getChildAt(i));
            }
        } else {
            String relationship = rootNode.getData().getText();
            // Pre Processing
            relationship = relationship.replaceAll("\\)|\\+", "");
            System.out.println(relationship);
            // kinship=1, love=2, friendship=3, teacher_student_relationship=4, business_relationship=5
            for (String k : kinship.getLineList()) {
                if (relationship.equals(k)) {
                    relationshipCandidate.put(k, ModuleConstant.KINSHIP);
                }
            }
            for (String l : love.getLineList()) {
                if (relationship.equals(l)) {
                    relationshipCandidate.put(l, ModuleConstant.LOVE);
                }
            }
            for (String f : friendship.getLineList()) {
                if (relationship.equals(f)) {
                    relationshipCandidate.put(f, ModuleConstant.FRIENDSHIP);
                }
            }
            for (String t : teacherStudentRelationship.getLineList()) {
                if (relationship.equals(t)) {
                    relationshipCandidate.put(t, ModuleConstant.TEACHER_STUDENT_RELATIONSHIP);
                }
            }
            for (String b : businessRelationship.getLineList()) {
                if (relationship.equals(b)) {
                    relationshipCandidate.put(b, ModuleConstant.BUSINESS_RELATIONSHIP);
                }
            }
        }
    }

    private ArrayList<CKIPParserClient.Triple<String, String, String>> NERCandidateWordList;
    private boolean eventPresence;
    /**
     * Find Person or Object.
     * @param rootNode root
     */
    private void findNERCandidate(Node<Term> rootNode) {
        if (rootNode.getChildren().size() != 0) {
            for (int i = 0; i < rootNode.getChildren().size(); i++) {
                findNERCandidate(rootNode.getChildAt(i));
            }
        } else {
            boolean entityPresence = false;
            // Pre Processing
            String entity = rootNode.getData().getText();
            entity = entity.replaceAll("\\)|\\+|-|#", "");
            if (!entity.equals("")) {
                System.out.println(entity);
                Iterator postEventIterator = NERDictionaryConstant.COMPLEX_EVENT_RULE_SET.iterator();
                Iterator personObjectIterator = NERDictionaryConstant.PERSON_OBJECT_RULE_SET.iterator();
                Iterator locationIterator = NERDictionaryConstant.LOCATION_RULE_SET.iterator();
                Iterator timeIterator = NERDictionaryConstant.TIME_RULE_SET.iterator();
                Iterator eventIterator = NERDictionaryConstant.EVENT_RULE_SET.iterator();
                Iterator preEventIterator = NERDictionaryConstant.COMPLEX_EVENT_RULE_SET.iterator();
                Iterator stateIterator = NERDictionaryConstant.STATE_RULE_SET.iterator();
                // Complex Event Post Rule
                while (postEventIterator.hasNext() && eventPresence) {
                    String testSet = (String) postEventIterator.next();
                    String segmentWord = NERCandidateWordList.get(NERCandidateWordList.size() - 1).getSegmentWord();
                    String tagging = NERCandidateWordList.get(NERCandidateWordList.size() - 1).getTagging();
                    String thematicRole = NERCandidateWordList.get(NERCandidateWordList.size() - 1).getThematicRole();
                    String[] testList = testSet.split("\\+");
                    if ((thematicRole + ":" + tagging).equals(testList[0])) {
                        if ((rootNode.getData().getThematicRole() + ":"
                                + rootNode.getData().getPos()).equals(testList[1])) {
                            CKIPParserClient.Triple<String, String, String> r;
                            r = new CKIPParserClient.Triple<>(segmentWord + entity,
                                    tagging + rootNode.getData().getPos(),
                                    thematicRole + rootNode.getData().getThematicRole());
                            NERCandidateWordList.set(NERCandidateWordList.size() - 1, r);
                            entityPresence = true;
                            eventPresence = false;
                            System.out.println("hi7");
                        }
                    }
                } // while (NERDictionaryConstant.iterator.hasNext())
                // Person and Object Rule
                while (personObjectIterator.hasNext() && !entityPresence) {
                    String testSet = (String) personObjectIterator.next();
                    if ((rootNode.getData().getThematicRole() + ":"
                            + rootNode.getData().getPos()).equals(testSet)) {
                        CKIPParserClient.Triple<String, String, String> r;
                        r = new CKIPParserClient.Triple<>(entity, rootNode.getData().getPos(), rootNode.getData().getThematicRole());
                        if (eventPresence && NERCandidateWordList.get(NERCandidateWordList.size() - 1).getThematicRole().equals("negation")) {
                            NERCandidateWordList.set(NERCandidateWordList.size() - 1, r);
                        } else {
                            NERCandidateWordList.add(r);
                        }
                        entityPresence = true;
                        eventPresence = false;
                        System.out.println("hi1");
                    }
                } // while (NERDictionaryConstant.iterator.hasNext())
                // Location Rule
                while (locationIterator.hasNext() && !entityPresence) {
                    String testSet = (String) locationIterator.next();
                    if ((rootNode.getData().getThematicRole() + ":"
                            + rootNode.getData().getPos()).equals(testSet)) {
                        CKIPParserClient.Triple<String, String, String> r;
                        r = new CKIPParserClient.Triple<>(entity, rootNode.getData().getPos(), rootNode.getData().getThematicRole());
                        if (eventPresence && NERCandidateWordList.get(NERCandidateWordList.size() - 1).getThematicRole().equals("negation")) {
                            NERCandidateWordList.set(NERCandidateWordList.size() - 1, r);
                        } else {
                            NERCandidateWordList.add(r);
                        }
                        entityPresence = true;
                        eventPresence = false;
                        System.out.println("hi2");
                    }
                } // while (NERDictionaryConstant.iterator.hasNext())
                // Time Rule
                while (timeIterator.hasNext() && !entityPresence) {
                    String testSet = (String) timeIterator.next();
                    if ((rootNode.getData().getThematicRole() + ":"
                            + rootNode.getData().getPos()).equals(testSet)) {
                        CKIPParserClient.Triple<String, String, String> r;
                        r = new CKIPParserClient.Triple<>(entity, rootNode.getData().getPos(), rootNode.getData().getThematicRole());
                        if (eventPresence && NERCandidateWordList.get(NERCandidateWordList.size() - 1).getThematicRole().equals("negation")) {
                            NERCandidateWordList.set(NERCandidateWordList.size() - 1, r);
                        } else {
                            NERCandidateWordList.add(r);
                        }
                        entityPresence = true;
                        eventPresence = false;
                        System.out.println("hi3");
                    }
                } // while (NERDictionaryConstant.iterator.hasNext())
                // Event Rule
                while (eventIterator.hasNext() && !entityPresence) {
                    String testSet = (String) eventIterator.next();
                    if ((rootNode.getData().getThematicRole() + ":"
                            + rootNode.getData().getPos()).equals(testSet)) {
                        CKIPParserClient.Triple<String, String, String> r;
                        r = new CKIPParserClient.Triple<>(entity, rootNode.getData().getPos(), rootNode.getData().getThematicRole());
                        if (eventPresence && NERCandidateWordList.get(NERCandidateWordList.size() - 1).getThematicRole().equals("negation")) {
                            NERCandidateWordList.set(NERCandidateWordList.size() - 1, r);
                        } else {
                            NERCandidateWordList.add(r);
                        }
                        entityPresence = true;
                        eventPresence = false;
                        System.out.println("hi4");
                    }
                } // while (NERDictionaryConstant.iterator.hasNext())
                // Complex Event Pre Rule
                while (preEventIterator.hasNext() && !entityPresence) {
                    String testSet = (String) preEventIterator.next();
                    if ((rootNode.getData().getThematicRole() + ":"
                            + rootNode.getData().getPos()).equals(testSet.split("\\+")[0])) {
                        CKIPParserClient.Triple<String, String, String> r;
                        r = new CKIPParserClient.Triple<>(entity, rootNode.getData().getPos(), rootNode.getData().getThematicRole());
                        if (eventPresence && NERCandidateWordList.get(NERCandidateWordList.size() - 1).getThematicRole().equals("negation")) {
                            NERCandidateWordList.set(NERCandidateWordList.size() - 1, r);
                        } else {
                            NERCandidateWordList.add(r);
                        }
                        entityPresence = true;
                        eventPresence = true;
                        System.out.println("hi5");
                    }
                } // while (NERDictionaryConstant.iterator.hasNext())
                // State Rule
                while (stateIterator.hasNext() && !entityPresence) {
                    String testSet = (String) stateIterator.next();
                    if ((rootNode.getData().getThematicRole() + ":"
                            + rootNode.getData().getPos()).equals(testSet)) {
                        CKIPParserClient.Triple<String, String, String> r;
                        r = new CKIPParserClient.Triple<>(entity, rootNode.getData().getPos(), rootNode.getData().getThematicRole());
                        if (eventPresence && NERCandidateWordList.get(NERCandidateWordList.size() - 1).getThematicRole().equals("negation")) {
                            NERCandidateWordList.set(NERCandidateWordList.size() - 1, r);
                        } else {
                            NERCandidateWordList.add(r);
                        }
                        entityPresence = true;
                        eventPresence = false;
                        System.out.println("hi6");
                    }
                } // while (NERDictionaryConstant.iterator.hasNext())
            }
        }
    }
}
