def tuple_remove(target=(), element=""):
    y = list(target)
    y.remove(element)
    target = tuple(y)
    return target

