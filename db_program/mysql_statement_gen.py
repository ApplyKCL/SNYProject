import string
import json


class sql_table:
    def __init__(self, table_dirc={}):
        self.table_dirc = table_dirc
        self.context = ""
        self.values = []
        self.sql_variable = ""
        self.sql_cond = ""
        self.counter = 0

    def data_read(self):
        values = []
        for self.counter in range(0, self.table_dirc["elements_amount"]):
            values.append(input("Please input " + self.table_dirc["elements_name"][self.counter] +
                                " enter to skip "))
            print(values, self.counter)
            if values[self.counter] == "\n":
                values[self.counter] = ''
        return values

    def data_listing(self):
        choice = "Y"
        while choice == "Y":
            self.values.append(tuple(self.data_read()))
            self.counter = 0
            choice = input("If you have another record to add, enter Y")
        print(self.values)

    def data_select(self):
        choice = "Y"
        while choice == "Y":
            choice = input("Pleases Enter the value that u what to display")
            self.sql_variable.append()
            choice = input("Do you have another value to enter")
    def data_update(self):
        choice = input("1. Change Specific Record\n2. Change Specific Value ?")
        if choice == 1:
            print("Enter the specific value")
        elif choice == 2:
            print("Enter the specific value")
def generate_mysql_statement(dirc):
    operation = {
        "insert": "insert into {} ({}) valuse ({})",
        "update": "update {} set {} where {} = %s",
        "select": "select {} from {}",
        "delete": "delete from {} where {} = %s",
        "tables": {
            "A": "device_table",
            "B": "comp_table",
            "C": "inst_table",
            "D": "step_table",
            "E": "param_table"
        }
    }
    print("Please choose tables: ")
    for nums in range(0, len(operation["tables"])):
        print("\t" + string.ascii_uppercase[nums] + '.', operation["tables"][string.ascii_uppercase[nums]])
    file = open("dbtable_config.json", "rt")
    json_dirc = json.loads(file.read())
    sql_class = sql_table(json_dirc[operation["tables"][input()]])
    if dirc == "insert":
        sql_class.data_listing()
    elif dirc == "update":
        sql_class.data_update()
