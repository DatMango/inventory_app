class MySQLRequest:
    """
    Parent class for all MySQL request classes.
    Provides a common structure for generating MySQL queries and descriptions.
    """
    def __init__(self, table_name):
        self.table_name = table_name

    def get_query(self):
        """
        Returns the MySQL query as a string.
        Must be implemented by child classes.
        """
        raise NotImplementedError("Child classes must implement the `get_query` method.")

    def get_description(self):
        """
        Returns a description of what the action does.
        Must be implemented by child classes.
        """
        raise NotImplementedError("Child classes must implement the `get_description` method.")
# hello world
class PullData(MySQLRequest):
    """
    Pulls all data from a table using a query
    """
    def __init__(self):
        #Implement
        

    def get_query(self):
        #Implement
        

    def get_description(self):
        #Implement
        

class InsertData(MySQLRequest):
    """
    Inserts a single row of data into a table.
    """
    def __init__(self):
        #Implement

    def get_query(self):
        #Implement

    def get_description(self):
        #Implement

class InsertMultipleRows(MySQLRequest):
    """
    Inserts multiple rows of data into a table.
    """
    def __init__(self, table_name, columns, values_list):
        super().__init__(table_name)
        self.columns = columns
        self.values_list = values_list

    def get_query(self):
        values_placeholders = ', '.join(['(' + ', '.join(['%s'] * len(self.columns)) + ')'] * len(self.values_list))
        return f"""
        INSERT INTO {self.table_name} ({', '.join(self.columns)})
        VALUES {values_placeholders};
        """

    def get_description(self):
        return f"Inserts multiple rows into the '{self.table_name}' table with the specified columns and values."


class UpdateData(MySQLRequest):
    """
    Updates existing data in a table based on a condition.
    """
    def __init__(self, table_name, set_values, condition):
        super().__init__(table_name)
        self.set_values = set_values
        self.condition = condition

    def get_query(self):
        set_clause = ', '.join([f"{col} = %s" for col in self.set_values.keys()])
        return f"""
        UPDATE {self.table_name}
        SET {set_clause}
        WHERE {self.condition};
        """

    def get_description(self):
        return f"Updates rows in the '{self.table_name}' table where the condition '{self.condition}' is met."


class DeleteData(MySQLRequest):
    """
    Deletes rows from a table based on a condition.
    """
    def __init__(self, table_name, condition):
        super().__init__(table_name)
        self.condition = condition

    def get_query(self):
        return f"""
        DELETE FROM {self.table_name}
        WHERE {self.condition};
        """

    def get_description(self):
        return f"Deletes rows from the '{self.table_name}' table where the condition '{self.condition}' is met."


class SelectAllData(MySQLRequest):
    """
    Selects all rows and columns from a table.
    """
    def get_query(self):
        return f"""
        SELECT * FROM {self.table_name};
        """

    def get_description(self):
        return f"Selects all rows and columns from the '{self.table_name}' table."


class SelectSpecificColumns(MySQLRequest):
    """
    Selects specific columns from a table.
    """
    def __init__(self, table_name, columns):
        super().__init__(table_name)
        self.columns = columns

    def get_query(self):
        return f"""
        SELECT {', '.join(self.columns)} FROM {self.table_name};
        """

    def get_description(self):
        return f"Selects the columns {', '.join(self.columns)} from the '{self.table_name}' table."


class FilterDataWithWhere(MySQLRequest):
    """
    Selects rows from a table based on a condition.
    """
    def __init__(self, table_name, condition):
        super().__init__(table_name)
        self.condition = condition

    def get_query(self):
        return f"""
        SELECT * FROM {self.table_name}
        WHERE {self.condition};
        """

    def get_description(self):
        return f"Selects rows from the '{self.table_name}' table where the condition '{self.condition}' is met."


class SortDataWithOrderBy(MySQLRequest):
    """
    Selects rows from a table and sorts them by a column.
    """
    def __init__(self, table_name, order_by_column, order='ASC'):
        super().__init__(table_name)
        self.order_by_column = order_by_column
        self.order = order

    def get_query(self):
        return f"""
        SELECT * FROM {self.table_name}
        ORDER BY {self.order_by_column} {self.order};
        """

    def get_description(self):
        return f"Selects rows from the '{self.table_name}' table and sorts them by '{self.order_by_column}' in {self.order} order."


