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
    RST212/short_underline.py:9:1: RST212 Title underline too short.
    RST212/short_underline.py:9:1: RST212 Title underline too short.

Note RST212 gets displayed twice, due to a known docutils bug.
See https://sourceforge.net/p/docutils/bugs/346/

Nice
====
Finally, this underline is just right.

"""

print("Hello world")
