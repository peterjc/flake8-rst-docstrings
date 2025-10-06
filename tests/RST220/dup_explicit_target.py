"""Print 'Hello world' to the terminal; test links in docstrings.

Suppose we want to link to the Python_ home page, but have duplicate
link targets defined?

What happens here?

    $ flake8 --select RST RST220/dup_explicit_target.py
    RST220/dup_explicit_target.py:3:1: RST399 Duplicate target name, cannot be used as a unique reference: "python".
    RST220/dup_explicit_target.py:15:1: RST220 Duplicate explicit target name: "python".

This file triggers an error as there are repeated conflicting definitions:

.. _Python: https://www.python.org
.. _Python: https://python.org

"""  # noqa: E501

print("Hello world")
