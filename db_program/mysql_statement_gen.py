import string
import json


class databaseAPI:
    def __init__(self, db_cursor, db_class, table):
        self.cursor = db_cursor
        self.databases = db_class
        self.table_dirc = table
        self.inst_type = ""
        self.table_variable = []
        self.variable_value = []
        self.constrain_variable = []
        self.constrain_value = []
        self.constrain_type = []

    def executor(self, cmd_str):
        result = {}
        self.cursor.execute(cmd_str)
        if self.inst_type == "select":
            result = self.cursor.fetchall()
        self.databases.commit()
        execution_result = {
            "result": result,
            "changed": self.cursor.rowcount
        }
        return execution_result

    def database_operation(self, instruction, operate_variable=(), variable_value=(), constrain_variable=(),
                           constrain_value=(), constrain_type=()):
        self.inst_type = instruction
        self.variable_value = operate_variable
        self.variable_value = variable_value
        self.constrain_variable = constrain_variable
        self.constrain_value = constrain_value
        self.constrain_type = constrain_type
        cmd_str = self.gen_sql_statements()

    def constrain_str(self):
        if self.constrain_type == "between":
            constr_str = "{} between %s and %s".format(self.constrain_variable[0])
        elif self.constrain_type == "and":
            constr_str = "{} = %s and {} = %s".format(self.constrain_variable[0], self.constrain_variable[1])
            self.constrain_variable.remove(self.constrain_variable[0])
        elif self.constrain_type == "or":
            constr_str = "{} = %s or {} = %s".format(self.constrain_variable[0], self.constrain_variable[1])
            self.constrain_variable.remove(self.constrain_variable[0])
        elif self.constrain_type == "not":
            constr_str = "not {} = %s".format(self.constrain_variable[0])
        elif self.constrain_type == "no_tp":
            constr_str = "{} = %s".format(self.constrain_variable[0])
        else:
            return None
        self.constrain_variable.remove(self.constrain_variable[0])
        self.constrain_type.remove(self.constrain_type[0])
        constr_str += self.constrain_str()
        if self.constrain_variable is None:
            return constr_str

    def len_check(self):
        if len(self.table_variable) != len(self.variable_value[0]):
            return False
        if len(self.constrain_variable) != len(self.constrain_value[0]):
            return False
        return True

    def gen_sql_statements(self):
        if self.inst_type == "insert":
            cmd_str = self.insert()
        elif self.inst_type == "update":
            cmd_str = self.update()
        elif self.inst_type == "select":
            cmd_str = self.insert()
        elif self.inst_type == "delete":
            cmd_str = "delect"
        return cmd_str

    def insert(self):
        cmd_str = "insert into {} ({}) values ({})"
        values_field = ''
        if not self.len_check():
            return None
        for nums in range(len(self.table_variable)):
            values_field += "%s,"
        values_field = values_field.rstrip(",")
        variable_field = ", ".join(self.table_variable)
        cmd_str = cmd_str.format(self.table_dirc["*"], variable_field, values_field)
        return cmd_str

    def update(self):
        cmd_str = "update {} set {} where {}"
        if not self.len_check():
            return None
        variable_field = " = %s, ".join(self.table_variable) + " = %s"
        constrain_field = self.constrain_str()
        cmd_str = cmd_str.format(self.table_dirc["*"], variable_field, constrain_field)
        return cmd_str

    def select(self):
        cmd_str = "select {} from {}"
        if not self.len_check():
            return None
        variable_field = ", ".join(self.table_variable)
        if self.constrain_type is not None:
            cmd_str = cmd_str + " where {}"
            constrain_field = self.constrain_str()
            cmd_str = cmd_str.format(variable_field, self.table_dirc["*"], constrain_field)
        else:
            cmd_str = cmd_str.format(variable_field, self.table_dirc["*"])
        return cmd_str
