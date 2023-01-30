import dsp_rec
import string_function
import checkvalues


def add_emp(db_cursor, mydb):
    cmd_str = """
        alter table employee auto_increment = 1;
    """
    db_cursor.execute(cmd_str)
    cmd_str = """
        insert into employee (account_number, name, password, job, entry_date) values (%s, %s, %s, %s, current_date())
    """
    name = input("Enter the New Employee Name: ")
    password = input("Enter the Password: ")
    job = input("Enter the Job: ")
    log_data = [string_function.get_number_string(), name, password, job]
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
    db_cursor.execute(cmd_str, update)
    # Submit the changes of the data
    mydb.commit()
    while checkvalues.check_dep(db_cursor) is True:
        choice = input("Do you want to add dependency [Y/N] ?")
        if choice == "N":
            break


def delete_db(db_cursor):
    cmd_str = """
        drop database if exists SYNProject
    """
    print("Database Deleted")
    db_cursor.execute(cmd_str)

