## Author: Shaonan Hu
import databaseinit
import update_db
import loadModule
import checkvalues
import dsp_rec
import mysql.connector
from datetime import datetime
import time
import json


if __name__ == '__main__':
    # Check the init configuration
    # Could be changed later
    try:
        # Open the json file
        # dbinit.json: database name and exp time
        file = open("dbinit.json", "rt")
        json_dirc = json.loads(file.read())
        data_base_name = json_dirc["name"]
        # get expire time
        login_expire_time = int(json_dirc["time"])
    except:
        # When file is not configured
        # data_base_name -> name of your database
        # login_expire_time -> when the login expired
        data_base_name = input("Input the Database Name That You Want: ")
        login_expire_time = input("Login Expire Time in Second That You Want: ")
        data_dirc = {
            "name": data_base_name,
            "time": login_expire_time
        }
        # write to the file
        file = open("dbinit.json", "wt")
        json.dump(data_dirc, file)
        # Close the file
    file.close()
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
    # init db to set the tables
    init_db = databaseinit.db_init(mycursor, data_base_name)
    init_db.init_databases()
    mydb.database = data_base_name
    init_db.init_tb()
    del init_db
    # load the variable to
    if not checkvalues.check_emp(mycursor):
        loadModule.load_emp(mycursor, mydb)
        loadModule.load_comp(mycursor, mydb)
        loadModule.load_prompt(mycursor, mydb)
        loadModule.load_param(mycursor, mydb)
        loadModule.load_com_table(mycursor, mydb)
    #CheckValues.check_emp(mycursor)
    choice = "0"
    table_type = '*'
    table_name = {"1": "employee",
                  "2": "component",
                  "3": "param",
                  "4": "promopt"}
    start_time = 0
    flag = False
    flag_count = 0
    while choice != 'X':
        '''
            if not flag:
            flag = CheckValues.log_in(mycursor)
            start_time = time.time()
            flag_count += 1
            if flag_count > 3 and not flag:
                print("Program Terminated")
                flag_count = 0
                flag = True
                break
            continue
        flag_count = 0
        '''
        choice = input("Enter your Choice\nA. Add Employee\nB. Add Component\nD. Delete Database\
           \nE. To Display Values\nX.To terminate\nInput: ")
        #end_time = time.time()
        #if (end_time - start_time) > login_expire_time:
        #    print("Time Expire, please Sign in again")
        #    flag = False
        #D    continue
        # Console Interface
        if choice == 'A':
            update_db.add_emp(mycursor, mydb)
        elif choice == 'B':
            update_db.add_comp(mycursor, mydb)
        elif choice == 'D':
            update_db.delete_db(mycursor)
            break
        elif choice == 'E':
            while table_type != "#":
                table_type = str(input("Choice the table to choice\n1. Employee\n2. Component\n#. Close\n Input: "))
                if table_type == "#":
                    break
                dsp_rec.dis_tb(mycursor, mydb, str(table_name[table_type]))
        elif choice == 'X':
            print("Exit the Program\n")
        else:
            print("Please Enter the Valid Input")

mydb.close()

