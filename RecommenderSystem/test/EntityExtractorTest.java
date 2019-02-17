import nlp.ArticleClassification;

import java.io.IOException;

/**
 * Relation Feature Generation Model.
 * @version 1.0 2018年10月28日
 * @author Alex
 *
 */
public class EntityExtractorTest {
    public static void main(String[] args) {
        try {
            ArticleClassification articleClassification = new ArticleClassification();
            articleClassification.titleClassification();
        } catch (IOException e) {
            System.out.println(e.toString());
        }
    }
}
