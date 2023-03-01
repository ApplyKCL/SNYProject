# Author Shaonan Hu
import mysql_statement_gen as sqlgen


# Define User Class
class User:
    def __init__(self, account_number, password):
        self.account_number = account_number
        self.password = password


    def check_admin(self, myclass):
        return False


# Define the employee class, subclass of User
class Employee(User):

    def create_progess(self):
        print("create")

    def check_progress(self):
        print("check")

    def continue_progress(self):
        print("continue")


# Subclass of Employee
class Admin(Employee):
    def add_param(self):
        print("add parameter")