package dictionary;

import constant_field.NERDictionaryConstant;

import java.io.*;

/**
 * Person and Object and Location and Time and Event and State.
 * Read Thematic role or POS Dictionary.
 *
 * @version 1.0 2018年10月30日
 * @author Alex
 *
 */
public class ReadRoleDictionary {
    /**
     * Read role dictionary.
     */
    public void setRoleDictionary() {
        try {
            // Person and Object Rule File
            readRoleDictionary(NERDictionaryConstant.PERSON_OBJECT_RULE,
                    getBufferedReader(NERDictionaryConstant.PERSON_OBJECT_RULE
                            + NERDictionaryConstant.FILE_EXTENSION));
            // Location Rule File
            readRoleDictionary(NERDictionaryConstant.LOCATION_RULE,
                    getBufferedReader(NERDictionaryConstant.LOCATION_RULE
                            + NERDictionaryConstant.FILE_EXTENSION));
            // Time Rule File
            readRoleDictionary(NERDictionaryConstant.TIME_RULE,
                    getBufferedReader(NERDictionaryConstant.TIME_RULE
                            + NERDictionaryConstant.FILE_EXTENSION));
            // Event Rule File
            readRoleDictionary(NERDictionaryConstant.EVENT_RULE,
                    getBufferedReader(NERDictionaryConstant.EVENT_RULE
                            + NERDictionaryConstant.FILE_EXTENSION));
            // Complex Event Rule File
            readRoleDictionary(NERDictionaryConstant.COMPLEX_EVENT_RULE,
                    getBufferedReader(NERDictionaryConstant.COMPLEX_EVENT_RULE
                            + NERDictionaryConstant.FILE_EXTENSION));
            // State Rule File
            readRoleDictionary(NERDictionaryConstant.STATE_RULE,
                    getBufferedReader(NERDictionaryConstant.STATE_RULE
                            + NERDictionaryConstant.FILE_EXTENSION));
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    /**
     * Read all content from a dictionary file.
     * @param reader file reader for a dictionary file
     * @param filename file name
     * @throws IOException if anything goes wrong when read dictionary file
     */
    @SuppressWarnings("unchecked")
    private void readRoleDictionary(String filename, final BufferedReader reader)
            throws IOException {
        switch (filename) {
            // Person and Object Rule Set
            case NERDictionaryConstant.PERSON_OBJECT_RULE:
                while (reader.ready()) {
                    NERDictionaryConstant.PERSON_OBJECT_RULE_SET.add(reader.readLine());
                }
                break;
            // Location Rule Set
            case NERDictionaryConstant.LOCATION_RULE:
                while (reader.ready()) {
                    NERDictionaryConstant.LOCATION_RULE_SET.add(reader.readLine());
                }
                break;
            // Time Rule Set
            case NERDictionaryConstant.TIME_RULE:
                while (reader.ready()) {
                    NERDictionaryConstant.TIME_RULE_SET.add(reader.readLine());
                }
                break;
            // Event Rule Set
            case NERDictionaryConstant.EVENT_RULE:
                while (reader.ready()) {
                    NERDictionaryConstant.EVENT_RULE_SET.add(reader.readLine());
                }
                break;
            // Complex Event Rule Set
            case NERDictionaryConstant.COMPLEX_EVENT_RULE:
                while (reader.ready()) {
                    NERDictionaryConstant.COMPLEX_EVENT_RULE_SET.add(reader.readLine());
                }
                break;
            // State Rule Set
            case NERDictionaryConstant.STATE_RULE:
                while (reader.ready()) {
                    NERDictionaryConstant.STATE_RULE_SET.add(reader.readLine());
                }
                break;
            default:
                break;
        }
    }

    /**
     * Get buffered reader for a dictionary file.
     * @param fileName dictionary full file name
     * @return a BufferedReader instance
     * @throws UnsupportedEncodingException if UTF-8 is not supported
     */
    private BufferedReader getBufferedReader(final String fileName)
            throws IOException {
        InputStream configStream = this.getClass().getResourceAsStream(
                "/resources/" + fileName);
        return new BufferedReader(new InputStreamReader(configStream, "UTF-8"));
    }
}
