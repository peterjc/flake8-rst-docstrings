"""Test suite."""
import glob
import os.path
from os.path import join
from subprocess import Popen, PIPE, DEVNULL

import pytest


def pytest_generate_tests(metafunc):
    """Handle listing and generating the ``expected_failure`` test cases."""
    if "expected_failure" in metafunc.fixturenames:
        modpath = os.path.dirname(metafunc.module.__file__)
        pattern = os.path.join(modpath, "RST???", "*.py")
        metafunc.parametrize(
            "expected_failure",
            [os.path.relpath(p, modpath) for p in sorted(glob.glob(pattern))],
        )


@pytest.fixture(scope="module")
def modpath(request):
    """Provide the path of the module being run, for access to test files."""
    return os.path.dirname(request.module.__file__)


def flake8(path, *, select="RST", roles=None, directives=None):
    """Run flake8 on a specific ``path`` and report the results.

    :param str path: path to run flake8 on
    :param str select: error codes to check, defaults to ``RST``
    :param str roles: comma-separated list of roles to ignore (for ``RST304``)
    :param str directives: comma-separated list of directives to ignore
        (for ``RST303``)
    :returns: a pair of flake8"s return code and its decoded stdout
    :rtype: tuple[int, str]
    """
    args = ["flake8", "--select", select]
    if roles:
        args.extend(["--rst-roles", roles])
    if directives:
        args.extend(["--rst-directives", directives])
    args.append(path)

    p = Popen(args, stdin=DEVNULL, stdout=PIPE)
    out, _ = p.communicate()
    return p.returncode, out.decode()


def test_expected_failures(modpath, expected_failure):
    """Check a single expected failure (negative test case).

    Runs flake8 on ``expected_failure`` which should be of the form
    :samp:`{code}/{file}`.

    Validates that the run fails, and outputs the expected error code.
    """
    code = os.path.dirname(expected_failure)
    retcode, out = flake8(join(modpath, expected_failure))
    assert retcode, "expected failure (%s), got success" % code
    needle = ": %s " % code
    assert needle in out


def test_expected_successes(modpath):
    """Verify the positive test cases (expected successes)."""
    retcode, out = flake8(join(modpath, "test_cases"))
    assert not retcode, out


def test_extra_directives(modpath):
    """Verify that ``RST303`` can be fixed by specifying directives to allow."""
    retcode, out = flake8(
        join(modpath, "RST303/sphinx-directives"),
        directives="req,spec,needfilter",
    )
    assert not retcode, out


def test_extra_roles(modpath):
    """Verify that ``RST304`` can be fixed by specifying roles to allow."""
    retcode, out = flake8(
        join(modpath, "RST304/sphinx-roles.py"),
        roles="need,need_incoming",
    )
    assert not retcode, out


def test_help():
    """Check that ``rst-docstrings``" options show up in the help text."""
    p = Popen(["flake8", "-h"], stdin=DEVNULL, stdout=PIPE)
    out, err = p.communicate()

    assert not p.returncode, err
    assert b" --rst-" in out, "rst options should appear in help text"
    assert not err


def test_version():
    """Check that ``rst-docstrings`` appears in the help text."""
    p = Popen(["flake8", "--version"], stdin=DEVNULL, stdout=PIPE)
    out, err = p.communicate()

    assert not p.returncode, err
    assert b"rst-docstrings:" in out, "should appear in flake8 version string"
    assert not err
