"""Print 'Hello world' to the terminal.

Long
=====
An overly long underline (here one extra equals sign)
is considered acceptable.

Short
====
There is a missing equals sign on the above underline,
and that is considered an error. This should fail::

    $ flake8 --select RST RST212/short_underline.py
    RST212/short_underline.py:10:1: RST212 Title underline too short.

Nice
====
Finally, this underline is just right.

"""

print("Hello world")
