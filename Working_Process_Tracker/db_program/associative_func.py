"""
Author: Shaonan Hu
Description: This some of the data usage function that used to assistant the data processing
Last Update Time: April 04 2023
"""
import device_class as dc
import config


# Function to remove elements from tuple
def tuple_remove(target=(), element=""):
    # change the tuple to list
    y = list(target)
    # Remove the elements
    y.remove(element)
    target = tuple(y)
    return target


# Function that used to create the device, this is for the
# orginal design, might be useful for future
def device_list_append(dev_sql_result) -> list:
    device_list = []
    for index in range(0, len(dev_sql_result)):
        # Append the device list
        device_list.append(dc.Device(dev_id=int(dev_sql_result[index][0]),
                                     device_name=str(dev_sql_result[index][1]),
                                     device_SN=str(dev_sql_result[index][2])))
    return device_list


# Display the row of the list
def display_row(row_list):
    for index in range(0, len(row_list)):
        # Choice ID
        print(f"Choice #{index + 1}", end="\t")
        # Display the colm for the devices
        for colm in range(0, len(row_list[index])):
            print(f"{row_list[index][colm]}", end="\t")
        print("\n")


# Function that used to display the device information
def display_dev(dev_class: dc.Device):
    # Display the device information
    print("""
    Device ID: {}
    Device Name: {}
    Device Serial Number: {}
                """.format(dev_class.id, dev_class.device_name, dev_class.device_SN))


# Function used to check if the input colm is same as the colm they required
def check_colm(db_check_colm: tuple, db_colm: tuple):
    # If is not in the colm, return False
    if not set(db_check_colm).issubset(set(db_colm)):
        return False
    # Else return True
    return True


# Choose the row
def choose_row(table_name, row_list):
    # Get the Colm
    colm_name = config.table_elements_name_dict[table_name]
    print("Choice ID:\t" + "\t".join(tuple(colm_name)))
    # display the row list
    display_row(row_list)
    # Prompt the user to input the choice
    choice: int = int(input("Choice: [#/0 to exit]"))
    if choice == 0:
        return None
    # Choice count
    choice = choice - 1
    print("Select:")
    # Based on the choice count
    for index in range(0, len(row_list[choice])):
        print(f"{colm_name[index]}: {row_list[choice][index]}\n")
    return row_list[choice]


# Function that to remove the repeated tuple
def remove_repeat_tuple(input_rec: list = None):
    """
    :param input_rec: Rec may has repeat elements
    :return: Return the unique list
    """
    if input_rec is None:
        return None
    unique_list = []
    # append the unique rec to the list
    for tup in input_rec:
        if tup not in unique_list and tup != (None, ):
            unique_list.append(tup)
    return unique_list
