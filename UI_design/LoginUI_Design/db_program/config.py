import json
device_position: int = 0
comp_position: int = 1
inst_position: int = 2
step_position: int = 3
param_position: int = 4
employee_position: int = 5
process_position: int = 6
data_position: int = 7
aso_step_position: int = 8
aso_pro_position: int = 9
table_name_file = open("db_program/json/table.json", "r")
table_name = json.loads(table_name_file.read())["table_name"]
print(table_name)
