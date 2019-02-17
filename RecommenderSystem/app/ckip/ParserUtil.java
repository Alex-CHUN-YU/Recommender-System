//
// Source code recreated from a .class file by IntelliJ IDEA
// (powered by Fernflower decompiler)
//

package ckip;

import generictree.Tree;
import java.io.ByteArrayInputStream;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import java.util.Map;
import javax.xml.bind.JAXBContext;
import javax.xml.bind.JAXBException;
import javax.xml.bind.Unmarshaller;
import org.eclipse.persistence.jaxb.JAXBContextFactory;

public class ParserUtil {
    private static final String XML_REQ_FORMAT = "<?xml version=\"1.0\" ?><wordsegmentation version=\"0.1\"><option showcategory=\"1\" /><authentication username=\"%s\" password=\"%s\" /><text>%s</text></wordsegmentation>";

    public ParserUtil() {
    }

    public static ParserResult xmlToResult(String xml) throws JAXBException {
        new ParserResult();
        InputStream stream = new ByteArrayInputStream(xml.getBytes(StandardCharsets.UTF_8));
        JAXBContext jaxbContext = JAXBContextFactory.createContext(new Class[]{ParserResult.class}, (Map)null);
        Unmarshaller jaxbUnmarshaller = jaxbContext.createUnmarshaller();
        return (ParserResult)jaxbUnmarshaller.unmarshal(stream);
    }

    public static String generateXmlRequest(String account, String password, String sentence) {
        String s = String.format("<?xml version=\"1.0\" ?><wordsegmentation version=\"0.1\"><option showcategory=\"1\" /><authentication username=\"%s\" password=\"%s\" /><text>%s</text></wordsegmentation>", account, password, sentence);
        return s;
    }

    public static Tree<Term> taggedTextToTermTree(String text) {
        TermTreeConverter converter = new TermTreeConverter(text);
        return converter.convert();
    }
}
