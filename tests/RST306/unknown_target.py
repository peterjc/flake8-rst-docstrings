"""Print 'Hello world' to the terminal.

Here's where the hyperlink-name_ is used, the target definition
is next.

.. _hyperlink-name: Here's where the hyperlink target is defined.

So far so good, but what if the definition is not in the same
docstring fragment - it could be in an included footer?

Here a missing-link_ hyperlink is used, so this docstring in
isolation should fail validation::

    $ flake8 --select RST  RST306/unknown_target.py
    RST306/unknown_target.py:11:1: RST306 Unknown target name: "missing-link".

"""

print("Hello world")
