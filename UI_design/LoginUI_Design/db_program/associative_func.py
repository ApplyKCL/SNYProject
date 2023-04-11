"""
Author: Shaonan Hu
Last Update Time: April 04 2023
"""
import device_class as dc
import config


# Function to remove elements from tuple
def tuple_remove(target=(), element=""):
    y = list(target)
    y.remove(element)
    target = tuple(y)
    return target


def device_list_append(dev_sql_result) -> list:
    device_list = []
    for index in range(0, len(dev_sql_result)):
        device_list.append(dc.Device(dev_id=int(dev_sql_result[index][0]),
                                     device_name=str(dev_sql_result[index][1]),
                                     device_SN=str(dev_sql_result[index][2])))
    return device_list


def display_row(row_list):
    for index in range(0, len(row_list)):
        print(f"Choice #{index + 1}", end="\t")
        for colm in range(0, len(row_list[index])):
            print(f"{row_list[index][colm]}", end="\t")
        print("\n")


def display_dev(dev_class: dc.Device):
    print("""
    Device ID: {}
    Device Name: {}
    Device Product ID: {}
                """.format(dev_class.id, dev_class.device_name, dev_class.device_SN))


def check_colm(db_check_colm: tuple, db_colm: tuple):
    if not set(db_check_colm).issubset(set(db_colm)):
        # print(db_check_colm)
        # print(db_colm)
        # print("*")
        return False
    # print("True")
    return True


def choose_row(table_name, row_list):
    # Get the Colm
    colm_name = config.table_elements_name_dict[table_name]
    print("Choice ID:\t" + "\t".join(tuple(colm_name)))
    # print(row_list)
    display_row(row_list)
    choice: int = int(input("Choice: [#/0 to exit]"))
    if choice == 0:
        return None
    choice = choice - 1
    print("Select:")
    for index in range(0, len(row_list[choice])):
        print(f"{colm_name[index]}: {row_list[choice][index]}\n")
    return row_list[choice]


def remove_repeat_tuple(input_rec: list = None):
    if input_rec is None:
        return None
    unique_list = []
    for tup in input_rec:
        if tup not in unique_list and tup != (None, ):
            unique_list.append(tup)
    return unique_list
