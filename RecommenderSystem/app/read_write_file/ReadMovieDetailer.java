package read_write_file;

import constant_field.DatabaseConstant;
import database.MysqlDatabaseController;

import java.sql.ResultSet;
import java.sql.SQLException;

/**
 * 主要用來讀取資料庫電影相關資訊的類別.
 */
public class ReadMovieDetailer {
    /**
     * Movie Name, link, storyline.
     */
    public String name = "", link = "", storyline = "";
    /**
     * Constructor.
     */
    public ReadMovieDetailer(String movieID) {
        MysqlDatabaseController mysqlDatabaseController = new MysqlDatabaseController();
        ResultSet resultSet = mysqlDatabaseController.execSelect( DatabaseConstant.MOVIE_NAME + "," +
                DatabaseConstant.MOVIE_LINK + "," + DatabaseConstant.STORYLINE, DatabaseConstant.MOVIES
                , DatabaseConstant.ID + "=" + movieID);
        try {
            if (resultSet.next()) {
                this.name = resultSet.getString(1);
                this.link = resultSet.getString(2);
                this.storyline = resultSet.getString(3);
            }
        } catch (SQLException e) {
            System.out.print(e.getErrorCode());
        }
    }
    /**
     * Get Movie Name.
     */
    public String getName() {
        return name;
    }
    /**
     * Get Movie Link.
     */
    public String getLink() {
        return link;
    }
    /**
     * Get Storyline.
     */
    public String getStoryline() {
        return storyline;
    }
}
