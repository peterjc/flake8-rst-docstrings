"""Check Python docstrings validate as reStructuredText (RST).

This is a plugin for the tool flake8 tool for checking Python
source code.
"""

import logging
import re
import sys

import tokenize as tk

from pydocstyle.parser import Parser

try:
    from StringIO import StringIO
except ImportError:  # Python 3.0 and later
    from io import StringIO
    from io import TextIOWrapper

#####################################
# Start of backported tokenize code #
#####################################

# If possible (python >= 3.2) use tokenize.open to open files, so PEP 263
# encoding markers are interpreted.
try:
    tokenize_open = tk.open
except AttributeError:
    # Fall back on a backport of the encoding aware tokenize open function,
    # which requires we back port tokenize.detect_encoding to implement.
    from codecs import lookup, BOM_UTF8
    from io import open as io_open

    cookie_re = re.compile(r"^[ \t\f]*#.*?coding[:=][ \t]*([-\w.]+)")
    blank_re = re.compile(br"^[ \t\f]*(?:[#\r\n]|$)")

    # I don't think 'blank regular expression' is well named, think
    # it looks for blank line after any Python # comment removed.
    # Key test case of interest is hashbang lines!
    assert blank_re.match(b"\n")
    assert blank_re.match(b"# Comment\n")
    assert blank_re.match(b"#!/usr/bin/python\n")
    assert blank_re.match(b"#!/usr/bin/env python\n")
    assert not blank_re.match(b'"""Welcome\n')
    assert not blank_re.match(b'"""Welcome"""\n')

    def _get_normal_name(orig_enc):
        """Imitates get_normal_name in tokenizer.c (PRIVATE)."""
        # sys.stderr.write("DEBUG: _get_normal_name(%r)\n" % orig_enc)
        # Only care about the first 12 characters.
        enc = orig_enc[:12].lower().replace("_", "-")
        if enc == "utf-8" or enc.startswith("utf-8-"):
            return "utf-8"
        if enc in ("latin-1", "iso-8859-1", "iso-latin-1") or enc.startswith(
            ("latin-1-", "iso-8859-1-", "iso-latin-1-")
        ):
            return "iso-8859-1"
        return orig_enc

    def _find_cookie(line, filename, bom_found):
        """Find encoding string in a line of Python (PRIVATE)."""
        # sys.stderr.write("DEBUG: _find_cookie(%r, %r, %r)\n"
        #                  % (line, filename, bom_found))
        match = cookie_re.match(line)
        if not match:
            return None
        encoding = _get_normal_name(match.group(1))
        try:
            lookup(encoding)
        except LookupError:
            # This behaviour mimics the Python interpreter
            raise SyntaxError(
                "unknown encoding for {!r}: {}".format(filename, encoding)
            )

        if bom_found:
            if encoding != "utf-8":
                # This behaviour mimics the Python interpreter
                raise SyntaxError("encoding problem for {!r}: utf-8".format(filename))
            encoding += "-sig"
        return encoding

    def tokenize_open(filename):
        """Simulate opening a Python file read only with the correct encoding.

        While this was based on the Python 3 standard library function
        tokenize.open in order to backport it to Python 2.7, this proved
        painful.

        Note that because this text will later be fed into ``exex(...)`` we
        would hit SyntaxError encoding declaration in Unicode string, so the
        handle returned has the encoding line masked out!

        Note we don't just remove the line as that would throw off the line
        numbers, it is replaced with a Python comment.
        """
        # sys.stderr.write("DEBUG: tokenize_open(%r)\n" % filename)
        # Will check the first & second lines for an encoding
        # AND REMOVE IT FROM THE TEXT RETURNED
        with io_open(filename, "rb") as handle:
            lines = list(handle)

        # Find the encoding
        first = lines[0] if lines else b""
        second = lines[1] if len(lines) > 1 else b""
        default = "utf-8"
        bom_found = False
        if first.startswith(BOM_UTF8):
            bom_found = True
            first = first[3:]
            default = "utf-8-sig"
        encoding = _find_cookie(first, filename, bom_found)
        if encoding:
            lines[0] = "# original encoding removed\n"
        if not encoding and blank_re.match(first):
            # sys.stderr.write("DEBUG: Trying second line %r\n"
            #                  % second)
            encoding = _find_cookie(second, filename, bom_found)
            if encoding:
                lines[1] = "# original encoding removed\n"
        if not encoding:
            encoding = default

        # sys.stderr.write("DEBUG: tokenize_open using encoding=%r\n"
        #                  % encoding)

        # Apply the encoding, using StringIO as we removed the
        # original encoding to help legacy code using exec.
        # for b in lines:
        #     sys.stderr.write(b"DEBUG: " + b)
        return StringIO("".join(b.decode(encoding) for b in lines))


###################################
# End of backported tokenize code #
###################################

import restructuredtext_lint as rst_lint


__version__ = "0.1.0"


log = logging.getLogger(__name__)

rst_prefix = "RST"
rst_fail_load = 900
rst_fail_parse = 901
rst_fail_all = 902
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


####################################
# Start of code copied from PEP257 #
####################################

