package read_write_file;

import constant_field.FileName;

import java.io.*;

/**
 * Write Data Into File.
 *
 * @version 1.0 2017年10月23日
 * @author Alex
 *
 */
public class WriteFileController {
    /**
     * Constructor.
     */
    public WriteFileController() {
        // pass
    }

    /**
     * Write Data Into File And Show Result.
     * @param fileName file name
     * @param content content
     * @throws Exception if anything goes wrong when write dictionary file
     */
    public void writeDataIntoFile(final String fileName, final String content)
            throws Exception {
        Writer f = new OutputStreamWriter(
                new FileOutputStream(FileName.RESOURCE + fileName, false),
                        "UTF-8");
        BufferedWriter bw;
        try {
            // true 是一直追加下去， false 直接覆蓋掉
            bw = new BufferedWriter(f);
            bw.write(content);
            bw.close();
            System.out.println("Successful " + fileName);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
