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
    # Inherent the features from the user class
    def __init__(self, user_id: str, user_name: str, user_email: str, db_class: classmethod):
        super().__init__(user_id, user_name, user_email)
        """
        db_class: database connector class
        sql_class: SQL generator class that has defined in mysql_statement_gen.py
        dev_context: device context that used in the admin
        accout_number_status: N/A
        process_
        """
        # Employee Info
        self.database = db_class
        self.sql_class = sql_generator.databaseAPI(db_class=self.database, table='')
        self.dev_context: device_class.DeviceContext = device_class.DeviceContext(context_id=0)
        self.accout_number_status = True
        self.process_context: device_class.ProcessContext = device_class.ProcessContext(user_id=self.user_id)

    def barcode_context(self, barcode: str = None):
        """
        :param barcode: This is the barcode that you should input in
        :return:
        """
        if barcode is None:
            return None
        if barcode == "next":
            return self.next_step()
        data_result = []
        # read the barcode from the database to check if there has an exist barcode
        self.sql_class.table_name = config.table_name[config.process_position]
        pro_result = self.sql_class.database_operation(instruction="select",
                                                       operate_variable=("*",),
                                                       constrain_variable=("barcode",),
                                                       constrain_type=("no_tp",),
                                                       constrain_value=(barcode,)
                                                       )
        # This means that there is no exist barcode in the system
        if pro_result is None:
            return "NEW"
        self.update_process_context(table_name=config.table_name[config.device_position],
                                    context_id=pro_result[config.table_exe_result][0][1])
        self.update_process_context(table_name=config.table_name[config.comp_position],
                                    context_id=pro_result[config.table_exe_result][0][2])
        self.update_process_context(table_name=config.table_name[config.process_position],
                                    context_id=pro_result[config.table_exe_result][0][0])
        # Get all of the data_id that related with the process and the user ID
        aso_pro_result = self.query_table(table_name=config.table_name[config.aso_pro_position],
                                          rtn_colm=("id", "data_id"),
                                          value_type=("emp_id", "pro_id"),
                                          value=(self.user_id,
                                                 pro_result[config.table_exe_result][0][0]))
        # Make sure there is no error in this query
        if aso_pro_result is None:
            aso_pro_result = self.query_table(table_name=config.table_name[config.aso_pro_position],
                                              rtn_colm=("id", "data_id"),
                                              value_type=("pro_id",),
                                              value=(pro_result[config.table_exe_result][0][0],))
            return self.allocate_workflow_data(value_list=aso_pro_result[config.table_exe_result])
        offset = 0
        # Check which is the latest step and the latest data or where this ID occupied
        for index in range(0, len(aso_pro_result[config.table_exe_result])):
            self.sql_class.table_name = config.table_name[config.data_position]
            data_result = self.sql_class.database_operation(instruction="select",
                                                            operate_variable=("*",),
                                                            constrain_variable=("id",),
                                                            constrain_type=("no_tp",),
                                                            constrain_value=(
                                                                aso_pro_result[config.table_exe_result][index][1],))
            if not data_result[config.table_exe_result] \
                    or data_result is None \
                    or data_result[config.table_exe_changed] <= 0:
                continue
            offset = index
            # if the data is non, load
            if data_result[config.table_exe_result][0][config.data_value_offset] is None:
                break
        self.update_process_context(table_name=config.table_name[config.aso_pro_position],
                                    context_id=aso_pro_result[config.table_exe_result][offset][0])
        if data_result is None or data_result == [] or data_result[config.table_exe_changed] <= 0:
            return None
        self.update_process_context(table_name=config.table_name[config.inst_position],
                                    context_id=data_result[config.table_exe_result][0][1])
        self.update_process_context(table_name=config.table_name[config.step_position],
                                    context_id=data_result[config.table_exe_result][0][2])
        data_list = []
        data_obj = device_class.Data()
        for query_index in range(0, len(aso_pro_result[config.table_exe_result])):
            exe_result = self.query_table(table_name=config.table_name[config.data_position],
                                          value_type=("step_id", "id"),
                                          value=(self.process_context.DataClass.StepClass.id,
                                                 aso_pro_result[config.table_exe_result][query_index][1]))
            print(exe_result)
            if exe_result is not None:
                data_obj.update_elements_list(exe_result[config.table_exe_result][0])
                data_list.append(data_obj.elements_list)
        return [self.get_page_number(), data_list]

    # Get the latest instruction or steps
    def get_latest_inst_steps(self, id_list: list = None):
        data_list = self.query_multiple_rec(table_name=config.table_name[config.data_position],
                                            query_return=("inst_id", "step_id"),
                                            query_list=id_list)
        inst_list = [(inst[0],) for inst in data_list]
        latest_inst = self.find_last_first_rec(value_rec_id=inst_list, offset=config.inst_position)[0][0]
        step_list = [(step[1],) for step in data_list if latest_inst == step[0]]
        latest_step = self.find_last_first_rec(value_rec_id=step_list, offset=config.step_position)[0][0]
        return [latest_inst, latest_step]

    def find_last_first_rec(self, value_rec_id: list = None, offset: int = config.inst_position,
                            pre_next: str = "next"):
        if config.debug_flag:
            print(f"value_id: {value_rec_id},"
                  f"offset {offset}"
                  f"position {config.inst_position}")
        if offset == config.step_position:
            rtn_colm = "_step"
        elif offset == config.param_position:
            rtn_colm = "_param"
        else:
            rtn_colm = "_inst"
        rtn_colm = pre_next + rtn_colm
        value_query = self.query_table(table_name=config.table_name[offset],
                                       rtn_colm=(rtn_colm,),
                                       value_type=("id",),
                                       value=value_rec_id[0])
        # if config.debug_flag:
        #     print(f"query_rec {value_query}")
        if value_query[config.table_exe_result][0][0] == 0 or len(value_rec_id) == 1:
            return [value_rec_id[0]]
        if value_query[config.table_exe_result][0] in value_rec_id:
            value_rec_id.pop(0)
            index = value_rec_id.index(value_query[config.table_exe_result][0])
            value_rec_id = [value_query[config.table_exe_result][0]] + value_rec_id[:index] + value_rec_id[index + 1:]
            return self.find_last_first_rec(value_rec_id=value_rec_id, offset=offset, pre_next=pre_next)
        return [value_rec_id[0]]

    def display_work_flow(self, barcode: str = None):
        get_pro_id = self.query_table(table_name=config.table_name[config.process_position],
                                      rtn_colm=("id", ),
                                      value_type=("barcode", ),
                                      value=(barcode, ))
        exist_workflow = self.query_table(table_name=config.table_name[config.aso_pro_position],
                                          rtn_colm=("data_id", ),
                                          value_type=("pro_id",),
                                          value=(get_pro_id[config.table_exe_result][0][0],))
        data_rec = self.query_multiple_rec(table_name=config.table_name[config.data_position],
                                           query_list=exist_workflow[config.table_exe_result],
                                           query_list_variable_type=("id", ))
        if data_rec is None:
            return None
        return data_rec

    def allocate_workflow_data(self, value_list: list = None):
        data_id_list = value_list
        data_id_list = [(data_id[1],) for data_id in data_id_list]
        latest_list = self.get_latest_inst_steps(id_list=data_id_list)
        next_step = self.query_table(table_name=config.table_name[config.step_position],
                                     rtn_colm=("next_step",),
                                     value_type=("id",),
                                     value=(latest_list[1],))
        next_step_id = next_step[config.table_exe_result][0][0]
        if next_step[config.table_exe_result][0][0] == 0:
            next_inst = self.query_table(table_name=config.table_name[config.inst_position],
                                         rtn_colm=("next_inst",),
                                         value_type=("id",),
                                         value=(latest_list[0],))
            if next_inst[config.table_exe_result][0][0] == 0:
                return None
            available_step = self.query_table(table_name=config.table_name[config.aso_step_position],
                                              rtn_colm=("step_id",),
                                              value_type=("inst_id",),
                                              value=(next_inst[config.table_exe_result][0][0],))
            self.update_process_context(table_name=config.table_name[config.inst_position],
                                        context_id=next_inst[config.table_exe_result][0][0])
            first_step_rec = self.find_last_first_rec(value_rec_id=available_step[config.table_exe_result],
                                                      offset=config.step_position,
                                                      pre_next="previous")[0][0]
            next_step_id = first_step_rec
        # Update the context information
        self.update_process_context(table_name=config.table_name[config.step_position],
                                    context_id=next_step_id)
        # Call the workflow distribution function
        return self.workflow_data_distribute()

    def workflow_data_distribute(self):
        param_rec = self.query_table(table_name=config.table_name[config.aso_step_position],
                                     rtn_colm=("param_id",),
                                     value_type=("step_id",),
                                     value=(self.process_context.DataClass.StepClass.id,))
        data_object_list = self.workflow_data_insert(param_list=param_rec[config.table_exe_result])
        if data_object_list is None:
            return None
        return [self.get_page_number(), data_object_list]

    def data_insert(self):
        insert_result = self.insert_value(table_name=config.table_name[config.data_position],
                                          operate_variable=("inst_id", "step_id", "param_id"),
                                          value=(self.process_context.DataClass.InstClass.id,
                                                 self.process_context.DataClass.StepClass.id,
                                                 self.process_context.DataClass.ParamClass.id))
        return insert_result

    def process_aso(self):
        insert_result = self.insert_value(table_name=config.table_name[config.aso_pro_position],
                                          operate_variable=("emp_id", "pro_id", "data_id"),
                                          value=(self.user_id,
                                                 self.process_context.ProcessClass.id,
                                                 self.process_context.DataClass.id))
        return insert_result

    def workflow_data_insert(self, param_list: list = None):
        if param_list is None:
            return None
        data_object_list = []
        for param_id in param_list:
            self.update_process_context(table_name=config.table_name[config.param_position],
                                        context_id=param_id[0])
            data_insert_result = self.data_insert()
            if data_insert_result is None:
                return None
            self.update_process_context(table_name=config.table_name[config.data_position],
                                        context_id=data_insert_result[config.table_exe_id])
            process_aso_insert_result = self.process_aso()
            if process_aso_insert_result is None:
                return None
            self.process_context.DataClass.list_elements()
            data_object_list.append(self.process_context.DataClass.elements_list)
        return data_object_list

    def get_page_number(self):
        # Create the data pages to indicate which step associated with UI the user are written to
        # Format: device_id:component_id:inst_id:step_id
        # Usually 1 step is 1 pages of the UI
        # Sometimes the 1 instruction could has multiple steps and 1 steps could have multiple data
        page_number = str(self.process_context.ProcessClass.DeviceClass.id) + ":" + \
                      str(self.process_context.ProcessClass.CompClass.id) + ":" + \
                      str(self.process_context.DataClass.InstClass.id) + ":" + \
                      str(self.process_context.DataClass.StepClass.id)
        # Return the Page Number
        return page_number

    def input_data(self, data_list: list = None):
        if data_list is None:
            return None
        for data in data_list:
            self.sql_class.table_name = config.table_name[config.data_position]
            update_result = self.sql_class.database_operation(instruction="update",
                                                              operate_variable=tuple(config.table_elements_dict[
                                                                                         config.table_name[
                                                                                             config.data_position]][
                                                                                     1:]),
                                                              variable_value=tuple(data[1:]),
                                                              constrain_type=("no_tp",),
                                                              constrain_variable=("id",),
                                                              constrain_value=(data[0],))
            if update_result is None:
                return False
        return True

    def none_check(self, query_list: dict = None):
        if query_list is None:
            return None
        null_check = self.query_multiple_rec(table_name=config.table_name[config.data_position],
                                             query_return=("value", ),
                                             query_list_variable_type=("id", ),
                                             query_list=query_list[config.table_exe_result])
        for data in null_check:
            if data[0] is None or data[0] == '':
                return False
        return True

    def check_step_status(self):
        data_list = self.query_table(table_name=config.table_name[config.aso_pro_position],
                                     rtn_colm=("data_id", ),
                                     value_type=("emp_id", "pro_id"),
                                     value=(self.user_id, self.process_context.ProcessClass.id))
        chk_value = self.none_check(data_list)
        if chk_value is None:
            return None
        return chk_value

    def check_finish_status(self):
        data_list = self.query_table(table_name=config.table_name[config.aso_pro_position],
                                     rtn_colm=("data_id",),
                                     value_type=("pro_id", ),
                                     value=(self.process_context.ProcessClass.id, ))
        chk_value = self.none_check(data_list)
        if chk_value is None:
            return None
        if chk_value:
            self.sql_class.table_name = config.table_name[config.process_position]
            update_result = self.sql_class.database_operation(instruction="update",
                                                              operate_variable=("status", ),
                                                              variable_value=(True, ),
                                                              constrain_type=("no_tp", ),
                                                              constrain_variable=("id", ),
                                                              constrain_value=(self.process_context.ProcessClass.id,))
            if update_result is None:
                return False
            return True
        return False

    # Function used to go to next step
    def next_step(self):
        if not self.check_step_status():
            return "NF"
        # At the first should
        next_step = self.query_table(table_name=config.table_name[config.step_position],
                                     rtn_colm=("next_step",),
                                     value_type=("id",),
                                     value=(self.process_context.DataClass.StepClass.id,))
        if next_step is None:
            return None
        next_step_id = next_step[config.table_exe_result][0][0]
        # This will handle with no next step situation which will query the next instruction
        if next_step[config.table_exe_result][0][0] == 0:
            # Get the next instruction
            next_inst = self.query_table(table_name=config.table_name[config.inst_position],
                                         rtn_colm=("next_inst",),
                                         value_type=("id",),
                                         value=(self.process_context.DataClass.InstClass.id,))
            if next_inst[config.table_exe_result][0][0] == 0:
                # There is no more instruction could be operated on
                return "END"
            # Update the new instruction
            self.update_process_context(table_name=config.table_name[config.inst_position],
                                        context_id=next_inst[config.table_exe_result][0][0])
            next_step = self.query_table(table_name=config.table_name[config.aso_step_position],
                                         rtn_colm=("step_id",),
                                         value_type=("inst_id",),
                                         value=(self.process_context.DataClass.InstClass.id,))

            first_step_rec_id = self.find_last_first_rec(value_rec_id=next_step[config.table_exe_result],
                                                         offset=config.step_position,
                                                         pre_next="previous")[0][0]
            next_step_id = first_step_rec_id
        self.update_process_context(table_name=config.table_name[config.step_position],
                                    context_id=next_step_id)
        return self.workflow_data_distribute()

    # The device id and the component id is actually reserved for the future design since in the future, the system
    # is possible to support the multiple device and multiple component belong to the specific component
    def update_process_context(self, table_name: str = None, context_id: int = None):
        context = self.query_table(table_name=table_name,
                                   value_type=("id",),
                                   value=(context_id,))
        if context is None:
            return False
        if table_name == config.table_name[config.device_position]:
            # Update the device context
            self.process_context.ProcessClass.DeviceClass.update_elements_list(
                context[config.table_exe_result][0])
        elif table_name == config.table_name[config.comp_position]:
            self.process_context.ProcessClass.CompClass.update_elements_list(
                context[config.table_exe_result][0])
        elif table_name == config.table_name[config.inst_position]:
            self.process_context.DataClass.InstClass.update_elements_list(
                context[config.table_exe_result][0])
        elif table_name == config.table_name[config.step_position]:
            self.process_context.DataClass.StepClass.update_elements_list(
                context[config.table_exe_result][0])
        elif table_name == config.table_name[config.param_position]:
            self.process_context.DataClass.ParamClass.update_elements_list(
                context[config.table_exe_result][0])
        elif table_name == config.table_name[config.data_position]:
            self.process_context.DataClass.update_elements_list(
                context[config.table_exe_result][0])
        elif table_name == config.table_name[config.process_position]:
            self.process_context.ProcessClass.update_elements_list(
                context[config.table_exe_result][0])
        elif table_name == config.table_name[config.aso_pro_position]:
            self.process_context.update_elements_list(
                context[config.table_exe_result][0])
        else:
            return False
        self.process_context.list_elements()
        self.process_context.ProcessClass.list_elements()
        self.process_context.DataClass.list_elements()
        return True

    # Function that used to initial the process context init the process and store it in database
    def initial_process_context(self, dev_id: int = None, comp_id: int = None, barcode: str = None):
        # Check if the id is exist or not, if not exist return None
        if dev_id is None or comp_id is None or barcode is None:
            return None
        # Assume that the device Id and the component id has already known
        check = self.update_process_context(table_name=config.table_name[config.device_position], context_id=dev_id)
        if not check:
            return None
        check = self.update_process_context(table_name=config.table_name[config.comp_position], context_id=comp_id)
        # if the check is false
        if not check:
            return None
        # Update the barcode
        self.process_context.ProcessClass.barcode = barcode
        # Change the process status to be false
        self.process_context.ProcessClass.status = False
        self.process_context.ProcessClass.list_elements()
        # initialize the process
        process_insert_result = self.insert_value(table_name=config.table_name[config.process_position],
                                                  operate_variable=tuple(
                                                      config.table_elements_dict[
                                                          config.table_name[config.process_position]][
                                                      1:]),
                                                  value=tuple(
                                                      self.process_context.ProcessClass.elements_list[
                                                      1:]))
        return process_insert_result

    def insert_value(self, table_name: str = None, operate_variable: tuple = None, value: tuple = None):
        self.sql_class.table_name = table_name
        insert_result = self.sql_class.database_operation(instruction="insert",
                                                          operate_variable=operate_variable,
                                                          variable_value=value)
        return insert_result

    # Automatically update the table context
    def update_process_context_base_on_previous(self, query_list: list = None, table_offset: int = None):
        for index in range(0, len(query_list)):
            # Query all the value in the list
            query_result = self.query_table(table_name=config.table_name[table_offset],
                                            rtn_colm=(
                                                "id", config.input_pattern[config.table_name[table_offset]][1][0],),
                                            value_type=("id",),
                                            value=(query_list[index][0],))
            # Debug information that used to show what is
            # print(f"Previous:{query_result[config.table_exe_result][0][1]}")
            # Check the Query result
            if query_result is None:
                print("fatal: NO existence query")
                return None
            if query_result[config.table_exe_result][0][1] == 0:
                self.update_process_context(table_name=config.table_name[table_offset],
                                            context_id=query_result[config.table_exe_result][0][0])
                print(f"id {query_result[config.table_exe_result][0][0]}")
                return query_result[config.table_exe_result][0][0]

    # Initial Data
    def init_data(self, device_id: int = None, comp_id: int = None):
        if device_id is None or comp_id is None:
            return None
        # Initial the offset
        table_offset = config.step_position
        variable_offset = config.step_comp_offset + 1
        check_value = [device_id, comp_id]
        while table_offset <= config.param_position + 1:
            aso_step_query_result = self.query_table(table_name=config.table_name[config.aso_step_position],
                                                     rtn_colm=(config.table_elements_dict[
                                                                   config.table_name[config.aso_step_position]][
                                                                   table_offset],),
                                                     value_type=
                                                     tuple(config.table_elements_dict[
                                                               config.table_name[config.aso_step_position]][
                                                           config.step_device_offset:variable_offset]),
                                                     value=tuple(check_value))
            if aso_step_query_result is None:
                return None
            query_list = af.remove_repeat_tuple(list(aso_step_query_result[config.table_exe_result]))
            # print("This is My Query list")
            # print(query_list)
            new_id = self.update_process_context_base_on_previous(query_list=query_list, table_offset=table_offset - 1)
            check_value.append(new_id)
            table_offset += 1
            variable_offset += 1

        return self.workflow_data_distribute()

    def create_new_process(self, barcode: str = None, device_id: int = 1, comp_id: int = 1):
        if barcode is None:
            return None
        # Since this the new set of the record, the program should be found the first step for the program
        # By getting the first rec, the better way is find the all associated table foreign key in the aso_step_table
        # can be used by the multi table selection instead, but I have no time to update my API, hope you can do this.
        # It is fine if do not want to cause it will not cause any issues
        init_proces = self.initial_process_context(dev_id=device_id, comp_id=comp_id, barcode=barcode)
        if init_proces is None:
            return None
        # When we have the new process in the process table, the next thing should be done is to initial the data
        # First we should get the step
        self.update_process_context(table_name=config.table_name[config.process_position],
                                    context_id=init_proces[config.table_exe_id])
        insert_data = self.init_data(device_id=device_id,
                                     comp_id=comp_id)
        if insert_data is None:
            return None

        return insert_data

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
        result = self.sql_class.database_operation(instruction="update",
                                                   operate_variable=tuple(config.table_elements_dict[table_name]),
                                                   variable_value=tuple(new_vale_list),
                                                   constrain_type=tuple(constrain),
                                                   constrain_variable=tuple(config.table_elements_dict[table_name]),
                                                   constrain_value=tuple(old_value_list))
        if not result:
            return None
        return result

    def query_multiple_rec(self, table_name: str = None, query_return: tuple = ("*",), query_list: list = None,
                           query_list_variable_type: tuple = ("id",)):
        if table_name is None or query_list is None:
            return None
        record_list = [
            self.query_table(table_name=table_name, rtn_colm=query_return, value_type=query_list_variable_type,
                             value=query)[config.table_exe_result][0] for query in query_list]
        return record_list

    def query_table(self, table_name: str = None, rtn_colm: tuple = ("*",), value_type: tuple = None,
                    value: tuple = None):
        # if config.debug_flag == 1:
        #     print("------__query_table__------")
        #     print("---------__DEBUG__---------")
        #     print(f"Table Name: {table_name}")
        #     print(f"Return Colm: {rtn_colm}")
        #     print(f"Value Type: {value_type}")
        #     print(f"Value: {value}")
        #     print("---------------------------")
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
                print("fatal_Debug Here")
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


