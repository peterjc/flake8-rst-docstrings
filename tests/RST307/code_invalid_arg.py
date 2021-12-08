"""Print 'Hello world' to the terminal.

This is a code block with no arguments other
than the format:

.. code:: pycon

  >>> print("Hello")
  Hello

Now with an invalid code block argument:

.. code:: pycon
  :wibble:

  >>> print("Hello")
  Hello

Here are some actual examples from the Sphinx v4.0.0
documentation:

.. code-block:: python
   :caption: this.py
   :name: this-py

   print "Explicit is better than implicit."

And:

.. code-block:: ruby
   :dedent: 4

       some ruby code

Sadly docutils considers all three examples to be invalid:

    $ flake8 --select RST  RST307/code_invalid_arg.py
    RST307/code_invalid_arg.py:13:1: RST307 Error in "code" directive:
    RST307/code_invalid_arg.py:22:1: RST307 Error in "code-block" directive:
    RST307/code_invalid_arg.py:30:1: RST307 Error in "code-block" directive:

"""

print("Hello world")
