# Author Shaonan Hu
import mysql_statement_gen as sqlgen
import device_class
import config
import associative_func as af


# Define User Class
class User:
    def __init__(self, user_id: str, user_name: str, user_email: str):
        # User Info
        self.user_id = user_id
        self.user_name = user_name
        self.user_email = user_email


# Define the employee class, subclass of User
class Employee(User):
    def __init__(self, user_id: str, user_name: str, user_email: str, db_class: classmethod):
        super().__init__(user_id, user_name, user_email)
        # Employee Info
        self.database = db_class
        self.cursor = db_class.cursor()
        self.sql_class = sqlgen.databaseAPI(db_class=self.database, table='')
        self.dev_class = None

    def Emp_print(self):
        print("emp")


# Subclass of Employee
class Admin(Employee):
    # Create a new Instruction
    def create_new(self):
        # Query if there has the device in DB
        device = self.query_device()
        # If no, create by user
        if not device:
            device = self.create_new_device()
            # Check if device create successfully
            if not device:
                return False
        # list all device
        device_list = af.device_list_append(device)
        if not device_list:
            return False
        # choose the device
        self.choose_device(device_list)

    # Create the new device
    def create_new_device(self):
        self.sql_class.table_name = config.table_name[config.device_position]
        device_name = input("Enter the Device Name: ")
        product_id = input("Enter the product ID: ")
        result = self.sql_class.database_operation(instruction="insert",
                                                   operate_variable=("name", "product_id"),
                                                   variable_value=(device_name, product_id))
        if not result:
            return False
        result = self.query_device()
        return result

    # Query the device with ID/No ID
    def query_device(self, dev_id: int = None):
        self.sql_class.table_name = config.table_name[config.device_position]
        # Function that used to query the device information
        if dev_id is not None:
            constrain_type = ("no_tp",)
            constrain_variable = ("id",)
            constrain_value = (dev_id,)
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

    def choose_device(self, dev_list):
        for index in range(0, len(dev_list)):
            af.display_dev(dev_list[index])
        choice: str = input("Device ID [ID/N]: ")
        if choice is "N":
            self.dev_class = None
        self.dev_class = dev_list[int(choice) - 1]
        print("""
        The Device is:
        {}
        """.format(af.display_dev(self.dev_class)))


