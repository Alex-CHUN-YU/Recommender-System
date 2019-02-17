package ckip;

import javax.xml.bind.JAXBException;
import java.io.*;
import java.net.Socket;
import java.util.ArrayList;
import java.util.List;

/**
 * Client implementation to access ckip parser.
 *
 * @version 1.0 2017年5月19日
 * @author ken
 *
 */
public class CKIPParserClient extends ParserClient {
    /**
     * IP Address of ckip parser server.
     */
    private String ip = "140.109.19.112";
    /**
     * Port number of ckip parser server.
     */
    private int port = 8000;
    /**
     * Account for using ckip parser server.
     */
    private String account = "s10227004";
    /**
     * Password for using ckip parser server.
     */
    private String password = "10227004s";

    /**
     * Default constructor.
     */
    public CKIPParserClient() {
    }

    /**
     * Default constructor.
     * @param ip ip address of ckip parser
     * @param port port number
     * @param account account
     * @param password password
     */
    public CKIPParserClient(String ip, int port, String account, String password) {
        this.ip = ip;
        this.port = port;
        this.account = account;
        this.password = password;
    }

    /**
     * 將語句送往ckip parser進行處理,並取得回傳的結果.
     * @param sentence 一個語句,ex: 台新金控12月3日將召開股東臨時會進行董監改選
     * @return ckip parser的分析結果, 原本是一份xml文件,我們將它轉成一個Java Bean
     */
    public List parse(String sentence) {
        List<ParserResult> parserResultArrayList = new ArrayList<>();
        Socket s = createSocket();
        try (
                OutputStreamWriter osw = new OutputStreamWriter(s.getOutputStream(), "Big5");
                PrintWriter pw = new PrintWriter(osw);
                InputStreamReader isr = new InputStreamReader(s.getInputStream(), "Big5");
                BufferedReader br = new BufferedReader(isr)
                ) {
            pw.println(ParserUtil.generateXmlRequest(account, password, sentence) + "\n");
            pw.flush();
            parserResultArrayList.add(ParserUtil.xmlToResult(br.readLine()));
           return parserResultArrayList;
        } catch (IOException | JAXBException e) {
           throw new IllegalStateException(e);
        }
    }

    /**
     * Create a tcp socket.
     * @return a tcp socket
     */
    protected Socket createSocket() {
        Socket s;
        try {
            s = new Socket(this.ip, this.port);
        } catch (IOException e) {
            throw new IllegalStateException(e);
        }
        return s;
    }

    /**
     * Trouble Format.
     *
     * @param <X> declare X
     * @param <Y> declare Y
     * @param <Z> declare Z
     *
     */
    public static class Triple<X, Y, Z> {
        /**
         * SegmentWord.
         */
        private X segmentWord;
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
        public X getSegmentWord() {
            return segmentWord;
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
         * @param x is X declare
         * @param y is Y declare
         * @param z is Z declare
         */
        public Triple(final X x, final Y y, final Z z) {
            this.segmentWord = x;
            this.tagging = y;
            this.thematicRole = z;
        }
    }
}
