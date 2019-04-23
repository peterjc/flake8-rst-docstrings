"""Example reStructuredText from Sphinx-Needs project.

From http://sphinxcontrib-needs.readthedocs.io/en/latest/
but will not work in isolation - cut down just to trigger
RST304.

**Some text**

Wohooo, we have created :need:`req_001`,
which is linked by :need_incoming:`req_001`.

"""

print("sphinx-needs defines its own reStructuredText roles.")
