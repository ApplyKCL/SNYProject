"""
Author: Shaonan Hu
Description: Backdoor program for the admin,
"""
import mysql.connector
from datetime import datetime
import mysql_execute
import config_table
import config
import mysql_statement_gen
import sys
import user
import check_user as chk_user
# No Bug Prey, just ignore it :>
print("""
-------------------------------NO!-------------------------------------
-------------------------------BUG-------------------------------------
-----------------------------PLEASE!-----------------------------------
""")
"""
This is Admin Console that could be used for the Admin, which is also a
Backdoor function that used for test purpose or the data written purpose.
You cannot operate the database workflow without the data loaded.
Well, the more smart idea is to written a load module for load all of the
test data rather than manually input it. BBBBBut, the mean to exist this
is to give client a reference that how to writen the workflow page
info to the database.
In addition, it should be run once is this operated as a admin machine which
is where the database are.
Furthermore, the database initial file is in json\dbinit.json
"""

if __name__ == '__main__':
    # Display the data
    print("Date:", (datetime.now()).strftime("%d/%m/%y %H:%M:%S"))
    # database infor, will be considered to be treated as file
    # STEP 1
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="215046Aa."
    )

    # mycursor the cursor of the mysql connector api func
    mycursor = mydb.cursor()
    cmd_str = """
        create database if not exists DaxsonicsBuildTrackDB
    """
    mysql_execute.execute_mysql(mydb, cmd_str, 0)
    # Database Name
    mydb.database = "DaxsonicsBuildTrackDB"
    config_table.create_table(mycursor, mydb)
    choice: str = "#"
    # Check if the admin exist or not
    if chk_user.query_admin(sql_class=mysql_statement_gen.databaseAPI(db_class=mydb,
                                                                      table=config.table_name[
                                                                          config.employee_position])) is None:
        # Not to register the admin
        admin_create_choice = input("First Use the System. Register Admin ? [Y/other exit]: ")
        if admin_create_choice != "Y":
            print("System Terminate")
            sys.exit()
        # Check if the admin is exist or not
        register_result = chk_user.register_admin(sql_class=mysql_statement_gen.databaseAPI(db_class=mydb,
                                                                                            table=config.table_name[
                                                                                                config.employee_position]))
        if register_result is None:
            sys.exit()

    barcode = "888888"
    while choice != "*":
        # if user is not login
        if not config.login_flag:
            # Check the user login
            user_chk_result = chk_user.admin_console_check_user(mydb)
            # Change the login status if the user login
            if user_chk_result is None and not config.login_flag:
                continue
            elif user_chk_result is None and config.login_flag:
                sys.exit()
            # Create the admin the status
            admin = user.Admin(user_id=user_chk_result[0],
                               user_name=user_chk_result[1],
                               user_email=user_chk_result[3],
                               db_class=mydb)
            config.login_flag = 1
        else:
            # Testing Purpose to avoid the repeatedly login
            admin = user.Admin(user_id=1,
                               user_name="Shaonan Hu",
                               user_email="Do not Care",
                               db_class=mydb)
        choice = input("Please Input Your Choice:\n1. Create the New Procedure\n2. Input Barcode and start to write.")
        # Choice 1 to create a new procedure
        if choice == '1':
            create_result = admin.create_new()
            if create_result is None:
                # Close the system
                sys.exit()
        elif choice == '2':
            # Check if the barcode exist

            # If not, return "NEW"
            read_result = admin.barcode_context(barcode=barcode)
            print(read_result)
            if read_result == "NEW":
                # Try to create the new process
                rec = admin.create_new_process(barcode=barcode)
                print(rec)
            barcode = "next"
mydb.close()
