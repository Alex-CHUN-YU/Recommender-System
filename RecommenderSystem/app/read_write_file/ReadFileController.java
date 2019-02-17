package read_write_file;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.UnsupportedEncodingException;
import java.util.ArrayList;
import java.util.List;

/**
 * Read Dictionary.
 *
 * @version 1.0 2017年9月11日
 * @author Alex
 *
 */
public class ReadFileController {
    /**
     * Line List.
     */
    private List<String> lineList;

    /**
     * Constructor.
     * @param fileName file name
     * @throws IOException if anything goes wrong when read dictionary file
     */
    public ReadFileController(final String fileName) throws IOException {
        lineList = new ArrayList<String>();
        BufferedReader bufferedReader =
                getBufferedReader(fileName);
        while (bufferedReader.ready()) {
            lineList.add(bufferedReader.readLine());
        }
    }

    /**
     * Get buffered reader for a dictionary file.
     * @param fileName dictionary full file name
     * @return a BufferedReader instance
     * @throws UnsupportedEncodingException if UTF-8 is not supported
     */
    private BufferedReader getBufferedReader(final String fileName)
            throws UnsupportedEncodingException {
        InputStream configStream = Thread.currentThread().
                getContextClassLoader().getResourceAsStream(fileName);
        return new BufferedReader(new InputStreamReader(configStream, "UTF-8"));
    }

    /**
     * Get Line List.
     * @return line
     */
    public List<String> getLineList() {
        return lineList;
    }

    /**
     * Get Line String.
     * @return line
     */
    public String getLine() {
        return lineList.get(0);
    }
}
