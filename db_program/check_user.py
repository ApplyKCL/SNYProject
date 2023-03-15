import mysql_statement_gen as sqlgen


# function that used to check the user is exist or not
def check_user(account_number: str, password: str, sql_class: sqlgen.databaseAPI):
    # Get the operation to read the information from the database
    """
    :param account_number: Account Number -> Str
    :param password: Password -> Str
    :param sql_class: databaseAPI class
    :return:
    """
    result = sql_class.database_operation(instruction="select",
                                          # Admin Status: True (1) or False (0)
                                          operate_variable=("id", "name", "email", "admin_status"),
                                          constrain_type=("no_tp", "and"),
                                          constrain_variable=("account_number", "password"),
                                          constrain_value=(account_number, password))
    if not result:
        return False
    return list(result[0])
