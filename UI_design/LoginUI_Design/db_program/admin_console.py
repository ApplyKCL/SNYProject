## Author: Shaonan Hu
import mysql.connector
from datetime import datetime
import mysql_execute
import config_table
import mysql_statement_gen
import user
import check_user as chk_user
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
        create database if not exists test_db
    """
    mysql_execute.execute_mysql(mydb, cmd_str, 0)
    mydb.database = "test_db"
    config_table.create_table(mycursor, mydb)
    choice = "0"
    table_type = '*'
    table_name = {"1": "employee",
                  "2": "component",
                  "3": "param",
                  "4": "promopt"}
    table_dirc = {
        '*': "employee_table"
    }
    # pass the database class into the function
    # Pass the database connector class to the databaseAPI class to create the database API class
    # Pass the table name (Optional)
    # STEP 2
    myclass = mysql_statement_gen.databaseAPI(mydb, "employee_table")
    start_time = 0
    flag = False
    flag_count = 0
    # Check the user if it is exist
    # STEP 3
    result = chk_user.check_user("sh258955", "123456", myclass)
    if not result:
        print("Error In Use")
    print(result)
    # [a, b, c ...., 1]
    if result[len(result) - 1] == 1:
        # STEP 4
        admin = user.Admin(user_id=result[0],
                           user_name=result[1],
                           user_email=result[2],
                           db_class=mydb)
        admin.register_user(user_name="Shaonan Hu",
                            user_job="CE",
                            user_email="sh@sb.com",
                            account_number="sh123456",
                            password="123456")
        print(admin.query_user())
        print("admin")
    else:
        print("Emp")
    """
    account_number = input("Input Account Number: ")
    password = input("Input Password: ")
    login_user = u.User(account_number, password)
    print(login_user.account_number, password)
    """
mydb.close()
