## Author: Shaonan Hu
import mysql.connector
from datetime import datetime
import mysql_execute
import config_table
import  mysql_statement_gen
if __name__ == '__main__':
    # Display the data
    print("Date:", (datetime.now()).strftime("%d/%m/%y %H:%M:%S"))
    # database infor, will be considered to be treated as file
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
    mysql_execute.execute_mysql(mycursor, mydb, cmd_str, 0)
    mydb.database = "test_db"
    config_table.create_table(mycursor, mydb)
    choice = "0"
    table_type = '*'
    table_name = {"1": "employee",
                  "2": "component",
                  "3": "param",
                  "4": "promopt"}
    option = {
        "A": "insert",
        "B": "update",
        "C": "select",
        "D": "delete",
        "X": "abort"
    }

    start_time = 0
    flag = False
    flag_count = 0
    while choice != 'X':
        choice = input("Enter your Choice\nA. Add New\nB. Change Record\nC. Check Record\
           \nD. Delete Record\nX.To terminate\nInput: ")
        if choice == 'X':
            break
        mysql_statement_gen.generate_mysql_statement(option[choice])
mydb.close()

