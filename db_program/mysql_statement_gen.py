import string
import json
import associative_func


# Class used to generate the SQL statement
class databaseAPI:
    def __init__(self, db_class: classmethod, table: str):
        self.cursor = db_class.cursor()
        self.databases = db_class
        self.table_name = table
        self.inst_type: str = ""
        self.table_variable: tuple = ()
        self.variable_value: tuple = ()
        self.constrain_variable: tuple = ()
        self.constrain_value: tuple = ()
        self.constrain_type: tuple = ()

    # Function that used to execute the SQL
    def executor(self, cmd_str: str):
        result = {}
        self.cursor.execute(cmd_str, self.constrain_value)
        if self.inst_type == "select":
            result = self.cursor.fetchall()
        self.databases.commit()
        execution_result = {
            "result": result,
            "changed": self.cursor.rowcount
        }
        return execution_result

    def database_operation(self, instruction,
                           operate_variable=(),
                           variable_value=(),
                           constrain_variable=(),
                           constrain_value=(),
                           constrain_type=()):
        self.inst_type = instruction
        self.table_variable = operate_variable
        self.variable_value = variable_value
        self.constrain_variable = constrain_variable
        self.constrain_value = constrain_value
        self.constrain_type = constrain_type
        cmd_str = self.gen_sql_statements()
        result_dirc: dir = self.executor(cmd_str)
        self.inst_type = ""
        self.variable_value = ()
        self.variable_value = ()
        self.constrain_variable = ()
        self.constrain_value = ()
        self.constrain_type = ()
        print(cmd_str)
        if result_dirc["changed"] <= 0:
            return False
        return result_dirc["result"]

    # Set the filter but has some issues
    def constrain_str(self):
        if self.constrain_type == ():
            return ""
        if self.constrain_type[0] == "between":
            constr_str = "{} between %s and %s ".format(self.constrain_variable[0])
        elif self.constrain_type[0] == "and":
            constr_str = "and {} = %s ".format(self.constrain_variable[0])
        elif self.constrain_type[0] == "or":
            constr_str = "{} = %s or {} = %s ".format(self.constrain_variable[0],
                                                      self.constrain_variable[1])
            self.constrain_variable = associative_func.tuple_remove(self.constrain_variable,
                                                                    self.constrain_variable[0])
        elif self.constrain_type == "not":
            constr_str = "not {} = %s ".format(self.constrain_variable[0])
        elif self.constrain_type[0] == "no_tp":
            constr_str = "{} = %s ".format(self.constrain_variable[0])
        else:
            return None
        self.constrain_variable = associative_func.tuple_remove(self.constrain_variable,
                                                                self.constrain_variable[0])
        self.constrain_type = associative_func.tuple_remove(self.constrain_type,
                                                            self.constrain_type[0])
        temp = self.constrain_str()
        if temp is None:
            return None
        constr_str += temp
        if self.constrain_type == ():
            return constr_str

    # varify if the function has the proper variable to use
    def len_check(self):
        if len(self.table_variable) != len(self.variable_value[0]):
            return False
        if len(self.constrain_variable) != len(self.constrain_value[0]):
            return False
        return True

    # define the function that used to generate the mysql sentence
    def gen_sql_statements(self):
        if self.inst_type == "insert":
            # generate the insert SQL
            cmd_str = self.insert()
        elif self.inst_type == "update":
            # generate the update SQL
            cmd_str = self.update()
        elif self.inst_type == "select":
            # generate the select SQL
            cmd_str = self.select()
        elif self.inst_type == "delete":
            # not implement, geneart the delete
            cmd_str = "delect"
        return cmd_str

# Function that used to cascade the insert function
    def insert(self):
        # The command string that
        cmd_str = "insert into {} ({}) values ({})"
        values_field = ''
        for nums in range(len(self.table_variable)):
            values_field += "%s,"
        values_field = values_field.rstrip(",")
        variable_field = ", ".join(self.table_variable)
        cmd_str = cmd_str.format(self.table_name,
                                 variable_field,
                                 values_field)
        return cmd_str

    def update(self):
        cmd_str = "update {} set {} where {}"
        variable_field = " = %s, ".join(self.table_variable) + " = %s"
        if self.constrain_type == ():
            return None
        # need to be modified
        cmd_str = cmd_str.format(self.table_name,
                                 variable_field)
        return cmd_str

    def select(self):
        cmd_str = "select {} from {}"

        variable_field = ", ".join(self.table_variable)
        # if there has constrain
        if self.constrain_type != ():
            cmd_str = cmd_str + " where {}"
            constrain_field = self.constrain_str()
            cmd_str = cmd_str.format(variable_field,
                                     self.table_name,
                                     constrain_field)
        else:
            cmd_str = cmd_str.format(variable_field,
                                     self.table_name)
        return cmd_str