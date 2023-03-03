# Author Shaonan Hu
import mysql_statement_gen as sqlgen
import config

# Define User Class
class User:
    def __init__(self, user_id: str, user_name: str, user_email: str):
        self.user_id = user_id
        self.user_name = user_name
        self.user_email = user_email


# Define the employee class, subclass of User
class Employee(User):
    def __init__(self, user_id: str, user_name: str, user_email: str, db_class: classmethod):
        super().__init__(user_id, user_name, user_email)
        self.database = db_class
        self.cursor = db_class.cursor()
        self.sql_class = sqlgen.databaseAPI(db_class=self.database, table='')

    def Emp_print(self):
        print("emp")


# Subclass of Employee
class Admin(Employee):
    def Admin_print(self):
        print("admin")


    def create_new(self):
        choice = input("Product ID [ID/N]: ")
        if choice == "N":
        return True


    #Create the new device
    def create_new_device(self):
        self.sql_class.table_name = config.table_name[config.device_position]
        device_name = input("Enter the Device Name: ")
        product_id = input("Enter the product ID: ")
        result = self.sql_class.database_operation(instruction="insert",
                                                   operate_variable=("name", "product_id"),
                                                   variable_value=(device_name, product_id))
        return result

    #Query the device with ID/No ID
    def query_device(self, product_id: str = None):
        self.sql_class.table_name = config.table_name[config.device_position]
        # Function that used to query the device information
        if product_id is not None:
            constrain_type = ("no_tp",)
            constrain_variable = ("product_id",)
            constrain_value = (product_id,)
        else:
            constrain_type = ()
            constrain_variable = ()
            constrain_value = ()
        result = self.sql_class.database_operation(instruction="select",
                                                   operate_variable=("id", "name", "product_id"),
                                                   constrain_type=constrain_type,
                                                   constrain_variable=constrain_variable,
                                                   constrain_value=constrain_value)
        return result
