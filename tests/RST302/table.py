"""Example with some RST tables.

This file should fail RST validation:

    $ flake8 --select RST RST302/table.py
    RST302/table.py:27:1: RST302 Malformed table.
    RST302/table.py:45:1: RST302 Malformed table.

See below.
"""  # noqa: E510


# Deliberately has lots of arguments to be a multi-line statement:
def simple_table(
    data,
    alignment="left",
    col_gap=1,
    line_top="=",
    line_middle="-",
    line_bottom="=",
    title_case=False,
):
    """Print a simple RST table.

    Sample output:

    == ====
    ID Name
    -- ----
    01 Paul
    02 Peter
    -- ----

    As you should spot, the table lines are too short
    for valid RST.
    """
    pass


def grid_table(data):
    """Print an RST grid table.

    Sample output:

    +--+----+
    |ID|Name|
    +==+====+
    |01|Paul|
    |02|Peter|
    +--+----+

    Again, not quite right.
    """
    pass
