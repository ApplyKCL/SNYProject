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
table_print_name = ["Device", "Component", "Instruction", "Step", "Parameter"]
table_tree = """
Device
\t|
\t--> Component
\t\t|
\t\t-->Instruction
\t\t\t|
\t\t\t-->Step #1
\t\t\t\t|
\t\t\t\t-->Parameter #1
\t\t\t\t|
\t\t\t\t-->Parameter #2
\t\t\t\t|
\t\t\t\t-->Parameter #3
"""
print(table_tree)
table_file = open("json/table.json", "r")
table_json_content = json.loads(table_file.read())
table_name: list = table_json_content["table_name"]
table_elements_dict: dict = table_json_content["table_elements"]
table_elements_list: list = []
for i in range(0, aso_pro_position):
    table_elements_list.append(table_elements_dict[table_name[i]])

