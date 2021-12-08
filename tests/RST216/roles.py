"""Print 'Hello world' to the terminal.

RST uses single backticks or back-quotes for various things including
interpreted text roles and references.

Without a semi-colon prefix or suffix, `example` has the default role.
A prefix like :code:`example` or a suffix like `example`:math: is allowed.

However, :code:`example`:math: with both prefix and suffix is considered to be
an error and should fail validation:

    $ flake8 --select RST RST216/roles.py
    RST216/roles.py:9:1: RST216 Multiple roles in interpreted text (both prefix and suffix present; only one allowed).

"""  # noqa: E501

print("Hello world")
