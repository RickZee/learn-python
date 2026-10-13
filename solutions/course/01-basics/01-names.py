def type_name(value):
    return type(value).__name__


def kind(value):
    type_obj = type(value)
    name = type_obj.__name__
    if name == "NoneType":
        return "missing"
    return name


def type_of_type(value):
    return type(type(value)).__name__
