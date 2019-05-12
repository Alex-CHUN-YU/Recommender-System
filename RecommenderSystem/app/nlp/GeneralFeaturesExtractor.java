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
 * General Features Extractor(人,事,時,地,物,情感).
 * 可取出人事時地物全部內容也可單獨取出人事時地物.
 * @version 1.0 2018年11月03日
 * @author Alex
 *
 */
public class GeneralFeaturesExtractor {
    /**
     * NER Result(不會經過辭典).
     */
    private String NERResult;
    /**
     * Stop Word list.
     */
    private ReadFileController stopWords, character_objectDic, locationDic, timeDic, emotionDic, eventDic;
    /**
     * Person Object Result.
     */
    private String personObjects;
    /**
     * Time Result.
     */
    private String time;
    /**
     * Location Result.
     */
    private String location;
    /**
     * Event Result.
     */
    private String events;
    /**
     * Emotion Result.
     */
    private String emotions;
    /**
     * Data Statistic.
     */
    private int Na, Naa, Nab, Nac, Nad, Naeb, Nba;
    private int Nc, Nca, Ncb, Ncc, Ncdb, Nce;
    private int Ndaad, Ndabd, Ndabe, Ndc, Ndda, Nddb, Nddc, Dd, Nd;
    private int VH, VH11, negationVH11, VH16, VH21, negationVH21, VH22, VK1, negationVK1, VK2, VJ2, VL1;
    private int IntransitiveVerb, AdverbIntransitiveVerb, transitiveVerb, AdverbtransitiveVerb;
    private int TransitiveVerbPersonObject, TransitiveVerbLocation, TransitiveVerbTime, TransitiveVerbEmotion;
    /**
     * Constructor.
     */
    public GeneralFeaturesExtractor() {
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
        // Person and Object
        Na = 0; Naa = 0; Nab = 0; Nac = 0; Nad = 0; Naeb = 0; Nba = 0;
        // Location
        Nc = 0; Nca = 0; Ncb = 0; Ncc = 0; Ncdb = 0; Nce = 0;
        // Time
        Ndaad = 0; Ndabd = 0; Ndabe = 0; Ndc = 0; Ndda = 0; Nddb = 0; Nddc = 0; Dd = 0; Nd = 0;
        // Emotion
        VH = 0; VH11 = 0; negationVH11 = 0; VH16 = 0; VH21 = 0; negationVH21 = 0; VH22 = 0; VK1 = 0; negationVK1 = 0; VK2 = 0; VJ2 = 0; VL1 = 0;
        // Event
        IntransitiveVerb = 0; AdverbIntransitiveVerb = 0; transitiveVerb = 0; AdverbtransitiveVerb = 0;
        TransitiveVerbPersonObject = 0; TransitiveVerbLocation = 0; TransitiveVerbTime = 0; TransitiveVerbEmotion = 0;
    }

