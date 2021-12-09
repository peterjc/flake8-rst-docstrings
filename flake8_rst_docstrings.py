"""Check Python docstrings validate as reStructuredText (RST).

This is a plugin for the tool flake8 tool for checking Python
source code.
"""
import ast

import restructuredtext_lint as rst_lint


__version__ = "0.2.4"


rst_prefix = "RST"
rst_fail_load = 900
# rst_fail_parse = 901
# rst_fail_all = 902
rst_fail_lint = 903

# Level 1 - info
code_mapping_info = {
    "Possible title underline, too short for the title.": 1,
    "Unexpected possible title overline or transition.": 2,
}

# Level 2 - warning
code_mapping_warning = {
    # XXX ends without a blank line; unexpected unindent:
    "Block quote ends without a blank line; unexpected unindent.": 1,
    "Bullet list ends without a blank line; unexpected unindent.": 2,
    "Definition list ends without a blank line; unexpected unindent.": 3,
    "Enumerated list ends without a blank line; unexpected unindent.": 4,
    "Explicit markup ends without a blank line; unexpected unindent.": 5,
    "Field list ends without a blank line; unexpected unindent.": 6,
    "Literal block ends without a blank line; unexpected unindent.": 7,
    "Option list ends without a blank line; unexpected unindent.": 8,
    # Other:
    "Inline strong start-string without end-string.": 10,
    "Blank line required after table.": 11,
    "Title underline too short.": 12,
    "Inline emphasis start-string without end-string.": 13,
    "Inline literal start-string without end-string.": 14,
    "Inline interpreted text or phrase reference start-string without end-string.": 15,
    "Multiple roles in interpreted text (both prefix and suffix present; only one allowed).": 16,  # noqa: E501
    "Mismatch: both interpreted text role suffix and reference suffix.": 17,
    "Literal block expected; none found.": 18,
    "Inline substitution_reference start-string without end-string.": 19,
}

# Level 3 - error
code_mapping_error = {
    "Unexpected indentation.": 1,
    "Malformed table.": 2,
    # e.g. Unknown directive type "req".
    'Unknown directive type "*".': 3,
    # e.g. Unknown interpreted text role "need".
    'Unknown interpreted text role "*".': 4,
    # e.g. Undefined substitution referenced: "dict".
    'Undefined substitution referenced: "*".': 5,
    # e.g. Unknown target name: "license_txt".
    'Unknown target name: "*".': 6,
    # e.g. Error in "code" directive:
    'Error in "*" directive:': 7,
}

# Level 4 - severe
code_mapping_severe = {"Unexpected section title.": 1}

code_mappings_by_level = {
    1: code_mapping_info,
    2: code_mapping_warning,
    3: code_mapping_error,
    4: code_mapping_severe,
}


def code_mapping(level, msg, extra_directives, extra_roles, default=99):
    """Return an error code between 0 and 99."""
    try:
        return code_mappings_by_level[level][msg]
    except KeyError:
        pass
    # Following assumes any variable messages take the format
    # of 'Fixed text "variable text".' only:
    # e.g. 'Unknown directive type "req".'
    # ---> 'Unknown directive type'
    # e.g. 'Unknown interpreted text role "need".'
    # ---> 'Unknown interpreted text role'
    if msg.count('"') == 2 and ' "' in msg:
        value = msg.split('"', 2)[1]
        txt = msg.replace(' "' + value + '"', ' "*"')
        if txt == 'Unknown directive type "*".' and value in extra_directives:
            return 0
        if txt == 'Unknown interpreted text role "*".' and value in extra_roles:
            return 0
        return code_mappings_by_level[level].get(txt, default)
    return default


class reStructuredTextChecker:
    """Checker of Python docstrings as reStructuredText."""

    name = "rst-docstrings"
    version = __version__

    def __init__(self, tree, filename="(none)"):
        """Initialise."""
        self.tree = tree
        self.filename = filename

    @classmethod
    def add_options(cls, parser):
        """Add RST directives and roles options."""
        parser.add_option(
            "--rst-directives",
            metavar="LIST",
            default="",
            parse_from_config=True,
            comma_separated_list=True,
            help="Comma-separated list of additional RST directives.",
        )
        parser.add_option(
            "--rst-roles",
            metavar="LIST",
            default="",
            parse_from_config=True,
            comma_separated_list=True,
            help="Comma-separated list of additional RST roles.",
        )

    @classmethod
    def parse_options(cls, options):
        """Adding black-config option."""
        cls.extra_directives = options.rst_directives
        cls.extra_roles = options.rst_roles

    def run(self):
        """Use docutils to check docstrings are valid RST."""
        if self.tree is None:
            msg = "%s%03i %s" % (
                rst_prefix,
                rst_fail_load,
                "Failed to load file: %s" % self.err,
            )
            yield 0, 0, msg, type(self)
        else:
            try:
                wanted = (
                    ast.Module,
                    ast.ClassDef,
                    ast.FunctionDef,
                    ast.AsyncFunctionDef,
                )
            except AttributeError:
                # Python 3.3 and 3.4 lacked ast.AsyncFunctionDef
                wanted = (ast.Module, ast.ClassDef, ast.FunctionDef)
            for node in ast.walk(self.tree):
                if not isinstance(node, wanted):
                    continue
                docstring = ast.get_docstring(node, clean=True)
                if not docstring:
                    # People can use flake8-docstrings to report missing docstrings
                    continue
                try:
                    rst_errors = list(rst_lint.lint(docstring))
                except Exception as err:
                    # e.g. UnicodeDecodeError
                    msg = "%s%03i %s" % (
                        rst_prefix,
                        rst_fail_lint,
                        "Failed to lint docstring: %s - %s" % (node.name, err),
                    )
                    yield 0, 0, msg, type(self)
                    continue

                if rst_errors:
                    try:
                        node.body[0].end_lineno
                        # Worked, on Python 3.8+ and can trust the start
                        start = node.body[0].lineno - 1  # AST value 1 based
                    except AttributeError:
                        # On Python 3.7 or older, and must compute start line
                        start = (
                            node.body[0].lineno
                            - ast.get_docstring(node, clean=False).count("\n")
                            - 1
                        )
                    assert (
                        node.body[0].lineno >= 1 and start >= 0
                    ), "Bad start line, node line number %i for: %s\n" % (
                        node.body[0].lineno,
                        docstring,
                    )
                for rst_error in rst_errors:
                    # TODO - make this a configuration option?
                    if rst_error.level <= 1:
                        continue
                    # Levels:
                    #
                    # 0 - debug   --> we don't receive these
                    # 1 - info    --> RST1## codes
                    # 2 - warning --> RST2## codes
                    # 3 - error   --> RST3## codes
                    # 4 - severe  --> RST4## codes
                    #
                    # Map the string to a unique code:
                    msg = rst_error.message.split("\n", 1)[0]
                    code = code_mapping(
                        rst_error.level, msg, self.extra_directives, self.extra_roles
                    )
                    if not code:
                        # We ignored it, e.g. a known Sphinx role
                        continue
                    assert 0 < code < 100, code
                    code += 100 * rst_error.level
                    msg = "%s%03i %s" % (rst_prefix, code, msg)

                    # We don't know the column number, leaving as zero.
                    yield start + rst_error.line, 0, msg, type(self)
