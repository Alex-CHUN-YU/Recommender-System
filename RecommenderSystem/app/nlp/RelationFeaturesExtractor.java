package nlp;

import ckip.ParserUtil;
import ckip.Term;
import constant_field.FileName;
import constant_field.ModuleConstant;
import constant_field.NERDictionaryConstant;

import generictree.Node;
import generictree.Tree;
import read_write_file.ReadFileController;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;

/**
 * Relation Features Extractor(人,事,時,地,物).
 * 主要負責 relationship model 標記用(目前是利用 E-HowNet)
 * @version 1.0 2018年11月03日
 * @author Alex
 *
 */
public class RelationFeaturesExtractor {
    /**
     * NER Result.
     */
    private String NERResult;
    /**
     * Stop Word list.
     */
    private ReadFileController stopWords, character_objectDic, locationDic, timeDic, emotionDic, eventDic;
    /**
     * Relationship.
     */
    private ReadFileController kinship, love, friendship, teacherStudentRelationship, businessRelationship;
    /**
     * Constructor.
     */
    public RelationFeaturesExtractor() throws IOException {
        try {
            stopWords = new ReadFileController(FileName.FILTER + FileName.STOP_WORDS);
            character_objectDic = new ReadFileController(FileName.FILTER + FileName.CHARACTER_OBJECT);
            locationDic = new ReadFileController(FileName.FILTER + FileName.LOCATION);
            timeDic = new ReadFileController(FileName.FILTER + FileName.TIME);
            emotionDic = new ReadFileController(FileName.FILTER + FileName.EMOTION);
            eventDic = new ReadFileController(FileName.FILTER + FileName.EVENT);
        } catch (IOException e) {
            System.out.println("Can't load Stop word dictionary!");
        }
        // Read Relation Dictionary(E-HowNet).
        kinship = new ReadFileController(FileName.RELATION + FileName.KINSHIP);
        love = new ReadFileController(FileName.RELATION + FileName.ROMANTIC_RELATIONSHIP);
        friendship = new ReadFileController(FileName.RELATION + FileName.FRIENDSHIP);
        teacherStudentRelationship = new ReadFileController(FileName.RELATION + FileName.TEACHER_STUDENT_RELATIONSHIP);
        businessRelationship = new ReadFileController(FileName.RELATION + FileName.BUSINESS_RELATIONSHIP);
//        System.out.println(kinship.getLineList());
//        System.out.println(love.getLineList());
//        System.out.println(friendship.getLineList());
//        System.out.println(teacherStudentRelationship.getLineList());
//        System.out.println(businessRelationship.getLineList());
    }

