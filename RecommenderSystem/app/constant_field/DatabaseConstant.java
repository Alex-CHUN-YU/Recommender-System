package constant_field;

/**
 * Save Database Constants.
 *
 * @version 1.0 2018年8月18日
 * @author Alex
 *
 */
public class DatabaseConstant {
    // Database Initialize Setting
    public static String DATABASE_PROPERTIES = "conf/databaseConfiguration.properties";
    public static String DB_HOST = "dbHost";
    public static String DB_NAME = "dbName";
    public static String USERNAME = "userName";
    public static String PASSWORD = "password";
    // Articles Table Name
    public static String ARTICLES = "articles";
    // Column Name
    public static String ID = "id";
    public static String TITLE = "title";
    public static String CONTENT = "content";
    public static String TYPE = "relationship_type";
    // Articles Parser Table Name
    public static String ARTICLES_PARSER = "articles_parser";
    // Column Name
    public static String TITLE_PARSER_RESULT = "title_parser_result";
    public static String CONTENT_PARSER_RESULT = "content_parser_result";
    // Articles NER Table Name
    public static String ARTICLES_NER = "articles_ner";
    // Column Name
    public static String TITLE_NER = "title_ner";
    public static String CONTENT_NER = "content_ner";
    public static String CONTENT_NER_TAG = "content_ner_tag";
    public static String ARTICLE_EMOTIONS = "emotion";
    public static String ARTICLE_EVENTS = "event";
    public static String ARTICLE_PERSON_OBJECT = "person_object";
    public static String ARTICLE_TIME = "time";
    public static String ARTICLE_LOCATION = "location";
    public static String RELATION_TITLE_NER = "relation_title_ner";
    public static String RELATION_CONTENT_NER = "relation_content_ner";

    // Movies Table Name
    public static String MOVIES = "movies";
    // Column Name
    public static String STORYLINE = "storyline";
    public static String MOVIE_NAME = "name";
    public static String MOVIE_LINK = "link";
    public static String SCENARIO_TYPE = "scenario_type";
    // Movies Parser Table Name
    public static String MOVIES_PARSER = "movies_parser";
    // Column Name
    public static String STORYLINE_PARSER_RESULT = "storyline_parser_result";
    // Movies NER Table Name
    public static String MOVIES_NER = "movies_ner";
    // Column Name
    public static String MOVIES_NER_TAG = "storyline_ner_tag";
    // Column Name
    public static String STORYLINE_NER = "storyline_ner";
    public static String STORYLINE_NER_Tag = "storyline_ner_tag";
    public static String FILM_EMOTIONS = "emotion";
    public static String FILM_EVENTS = "event";
    public static String SCENARIO_NER = "scenario_ner";
}
