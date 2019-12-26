r"""Print 'Hello world' to the terminal.

RST supports inline substitution references,
and the string |000...00> looks a bit like one
so triggers an error:

    $ flake8 --select RST RST219/bad_sub_ref.py
    RST219/bad_sub_ref.py:4:1: RST219 Inline substitution_reference start-string without end-string

One potential way to avoid this using ``|000...00>``
instead (wrapping in backticks as a inline literal).

Better, escape the opening pipe as \|000...00>
instead.
"""

print("Hello world")
