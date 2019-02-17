package controllers;

import com.fasterxml.jackson.databind.JsonNode;
import database.MysqlDatabaseController;
import database.SqlObject;
import json.JSONObject;
import play.mvc.*;

/**
 * Main Controller.
 *
 * @version 1.0 2018年8月14日
 * @author Alex
 *
 */
public class MainController extends Controller {


    public Result HelloWorld() {
        return ok("HelloWorld");
    }

    /**
     * Main Controller.
     */
    public Result getUserData() {
        JsonNode request = request().body().asJson();
        JSONObject userDataJsonObject = new JSONObject(request.toString());
        String text = userDataJsonObject.getString("text");
        int value = userDataJsonObject.getInt("value");
        System.out.println(text + ":" + value);


        /*DatabaseController databaseController = new DatabaseController();
        JsonNode request = request().body().asJson();
        int id = Integer.parseInt(request.findPath(ConstantField.userAndArticleID).toString());
        int systemType = Integer.parseInt(request.findPath(ConstantField.userAndArticleSystemType).textValue());
        JsonNode result = Json.newObject();
        ResultSet resultSet = databaseController.execSelect(sqlCommandComposer.getUserDataSqlByIdAndSystemType(id, systemType));
        try {
            ResultSetMetaData resultSetMetaData = resultSet.getMetaData();
            JSONObject resultJsonObject = new JSONObject();
            if (resultSet.next()) {
                for (int i = 1; i <= resultSetMetaData.getColumnCount(); i++) {
                    Object columnValue = resultSet.getObject(i);
                    if (resultSetMetaData.getColumnTypeName(i).equals(ConstantField.databaseStringType)) {
                        resultJsonObject.put(resultSetMetaData.getColumnName(i), columnValue.toString());
                    } else if (resultSetMetaData.getColumnTypeName(i).equals(ConstantField.databaseIntType)) {
                        resultJsonObject.put(resultSetMetaData.getColumnName(i), Integer.parseInt(columnValue.toString()));
                    }
                }
            }
            result = Json.parse(resultJsonObject.toString());
        } catch (SQLException e) {
            e.printStackTrace();
        }*/
        return ok("OK");
    }
}
