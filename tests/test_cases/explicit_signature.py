"""This files uses signature overloading / overriding.

When Python can not express a signature, it is permissible to use the
first line of the docstring as a signature, this is extracted by
e.g. sphinx.

Examples from the standard library:
https://github.com/python/cpython/blob/3.10/Lib/textwrap.py#L350

"""


def legacy_positional(*args, **kwargs):
    """legacy_positional([thing][, **things])

    Can be confused with RST210 (inline strong without end).

    Before Python 3.8 (PEP 570), pure python did not have
    positional-only arguments (to say nothing of optional ones), they
    had to be emulated via `*args` and signature overrides allowed
    properly documenting them regardless.
    """  # noqa: D400, D402


# fmt: off
def forwarding(*args):
    """ forwarding(x, *y)

    Can be confused with RST213 (inline emphasis without end).

    An other common use case is forwarding args directly but wanting
    to properly document *some* still.
    """  # noqa: D210, D400, D402
