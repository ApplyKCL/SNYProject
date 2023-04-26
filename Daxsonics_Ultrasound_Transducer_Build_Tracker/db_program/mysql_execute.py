# Author Shaonan Hu
# This may not use
def execute_mysql(mydb, cmd_str, execution_type):
    mydb.cursor().execute(cmd_str)
    # mydb.commit()