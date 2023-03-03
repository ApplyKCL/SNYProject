# Author: Shaonan Hu

# Function to remove elements from tuple
def tuple_remove(target=(), element=""):
    y = list(target)
    y.remove(element)
    target = tuple(y)
    return target

