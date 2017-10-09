'''This is a module docstring with bad RST and specific no-QA.

   * Bullet
   * Bullet
  Bad indentation

We expect this to fail validation, specifically line 6:

``RST201 Block quote ends without a blank line; unexpected unindent.``

I've also put an unescaped slash here, \, which means if the
plugin ``flake8-docstrings`` is also installed, it should
would trigger the following (reported against line 1):

``D301 Use r""" if any backslashes in a docstring``

Therefore entire multi-line triple-quoted Python statement
has a no-quality-assurance comment. In this case we are
listing these two codes as arguments to the flake8 directive.
'''  # noqa: RST201,D301


def example_function(value):
    """Silly doubling function using bad RST in docstring.

        * Bullet
        * Bullet
       Bad indentation

    We expect this to fail validation with RST201.
    """  # noqa: RST201
    return value * 2


print("Checking flake8 #noqa directive with arguments.")
