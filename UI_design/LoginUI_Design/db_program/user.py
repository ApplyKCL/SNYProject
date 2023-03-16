# Author Shaonan Hu
import mysql_statement_gen as sqlgen
import device_class
import config
import associative_func as af


# -> login -> database have queried if the user exist
# -> check function -> user info
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
        """
        db_class: database connector class
        """
        # Employee Info
        self.database = db_class
        self.cursor = db_class.cursor()
        self.sql_class = sqlgen.databaseAPI(db_class=self.database, table='')
        self.dev_context: device_class.DeviceContext = device_class.DeviceContext(context_id=0)

    def Emp_print(self):
        print("emp")


# Subclass of Employee
class Admin(Employee):
    # Create a new Instruction
    def register_user(self, user_name, user_job, user_email, account_number, password, admin_status=False):
        """
        :param user_name: Name of User
        :param user_job: Job Of User
        :param user_email: Email of User | optional
        :param account_number: Account Number, Unique
        :param password:  May Need to be Encrypted
        :param admin_status: Whether he is admin or not, default False (Not)
        :return: The result of the execution, represent how many row changes in db
        """
        # Call to check if the account number is already exit
        if self.check_account_number(account_number):
            return False
        # update the table name
        self.sql_class.table_name = config.table_name[config.employee_position]
        # Call to gen and execute sql
        result = self.sql_class.database_operation(instruction="insert",
                                                   operate_variable=("name", "job", "email",
                                                                     "account_number", "password", "admin_status"),
                                                   variable_value=(user_name, user_job, user_email, account_number,
                                                                   password, admin_status))
        if not result:
            return False
        else:
            return True

    def check_account_number(self, account_number):
        """
        :param account_number: account number for user
        :return: True or False for the correct output
        """
        self.sql_class.table_name = config.table_name[config.employee_position]
        result = self.sql_class.database_operation(instruction="select",
                                                   operate_variable=("name",),
                                                   constrain_variable=("account_number",),
                                                   constrain_type=("no_tp",),
                                                   constrain_value=(account_number,))
        if not result:
            return False
        else:
            return True

    def query_user(self):
        self.sql_class.table_name = config.table_name[config.employee_position]
        result = self.sql_class.database_operation(instruction="select",
                                                   operate_variable=("id", "name", "job", "email",
                                                                     "account_number", "password", "admin_status")
                                                   )
        if not result:
            return False
        else:
            return result

    def create_new(self):
        choice = ''
        state_index = 0
        while choice != '*':
            result = self.query_table(config.table_name[state_index])
            if not result:
                print("Missing" + config.table_print_name[state_index])
                choice = input("Create A new"+config.table_print_name[state_index]+"?[Y/N]")
                if choice != "Y":
                    return None
                insert_result = self.insert_new_value(config.table_name[state_index])
                if not insert_result:
                    print("Error Adding")
                    return None
                continue
            print(result)

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

    def insert_new_value(self, table_name):
        input_require = config.table_elements_dict[table_name].pop(0)
        input_list = input("Input"+input_require.join("\t")).split()
        result = self.sql_class.database_operation(instruction="insert",
                                                   operate_variable=tuple(input_require),
                                                   variable_value=tuple(input_list))
        if not result:
            return None
        return result

    # Create the new device
    def create_new_device(self):
        self.sql_class.table_name = config.table_name[config.device_position]
        [device_name, product_id] = input("Enter: \nDevice Name\tProduct ID")
        result = self.sql_class.database_operation(instruction="insert",
                                                   operate_variable=("name", "product_id"),
                                                   variable_value=(device_name, product_id))
        if not result:
            return False
        result = self.query_device()
        return result

    def query_table(self, table_name, read_id: int = None, db_check_colm: tuple = ("*",)):
        if table_name not in config.table_name:
            return None
        if not af.check_colm(list(db_check_colm), config.table_elements_dict[table_name]):
            return None
        self.sql_class.table_name = table_name
        if read_id is not None:
            constrain_type = ("no_tp",)
            constrain_variable = ("id",)
            constrain_value = (read_id,)
        else:
            constrain_type = ()
            constrain_variable = ()
            constrain_value = ()
        result = self.sql_class.database_operation(instruction="select",
                                                   operate_variable=db_check_colm,
                                                   constrain_type=constrain_type,
                                                   constrain_variable=constrain_variable,
                                                   constrain_value=constrain_value)
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
        if choice == "N":
            return None
        dev_choice = dev_list[int(choice) - 1]
        self.device_class_assign(dev_choice)
        print("""
        The Device is:
        {}
        """.format(af.display_dev(self.dev_choice)))

    def device_class_assign(self, dev_choice: list):
        device = device_class.Device(id=dev_choice[0],
                                     device_name=dev_choice[1],
                                     product_id=dev_choice[2])
        self.dev_context.DeviceClass = device