# This is the reference implementation of the alogrithm
# in PEP257 for removing the indentation of a docstring,
# which has been placed in the public domain.
#
# This includes the minor change from sys.maxint to
# sys.maxsize for Python 3 compatibility.
#
# https://www.python.org/dev/peps/pep-0257/#handling-docstring-indentation


def trim(docstring):
    """PEP257 docstring indentation trim function."""
    if not docstring:
        return ""
    # Convert tabs to spaces (following the normal Python rules)
    # and split into a list of lines:
    lines = docstring.expandtabs().splitlines()
    # Determine minimum indentation (first line doesn't count):
    indent = sys.maxsize
    for line in lines[1:]:
        stripped = line.lstrip()
        if stripped:
            indent = min(indent, len(line) - len(stripped))
    # Remove indentation (first line is special):
    trimmed = [lines[0].strip()]
    if indent < sys.maxsize:
        for line in lines[1:]:
            trimmed.append(line[indent:].rstrip())
    # Strip off trailing and leading blank lines:
    while trimmed and not trimmed[-1]:
        trimmed.pop()
    while trimmed and not trimmed[0]:
        trimmed.pop(0)
    # Return a single string:
    return "\n".join(trimmed)


##################################
# End of code copied from PEP257 #
##################################


def dequote_docstring(text):
    """Remove the quotes delimiting a docstring."""
    # TODO: Process escaped characters unless raw mode?
    text = text.strip()
    if len(text) > 6 and text[:3] == text[-3:] == '"""':
        # Standard case, """..."""
        return text[3:-3]
    if len(text) > 7 and text[:4] in ('u"""', 'r"""') and text[-3:] == '"""':
        # Unicode, u"""...""", or raw r"""..."""
        return text[4:-3]
    # Other flake8 tools will report atypical quotes:
    if len(text) > 6 and text[:3] == text[-3:] == "'''":
        return text[3:-3]
    if len(text) > 7 and text[:4] in ("u'''", "r'''") and text[-3:] == "'''":
        return text[4:-3]
    if len(text) > 2 and text[0] == text[-1] == '"':
        return text[1:-1]
    if len(text) > 3 and text[:2] in ('u"', 'r"') and text[-1] == '"':
        return text[2:-1]
    if len(text) > 2 and text[0] == text[-1] == "'":
        return text[1:-1]
    if len(text) > 3 and text[:2] in ("u'", "r'") and text[-1] == "'":
        return text[2:-1]
    raise ValueError("Bad quotes!")


parse = Parser()  # from pydocstyle


class reStructuredTextChecker(object):
    """Checker of Python docstrings as reStructuredText."""

    name = "rst-docstrings"
    version = __version__

    STDIN_NAMES = {"stdin", "-", "(none)", None}

    def __init__(self, tree, filename="(none)"):
        """Initialise."""
        self.tree = tree
        self.filename = filename
        try:
            self.load_source()
            self.err = None
        except Exception as err:
            self.source = None
            self.err = err

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
        # Is there any reason not to call load_source here?
        if self.err is not None:
            assert self.source is None
            msg = "%s%03i %s" % (
                rst_prefix,
                rst_fail_load,
                "Failed to load file: %s" % self.err,
            )
            yield 0, 0, msg, type(self)
            module = []
        try:
            module = parse(StringIO(self.source), self.filename)
        except SyntaxError as err:
            msg = "%s%03i %s" % (
                rst_prefix,
                rst_fail_parse,
                "Failed to parse file: %s" % err,
            )
            yield 0, 0, msg, type(self)
            module = []
        if module.dunder_all_error:
            msg = "%s%03i %s" % (
                rst_prefix,
                rst_fail_all,
                "Failed to parse __all__ entry.",
            )
            yield 0, 0, msg, type(self)
            # module = []
        for definition in module:
            if not definition.docstring:
                # People can use flake8-docstrings to report missing
                # docstrings
                continue
            try:
                # Note we use the PEP257 trim algorithm to remove the
                # leading whitespace from each line - this avoids false
                # positive severe error "Unexpected section title."
                unindented = trim(dequote_docstring(definition.docstring))
                # Off load RST validation to reStructuredText-lint
                # which calls docutils internally.
                # TODO: Should we pass the Python filename as filepath?
                rst_errors = list(rst_lint.lint(unindented))
            except Exception as err:
                # e.g. UnicodeDecodeError
                msg = "%s%03i %s" % (
                    rst_prefix,
                    rst_fail_lint,
                    "Failed to lint docstring: %s - %s" % (definition.name, err),
                )
                yield definition.start, 0, msg, type(self)
                continue
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

                # This will return the line number by combining the
                # start of the docstring with the offet within it.
                # We don't know the column number, leaving as zero.
                yield definition.start + rst_error.line, 0, msg, type(self)

    def load_source(self):
        """Load the source for the specified file."""
        if self.filename in self.STDIN_NAMES:
            self.filename = "stdin"
            if sys.version_info[0] < 3:
                self.source = sys.stdin.read()
            else:
                self.source = TextIOWrapper(sys.stdin.buffer, errors="ignore").read()
        else:
            # Could be a Python 2.7 StringIO with no context manager, sigh.
            # with tokenize_open(self.filename) as fd:
            #     self.source = fd.read()
            handle = tokenize_open(self.filename)
            self.source = handle.read()
            handle.close()
