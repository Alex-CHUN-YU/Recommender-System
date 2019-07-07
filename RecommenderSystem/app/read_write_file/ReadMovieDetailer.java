package read_write_file;

import constant_field.DatabaseConstant;
import database.MysqlDatabaseController;
import play.db.Database;

import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;

/**
 * 主要用來讀取資料庫電影相關資訊的類別.
 */
public class ReadMovieDetailer {
    /**
     * Movie Name, link, storyline.
     */
    public String name = "", link = "", storyline = "", storylineNERTag = "";
    /**
     * Entity.
     */
    public String character = "", emotion = "", event = "", location = "", time = "";
    /**
     * Constructor.
     */
    public ReadMovieDetailer(String movieID) {
        MysqlDatabaseController mysqlDatabaseController = new MysqlDatabaseController();
        ResultSet resultSet = mysqlDatabaseController.execSelect( "a." + DatabaseConstant.MOVIE_NAME + "," +
                        "a." + DatabaseConstant.MOVIE_LINK + "," + "a." + DatabaseConstant.STORYLINE + "," + "b." +
                        DatabaseConstant.MOVIES_NER_TAG, DatabaseConstant.MOVIES + " as a, " +
                        DatabaseConstant.MOVIES_NER + " as b", "a." + DatabaseConstant.ID + "=" + movieID + " and a.id=b.id");
        try {
            if (resultSet.next()) {
                this.name = resultSet.getString(1);
                this.link = resultSet.getString(2);
                this.storyline = resultSet.getString(3);
                this.storylineNERTag = resultSet.getString(4);
            }
        } catch (SQLException e) {
            System.out.print(e.getErrorCode());
        }
//        System.out.println(this.storylineNERTag);
        setEntity();
    }
    /**
     * Set character, emotion, event, location, time.
     */
    public void setEntity() {
        this.character = "";
        this.emotion = "";
        this.event = "";
        this.location = "";
        this.time = "";
//        System.out.println(this.storylineNERTag);
        String[] sentencesList = this.storylineNERTag.split("@");
        for (int i = 0; i < sentencesList.length; i++) {
            String[] sentenceList = sentencesList[i].split(" ");
            for (int j = 0; j < sentenceList.length; j++) {
                String[] entityInformation = sentenceList[j].split(":");
//                System.out.println(sentenceList[j]);
//                System.out.println(entityInformation.length);
//                System.out.println(entityInformation);
                if (entityInformation.length == 4) {
                    if (entityInformation[1].equals("po")) {
                        if (!this.character.contains(entityInformation[0])) {
                            this.character += entityInformation[0] + " ";
                        }
                    } else if (entityInformation[1].equals("em")) {
                        if (!this.emotion.contains(entityInformation[0])) {
                            this.emotion += entityInformation[0] + " ";
                        }
                    } else if (entityInformation[1].equals("ev")) {
                        if (!this.event.contains(entityInformation[0])) {
                            this.event += entityInformation[0] + " ";
                        }
                    } else if (entityInformation[1].equals("lo")) {
                        if (!this.location.contains(entityInformation[0])) {
                            this.location += entityInformation[0] + " ";
                        }
                    } else if (entityInformation[1].equals("ti")) {
                        if (!this.time.contains(entityInformation[0])) {
                            this.time += entityInformation[0] + " ";
                        }
                    }
                }
            }
        }
    }
    /**
     * Get Character.
     */
    public String getCharacter() {
        return this.character;
    }
    /**
     * Get Emotion.
     */
    public String getEmotion() {
        return this.emotion;
    }
    /**
     * Get Event.
     */
    public String getEvent() {
        return this.event;
    }
    /**
     * Get Location.
     */
    public String getLocation() {
        return this.location;
    }
    /**
     * Get Time.
     */
    public String getTime() {
        return this.time;
    }
    /**
     * Get Movie Name.
     */
    public String getName() {
        return this.name;
    }
    /**
     * Get Movie Link.
     */
    public String getLink() {
        return this.link;
    }
    /**
     * Get Storyline.
     */
    public String getStoryline() {
        return this.storyline;
    }
}
