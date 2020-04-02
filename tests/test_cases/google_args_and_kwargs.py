"""Google docstring style test case."""


def module_level_function(param1, param2=None, *args, **kwargs):
    """Accept keyword arguments.

    Here using the Google docstring style, notice that we have *not* escaped
    the asterisk in ``*args*`` or ``**kwargs`` in the argument list.

    Args:
        param1 (int): The first parameter.
        param2 (str, optional): The second parameter. Defaults to None.
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.

    ...
    """
    pass
