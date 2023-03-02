import mysql_statement_gen as sqlgen


# function that used to check the user is exist or not
def check_user(account_number: str, password: str, sql_class: sqlgen.databaseAPI):
    # Get the operation to read the information from the database
    result = sql_class.database_operation(instruction="select",
                                          operate_variable=("id", "name", "email", "admin_status"),
                                          constrain_type=("no_tp", "and"),
                                          constrain_variable=("account_number", "password"),
                                          constrain_value=(account_number, password))
    if not result:
        return False
    result = list(result[0])
    if result[len(result)-1] == 1:
        print("AD")
    return None
