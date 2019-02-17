package database;

import java.util.ArrayList;

/**
 * 根據不同 SQL 語法所設計出來的 SQL 物件.
 *
 * @version 1.0 2017年11月01日
 * @author Alex
 *
 */
public class SqlObject {
    /**
     * Sql Object Size.
     */
    private int size;
    /**
     * Sql Object Column Name.
     */
    private ArrayList<String> columnName;
    /**
     * Sql Object Column Value.
     */
    private ArrayList<Object> columnValue;

    /**
     * Constructor.
     */
    public SqlObject() {
        columnName = new ArrayList<String>();
        columnValue = new ArrayList<Object>();
        size = 0;
    }

    /**
     * Add Sql Object (Format : Column, Value).
     * @param column column
     * @param value value
     */
    public void addSqlObject(String column, Object value) {
        if (columnName.contains(column)) {
            columnValue.add(columnName.indexOf(column), value);
            columnValue.remove(columnName.indexOf(column) + 1);
        } else {
            columnName.add(column);
            columnValue.add(value);
            size = columnName.size();
        }
    }

    /**
     * Get Sql Object Size.
     * @return size
     */
    public int getSize() {
        return size;
    }

    /**
     * Get Sql Object column Name index of your number.
     * @param i your number
     * @return size
     */
    public String getColumnNameIndexOf(int i) {
        return columnName.get(i);
    }

    /**
     * Get Every Column Name.
     * @param column column
     * @return value
     */
    public int getColumnNameIndex(String column) {
        if (columnName.contains(column)) {
            return columnName.lastIndexOf(column);
        } else {
            return -1;
        }
    }

    /**
     * Get Sql Object column Value index of your number.
     * @param i your number
     * @return value
     */
    public Object getColumnValueIndexOf(int i) {
        if (columnName.size() >= i) {
            return columnValue.get(i);
        }
        return null;
    }

    /**
     * Get All Column Name For Data Insert.
     * @return column String
     */
    public String getColumnNameString() {
        StringBuilder columnString = new StringBuilder();
        if (size != 0) {
            columnString.append(columnName.get(0));
            for (int i = 1; i < size; i++) {
                columnString.append(",");
                columnString.append(columnName.get(i));
            }
        }
        return columnString.toString();
    }

    /**
     * Get All Column Value For Data Insert.
     * @return column Prepared Statement String
     */
    public String getColumnValueString() {
        StringBuilder columnPreparedStatementString = new StringBuilder();
        if (size != 0) {
            columnPreparedStatementString.append(toSqlValue(columnValue.get(0)));
            for (int i = 1; i < size; i++) {
                columnPreparedStatementString.append(",");
                columnPreparedStatementString.append(toSqlValue(columnValue.get(i)));
            }
        }
        return  columnPreparedStatementString.toString();
    }

    /**
     * Get Column Name Value Pair String For Data Update.
     * @return column Prepared Statement String
     */
    public String getColumnNameValuePairString() {
        StringBuilder columnPreparedStatementString = new StringBuilder();
        if (size != 0) {
            columnPreparedStatementString.append(columnName.get(0));
            columnPreparedStatementString.append("=");
            columnPreparedStatementString.append(toSqlValue(columnValue.get(0)));
            for (int i = 1; i < size; i++) {
                columnPreparedStatementString.append(",");
                columnPreparedStatementString.append(columnName.get(i));
                columnPreparedStatementString.append("=");
                columnPreparedStatementString.append(toSqlValue(columnValue.get(i)));
            }
        }
        return columnPreparedStatementString.toString();
    }

    /**
     * 如果為 String 根據 sql 語法必須加上單引號.
     * @param obj obj string object or integer object
     * @return string
     */
    private String toSqlValue(Object obj) {
        if (obj.getClass() == Integer.class) {
            return obj.toString();
        } else if (obj.getClass() == String.class) {
            return "'" + obj.toString() + "'";
        } else {
            return null;
        }
    }
}