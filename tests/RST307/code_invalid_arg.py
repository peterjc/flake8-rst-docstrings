"""Print 'Hello world' to the terminal.

This is a code block with not arguments other
than the format:

.. code:: pycon

  >>> print("Hello")
  Hello

Now with an invalid code block argument:

.. code:: pycon
  :wibble:

  >>> print("Hello")
  Hello

That second example should fail validation::

    $ flake8 --select RST  RST307/code_invalid_arg.py 
    RST307/code_invalid_arg.py:14:1: RST307 Error in "code" directive

"""

print("Hello world")
