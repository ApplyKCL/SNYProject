def dis_rec(rec, table):
    emp_str = """Employee ID: {}
Employee Name: {}
Job: {}
Entry Date: {}\n"""
    if table == "employee":
        print(emp_str.format(rec[0], rec[2], rec[4], rec[5]))
    elif table == "param":
        return


def dis_tb(db_cursor, mydb, table):
    cmd_str = """
        select * from {};
    """
    cmd_str = cmd_str.format(table)
    db_cursor.execute(cmd_str)

    for record in db_cursor.fetchall():
        dis_rec(record, table)