class LimitResults(MySQLRequest):
    """
    Limits the number of rows returned by a query.
    """
    def __init__(self, table_name, limit):
        super().__init__(table_name)
        self.limit = limit

    def get_query(self):
        return f"""
        SELECT * FROM {self.table_name}
        LIMIT {self.limit};
        """

    def get_description(self):
        return f"Limits the results from the '{self.table_name}' table to {self.limit} rows."


class PaginateResults(MySQLRequest):
    """
    Paginates results by specifying an offset and limit.
    """
    def __init__(self, table_name, offset, limit):
        super().__init__(table_name)
        self.offset = offset
        self.limit = limit

    def get_query(self):
        return f"""
        SELECT * FROM {self.table_name}
        LIMIT {self.offset}, {self.limit};
        """

    def get_description(self):
        return f"Paginates results from the '{self.table_name}' table with an offset of {self.offset} and a limit of {self.limit}."


class DistinctValues(MySQLRequest):
    """
    Selects distinct values from a column.
    """
    def __init__(self, table_name, column_name):
        super().__init__(table_name)
        self.column_name = column_name

    def get_query(self):
        return f"""
        SELECT DISTINCT {self.column_name} FROM {self.table_name};
        """

    def get_description(self):
        return f"Selects distinct values from the '{self.column_name}' column in the '{self.table_name}' table."


class AggregateFunctions(MySQLRequest):
    """
    Performs aggregate functions (COUNT, SUM, AVG, MIN, MAX) on a column.
    """
    def __init__(self, table_name, function, column_name):
        super().__init__(table_name)
        self.function = function
        self.column_name = column_name

    def get_query(self):
        return f"""
        SELECT {self.function}({self.column_name}) FROM {self.table_name};
        """

    def get_description(self):
        return f"Performs the {self.function} function on the '{self.column_name}' column in the '{self.table_name}' table."


class GroupDataWithGroupBy(MySQLRequest):
    """
    Groups rows by a column and applies an aggregate function.
    """
    def __init__(self, table_name, group_by_column, aggregate_function, aggregate_column):
        super().__init__(table_name)
        self.group_by_column = group_by_column
        self.aggregate_function = aggregate_function
        self.aggregate_column = aggregate_column

    def get_query(self):
        return f"""
        SELECT {self.group_by_column}, {self.aggregate_function}({self.aggregate_column})
        FROM {self.table_name}
        GROUP BY {self.group_by_column};
        """

    def get_description(self):
        return f"Groups rows by '{self.group_by_column}' and applies the {self.aggregate_function} function to the '{self.aggregate_column}' column in the '{self.table_name}' table."


class FilterGroupsWithHaving(MySQLRequest):
    """
    Filters groups based on a condition after using GROUP BY.
    """
    def __init__(self, table_name, group_by_column, aggregate_function, aggregate_column, having_condition):
        super().__init__(table_name)
        self.group_by_column = group_by_column
        self.aggregate_function = aggregate_function
        self.aggregate_column = aggregate_column
        self.having_condition = having_condition

    def get_query(self):
        return f"""
        SELECT {self.group_by_column}, {self.aggregate_function}({self.aggregate_column})
        FROM {self.table_name}
        GROUP BY {self.group_by_column}
        HAVING {self.having_condition};
        """

    def get_description(self):
        return f"Groups rows by '{self.group_by_column}', applies the {self.aggregate_function} function to the '{self.aggregate_column}' column, and filters groups using the condition '{self.having_condition}' in the '{self.table_name}' table."
    
class Subquery(MySQLRequest):
    """
    Uses a subquery to filter or retrieve data.
    """
    def __init__(self, table_name, column_name, subquery):
        super().__init__(table_name)
        self.column_name = column_name
        self.subquery = subquery

    def get_query(self):
        return f"""
        SELECT * FROM {self.table_name}
        WHERE {self.column_name} = ({self.subquery});
        """

    def get_description(self):
        return f"Uses a subquery to filter rows in the '{self.table_name}' table where '{self.column_name}' matches the result of the subquery."
