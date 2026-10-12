def type_name(value):
    return type(value).__name__


def kind(value):
    return type(value).__name__


def type_of_type(value):
    return type(type(value)).__name__