    /**
     * Produce Generation Features.
     */
    public void produceRelationFeatures(String parserResult) {
        NERResult = "";
        Tree<Term> rootNode;
        String[] parsers = parserResult.split("@");
        for (String parser : parsers) {
            try {
                NERCandidateWordList = new ArrayList<>();
//                System.out.println(parser);
                eventPresence = false;
                rootNode = ParserUtil.taggedTextToTermTree(parser);
                findNERCandidate(rootNode.getRoot());
                if (eventPresence) {
                    completeTaskProcess();
                }
                for (GeneralFeaturesExtractor.Quad r : NERCandidateWordList) {
                    // System.out.println(r.getSegmentWord() + ":" + r.getNER() + ":" + r.getTagging() + ":" + r.getThematicRole());
                    String result = r.getSegmentWord().toString();
                    boolean f = false;
                    for (String s : stopWords.getLineList()) {
                        if (result.equals(s)) {
                            f = true;
                            break;
                        }
                    }
                    // 透過辭典來過濾部必要的詞彙(改成 false 才算是有讀辭典)
                    boolean co = true;
                    boolean lo = true;
                    boolean ti = true;
                    boolean em = true;
                    boolean ev = true;
                    if (!f && !result.equals("")) {
                        for (String c : character_objectDic.getLineList()) {
                            if (result.equals(c)) {
                                co = true;
                                break;
                            }
                        }
                        for (String t : timeDic.getLineList()) {
                            if (result.equals(t)) {
                                ti = true;
                                break;
                            }
                        }
                        for (String l : locationDic.getLineList()) {
                            if (result.equals(l)) {
                                lo = true;
                                break;
                            }
                        }
                        for (String e : eventDic.getLineList()) {
                            if (result.equals(e)) {
                                ev = true;
                                break;
                            }
                        }
                        for (String e : emotionDic.getLineList()) {
                            if (result.equals(e)) {
                                em = true;
                                break;
                            }
                        }
                        if (co || ti || lo || ev || em) {
                            this.NERResult += result + " ";
                        }
                    }
                }
//                System.out.println("*********************************");
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }

    /**
     * Get NER Result.
     */
    public String getNERResult() {
        return this.NERResult;
    }

    /**
     * Produce Title Type.
     */
    public void produceTitleType(String titleParserResult) {
        try {
            Tree<Term> rootNode;
            rootNode = ParserUtil.taggedTextToTermTree(titleParserResult);
            relationshipCandidate = new HashMap<>();
            findRelationship(rootNode.getRoot());
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    /**
     * Get Title Type Result.
     */
    public HashMap<String, Integer> getTitleTypeResult() {
        return relationshipCandidate;
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
            relationship = relationship.replaceAll("\\)|\\+|#", "");
//            System.out.println(relationship);
            // kinship=1, love=2, friendship=3, teacher_student_relationship=4, business_relationship=5
            for (String b : businessRelationship.getLineList()) {
                if (relationship.equals(b)) {
                    relationshipCandidate.put(b, ModuleConstant.BUSINESS_RELATIONSHIP);
                }
            }
            for (String t : teacherStudentRelationship.getLineList()) {
                if (relationship.equals(t)) {
                    relationshipCandidate.put(t, ModuleConstant.TEACHER_STUDENT_RELATIONSHIP);
                }
            }
            for (String f : friendship.getLineList()) {
                if (relationship.equals(f)) {
                    relationshipCandidate.put(f, ModuleConstant.FRIENDSHIP);
                }
            }
            for (String l : love.getLineList()) {
                if (relationship.equals(l)) {
                    relationshipCandidate.put(l, ModuleConstant.LOVE);
                }
            }
            for (String k : kinship.getLineList()) {
                if (relationship.equals(k)) {
                    relationshipCandidate.put(k, ModuleConstant.KINSHIP);
                }
            }
        }
    }

    private ArrayList<GeneralFeaturesExtractor.Quad<String, String, String, String>> NERCandidateWordList;
    private boolean eventPresence;
    /**
     * Find Person or Object or Location or Time or Event or State.
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
                // 考慮順序 複雜事件, 事件, 狀態, 人物, 地點, 時間
//                System.out.println(entity);
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
                            GeneralFeaturesExtractor.Quad<String, String, String, String> r;
                            r = new GeneralFeaturesExtractor.Quad<>(segmentWord + entity, ModuleConstant.EVENT,
                                    tagging + rootNode.getData().getPos(),
                                    thematicRole + rootNode.getData().getThematicRole());
                            NERCandidateWordList.set(NERCandidateWordList.size() - 1, r);
                            entityPresence = true;
                            eventPresence = false;
                        }
                    }
                } // while (NERDictionaryConstant.iterator.hasNext())
                // Complex Event Pre Rule
                while (preEventIterator.hasNext() && !entityPresence) {
                    String testSet = (String) preEventIterator.next();
                    if ((rootNode.getData().getThematicRole() + ":"
                            + rootNode.getData().getPos()).equals(testSet.split("\\+")[0])) {
                        GeneralFeaturesExtractor.Quad<String, String, String, String> r;
                        r = new GeneralFeaturesExtractor.Quad<>(entity, ModuleConstant.EVENT, rootNode.getData().getPos(), rootNode.getData().getThematicRole());
                        if (eventPresence) {
                            completeTaskProcess();
                        } else {
                            eventPresence = true;
                        }
                        NERCandidateWordList.add(r);
                        entityPresence = true;
                    }
                } // while (NERDictionaryConstant.iterator.hasNext())
                // Event Rule
                while (eventIterator.hasNext() && !entityPresence) {
                    String testSet = (String) eventIterator.next();
                    if ((rootNode.getData().getThematicRole() + ":"
                            + rootNode.getData().getPos()).equals(testSet)) {
                        GeneralFeaturesExtractor.Quad<String, String, String, String> r;
                        r = new GeneralFeaturesExtractor.Quad<>(entity, ModuleConstant.EVENT, rootNode.getData().getPos(), rootNode.getData().getThematicRole());
                        if (eventPresence) {
                            completeTaskProcess();
                            eventPresence = false;
                        }
                        NERCandidateWordList.add(r);
                        entityPresence = true;
                    }
                } // while (NERDictionaryConstant.iterator.hasNext())
                // State Rule
                while (stateIterator.hasNext() && !entityPresence) {
                    String testSet = (String) stateIterator.next();
                    if ((rootNode.getData().getThematicRole() + ":"
                            + rootNode.getData().getPos()).equals(testSet)) {
                        GeneralFeaturesExtractor.Quad<String, String, String, String> r;
                        r = new GeneralFeaturesExtractor.Quad<>(entity, ModuleConstant.STATE, rootNode.getData().getPos(), rootNode.getData().getThematicRole());
                        if (eventPresence) {
                            completeTaskProcess();
                            eventPresence = false;
                        }
                        NERCandidateWordList.add(r);
                        entityPresence = true;
                    }
                } // while (NERDictionaryConstant.iterator.hasNext())
                // Person and Object Rule
                while (personObjectIterator.hasNext() && !entityPresence) {
                    String testSet = (String) personObjectIterator.next();
                    if ((rootNode.getData().getThematicRole() + ":"
                            + rootNode.getData().getPos()).equals(testSet)) {
                        GeneralFeaturesExtractor.Quad<String, String, String, String> r;
                        r = new GeneralFeaturesExtractor.Quad<>(entity, ModuleConstant.PERSON_OBJECT, rootNode.getData().getPos(), rootNode.getData().getThematicRole());
                        if (eventPresence) {
                            completeTaskProcess();
                            eventPresence = false;
                        }
                        NERCandidateWordList.add(r);
                        entityPresence = true;
                    }
                } // while (NERDictionaryConstant.iterator.hasNext())
                // Location Rule
                while (locationIterator.hasNext() && !entityPresence) {
                    String testSet = (String) locationIterator.next();
                    if ((rootNode.getData().getThematicRole() + ":"
                            + rootNode.getData().getPos()).equals(testSet)) {
                        GeneralFeaturesExtractor.Quad<String, String, String, String> r;
                        r = new GeneralFeaturesExtractor.Quad<>(entity, ModuleConstant.LOCATION, rootNode.getData().getPos(), rootNode.getData().getThematicRole());
                        if (eventPresence) {
                            completeTaskProcess();
                            eventPresence = false;
                        }
                        NERCandidateWordList.add(r);
                        entityPresence = true;
                    }
                } // while (NERDictionaryConstant.iterator.hasNext())
                // Time Rule
                while (timeIterator.hasNext() && !entityPresence) {
                    String testSet = (String) timeIterator.next();
                    if ((rootNode.getData().getThematicRole() + ":"
                            + rootNode.getData().getPos()).equals(testSet)) {
                        GeneralFeaturesExtractor.Quad<String, String, String, String> r;
                        r = new GeneralFeaturesExtractor.Quad<>(entity, ModuleConstant.TIME, rootNode.getData().getPos(), rootNode.getData().getThematicRole());
                        if (eventPresence) {
                            completeTaskProcess();
                            eventPresence = false;
                        }
                        NERCandidateWordList.add(r);
                        entityPresence = true;
                    }
                } // while (NERDictionaryConstant.iterator.hasNext())
            }
        }
    }

     /**
     * 複雜事件後位詞有其他 entity 存在, 故必須處理複雜事件前位詞是否屬於哪個 entity 沒有就移除.
     */
    private void completeTaskProcess() {
        boolean entityPresence = false;
        Iterator eventIterator = NERDictionaryConstant.EVENT_RULE_SET.iterator();
        Iterator stateIterator = NERDictionaryConstant.STATE_RULE_SET.iterator();
        Iterator personObjectIterator = NERDictionaryConstant.PERSON_OBJECT_RULE_SET.iterator();
        Iterator locationIterator = NERDictionaryConstant.LOCATION_RULE_SET.iterator();
        Iterator timeIterator = NERDictionaryConstant.TIME_RULE_SET.iterator();
        String entity = NERCandidateWordList.get(NERCandidateWordList.size() - 1).getSegmentWord();
        String tagging = NERCandidateWordList.get(NERCandidateWordList.size() - 1).getTagging();
        String thematicRole = NERCandidateWordList.get(NERCandidateWordList.size() - 1).getThematicRole();
        // Event Rule
        while (eventIterator.hasNext() && !entityPresence) {
            String testSet = (String) eventIterator.next();
            if ((thematicRole + ":" + tagging).equals(testSet)) {
                GeneralFeaturesExtractor.Quad<String, String, String, String> r;
                r = new GeneralFeaturesExtractor.Quad<>(entity, ModuleConstant.EVENT, tagging, thematicRole);
                NERCandidateWordList.set(NERCandidateWordList.size() - 1, r);
                entityPresence = true;
            }
        } // while (NERDictionaryConstant.iterator.hasNext())
        // State Rule
        while (stateIterator.hasNext() && !entityPresence) {
            String testSet = (String) stateIterator.next();
            if ((thematicRole + ":" + tagging).equals(testSet)) {
                GeneralFeaturesExtractor.Quad<String, String, String, String> r;
                r = new GeneralFeaturesExtractor.Quad<>(entity, ModuleConstant.STATE, tagging, thematicRole);
                NERCandidateWordList.set(NERCandidateWordList.size() - 1, r);
                entityPresence = true;
            }
        } // while (NERDictionaryConstant.iterator.hasNext())
        // Person and Object Rule
        while (personObjectIterator.hasNext() && !entityPresence) {
            String testSet = (String) personObjectIterator.next();
            if ((thematicRole + ":" + tagging).equals(testSet)) {
                GeneralFeaturesExtractor.Quad<String, String, String, String> r;
                r = new GeneralFeaturesExtractor.Quad<>(entity, ModuleConstant.PERSON_OBJECT, tagging, thematicRole);
                NERCandidateWordList.set(NERCandidateWordList.size() - 1, r);
                entityPresence = true;
            }
        } // while (NERDictionaryConstant.iterator.hasNext())
        // Location Rule
        while (locationIterator.hasNext() && !entityPresence) {
            String testSet = (String) locationIterator.next();
            if ((thematicRole + ":" + tagging).equals(testSet)) {
                GeneralFeaturesExtractor.Quad<String, String, String, String> r;
                r = new GeneralFeaturesExtractor.Quad<>(entity, ModuleConstant.LOCATION, tagging, thematicRole);
                NERCandidateWordList.set(NERCandidateWordList.size() - 1, r);
                entityPresence = true;
            }
        } // while (NERDictionaryConstant.iterator.hasNext())
        // Time Rule
        while (timeIterator.hasNext() && !entityPresence) {
            String testSet = (String) timeIterator.next();
            if ((thematicRole + ":" + tagging).equals(testSet)) {
                GeneralFeaturesExtractor.Quad<String, String, String, String> r;
                r = new GeneralFeaturesExtractor.Quad<>(entity, ModuleConstant.TIME, tagging, thematicRole);
                NERCandidateWordList.set(NERCandidateWordList.size() - 1, r);
                entityPresence = true;
            }
        } // while (NERDictionaryConstant.iterator.hasNext())
        // 複雜任務前衛詞如未屬與任何一個 entity 的話, 將被移除
        if (!entityPresence) {
            NERCandidateWordList.remove(NERCandidateWordList.size() - 1);
        }
    }
}
