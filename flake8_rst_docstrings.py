"""Check Python docstrings validate as reStructuredText (RST).

This is a plugin for the tool flake8 tool for checking Python
source code.
"""

import ast
import io

import docutils.core
import docutils.utils


__version__ = "0.3.0"


rst_prefix = "RST"
rst_fail_load = 900
rst_fail_parse = 901
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


def validate_rst(text, extra_directives=(), extra_roles=()):
    """Return list of any RST violations from docutils."""
    handle = io.StringIO()
    try:
        docutils.core.publish_string(
            text,
            # source_path="example.py",
            settings_overrides={
                "report_level": docutils.utils.Reporter.INFO_LEVEL,
                "warning_stream": handle,
            },
        )
    except docutils.utils.SystemMessage:
        pass
    for msg in handle.getvalue().splitlines():
        if not msg.startswith("<string>:"):
            # Ignore continuations of multi-line messages, e.g.
            #
            # example.py:2: (INFO/1) Possible title underline, too short for the title.
            # Treating it as ordinary text because it's so short.
            # example.py:4: (WARNING/2) Inline emphasis start-string without end-string
            #
            # where the filename is just <string> if omitted.
            continue
        _, line, msg = msg.split(":", 2)
        line = int(line)
        level, msg = msg.strip().split(" ", 1)
        if level == "(INFO/1)":
            if msg.startswith(('No directive entry for "', 'No role entry for "')):
                # Ignore, should also be an (ERROR/3) Unknown directive type
                # or (ERROR/3) Unknown interpreted text role
                continue
            code = 100 + code_mapping_info.get(msg, 99)
        elif level == "(WARNING/2)":
            code = 200 + code_mapping_warning.get(msg, 99)
        elif level == "(ERROR/3)":
            if msg.count('"') == 2 and ' "' in msg:
                # Following assumes any variable messages take the format
                # of 'Fixed text "variable text".' only:
                # e.g. 'Undefined substitution referenced: "dict".'
                # ---> 'Undefined substitution referenced: "*".'
                # e.g. 'Error in "code" directive:'
                # ---> 'Error in "*" directive:'
                value = msg.split('"', 2)[1]
                if (
                    msg.startswith('Unknown directive type "')
                    and value in extra_directives
                ) or (
                    msg.startswith('Unknown interpreted text role "')
                    and value in extra_roles
                ):
                    continue
                code = 300 + code_mapping_error.get(
                    msg.replace(' "%s"' % value, ' "*"'), 99
                )
            else:
                code = 300 + code_mapping_error.get(msg, 99)
        elif level == "(SEVERE/4)":
            code = 400 + code_mapping_severe.get(msg, 99)
        else:
            code = rst_fail_parse
            msg = "Failed to parse docutils message: " + msg
        yield line, "%s%03i %s" % (rst_prefix, code, msg)


assert list(validate_rst("Hello\n===\n\n*Bye!\n")) == [
    (2, "RST101 Possible title underline, too short for the title."),
    (4, "RST213 Inline emphasis start-string without end-string."),
]


class reStructuredTextChecker(object):
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
                    rst_errors = list(
                        validate_rst(docstring, self.extra_directives, self.extra_roles)
                    )
                except Exception as err:
                    # e.g. UnicodeDecodeError?
                    msg = "%s%03i %s" % (
                        rst_prefix,
                        rst_fail_lint,
                        "Failed to lint docstring: %s - %s" % (node.name, err),
                    )
                    yield 0, 0, msg, type(self)
                    continue

                if rst_errors:
                    start = node.body[0].lineno - len(
                        ast.get_docstring(node, clean=False).splitlines()
                    )

                for line, msg in rst_errors:
                    # We don't know the column number, leaving as zero.
                    yield start + line, 0, msg, type(self)
