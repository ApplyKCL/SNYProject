def dis_tb(db_cursor, mydb, table='employee'):
    cmd_str = """
        select * from {};
    """
    cmd_str = cmd_str.format(table)
    db_cursor.execute(cmd_str)

    for record in db_cursor.fetchall():
        print(record)

