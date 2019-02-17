
import database.MysqlDatabaseController;
import database.SqlObject;

import java.sql.ResultSet;
import java.sql.SQLException;

/**
 * Database(Insert, Select, Delete, Update) BasicNERTest Function.
 */
public class DataBaseTest {
    /**
     * Create Mysql Connection.
     */
    private static MysqlDatabaseController mysqlDatabaseController = new MysqlDatabaseController();

    public static void main(String[] args) throws SQLException {
        insertData();
        selectData();
        deleteData();
        updateData();
        mysqlDatabaseController.closeConnection();
    }

    /**
     * Insert Data BasicNERTest.
     */
    private static void insertData() {
        SqlObject sqlObject = new SqlObject();
        sqlObject.addSqlObject("value", "100999");
        sqlObject.addSqlObject("id", "17");
        sqlObject.addSqlObject("text", "insert test");
        mysqlDatabaseController.execInsert("test", sqlObject);
    }

    /**
     * Select Data BasicNERTest.
     */
    private static void selectData() throws SQLException {
        ResultSet result = mysqlDatabaseController.execSelect("id, text", "test", "value=100999");
        while (result.next()) {
            System.out.print(result.getString(1));
            System.out.println(result.getString(2));
        }
    }

    /**
     * Delete Data BasicNERTest.
     */
    private static void deleteData() throws SQLException {
        mysqlDatabaseController.execDelete("test", "id = 28");
    }

    /**
     * Update Data BasicNERTest.
     */
    private static void updateData() throws SQLException {
        SqlObject sqlObject = new SqlObject();
        sqlObject.addSqlObject("value", "0");
        sqlObject.addSqlObject("text", "this is a update test");
        mysqlDatabaseController.execUpdate("test", sqlObject, "id = 17");
    }
}
