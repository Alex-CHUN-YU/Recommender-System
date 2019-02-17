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
import java.util.Iterator;

/**
 * Scenario Features Extractor(事,情感).
 * @version 1.0 2018年11月03日
 * @author Alex
 *
 */
public class ScenarioFeaturesExtractor {
    /**
     * NER Result.
     */
    private String NERResult;
    /**
     * Stop Word list.
     */
    private ReadFileController stopWords;
    /**
     * Constructor.
     */
    public ScenarioFeaturesExtractor() {
        try {
            stopWords = new ReadFileController(FileName.FILTER + FileName.STOPWORDS);
        } catch (IOException e) {
            System.out.println("Can't load Stop word dictionary!");
        }
    }

    /**
     * Produce Generation Features.
     */
    public void produceScenarioFeatures(String parserResult) {
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
                for (GeneralFeaturesExtractor.Quad r : NERCandidateWordList) {
                    // System.out.println(r.getSegmentWord() + ":" + r.getNER() + ":" + r.getTagging() + ":" + r.getThematicRole());
                    String result = r.getSegmentWord().toString();
                    result = result.replaceAll("飾演", "");
                    result = result.replaceAll("飾", "");
                    if (r.getNER().equals(ModuleConstant.STATE) || r.getNER().equals(ModuleConstant.EVENT)) {
                        boolean f = false;
                        for (String s : stopWords.getLineList()) {
                            if (result.equals(s)) {
                                f = true;
                                break;
                            }
                        }
                        if (!f && !result.equals("")) {
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
                // Person and Object Rule
                while (personObjectIterator.hasNext() && !entityPresence) {
                    String testSet = (String) personObjectIterator.next();
                    if ((rootNode.getData().getThematicRole() + ":"
                            + rootNode.getData().getPos()).equals(testSet)) {
                        GeneralFeaturesExtractor.Quad<String, String, String, String> r;
                        r = new GeneralFeaturesExtractor.Quad<>(entity, ModuleConstant.PERSON_OBJECT, rootNode.getData().getPos(), rootNode.getData().getThematicRole());
                        if (eventPresence && NERCandidateWordList.get(NERCandidateWordList.size() - 1).getThematicRole().equals("negation")) {
                            NERCandidateWordList.set(NERCandidateWordList.size() - 1, r);
                        } else {
                            NERCandidateWordList.add(r);
                        }
                        entityPresence = true;
                        eventPresence = false;
                    }
                } // while (NERDictionaryConstant.iterator.hasNext())
                // Location Rule
                while (locationIterator.hasNext() && !entityPresence) {
                    String testSet = (String) locationIterator.next();
                    if ((rootNode.getData().getThematicRole() + ":"
                            + rootNode.getData().getPos()).equals(testSet)) {
                        GeneralFeaturesExtractor.Quad<String, String, String, String> r;
                        r = new GeneralFeaturesExtractor.Quad<>(entity, ModuleConstant.LOCATION, rootNode.getData().getPos(), rootNode.getData().getThematicRole());
                        if (eventPresence && NERCandidateWordList.get(NERCandidateWordList.size() - 1).getThematicRole().equals("negation")) {
                            NERCandidateWordList.set(NERCandidateWordList.size() - 1, r);
                        } else {
                            NERCandidateWordList.add(r);
                        }
                        entityPresence = true;
                        eventPresence = false;
                    }
                } // while (NERDictionaryConstant.iterator.hasNext())
                // Time Rule
                while (timeIterator.hasNext() && !entityPresence) {
                    String testSet = (String) timeIterator.next();
                    if ((rootNode.getData().getThematicRole() + ":"
                            + rootNode.getData().getPos()).equals(testSet)) {
                        GeneralFeaturesExtractor.Quad<String, String, String, String> r;
                        r = new GeneralFeaturesExtractor.Quad<>(entity, ModuleConstant.TIME, rootNode.getData().getPos(), rootNode.getData().getThematicRole());
                        if (eventPresence && NERCandidateWordList.get(NERCandidateWordList.size() - 1).getThematicRole().equals("negation")) {
                            NERCandidateWordList.set(NERCandidateWordList.size() - 1, r);
                        } else {
                            NERCandidateWordList.add(r);
                        }
                        entityPresence = true;
                        eventPresence = false;
                    }
                } // while (NERDictionaryConstant.iterator.hasNext())
                // Event Rule
                while (eventIterator.hasNext() && !entityPresence) {
                    String testSet = (String) eventIterator.next();
                    if ((rootNode.getData().getThematicRole() + ":"
                            + rootNode.getData().getPos()).equals(testSet)) {
                        GeneralFeaturesExtractor.Quad<String, String, String, String> r;
                        r = new GeneralFeaturesExtractor.Quad<>(entity, ModuleConstant.EVENT, rootNode.getData().getPos(), rootNode.getData().getThematicRole());
                        if (eventPresence && NERCandidateWordList.get(NERCandidateWordList.size() - 1).getThematicRole().equals("negation")) {
                            NERCandidateWordList.set(NERCandidateWordList.size() - 1, r);
                        } else {
                            NERCandidateWordList.add(r);
                        }
                        entityPresence = true;
                        eventPresence = false;
                    }
                } // while (NERDictionaryConstant.iterator.hasNext())
                // Complex Event Pre Rule
                while (preEventIterator.hasNext() && !entityPresence) {
                    String testSet = (String) preEventIterator.next();
                    if ((rootNode.getData().getThematicRole() + ":"
                            + rootNode.getData().getPos()).equals(testSet.split("\\+")[0])) {
                        GeneralFeaturesExtractor.Quad<String, String, String, String> r;
                        r = new GeneralFeaturesExtractor.Quad<>(entity, ModuleConstant.EVENT, rootNode.getData().getPos(), rootNode.getData().getThematicRole());
                        if (eventPresence && NERCandidateWordList.get(NERCandidateWordList.size() - 1).getThematicRole().equals("negation")) {
                            NERCandidateWordList.set(NERCandidateWordList.size() - 1, r);
                        } else {
                            NERCandidateWordList.add(r);
                        }
                        entityPresence = true;
                        eventPresence = true;
                    }
                } // while (NERDictionaryConstant.iterator.hasNext())
                // State Rule
                while (stateIterator.hasNext() && !entityPresence) {
                    String testSet = (String) stateIterator.next();
                    if ((rootNode.getData().getThematicRole() + ":"
                            + rootNode.getData().getPos()).equals(testSet)) {
                        GeneralFeaturesExtractor.Quad<String, String, String, String> r;
                        r = new GeneralFeaturesExtractor.Quad<>(entity, ModuleConstant.STATE, rootNode.getData().getPos(), rootNode.getData().getThematicRole());
                        if (eventPresence && NERCandidateWordList.get(NERCandidateWordList.size() - 1).getThematicRole().equals("negation")) {
                            NERCandidateWordList.set(NERCandidateWordList.size() - 1, r);
                        } else {
                            NERCandidateWordList.add(r);
                        }
                        entityPresence = true;
                        eventPresence = false;
                    }
                } // while (NERDictionaryConstant.iterator.hasNext())
            }
        }
    }
}