    /**
     * Produce Generation Features.
     */
    public void produceGenerationFeatures(String parserResult) {
        NERResult = "";
        personObjects = "";
        time = "";
        location = "";
        events = "";
        emotions = "";
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
                for (Quad r : NERCandidateWordList) {
                    // System.out.println(r.getSegmentWord() + ":" + r.getNER() + ":" + r.getTagging() + ":" + r.getThematicRole());
                    boolean f = false;
                    String result = r.getSegmentWord().toString();
                    for (String s : stopWords.getLineList()) {
                        if (result.equals(s)) {
                            f = true;
                            break;
                        }
                    }
                    // 透過辭典來過濾部必要的詞彙(改成 false 才算是有讀辭典)
                    boolean co = false;
                    boolean lo = false;
                    boolean ti = false;
                    boolean em = false;
                    boolean ev = false;
                    // 非 Stop word 在進入
                    if (!f && !result.equals("")) {
                        this.NERResult += result + " ";
                        if (r.getNER().equals(ModuleConstant.PERSON_OBJECT)) {
                            for (String c : character_objectDic.getLineList()) {
                                if (result.equals(c)) {
                                    co = true;
                                    break;
                                }
                            }
                            if (co) {
                                personObjects += result + " ";
                            }
                        } else if (r.getNER().equals(ModuleConstant.TIME)) {
                            for (String t : timeDic.getLineList()) {
                                if (result.equals(t)) {
                                    ti = true;
                                    break;
                                }
                            }
                            if (ti) {
                                time += result + " ";
                            }
                        } else if (r.getNER().equals(ModuleConstant.LOCATION)) {
                            for (String l : locationDic.getLineList()) {
                                if (result.equals(l)) {
                                    lo = true;
                                    break;
                                }
                            }
                            if (lo) {
                                location += result + " ";
                            }
                        } else if (r.getNER().equals(ModuleConstant.EVENT)) {
                            for (String e : eventDic.getLineList()) {
                                if (result.equals(e)) {
                                    ev = true;
                                    break;
                                }
                            }
                            if (ev) {
                                events += result + " ";
                            }
                        } else if (r.getNER().equals(ModuleConstant.STATE)) {
                            for (String e : emotionDic.getLineList()) {
                                if (result.equals(e)) {
                                    em = true;
                                    break;
                                }
                            }
                            if (em) {
                                emotions += result + " ";
                            }
                        }
//                        // Statistic
//                        if (r.getNER().equals(ModuleConstant.PERSON_OBJECT)) {
//                            if (r.getTagging().equals("Na")) {
//                                System.out.println("Na:" + r.getSegmentWord());
//                                Na += 1;
//                            } else if (r.getTagging().equals("Naa")) {
//                                Naa += 1;
//                            } else if (r.getTagging().equals("Nab")) {
//                                Nab += 1;
//                            } else if (r.getTagging().equals("Nac")) {
//                                Nac += 1;
//                            } else if (r.getTagging().equals("Nad")) {
//                                Nad += 1;
//                            } else if (r.getTagging().equals("Naeb")) {
//                                Naeb += 1;
//                            } else if (r.getTagging().equals("Nba")) {
//                                Nba += 1;
//                            }
//                        } else if (r.getNER().equals(ModuleConstant.LOCATION)) {
//                            if (r.getTagging().equals("Nc")) {
//                                System.out.println("NC:" + r.getSegmentWord());
//                                Nc += 1;
//                            } else if (r.getTagging().equals("Nca")) {
//                                Nca += 1;
//                            } else if (r.getTagging().equals("Ncb")) {
//                                Ncb += 1;
//                            } else if (r.getTagging().equals("Ncc")) {
//                                System.out.println("NCC:" + r.getSegmentWord());
//                                Ncc += 1;
//                            } else if (r.getTagging().equals("Ncdb")) {
//                                System.out.println("NCDB:" + r.getSegmentWord());
//                                Ncdb += 1;
//                            } else if (r.getTagging().equals("Nce")) {
//                                System.out.println("NCE:" + r.getSegmentWord());
//                                Nce += 1;
//                            }
//                        } else if (r.getNER().equals(ModuleConstant.TIME)) {
//                            if (r.getTagging().equals("Ndaad")) {
//                                System.out.println("NDDAD:" + r.getSegmentWord());
//                                Ndaad += 1;
//                            } else if (r.getTagging().equals("Ndabd")) {
//                                System.out.println("NDABD:" + r.getSegmentWord());
//                                Ndabd += 1;
//                            } else if (r.getTagging().equals("Ndabe")) {
//                                System.out.println("NDABE:" + r.getSegmentWord());
//                                Ndabe += 1;
//                            } else if (r.getTagging().equals("Ndc")) {
//                                System.out.println("NDC:" + r.getSegmentWord());
//                                Ndc += 1;
//                            } else if (r.getTagging().equals("Ndda")) {
//                                System.out.println("Ndda:" + r.getSegmentWord());
//                                Ndda += 1;
//                            } else if (r.getTagging().equals("Nddb")) {
//                                System.out.println("NDDB:" + r.getSegmentWord());
//                                Nddb += 1;
//                            } else if (r.getTagging().equals("Nddc")) {
//                                System.out.println("NDDC:" + r.getSegmentWord());
//                                Nddc += 1;
//                            } else if (r.getTagging().equals("Dd")) {
//                                Dd += 1;
//                            } else if (r.getTagging().equals("Nd")) {
//                                Nd += 1;
//                            }
//                        } else if (r.getNER().equals(ModuleConstant.STATE)) {
//                            if (r.getTagging().equals("VH")) {
//                                System.out.println("VH:" + r.getSegmentWord());
//                                VH += 1;
//                            } else if (r.getTagging().toString().contains("VH11")) {
//                                VH11+= 1;
//                            } else if (r.getTagging().equals("VH16")) {
//                                System.out.println("VH16:" + r.getSegmentWord());
//                                VH16 += 1;
//                            } else if (r.getTagging().toString().contains("VH21")) {
//                                VH21 += 1;
//                            } else if (r.getTagging().equals("VH22")) {
//                                System.out.println("VH22:" + r.getSegmentWord());
//                                VH22 += 1;
//                            } else if (r.getTagging().toString().contains("VK1")) {
//                                VK1 += 1;
//                            } else if (r.getTagging().equals("VK2")) {
//                                System.out.println("VK2:" + r.getSegmentWord());
//                                VK2 += 1;
//                            } else if (r.getTagging().equals("VJ2")) {
//                                VJ2 += 1;
//                            } else if (r.getTagging().equals("VL1")) {
//                                System.out.println("VL1:" + r.getSegmentWord());
//                                VL1 += 1;
//                            }
//                        } else if (r.getNER().equals(ModuleConstant.EVENT)) {
//                            if (r.getTagging().toString().contains("VH11") && r.getThematicRole().toString().contains("negation")) {
//                                negationVH11 += 1;
//                            } else if (r.getTagging().toString().contains("VH21") && r.getThematicRole().toString().contains("negation")) {
//                                System.out.println("VH21NEGATION:" + r.getSegmentWord());
//                                negationVH21 += 1;
//                            } else if (r.getTagging().toString().contains("VK1") && r.getThematicRole().toString().contains("negation")) {
//                                System.out.println("VK1NEGATION:" + r.getSegmentWord());
//                                negationVK1 += 1;
//                            } else if (r.getTagging().equals("VA4") || r.getTagging().equals("VA11") || r.getTagging().equals("VA13") || r.getTagging().equals("VB11")) {
//                                IntransitiveVerb += 1;
//                            } else if (r.getTagging().toString().contains("VA4") && r.getThematicRole().toString().contains("negation")) {
//                                AdverbIntransitiveVerb += 1;
//                            } else if (r.getTagging().equals("VC2")) {
//                                transitiveVerb += 1;
//                            } else if (r.getTagging().toString().contains("VC2") && r.getThematicRole().toString().contains("negation")) {
//                                System.out.println("VC2NEGATION:" + r.getSegmentWord());
//                                AdverbtransitiveVerb += 1;
//                            } else if (r.getTagging().toString().contains("VC") && (r.getTagging().toString().contains("Na") || r.getTagging().toString().contains("Nb"))) {
//                                TransitiveVerbPersonObject += 1;
//                            } else if (r.getTagging().toString().contains("VC") && r.getTagging().toString().contains("Nc")) {
//                                TransitiveVerbLocation += 1;
//                            } else if (r.getTagging().toString().contains("VC") && r.getTagging().toString().contains("Nd")) {
//                                System.out.println("VCND:" + r.getSegmentWord());
//                                TransitiveVerbTime += 1;
//                            } else if (r.getTagging().toString().contains("VC") && r.getTagging().toString().contains("VH")) {
//                                System.out.println("VCVH:" + r.getSegmentWord());
//                                TransitiveVerbEmotion += 1;
//                            }
//                        }
                    } else {
                        System.out.println("過濾掉的詞彙:" + r.getSegmentWord().toString());
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
     * Get Person and Object Result.
     */
    public String getPersonObjectsResult() {
        return this.personObjects;
    }

    /**
     * Get Time Result.
     */
    public String getTimeResult() {
        return this.time;
    }

    /**
     * Get Location Result.
     */
    public String getLocationResult() {
        return this.location;
    }

    /**
     * Get Events Result.
     */
    public String getEventsResult() {
        return this.events;
    }

    /**
     * Get Emotions Result.
     */
    public String getEmotionsResult() {
        return this.emotions;
    }

    /**
     * Print Statistic Result.
     */
    public void printStatisticResult() {
        System.out.println("Person and Object:");
        System.out.println(Na);
        System.out.println(Naa);
        System.out.println(Nab);
        System.out.println(Nac);
        System.out.println(Nad);
        System.out.println(Naeb);
        System.out.println(Nba);
        System.out.println(Na + Naa + Nab + Nac + Nad + Naeb + Nba);
        System.out.println("Location:");
        System.out.println(Nc);
        System.out.println(Nca);
        System.out.println(Ncb);
        System.out.println(Ncc);
        System.out.println(Ncdb);
        System.out.println(Nce);
        System.out.println(Nc + Nca + Ncb + Ncc + Ncdb + Nce);
        System.out.println("Time:");
        System.out.println(Ndaad);
        System.out.println(Ndabd);
        System.out.println(Ndabe);
        System.out.println(Ndc);
        System.out.println(Ndda);
        System.out.println(Nddb);
        System.out.println(Nddc);
        System.out.println(Dd);
        System.out.println(Nd);
        System.out.println(Ndaad + Ndabd + Ndabe + Ndc + Ndda + Nddb + Nddc + Dd + Nd);
        System.out.println("Emotion:");
        System.out.println(VH);
        System.out.println(VH11);
        System.out.println(negationVH11);
        System.out.println(VH16);
        System.out.println(VH21);
        System.out.println(negationVH21);
        System.out.println(VH22);
        System.out.println(VK1);
        System.out.println(negationVK1);
        System.out.println(VK2);
        System.out.println(VJ2);
        System.out.println(VL1);
        System.out.println(VH + VH11 + negationVH11 + VH16 + VH21 + negationVH21 + VH22 + VK1 + negationVK1 + VK2 + VJ2 + VL1);
        System.out.println("Event:");
        System.out.println(IntransitiveVerb);
        System.out.println(AdverbIntransitiveVerb);
        System.out.println(transitiveVerb);
        System.out.println(AdverbtransitiveVerb);
        System.out.println(TransitiveVerbPersonObject);
        System.out.println(TransitiveVerbLocation);
        System.out.println(TransitiveVerbTime);
        System.out.println(TransitiveVerbEmotion);
        System.out.println(IntransitiveVerb + AdverbIntransitiveVerb + transitiveVerb + AdverbtransitiveVerb + TransitiveVerbPersonObject + TransitiveVerbLocation + TransitiveVerbTime + TransitiveVerbEmotion);
    }


    private ArrayList<Quad<String, String, String, String>> NERCandidateWordList;
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
                            Quad<String, String, String, String> r;
                            r = new Quad<>(segmentWord + entity, ModuleConstant.EVENT,
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
                        Quad<String, String, String, String> r;
                        r = new Quad<>(entity, ModuleConstant.EVENT, rootNode.getData().getPos(), rootNode.getData().getThematicRole());
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
                        Quad<String, String, String, String> r;
                        r = new Quad<>(entity, ModuleConstant.EVENT, rootNode.getData().getPos(), rootNode.getData().getThematicRole());
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
                        Quad<String, String, String, String> r;
                        r = new Quad<>(entity, ModuleConstant.STATE, rootNode.getData().getPos(), rootNode.getData().getThematicRole());
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
                        Quad<String, String, String, String> r;
                        r = new Quad<>(entity, ModuleConstant.PERSON_OBJECT, rootNode.getData().getPos(), rootNode.getData().getThematicRole());
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
                        Quad<String, String, String, String> r;
                        r = new Quad<>(entity, ModuleConstant.LOCATION, rootNode.getData().getPos(), rootNode.getData().getThematicRole());
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
                        Quad<String, String, String, String> r;
                        r = new Quad<>(entity, ModuleConstant.TIME, rootNode.getData().getPos(), rootNode.getData().getThematicRole());
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

    /**
     * Quad Format.
     *
     * @param <W> declare W
     * @param <X> declare X
     * @param <Y> declare Y
     * @param <Z> declare Z
     *
     */
    public static class Quad<W, X, Y, Z> {
        /**
         * SegmentWord.
         */
        private W segmentWord;
        /**
         * SegmentWord.
         */
        private X ner;
        /**
         * POS tagging.
         */
        private Y tagging;
        /**
         * Thematic Role.
         */
        private Z thematicRole;

        /**
         * Get SegmentWord.
         * @return word
         */
        public W getSegmentWord() {
            return segmentWord;
        }

        /**
         * Get SegmentWord.
         * @return word
         */
        public X getNER() {
            return ner;
        }

        /**
         * Get POS tagging.
         * @return POS
         */
        public Y getTagging() {
            return tagging;
        }

        /**
         * Get Thematic Role.
         * @return POS
         */
        public Z getThematicRole() {
            return thematicRole;
        }

        /**
         * Parser Result.
         * @param w is W declare
         * @param x is X declare
         * @param y is Y declare
         * @param z is Z declare
         */
        public Quad(final W w, final X x, final Y y, final Z z) {
            this.segmentWord = w;
            this.ner = x;
            this.tagging = y;
            this.thematicRole = z;
        }
    }
}
