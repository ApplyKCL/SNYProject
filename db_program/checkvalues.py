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


def check_dep(db_cursor):
    cmd_str = """
    select id, name, next_comp from component;
    """
    db_cursor.execute(cmd_str)
    db_result = db_cursor.fetchall()
    count = 0
    for result in db_result:
        if result[2] is None:
            print(str(result[0]) + " " + result[1] + " is the last item to build or missing dependency")
            count += 1
    print(str(count) + " Missing Item")
    if count > 0:
        return True
    return False
