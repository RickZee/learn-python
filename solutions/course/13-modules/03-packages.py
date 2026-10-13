def exported() -> str:
    import pylearn

    return pylearn.__name__


def package_name() -> str:
    import pylearn

    return pylearn.__name__


def has_check() -> bool:
    import pylearn

    present = hasattr(pylearn, "check")
    name = pylearn.__name__
    return present and bool(name)


def edit_target() -> str:
    return "project"
