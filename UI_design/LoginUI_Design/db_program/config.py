"""
Author: Shaonan Hu
Description: This is the py file that used to store the database config information
"""
import json
# offsets
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
# Print Name
table_print_name = ["Device", "Component", "Instruction", "Step", "Parameter"]
# Offset for the steps of the workflow
step_device_offset = 1
step_comp_offset = 2
step_inst_offset = 3
step_step_offset = 4
step_param_offset = 5
debug_flag = 0
# Offset for the step
data_step_offset = 2
data_param_offset = 3
data_value_offset = 4
# table_file = open("json/table.json", "r")
# Open the json file in two different path
try:
    table_file = open("/home/eced4901/Desktop/SNYProject/UI_design/LoginUI_Design/db_program/json/table.json", "r")
except:
    table_file = open("json/table.json", "r")
# Control flag that used to control some of the insert operation
aso_step_insert_flag: bool = True
param_step_insert_flag: bool = False
# table_file = open("json/table.json", "r")
# input_pattern_file = open("json/input_pattern.json", "r")
try:
    input_pattern_file = open("/home/eced4901/Desktop/SNYProject/UI_design/LoginUI_Design/db_program/json/input_pattern.json", "r")
except:
    input_pattern_file = open("json/input_pattern.json", "r")

# Data input pattern for identifiy the input data features and contains some of the print name
input_pattern = json.loads(input_pattern_file.read())
# The symbol used to identify the previous
previous_symbol = "PRE"
next_symbol = "NEXT"
# Status symbol
status_symbol = "STATUS"
sub_symbol = "SUB"
# Set the flags
pre_flag: bool = False
next_flag: bool = False
sub_flag: bool = False
# Load the json file for opening the json file
table_json_content = json.loads(table_file.read())
table_name: list = table_json_content["table_name"]
table_elements_dict: dict = table_json_content["table_elements"]
table_elements_name_dict: dict = table_json_content["table_elements_name"]
table_exe_result = "result"
table_exe_id = "id"
table_exe_changed = "changed"
login_flag: bool = True
print(table_elements_name_dict)
table_elements_list: list = []
# Get the table elements name by using the for loop
for i in range(0, aso_pro_position):
    table_elements_list.append(table_elements_dict[table_name[i]])
# Close the file
table_file.close()
input_pattern_file.close()
