# Author Shaonan Hu
import mysql_statement_gen as sqlgen
class User:
    def __init__(self, account_number, password):
        self.account_number = account_number
        self.password = password

    def check_admin(self, myclass):
        return False