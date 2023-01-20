def check_emp(db_cursor):
    cmd_str = """
            select entry_date from employee
    """
    db_cursor.execute(cmd_str)
    db_result = db_cursor.fetchall()
    if len(db_result) != 0:
        return True
    return False


def log_in(db_cursor):
    account_number = input("Enter User Account Number: ")
    password = input("Enter Password: ")
    cmd_str = "select password from employee where account_number = "
    cmd_str = cmd_str + "'" + account_number + "'"
    db_cursor.execute(cmd_str)
    db_result = db_cursor.fetchone()
    if db_result is None:
        print("Wrong Password or Username, try again")
        return False
    if password in db_result:
        print("Verification Successfully")
        return True
    print("Wrong Password or Username, try again")
    return False
