def add_emp(db_cursor, mydb):
    cmd_str = """
        alter table employee auto_increment = 1;
    """
    db_cursor.execute(cmd_str)
    cmd_str = """
        insert into employee (name, password, job, entry_date) values (%s, %s, %s, current_date())
    """
    name = input("Enter the New Employee Name: ")
    password = input("Enter the Password: ")
    job = input("Enter the Job: ")
    log_data = [name, password, job]
    db_cursor.execute(cmd_str, log_data)
    mydb.commit()


def add_comp(db_cursor, mydb):
    cmd_str = """
        alter table component auto_increment = 1;
    """
    db_cursor.execute(cmd_str)
    cmd_str = """
            insert into component (name, require_amount) values (%s, %s)
        """
    name = input("Enter the New Component Name: ")
    rq_am = input("Enter the Required Amount: ")
    update = [name, rq_am]
    cmd_str = ""
    db_cursor.execute(cmd_str, update)
    mydb.commit()


def delete_db(db_cursor):
    cmd_str = """
        drop database if exists SYNProject
    """
    print("Database Deleted")
    db_cursor.execute(cmd_str)