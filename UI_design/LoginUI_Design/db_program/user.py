# Author Shaonan Hu
import mysql_statement_gen as sqlgen
import device_class
import config
import associative_func as af


def func(happy: list = None):
    print(type(happy))
    if type(happy) is list:
        print(happy)

func([0])
func(0)
func()
func([0, 1, 2, 3, 4])
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
        # query all
        result = self.sql_class.database_operation(instruction="select",
                                                   operate_variable=("*", ))
        # "id", "name", "job", "email",
        # "account_number", "password", "admin_status"
        if not result:
            return False
        else:
            return result

    def create_new(self):
        choice = ''
        state_index = 0
        read_id = 0
        context_id_list = [self.dev_context.DeviceClass.id,
                           self.dev_context.CompClass.id,
                           self.dev_context.InstClass.id,
                           self.dev_context.StepClass.id,
                           self.dev_context.ParamClass.id]
        while choice != '*':
            if context_id_list[state_index] is None or context_id_list[state_index] == 0:
                result = self.query_table(config.table_name[state_index], context_id_list,
                                          tuple(config.table_elements_dict[config.table_name[state_index]]))
            if not result:
                print("Missing" + config.table_print_name[state_index])
                choice = input("Create A new"+config.table_print_name[state_index]+"?[Y/N]")
                if choice != "Y":
                    return None
                insert_result = self.insert_new_values(config.table_name[state_index])
                if not insert_result:
                    print("Error Adding")
                    return None
                # Update the context list
                context_id_list[state_index] = insert_result[0]
                self.insert_update_aso()
                continue
            print(result)

    def insert_new_values(self, table_name):
        # Insert Aso Function May Added
        input_require = config.table_elements_dict[table_name]
        input_require.pop(0)
        input_list = input("Input"+"\t".join(tuple(input_require))).split()
        result = self.sql_class.database_operation(instruction="insert",
                                                   operate_variable=tuple(input_require),
                                                   variable_value=tuple(input_list))
        if not result:
            print("Cannot Write")
            return None
        result = self.query_table(table_name, input_list)
        if not result:
            print("Cannot Read")
            return None
        print("Updated:\n"+result)
        # Return the Correct Result
        return result

    def insert_update_aso(self, types="step"):
        # In here, should update the aso table based on the step
        pass

    def query_table(self, table_name, values: list = None, db_check_colm: tuple = ("*",)):
        if table_name not in config.table_name:
            return None
        if not af.check_colm(list(db_check_colm), config.table_elements_dict[table_name]):
            return None
        self.sql_class.table_name = table_name
        constrain_type = ("no_tp",)
        constrain_variable = ("id",)
        constrain_value = (values,)
        if type(values) is list:
            index = 1
            constrain_type = list(constrain_type)
            constrain_variable = list(constrain_variable)
            constrain_value = list(values[0])
            if values[0] is None:
                values = 0
            while values[index] is not None:
                constrain_type.append("and")
                constrain_variable.append(config.table_elements_dict["aso_step_table"][index])
                constrain_value.append(values[index])
            constrain_type = tuple(constrain_type)
            constrain_variable = tuple(constrain_variable)
            constrain_value = tuple(constrain_value)
        if values == 0:
            constrain_type = ()
            constrain_variable = ()
            constrain_value = ()
        result = self.sql_class.database_operation(instruction="select",
                                                   operate_variable=db_check_colm,
                                                   constrain_type=constrain_type,
                                                   constrain_variable=constrain_variable,
                                                   constrain_value=constrain_value)
        return result

    def choose_row(self, table_name, row_list):
        colm_name = config.table_print_name[table_name]
        colm_name.pop(0)
        print("\t".join(tuple(colm_name)))
        af.display_row(row_list)
        choice: int = input("Choice: ")
        return row_list[choice]


