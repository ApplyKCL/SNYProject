import json
import mysql_execute


def create_table(db_cursor, mydb):
    # Open the JSON file
    file = open("dbinit.json", "rt")
    # Read the JSON file content
    json_dirc = json.loads(file.read())
    # close file
    file.close()
    cmd_str = '\t'
    num = 0
    # For loop to go through the JSON Class and create the MYSQL Statement
    for table_index in range(0, len(json_dirc["tables"])):
        # Add the table name to the string
        cmd_str = cmd_str + "create table if not exists " + json_dirc["tables"][table_index]["table_name"] + "(\n\t"
        for statement_index in range(0, len(json_dirc["tables"][table_index]["table_elements"])):
            # Cascade each of the statement to the comment string
            cmd_str = cmd_str + "\t" + json_dirc["tables"][table_index]["table_elements"][statement_index] + "\n\t"
        cmd_str = cmd_str + ");\n\t"
        mysql_execute.execute_mysql(db_cursor, mydb, cmd_str, 0)
        cmd_str = "\t"

