# Author Shaonan Hu
import mysql_statement_gen as sql_generator
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
        self.sql_class = sql_generator.databaseAPI(db_class=self.database, table='')
        self.dev_context: device_class.DeviceContext = device_class.DeviceContext(context_id=0)

    def update_object_context(self, table_colm: list, table_name):
        if table_name == config.table_name[config.device_position]:
            self.dev_context.DeviceClass.update_elements_list(table_colm)
        elif table_name == config.table_name[config.comp_position]:
            self.dev_context.CompClass.update_elements_list(table_colm)
        elif table_name == config.table_name[config.inst_position]:
            print("2")
        elif table_name == config.table_name[config.step_position]:
            print("2")
        elif table_name == config.table_name[config.param_position]:
            print("2")
        elif table_name == config.table_name[config.employee_position]:
            print("2")
        elif table_name == config.table_name[config.process_position]:
            print("2")
        elif table_name == config.table_name[config.device_position]:
            print("2")
        elif table_name == config.table_name[config.device_position]:
            print("2")

    def read_barcode(self, barcode: str = None):
        if barcode is None:
            return None
        self.sql_class.table_name = config.table_name[config.process_position]
        pro_result = self.sql_class.database_operation(instruction="select",
                                                       operate_variable=("*",),
                                                       constrain_variable=("barcode",),
                                                       constrain_type=("no_tp",),
                                                       constrain_value=(barcode,)
                                                       )
        if pro_result is None:
            return pro_result
        self.sql_class.table_name = config.table_name[config.aso_step_position]
        aso_step_result = self.sql_class.database_operation(instruction="select",
                                                            operate_variable=("data_id",),
                                                            constrain_variable=("emp_id", "pro_id"),
                                                            constrain_type=("no_tp", "and"),
                                                            constrain_value=(self.user_id,
                                                                             pro_result[config.table_exe_result][0]))
        if aso_step_result is None:
            return aso_step_result
        self.sql_class.table_name = config.table_name[config.data_position]
        for index in range(0, len(aso_step_result[config.table_exe_result][0])):
            data_result = self.sql_class.database_operation(instruction="select",
                                                            operate_variable=("*",),
                                                            constrain_variable=("id",),
                                                            constrain_type=("no_tp",),
                                                            constrain_value=(
                                                                aso_step_result[config.table_exe_result][0][index]))
            if data_result is None:
                return
            if data_result[config.table_exe_result][0][7] is None and data_result[config.table_exe_result][0][
                8] is None:
                self.update_object_context(config.table_name[config.data_position],
                                           data_result[config.table_exe_result][0])
                # Context Should be load here

    def data_input(self, data):
        if data is None:
            return None


