import mysql_statement_gen as sqlgen


# function that used to check the user is exist or not
def check_user(account_number, password, sql_class=sqlgen.databaseAPI):
    sql_class.database_operation(instruction="select",
                                 operate_variable=("id", "name", "email", "admin_status"),
                                 constrain_type=("no_tp", "and"),
                                 constrain_variable=("account_number", "password"),
                                 constrain_value=(account_number, password))
    return None