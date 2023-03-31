## Author: Shaonan Hu
import mysql.connector
from datetime import datetime
import mysql_execute
import config_table
import config
import mysql_statement_gen
import sys
import user
import check_user as chk_user

print("""
-------------------------------NO!-------------------------------------
-------------------------------BUG-------------------------------------
-----------------------------PLEASE!-----------------------------------
""")
"""
UI: -> Login Page -> Account Number, Password
account = text editor(-- text --) (account number )
password = text editor(-- text --) (Password)
checkuser(account, password, db_connector)
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
    mydb.database = "DaxsonicsBuildTrackDB"
    config_table.create_table(mycursor, mydb)
    # Start the transaction for solve the violation of the data
    mydb.start_transaction()
    choice: str = "#"
    if chk_user.query_admin(sql_class=mysql_statement_gen.databaseAPI(db_class=mydb,
                                                                      table=config.table_name[
                                                                          config.employee_position])) is None:
        admin_create_choice = input("First Use the System. Register Admin ? [Y/other exit]: ")
        if admin_create_choice != "Y":
            print("System Terminate")
            sys.exit()
        register_result = chk_user.register_admin(sql_class=mysql_statement_gen.databaseAPI(db_class=mydb,
                                                                                            table=config.table_name[
                                                                                                config.employee_position]))
        if register_result is None:
            sys.exit()

    while choice != "*":
        if not config.login_flag:
            user_chk_result = chk_user.admin_console_check_user(mydb)
            if user_chk_result is None and not config.login_flag:
                continue
            elif user_chk_result is None and config.login_flag:
                sys.exit()
            admin = user.Admin(user_id=user_chk_result[0],
                               user_name=user_chk_result[1],
                               user_email=user_chk_result[3],
                               db_class=mydb)
            config.login_flag = 1
        else:
            admin = user.Admin(user_id=1,
                               user_name="Shaonan Hu",
                               user_email="abcabd",
                               db_class=mydb)
        admin.create_new()
mydb.close()
