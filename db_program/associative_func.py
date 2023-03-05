# Author: Shaonan Hu
import device_class as dc


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


def display_dev(dev_class: dc.Device):
    print("""
    Device ID: {}
    Device Name: {}
    Device Product ID: {}
                """.format(dev_class.id, dev_class.device_name, dev_class.product_id))
