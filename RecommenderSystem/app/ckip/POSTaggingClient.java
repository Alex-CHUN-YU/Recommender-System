package ckip;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import tw.cheyingwu.ckip.CKIP;
import tw.cheyingwu.ckip.Term;

import java.util.ArrayList;

/**
 * CKIP Part of Speech.
 *
 * @version 1.0 2017年4月27日
 * @author NCKU WMMKS LAB
 *
 */
public class POSTaggingClient {
    /**
     * Slf4j logger instance.
     */
    private final Logger logger = LoggerFactory.getLogger(POSTaggingClient.class);
    /**
     * CKIP serverIP.
     */
    private static String serverIP = "140.109.19.104";
    /**
     * CKIP serverPort.
     */
    private static int serverPort = 1501;
    /**
     * CKIP userName.
     */
    private static String userName = "P76064538"; // "kenmonmouth";
    /**
     * CKIP User Password.
     */
    private static String password = "Alove0906"; // "6cd25e45";
    /**
     * CKIP User connection.
     */
    private CKIP connection;

    /**
     * CKIP connect.
     */
    public POSTaggingClient() {
        connect(serverIP, serverPort, userName, password);
    }

    /**
     * CKIP connect.
     * @param serverIPTemp CKIP serverIP
     * @param serverPortTemp CKIP serverPort
     * @param userNameTemp CKIP userName
     * @param passwordTemp User Password
     */
    private void connect(final String serverIPTemp, final int serverPortTemp,
            final String userNameTemp, final String passwordTemp) {
        connection = new CKIP(serverIPTemp, serverPortTemp, userNameTemp, passwordTemp);
    }

    /**
     * CKIP connect.
     *
     * @param sentence Segment
     * @return object
     */
    public ArrayList<Tuple<String, String>> seg(final String sentence) {
        logger.info("sentence: " + sentence);
        ArrayList<Tuple<String, String>> result = new ArrayList<Tuple<String, String>>();
        connection.setRawText(sentence);
        connection.send();
        for (Term t : connection.getTerm()) {
            Tuple<String, String> pair = new Tuple<String, String>(t.getTerm(), t.getTag());
            result.add(pair);
        }
        logSegments(result);
        return result;
    }

    /**
     * Log segmentation result.
     * @param wsResult segmentation result
     */
    private void logSegments(final ArrayList<Tuple<String, String>> wsResult) {
        StringBuilder sb = new StringBuilder();
        sb.append("segment: [");
        wsResult.stream().forEach(s -> sb.append(s.getSegmentation() + ","));
        sb.append("]=[");
        wsResult.stream().forEach(s -> sb.append(s.getTagging() + ","));
        sb.append("]");
        logger.info(sb.toString());
    }

    /**
     * Tuple Format.
     *
     * @param <X> declare X
     * @param <Y> declare Y
     *
     */
    public static class Tuple<X, Y> {
        /**
         * X segmentation.
         */
        private X segmentation;
        /**
         * Y tagging.
         */
        private Y tagging;

        /**
         * Get Segment Word.
         * @return segmentation
         */
        public X getSegmentation() {
            return segmentation;
        }

        /**
         * Get POS Tagging.
         * @return POS
         */
        public Y getTagging() {
            return tagging;
        }

        /**
         * Pos Tagging.
         * @param x is X declare
         * @param y is Y declare
         */
        public Tuple(final X x, final Y y) {
            this.segmentation = x;
            this.tagging = y;
        }
    }
}
