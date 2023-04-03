# Author: Shaonan Hu
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
                                     product_id=str(dev_sql_result[index][2])))
    return device_list


def display_row(row_list):
    for index in range(0, len(row_list)):
        print(f"Choice #{index+1}", end="\t")
        for colm in range(0, len(row_list[index])):
            print(f"{row_list[index][colm]}", end="\t")


def display_dev(dev_class: dc.Device):
    print("""
    Device ID: {}
    Device Name: {}
    Device Product ID: {}
                """.format(dev_class.id, dev_class.device_name, dev_class.product_id))


def check_colm(db_check_colm: tuple, db_colm: tuple):
    if not set(db_check_colm).issubset(set(db_colm)):
        print(db_check_colm)
        print(db_colm)
        print("*")
        return False
    print("True")
    return True