# Subclass of Employee
class Admin(Employee):
    def register_user(self, user_name, user_job, user_email, account_number, password,
                      enable_status=True, admin_status=False):
        """
        :param enable_status: User is deleted or not
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
            self.accout_number_status = False
            return
        # update the table name
        self.sql_class.table_name = config.table_name[config.employee_position]
        # Call to gen and execute sql
        result = self.sql_class.database_operation(instruction="insert",
                                                   operate_variable=("name", "job", "email",
                                                                     "account_number", "password", "enable_status",
                                                                     "admin_status"),
                                                   variable_value=(user_name, user_job, user_email, account_number,
                                                                   password, enable_status, admin_status))
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
        # print(f'query_user: {constrain}, {constrain_value}, {required_value}')
        if constrain != ():
            constrain_type = ["no_tp"]
        else:
            constrain_type = ()
        for index in range(0, len(constrain) - 1):
            constrain_type.append("and")
        # query all
        # print(f'value is good')
        result = self.sql_class.database_operation(instruction="select",
                                                   operate_variable=required_value,
                                                   constrain_variable=constrain,
                                                   constrain_type=constrain_type,
                                                   constrain_value=constrain_value)

        # print(f'query_user_login: {result}')
        # "id", "name", "job", "email",
        # "account_number", "password", "admin_status"
        if not result or result[config.table_exe_result] == [] or result[config.table_exe_changed] <= 0:
            return False
        else:
            return result[config.table_exe_result]

    # This is the Function that used to create the procedure
    def create_new(self):
        # Initial the choice
        choice = ''
        # Define the state index used to toggle the index
        state_index = 0
        # While loop when the choice is *, break
        while choice != '*':
            context_id_list = self.update_step_context_list()
            """
            This function is not finished since it is used for load the procedure
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
                    config.table_elements_dict[config.table_name[config.aso_step_position]][1:state_index + 1])
                value = tuple(context_id_list[0:state_index])
                rtn_colm = (config.table_elements_dict[config.table_name[config.aso_step_position]][state_index + 1],)
                table_name = config.table_name[config.aso_step_position]
                # Should be always return serious of ID
            result = self.query_table(table_name=table_name,
                                      rtn_colm=rtn_colm,
                                      value_type=value_type,
                                      value=value)
            # This checked if the rec is empty
            if (result is None or result[config.table_exe_result][0][0] is None) and state_index != 4:
                # if missing
                print("Missing " + config.table_print_name[state_index])
                choice = input("Create A new " + config.table_print_name[state_index] + "?[Y/N]\n")
                if choice != "Y":
                    return None
                insert_result = self.insert_new_step_aso_values(config.table_name[state_index], state_index + 1)
                if insert_result is None:
                    print("Error Adding")
                    return None
                # Update the context
                context_id_list = self.update_step_context_list()
                context_id_list[state_index] = insert_result[config.table_exe_id]
                print(context_id_list)
                self.load_context_list(context_id_list)
                insert_result = self.query_table(table_name=config.table_name[state_index],
                                                 value_type=("id",),
                                                 value=(insert_result[config.table_exe_id],))

                aso_result = self.aso_update(types="step", state_index=state_index,
                                             table_object_rec=tuple(insert_result[config.table_exe_result][0]))
                if aso_result is None:
                    return None
                if state_index < 4:
                    state_index += 1
                continue
            if state_index == 4:
                # print(state_index)
                choice: str = input(f"Please Input the Operation:\n"
                                    f"1. File a New {config.table_print_name[state_index]}\n"
                                    f"2. Choose Another to Edit\n"
                                    )
            else:
                choice: str = input(f"Please Input the Operation:\n"
                                    f"1. File a New {config.table_print_name[state_index]}\n"
                                    f"2. Choose Another to Edit\n"
                                    f"3. Choose Exist {config.table_print_name[state_index]}\n"  # unfinished
                                    f"4. Edit Current {config.table_print_name[state_index]}\n"  # unfinished
                                    f"*. Exit\n")
            record_list = []
            if choice == '3' and state_index <= config.param_position:
                if state_index == 0:
                    for index in range(0, len(result[config.table_exe_result])):
                        record_list.append(result[config.table_exe_result][index])
                    # print(record_list)
                else:
                    query_list = af.remove_repeat_tuple(result[config.table_exe_result])
                    if not query_list:
                        return
                    record_list = self.query_multiple_rec(table_name=config.table_name[state_index],
                                                          query_list=query_list,
                                                          query_list_variable_type=("id",))
                selection = af.choose_row(config.table_name[state_index], record_list)
                aso_result = self.aso_update(types="step", state_index=state_index, table_object_rec=tuple(selection))
                # print(f"StateIndex{state_index}")
                if aso_result is None:
                    print("fatal: Error Update Associate Table")
                    return None
            # When the choice is one, Parameter is always empty
            elif choice == '1':
                file_result = self.insert_new_step_aso_values(table_name=config.table_name[state_index],
                                                              table_offset=state_index + 1)
                if file_result is None:
                    print("fatal: Wrong Insert")
                    continue
                new_rec = self.query_table(table_name=config.table_name[state_index],
                                           value_type=("id",),
                                           value=(file_result[config.table_exe_id],))
                if new_rec is None:
                    print("fatal: NO new record or Query Error")
                    continue
                # The zero represent that there is always should be the first rec
                # Well, there is a fetchone() for the mysql.connector API, can be used conditionally
                aso_result = self.aso_update(types="step", state_index=state_index,
                                             table_object_rec=tuple(new_rec[config.table_exe_result][0]))
                if aso_result is None:
                    return None
                """ When all of the previous operations are successful, the system will
                    prompt the user to keep adding the new parameters since the parameters
                    for one step might be a lot
                """
                if state_index == 4:
                    self.dev_context.ParamClass.id = None
                    self.dev_context.id = None
                    context_id_list = self.update_step_context_list()
            elif choice == '2':
                for choice_index in range(0, state_index):
                    print(f"#{choice_index}\t{config.table_name}")
                state_index: int = int(input("Please Input Which you want to edit: "))
            elif choice == '4' and state_index != config.param_position:
                pass
            elif choice == '*':
                print("Exit")
            else:
                print("Invalid Operation")
            if state_index < 4:
                state_index += 1
            print(result)

    def update_step_context(self, table_colm: tuple, table_name):
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

    def update_step_context_list(self):
        context_id_list = [self.dev_context.DeviceClass.id,
                           self.dev_context.CompClass.id,
                           self.dev_context.InstClass.id,
                           self.dev_context.StepClass.id,
                           self.dev_context.ParamClass.id]
        return context_id_list

    def load_context_list(self, context_id_list):
        self.dev_context.DeviceClass.id = context_id_list[0]
        self.dev_context.CompClass.id = context_id_list[1]
        self.dev_context.InstClass.id = context_id_list[2]
        self.dev_context.StepClass.id = context_id_list[3]
        self.dev_context.ParamClass.id = context_id_list[4]

    def aso_update(self, types="step", state_index: int = 0, table_object_rec: tuple = None):
        if not state_index or self.dev_context.id is None:
            # True for insert the value
            config.aso_step_insert_flag = True
        else:
            # False to update -- Should be only happened when there has the exit record
            config.aso_step_insert_flag = False
        self.update_step_context(table_colm=table_object_rec, table_name=config.table_name[state_index])
        aso_result = self.insert_update_aso(types=types)
        config.aso_step_insert_flag = False

        if aso_result is None:
            print("fatal: Error Update Associate Table")
            return None
        return aso_result

    def insert_new_step_aso_values(self, table_name, table_offset: int = 1):
        """
        :param table_name:  Table Name
        :param table_offset: table offset is where the id of the foreign key occupy for the current elements
        :return: The insert result should be a dict type data that contains the id
        """
        # Insert Aso Function May Added
        input_require = list(tuple(config.input_pattern[table_name][0]))
        input_require.pop(0)
        input_list = input("\tInput\n" + "\t".join(tuple(input_require)) + "\n").split(",")
        pre_rec = []
        next_offset = 0
        previous_offset = 0
        next_rec = []
        special_value_type = []
        type_list = []
        # Check if the input pattern has the special value
        if config.input_pattern[table_name][1]:
            # Update the current context
            context_id_list = self.update_step_context_list()
            # get the condition value
            aso_colm = tuple(config.table_elements_dict
                             [config.table_name[config.aso_step_position]][1:])
            type_list = config.input_pattern[table_name][1]
            feature_list = config.input_pattern[table_name][2]
            # for the special types
            pre_rec = []
            next_offset = 0
            previous_offset = 0
            selection_list = []
            for index in range(0, len(config.input_pattern[table_name][2])):
                # If the types is pre
                if feature_list[index] == config.previous_symbol:
                    previous_offset: int = len(config.input_pattern[table_name][0]) + index
                    next_offset: int = previous_offset + 1
                    # query table
                    exe_result = self.query_table(table_name=config.table_name[config.aso_step_position],
                                                  rtn_colm=(config.table_elements_dict
                                                            [config.table_name[config.aso_step_position]][
                                                                table_offset],),
                                                  value_type=aso_colm[:table_offset - 1],
                                                  value=tuple(context_id_list[:table_offset - 1]))
                    query_list = af.remove_repeat_tuple(exe_result[config.table_exe_result])
                    # if there is None, it is means that the start
                    if exe_result is None or query_list == []:
                        # Add 0 to the assigned position
                        special_value_type.append(0)
                        continue
                    # Get the selection list
                    selection_list = self.query_multiple_rec(table_name=table_name,
                                                             query_list=query_list)
                    if selection_list is None:
                        return None
                    pre_rec = af.choose_row(table_name=table_name, row_list=selection_list)
                    # check if the selection is valid
                    if pre_rec is None:
                        return None
                    config.pre_flag = True
                    # make sure the list is selection type
                    pre_rec = list(pre_rec)
                    # append the special value for th list
                    special_value_type.append(pre_rec[0])
                elif feature_list[index] == config.next_symbol:
                    # Next == 0 will be the end
                    print("Previous Rec")
                    print(pre_rec)
                    if not pre_rec:
                        special_value_type.append(0)
                        continue
                    if pre_rec[next_offset] == 0:
                        special_value_type.append(0)
                        continue
                    # the next record will be dispelled as next record id that dispelled at the previous record
                    special_value_type.append(pre_rec[next_offset])
                    next_rec = self.query_table(table_name=table_name,
                                                value_type=("id",),
                                                value=(pre_rec[next_offset],))
                    print("Next Rec")
                    print(next_rec)
                    config.next_flag = True
                elif feature_list[index] == config.status_symbol:
                    choice: str = input(f"{config.input_pattern[2][index]} [Y/Others]: ")
                    if choice != "Y":
                        special_value_type.append(0)
                        continue
                    selection_list.append(1)
                else:
                    return None
        # insert the new added value
        self.sql_class.table_name = table_name
        result = self.sql_class.database_operation(instruction="insert",
                                                   operate_variable=tuple(input_require) + tuple(type_list),
                                                   variable_value=tuple(input_list) + tuple(special_value_type))
        if result is None:
            print("Cannot Write")
            return None
        # After we finish a new record, we should re-link the table information
        # Must update the pre and the next context info that we required
        # Return the Correct Result
        # Notice: Duplicate Code here
        if config.pre_flag:
            # update the previous record
            pre_rec[next_offset] = result[config.table_exe_id]
            # Disable the previous flag to indicate that the previous record has already updated
            config.pre_flag = False
            self.sql_class.table_name = table_name
            pre_result = self.sql_class.database_operation(instruction="update",
                                                           operate_variable=(
                                                               config.table_elements_dict[table_name][next_offset],),
                                                           variable_value=(pre_rec[next_offset],),
                                                           constrain_type=("no_tp",),
                                                           constrain_variable=("id",),
                                                           constrain_value=(pre_rec[0],))
            if pre_result is None:
                return None

        # if the record is the next flag
        if config.next_flag:
            # update the next record
            next_rec = list(next_rec[config.table_exe_result][0])
            print("NextRec")
            print(next_rec)
            print(result)
            next_rec[previous_offset] = result[config.table_exe_id]
            next_rec_id = next_rec.pop(0)
            print(next_rec)
            config.next_flag = False
            self.sql_class.table_name = table_name
            next_result = self.sql_class.database_operation(instruction="update",
                                                            operate_variable=(
                                                                config.table_elements_dict[table_name][
                                                                    previous_offset],),
                                                            variable_value=(
                                                                next_rec[previous_offset - 1],),
                                                            constrain_type=("no_tp",),
                                                            constrain_variable=("id",),
                                                            constrain_value=(next_rec_id,))
            if next_result is None:
                return None
        return result

    # Update the table
    def insert_update_aso(self, types="step"):
        # In here, should update the aso table based on the step
        db_context = self.update_step_context_list()
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
            self.dev_context.id = result[config.table_exe_id]
        else:
            result = self.sql_class.database_operation(instruction="update",
                                                       operate_variable=operate_variable,
                                                       variable_value=tuple(db_context),
                                                       constrain_type=("no_tp",),
                                                       constrain_variable=("id",),
                                                       constrain_value=(self.dev_context.id,))
        return result
