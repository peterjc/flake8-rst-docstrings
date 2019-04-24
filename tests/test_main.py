"""Core test module for flake8-rst-docstrings."""

import re
import subprocess as sp
from pathlib import Path

import pytest


tests_dir_path = Path(__file__).parent

p_fail_dirname = re.compile(r"^RST(\d+)$", re.I)

fail_dirs = [
    d
    for d in tests_dir_path.iterdir()
    if d.is_dir() and p_fail_dirname.match(d.name)
]

good_files = [
    f
    for f in (tests_dir_path / "test_cases").iterdir()
    if f.is_file() and f.name.endswith(".py")
]


@pytest.mark.parametrize('dir_path', fail_dirs, ids=(lambda d: d.name))
def test_error_examples(dir_path, subtests):
    """Confirm expected-error docstrings."""
    for file_path in [
        f
        for f in dir_path.iterdir()
        if f.name.endswith(".py")
    ]:
        with subtests.test(msg=file_path.name):
            try:
                sp.check_output(
                    ["flake8", "--select", "RST", str(file_path.resolve())],
                    shell=True,
                )
            except sp.CalledProcessError as e:
                assert e.returncode == 1
                assert dir_path.name in e.output.decode()
            else:
                pytest.fail("Error code {} not raised".format(dir_path.name))


@pytest.mark.parametrize('file_path', good_files, ids=(lambda f: f.name))
def test_good_examples(file_path):
    """Confirm expect-no-error docstrings."""
    assert 0 == sp.call(["flake8", "--select", "RST", str(file_path.resolve())])