# Subclass of Employee
class Admin(Employee):
    # Create a new Instruction
    # The adminst
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

    # Admin Only
    def query_user(self, constrain=(), constrain_value=(), required_value=("*",)):
        """
        :param constrain: Type of constrain "id"
        :param constrain_value: Value of Constrain
        :param required_value: Required Name that will be returned in list as order you input
        :return:
        """
        self.sql_class.table_name = config.table_name[config.employee_position]
        if constrain != ():
            constrain_type = ["no_tp"]
        else:
            constrain_type = ()
        for index in range(0, len(constrain) - 1):
            constrain_type.append("and")
        # query all
        result = self.sql_class.database_operation(instruction="select",
                                                   operate_variable=required_value,
                                                   constrain_variable=constrain,
                                                   constrain_type=constrain_type,
                                                   constrain_value=constrain_value)
        # "id", "name", "job", "email",
        # "account_number", "password", "admin_status"
        if not result:
            return False
        else:
            return result

    # Could be used in employee if it can be used
    def update_table(self, new_vale_list: list = None, old_value_list: list = None, table_name: str = None):
        if new_vale_list is None or table_name is None or old_value_list is None:
            return None
        if len(new_vale_list) != len(old_value_list):
            return None
        constrain = ["no_tp"]
        for index in range(0, len(new_vale_list) - 1):
            constrain.append("and")
        if len(constrain) != len(new_vale_list):
            return None
        # assume a data [1, 2, 3]
        # constrain np and and
        # =1 and = 2 and = 3
        self.sql_class.table_name = table_name
        result = self.sql_class.database_operation(instruction="update",
                                                   operate_variable=tuple(config.table_elements_dict[table_name]),
                                                   variable_value=tuple(new_vale_list),
                                                   constrain_type=tuple(constrain),
                                                   constrain_variable=tuple(config.table_elements_dict[table_name]),
                                                   constrain_value=tuple(old_value_list))
        if not result:
            return None
        return result

    # This is the Function that used to create the procedure
    def create_new(self):
        # Initial the choice
        choice = ''
        # Define the state index used to toggle the index
        state_index = 0
        read_id = 0
        # Get the context id and list
        context_id_list = [self.dev_context.DeviceClass.id,
                           self.dev_context.CompClass.id,
                           self.dev_context.InstClass.id,
                           self.dev_context.StepClass.id,
                           self.dev_context.ParamClass.id]
        # While loop when the choice is *, break
        while choice != '*':
            # Check the id context to see if
            """
            Three Conditions can be meet whenever create the new elements
            1. No Available record (Either the table is empty or has record but no required , GAP for colmn should be abvoid
            since, the query are in the order of the colm)
            - Once the Device Choosed, the record should be implemented and get the record number from DB
            - Every Time the Record Updated, the writen should be put, once the rec completed, the new aso rec should be
            get
                        if self.dev_context.DeviceClass.id is None:
                result = self.query_table(config.table_name[state_index], context_id_list[state_index],
                                          tuple(config.table_elements_dict[config.table_name[state_index]]))
            else:
            """
            # The Rec is empty
            # Rather than get the entire rec, it is better to like get the rec that attach to the current state
            # The state is simply what is the data type that we are operate on.
            result = self.query_table(config.table_name[config.aso_step_position], context_id_list[state_index],
                                      (config.table_elements_dict[config.table_name[config.aso_step_position]]
                                            [state_index+1],))
            print(result)
            # This checked if the rec is empty
            if result is None:
                # if missing
                print("Missing " + config.table_print_name[state_index])
                choice = input("Create A new " + config.table_print_name[state_index] + "?[Y/N]")
                if choice != "Y":
                    return None
                insert_result = self.insert_new_values(config.table_name[state_index])
                if insert_result is None:
                    print("Error Adding")
                    return None
                context_id_list[state_index] = insert_result[config.table_exe_result][0]
                # Update the context list
                # Using ID is the best solution
                self.insert_update_aso(types="step", db_context=context_id_list)
                context_id_list = [self.dev_context.DeviceClass.id,
                                   self.dev_context.CompClass.id,
                                   self.dev_context.InstClass.id,
                                   self.dev_context.StepClass.id,
                                   self.dev_context.ParamClass.id]
                continue
                # The Operation
                """
                1. Choose [Table Elements] -> Display all can be add
                2. Continue -> Load the previous edit context
                3. 
                """
            # Previous Edition
            """
            Dev
            |->Comp
                |->Inst
                    |->Step et al
            """
            choice: str = input(f"Please Input the Operation:\n"
                                f"1. Choose {config.table_print_name[state_index]}\n"
                                f"2. Add New {config.table_print_name[state_index + 1]}\n"
                                f"3. Edit Current {config.table_print_name[state_index]}"
                                f"*. Exit")
            if choice == '1':
                selection = self.choose_row(config.table_name[state_index], result[config.table_exe_result])
            elif choice == '2':
                self.insert_new_values()
            else:
                print("Exit")
            print(result)

    def insert_new_values(self, table_name):
        # Insert Aso Function May Added
        input_require = list(tuple(config.table_elements_dict[table_name]))
        input_require.pop(0)
        input_list = input("\tInput\n" + "\t".join(tuple(input_require)) + "\n").split(" ")
        print(input_list)
        self.sql_class.table_name = table_name
        result = self.sql_class.database_operation(instruction="insert",
                                                   operate_variable=tuple(input_require),
                                                   variable_value=tuple(input_list))
        if result is None:
            print("Cannot Write")
            return None

        result = self.query_table(table_name=table_name, in_cons_value=input_list, db_check_colm=input_require)
        print(f"A: {result}")
        if result is None:
            print("Cannot Read")
            return None
        print("Updated:\n" + result)
        # Return the Correct Result
        return result

    # Update the table
    def insert_update_aso(self, types="step", db_context=None):
        # In here, should update the aso table based on the step
        if db_context is None:
            return None
        if types == "step":
            operate_variable = tuple(config.table_elements_dict[config.
                                     table_name[config.aso_step_position]])
        elif types == "pro":
            operate_variable = tuple(config.table_elements_dict[config.
                                     table_name[config.aso_pro_position]])
        if self.dev_context.DeviceClass.id is None:
            result = self.sql_class.database_operation(instruction="insert",
                                                       operate_variable=operate_variable,
                                                       variable_value=tuple(db_context))
        else:
            result = self.sql_class.database_operation(instruction="update",
                                                       operate_variable=operate_variable,
                                                       variable_value=tuple(db_context),
                                                       constrain_type=("no_tp",),
                                                       constrain_variable=("id",),
                                                       constrain_value=self.dev_context.id)
        return result

    def query_table(self, table_name, in_cons_value: list = None, db_check_colm: tuple = ("*",)):
        """
        :param table_name: Table Name
        :param in_cons_value: the checked value
        :param db_check_colm: the checked data type
        :return: list of result
        """
        print(in_cons_value)
        if table_name not in config.table_name:
            print("The Table Does Not Exist")
            return None
        if not af.check_colm(list(db_check_colm), config.table_elements_dict[table_name]) and (
                len(db_check_colm) != 1 and "*" in db_check_colm):
            return None
        self.sql_class.table_name = table_name
        # id is always the fist value to check
        constrain_type = ("no_tp",)
        constrain_variable = ("id",)
        constrain_value = (in_cons_value,)
        """
        Firstly, Formalize the value list, the return value for the id from the SQL is either a id or NULL, 0 as id is
        sort of the forbidden since some of the APP does not accept 0, so should be start from 1 and NULL as Invalid.
        """
        if type(in_cons_value) is list:
            constrain_type = list(constrain_type)
            constrain_variable = list(constrain_variable)
            print(constrain_value)
            # Set the Constrain
            for index in range(1, len(in_cons_value)):
                constrain_type.append("and")
                constrain_variable.append(config.table_elements_dict["aso_step_table"][index])
            constrain_type = tuple(constrain_type)
            constrain_variable = tuple(constrain_variable)
            print(constrain_value)
        if in_cons_value is None:
            constrain_type = ()
            constrain_variable = ()
            constrain_value = ()
        result = self.sql_class.database_operation(instruction="select",
                                                   operate_variable=db_check_colm,
                                                   constrain_type=constrain_type,
                                                   constrain_variable=constrain_variable,
                                                   constrain_value=constrain_value)
        print(result)
        return result

    def choose_row(self, table_name, row_list):
        colm_name = config.table_print_name[table_name]
        colm_name.pop(0)
        print("\t".join(tuple(colm_name)))
        af.display_row(row_list)
        choice: int = input("Choice: ")
        print("Select:\n")
        af.display_row(row_list[choice])
        return row_list[choice]
