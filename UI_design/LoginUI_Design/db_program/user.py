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

    def update_step_context(self, table_colm: list, table_name):
        if table_name == config.table_name[config.device_position]:
            self.dev_context.DeviceClass.update_elements_list(table_colm)
        elif table_name == config.table_name[config.comp_position]:
            self.dev_context.CompClass.update_elements_list(table_colm)
        elif table_name == config.table_name[config.inst_position]:
            self.dev_context.InstClass.update_elements_list(table_colm)
        elif table_name == config.table_name[config.step_position]:
            self.dev_context.StepClass.update_elements_list(table_colm)
        elif table_name == config.table_name[config.param_position]:
            self.dev_context.ParamClass.update_elements_list(table_colm)

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
                self.update_step_context(config.table_name[config.data_position],
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
        context_id_list = self.update_step_context_list()
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
            # The first step is always query the device to check which device that user should be work on
            if state_index == 0:
                value_type = None
                value = None
                rtn_colm = tuple(config.table_elements_dict[config.table_name[config.device_position]])
                table_name = config.table_name[config.device_position]
            # else, based on the selected device to query the associate table to check if there has available
            # component
            else:
                value_type = tuple(
                    config.table_elements_dict[config.table_name[config.aso_step_position]][1:state_index+1])
                value = tuple(context_id_list[0:state_index])
                rtn_colm = (config.table_elements_dict[config.table_name[config.aso_step_position]][state_index + 1],)
                table_name = config.table_name[config.aso_step_position]
                # Should be always return serious of ID
            result = self.query_table(table_name=table_name,
                                      rtn_colm=rtn_colm,
                                      value_type=value_type,
                                      value=value)
            if config.debug_flag == 1:
                print(f"---Query_Table---{config.table_name[config.aso_step_position]}")
                print(result)
                print("---------------------------------------------------------------")
            # This checked if the rec is empty
            if result is None or result[config.table_exe_result][0][0] is None:
                # if missing
                print("Missing " + config.table_print_name[state_index])
                choice = input("Create A new " + config.table_print_name[state_index] + "?[Y/N]")
                if choice != "Y":
                    return None
                insert_result = self.insert_new_values(config.table_name[state_index])
                if insert_result is None:
                    print("Error Adding")
                    return None
                if not state_index:
                    config.aso_step_insert_flag = True
                else:
                    config.aso_step_insert_flag = False
                insert_result = self.query_table(table_name=config.table_name[state_index],
                                                 value_type=("id",),
                                                 value=(insert_result[config.table_exe_id],))
                self.update_step_context(table_colm=insert_result[config.table_exe_result][0],
                                         table_name=config.table_name[state_index])
                print(self.dev_context.DeviceClass.id)
                context_id_list = self.update_step_context_list()
                print(context_id_list)
                aso_result = self.insert_update_aso(types="step", db_context=tuple(context_id_list))
                self.dev_context.id = aso_result[config.table_exe_id]
                state_index += 1
                if config.debug_flag == 1:
                    print("---Query_Table_Context---")
                    print(context_id_list)
                    print("------------------------")
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
            record_list = []
            if choice == '1':
                if state_index == 0:
                    for index in range(0, len(result[config.table_exe_result])):
                        record_list.append(result[config.table_exe_result][index])
                    print(record_list)
                else:
                    for index in range(0, len(result[config.table_exe_result])):
                        if config.debug_flag == 1:
                            print(f"-----------Choice: {config.table_name[state_index]}----------")
                            print(config.table_name[state_index])
                            print(result[config.table_exe_result][index])
                            print("-------------------------------------------------------------")
                        query_result = self.query_table(table_name=config.table_name[state_index],
                                                        value_type=("id",),
                                                        value=result[config.table_exe_result][index])
                        if config.debug_flag == 1:
                            print(f"-----Choice Result: {config.table_name[state_index]}----------------------------")
                            print(query_result)
                            print("-------------------------------------------------------------")
                selection = self.choose_row(config.table_name[state_index], record_list)
                if config.debug_flag == 1:
                    print("------------------------Choice Return--------------------")
                    print(f"---------------------{selection}------------------------")
                    print("---------------------------------------------------------")
                if not state_index:
                    config.aso_step_insert_flag = True
                else:
                    config.aso_step_insert_flag = False
                self.update_step_context(table_colm=selection, table_name=config.table_name[state_index])
                print(self.dev_context.DeviceClass.id)
                context_id_list = self.update_step_context_list()
                print(context_id_list)
                aso_result = self.insert_update_aso(types="step", db_context=tuple(context_id_list))
                if aso_result is None:
                    print("fatal: Error Update Associate Table")
                    return None
                state_index += 1
            elif choice == '2':
                pass
            else:
                print("Exit")
            print(result)

    def insert_new_values(self, table_name):
        # Insert Aso Function May Added
        input_require = list(tuple(config.table_elements_dict[table_name]))
        input_require.pop(0)
        input_list = input("\tInput\n" + "\t".join(tuple(input_require)) + "\n").split(" ")
        self.sql_class.table_name = table_name
        result = self.sql_class.database_operation(instruction="insert",
                                                   operate_variable=tuple(input_require),
                                                   variable_value=tuple(input_list))
        if result is None:
            print("Cannot Write")
            return None
        # Return the Correct Result
        return result

    # Update the table
    def insert_update_aso(self, types="step", db_context=None):
        # In here, should update the aso table based on the step
        if db_context is None:
            return None
        # insert the step table
        if types == "step":
            self.sql_class.table_name = config.table_name[config.aso_step_position]
            operate_variable = list(tuple(config.table_elements_dict[config.
                                          table_name[config.aso_step_position]]))
        elif types == "pro":
            self.sql_class.table_name = config.table_name[config.aso_pro_position]
            operate_variable = list(tuple(config.table_elements_dict[config.
                                          table_name[config.aso_pro_position]]))

        else:
            return None
        operate_variable.pop(0)
        operate_variable = tuple(operate_variable)
        if config.aso_step_insert_flag:
            result = self.sql_class.database_operation(instruction="insert",
                                                       operate_variable=operate_variable,
                                                       variable_value=tuple(db_context))
        else:
            result = self.sql_class.database_operation(instruction="update",
                                                       operate_variable=operate_variable,
                                                       variable_value=tuple(db_context),
                                                       constrain_type=("no_tp",),
                                                       constrain_variable=("id",),
                                                       constrain_value=(self.dev_context.id,))
        print(result)
        return result

    def query_table(self, table_name: str = None, rtn_colm: tuple = ("*",), value_type: tuple = None,
                    value: tuple = None):
        if config.debug_flag == 1:
            print("------__query_table__------")
            print("---------__DEBUG__---------")
            print(f"Table Name: {table_name}")
            print(f"Return Colm: {rtn_colm}")
            print(f"Value Type: {value_type}")
            print(f"Value: {value}")
            print("---------------------------")
        # Table Name can not be empty
        if table_name is None:
            print("fatal: missing Table Name")
            return None
        # Avoid "*" in the [0] position
        if "*" in rtn_colm and len(rtn_colm) != 1:
            print("fatal: invalid return query")
            return None
        # Check if the return colm in the defined database colm
        if not af.check_colm(db_check_colm=rtn_colm, db_colm=config.table_elements_dict[table_name]) and (
                rtn_colm[0] != "*"):
            print("fatal: invalid return query")
            return None
        # Constrain Condition that defined the type
        cons_cond = []
        """
        Here will be the explain of the value_type and value
        Both of them are initially set to be None, and there are met four conditions
        1. value_type = None and value = None:
        This represent to no condition/constrain been set, which means all value for 
        this table should be displayed.
        2. value_type = (t0, t1, t2), value = None:
        This is set the t0 = None and t1 = None and t2 = None, and the t0, t1, t2 do
        not have to be in the order of table colm being ordered
        3. value_type = None, value = (v0, v1, v2):
        This will set the c1 = v0 and c2 = v1 and c3 = v2 where c0 refer to first colm
        which is always id, and c1 refer to the colm of table after id, this will be in
        order of the table organized.
        4. value_type = (c3, c4, c1), value = (v0, v1, v2):
        This set c3 = v0 and c4 = v1 and c1 = v2, which is refer to the specific value
        """
        # Condition 1
        if value_type is None and value is None:
            value_type = ()
            value = ()
        # Condition 2
        elif value_type is not None and value is None:
            value = []
            for index in range(0, len(value_type)):
                value.append(None)
            value = tuple(value)
        # Condition 3
        elif value_type is None and value is not None:
            value_type = []
            for index in range(1, len(value)):
                value_type.append(config.table_elements_dict[table_name][index])
            value_type = tuple(value_type)
        # Condition 4
        else:
            if len(value_type) != len(value):
                return None
            if not af.check_colm(db_check_colm=value_type, db_colm=config.table_elements_dict[table_name]):
                return None
        if value_type != ():
            cons_cond = ["no_tp"]
            for index in range(0, len(value_type) - 1):
                cons_cond.append("and")
        cons_cond = tuple(cons_cond)
        self.sql_class.table_name = table_name
        result = self.sql_class.database_operation(instruction="select",
                                                   operate_variable=rtn_colm,
                                                   constrain_type=cons_cond,
                                                   constrain_variable=value_type,
                                                   constrain_value=value)
        return result

    def choose_row(self, table_name, row_list):
        # Get the Colm
        colm_name = config.table_elements_name_dict[table_name]
        print("Choice ID:\t" + "\t".join(tuple(colm_name)))
        print(row_list)
        af.display_row(row_list)
        choice: int = int(input("Choice: [#/0 to exit]"))
        if choice == 0:
            return None
        choice = choice - 1
        print("Select:")
        for index in range(0, len(row_list[choice])):
            print(f"{colm_name[index]}: {row_list[choice][index]}")
        return row_list[choice]

    def update_step_context_list(self):
        context_id_list = [self.dev_context.DeviceClass.id,
                           self.dev_context.CompClass.id,
                           self.dev_context.InstClass.id,
                           self.dev_context.StepClass.id,
                           self.dev_context.ParamClass.id]
        return context_id_list
