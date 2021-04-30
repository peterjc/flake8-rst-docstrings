"""Print 'Hello world' to the terminal.

RST uses double asterisks for **strong**, which is
normally rendered as **bold**.

Here **strong is missing a closing double asterisk.

That is considered to be an error, and should fail::

    $ flake8 --select RST RST210/strong.py
    RST210/strong.py:6:1: RST210 Inline strong start-string without end-string.

"""

print("Hello world")
