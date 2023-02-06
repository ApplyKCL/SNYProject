# Author Shaonan Hu
def execute_mysql(db_cursor, mydb, cmd_str, execution_type):
    db_cursor.execute(cmd_str)
    # mydb.commit()