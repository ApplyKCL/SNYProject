"""
Author: Shaonan Hu
Description: Used to query the user status
Last Update: March 31
"""
import mysql_statement_gen as sqlgen
import config
import sys


# Function used to query the admin
def query_admin(sql_class: sqlgen.databaseAPI):
    """
    :param sql_class:
    :return: query result
    """
    result = sql_class.database_operation(instruction="select",
                                          operate_variable=("*",),
                                          constrain_type=("no_tp",),
                                          constrain_variable=("admin_status",),
                                          constrain_value=(1,))
    # print(result)
    return result


# function that used to check the user is exist or not
def check_user(account_number: str, password: str, sql_class: sqlgen.databaseAPI):
    # Get the operation to read the information from the database
    """
    :param account_number: Account Number -> Str
    :param password: Password -> Str
    :param sql_class: databaseAPI class
    :return: The user exist in the database
    """
    result = sql_class.database_operation(instruction="select",
                                          # Admin Status: True (1) or False (0)
                                          operate_variable=("*",),
                                          constrain_type=("no_tp", "and"),
                                          constrain_variable=("account_number", "password"),
                                          constrain_value=(account_number, password))
    if not result or result[config.table_exe_result] == [] or result[config.table_exe_changed]<= 0:
        # print(f'Account Number or Password is not correct')
        return None
    # print(f'Welcome {result[config.table_exe_result][0][1]}')
    return list(result[config.table_exe_result][0])


# Function that used to register the admin
def register_admin(sql_class: sqlgen.databaseAPI):
    """
    :param sql_class:
    :return: the database insert result
    """
    input_list = []
    # Display the employee table elements name
    # print(config.table_elements_dict[config.table_name[config.employee_position]][1:])
    # for loop that used to let the user to input the information
    for index in range(1, len(config.table_elements_dict[config.table_name[config.employee_position]]) - 2):
        # Append the input
        input_list.append(input(f"{config.table_elements_dict[config.table_name[config.employee_position]][index]}: "))
    if len(input_list) != (len(config.table_elements_dict[config.table_name[config.employee_position]][1:]) - 2):
        sys.exit()
    # Append the status
    input_list.append(True)
    input_list.append(True)
    # Insert the info to the database
    result = sql_class.database_operation(instruction="insert",
                                          operate_variable=tuple(
                                              config.table_elements_dict[config.table_name[config.employee_position]][
                                              1:]),
                                          variable_value=tuple(input_list))
    if result is None:
        sys.exit()
    return result


# Function used for check the user and Log in
def admin_console_check_user(db_class):
    # choice = ''
    print("Welcome to Tracker Admin Console\nPlease Login")
    # Input account number
    account_number = input("Account Number: ")
    # Password
    password = input("Password: ")
    # Check if the user is exit
    user_chk_result = check_user(account_number=account_number,
                                 password=password,
                                 sql_class=sqlgen.databaseAPI(db_class=db_class,
                                                              table=config.table_name[
                                                                  config.employee_position]))

    if user_chk_result is None:
        print("fatal: Incorrect Account Number or Password")
        choice = input("Try Again [Y/Other to Exit]")
        # Let the user to login again
        if choice == "Y":
            return None
        else:
            config.login_flag = 1
            return None
    # Check is the user is admin or not
    # print(user_chk_result)
    if not user_chk_result[len(user_chk_result) - 1] \
            or not user_chk_result[len(user_chk_result) - 2]:
        print("fatal: No Authority")
        choice = input("Try Again [Y/Other to Exit]")
        if choice == "Y":
            return None
        else:
            config.login_flag = 1
            return None
    return user_chk_result
