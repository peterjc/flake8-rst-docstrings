"""Print 'Hello world' to the terminal.

RST uses single backticks or back-quotes for various things including
interpreted text roles and references.

Without a semi-colon prefix or suffix, `example` has the default role.
A prefix like :code:`example` or a suffix like `example`:math: is allowed.

However, trailing underscores have special meaning for referencing, thus
`code`:example:_ is considered to be an error:

    $ flake8 --select RST RST217/roles.py
    RST217/roles.py:9:1: RST217 Mismatch: both interpreted text role suffix and reference suffix.

"""  # noqa: E501

print("Hello world")
