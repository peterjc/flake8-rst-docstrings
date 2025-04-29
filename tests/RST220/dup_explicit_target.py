"""Print 'Hello world' to the terminal.

It is common in RST to use unnamed or anonymous links in text (like
`here <https://example.com/t-and-c/>`__ and `here
<https://example.org/co-op-rules.html>`__), but they should have two trailing
underscores!

You *can* use a `single trailing underscore <https://example.com/links.html>`_
but it is treated as an implicitly named link. You can use the exact same link
text and URL again too (`single trailing underscore
<https://example.com/links.html>`_).

However, the missing second underscore becomes a problem if the same link text
is used again for another implicitly named link weth a different URL (e.g.
missing `single trailing underscore <https://example.com/bad.html>`_ *again*).

What happens here?

    $ flake8 --select RST RST220/dup_explicit_target.py
    RST220/dup_explicit_target.py:15:1: RST220 Duplicate explicit target name: "single trailing underscore".

This file triggers an error when the implicitly named link is redefined.
"""

print("Hello world")
