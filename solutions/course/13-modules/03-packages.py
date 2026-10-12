
def exported() -> str:
    import pylearn

    return pylearn.__name__


def package_name() -> str:
    import pylearn

    return pylearn.__name__


def has_check() -> bool:
    import pylearn

    return hasattr(pylearn, "check")
