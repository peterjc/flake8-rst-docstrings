"""Print 'Hello world' to the terminal.

Here's where the |foo| substitution is used - it is defined
below.

.. |foo| replace:: Here's where it's defined.

So far so good, but what if the definition is not in the same
docstring fragment - it could be in an included footer?

Here the |bar| substituion definition is missing, so this
docstring in isolation should fail validation::

    $ flake8 --select RST RST305/substitution.py
    RST305/subsitution.py:12:1: RST305 Undefined substitution referenced: "bar"

"""

print("Hello world")
