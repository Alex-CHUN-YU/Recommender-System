package dictionary;

import constant_field.NERDictionaryConstant;

import java.io.*;

/**
 * Test.
 * Read Thematic role or POS Dictionary.
 *
 * @version 1.0 2017年9月11日
 * @author Alex
 *
 */
public class ReadRoleDictionaryTest {
    /**
     * Read role dictionary.
     */
    public void setRoleDictionary() {
        try {
            // Test
            readRoleDictionary(NERDictionaryConstant.PARSER_DICTIONARY_TEST,
                    getBufferedReader(NERDictionaryConstant.PARSER_DICTIONARY_TEST
                            + NERDictionaryConstant.FILE_EXTENSION));
            readRoleDictionary(NERDictionaryConstant.POS_TAGGING_DICTIONARY_TEST,
                    getBufferedReader(NERDictionaryConstant.POS_TAGGING_DICTIONARY_TEST
                            + NERDictionaryConstant.FILE_EXTENSION));
            // Who、Action、Object、When、Where
            readRoleDictionary(NERDictionaryConstant.WHO_DICTIONARY,
                    getBufferedReader(NERDictionaryConstant.WHO_DICTIONARY
                            + NERDictionaryConstant.FILE_EXTENSION));
            readRoleDictionary(NERDictionaryConstant.ACTION_DICTIONARY,
                    getBufferedReader(NERDictionaryConstant.ACTION_DICTIONARY
                            + NERDictionaryConstant.FILE_EXTENSION));
            readRoleDictionary(NERDictionaryConstant.OBJECT_DICTIONARY,
                    getBufferedReader(NERDictionaryConstant.OBJECT_DICTIONARY
                            + NERDictionaryConstant.FILE_EXTENSION));
            readRoleDictionary(NERDictionaryConstant.WHEN_DICTIONARY,
                    getBufferedReader(NERDictionaryConstant.WHEN_DICTIONARY
                            + NERDictionaryConstant.FILE_EXTENSION));
            readRoleDictionary(NERDictionaryConstant.WHERE_DICTIONARY,
                    getBufferedReader(NERDictionaryConstant.WHERE_DICTIONARY
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
            // Test
            case NERDictionaryConstant.PARSER_DICTIONARY_TEST:
                while (reader.ready()) {
                    NERDictionaryConstant.PARSER_RULE_TEST_SET.add(reader.readLine());
                }
                break;
            case NERDictionaryConstant.POS_TAGGING_DICTIONARY_TEST:
                while (reader.ready()) {
                    NERDictionaryConstant.POS_TAGGING_RULE_TEST_SET.add(reader.readLine());
                }
                break;
            // Who、Action、Object、When、Where
            case NERDictionaryConstant.WHO_DICTIONARY:
                while (reader.ready()) {
                    NERDictionaryConstant.WHO_POS_TAGGING_RULE.add(reader.readLine());
                }
                break;
            case NERDictionaryConstant.ACTION_DICTIONARY:
                while (reader.ready()) {
                    NERDictionaryConstant.ACTION_POS_TAGGING_RULE.add(reader.readLine());
                }
                break;
            case NERDictionaryConstant.OBJECT_DICTIONARY:
                while (reader.ready()) {
                    NERDictionaryConstant.OBJECT_POS_TAGGING_RULE.add(reader.readLine());
                }
                break;
            case NERDictionaryConstant.WHEN_DICTIONARY:
                while (reader.ready()) {
                    NERDictionaryConstant.WHEN_POS_TAGGING_RULE.add(reader.readLine());
                }
                break;
            case NERDictionaryConstant.WHERE_DICTIONARY:
                while (reader.ready()) {
                    NERDictionaryConstant.WHERE_POS_TAGGING_RULE.add(reader.readLine());
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
