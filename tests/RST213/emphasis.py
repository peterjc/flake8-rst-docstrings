"""Print 'Hello world' to the terminal.

RST uses single asterisks for *emphasis*, which is normally rendered as
*italics*.

Here *emphasis is missing a closing asterisk.

That is considered to be an error, and should fail::

    $ flake8 --select RST RST213/emphasis.py
    RST213/emphasis.py:6:1: RST213 Inline emphasis start-string without end-string.

"""

print("Hello world")
