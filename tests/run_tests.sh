#!/bin/bash
IFS=$'\n\t'
set -eu
# Note not using "set -o pipefile" until after check error message with grep

# Examples which should fail
for code in RST??? ; do
    echo "======"
    echo $code
    echo "======"
    for file in $code/*.py ; do
        echo "flake8 --select RST $file"
        flake8 --select RST $file 2>&1 | grep ": $code "
    done
    echo "Good, $code violations reported, as expected."
done
# echo "Positive tests passed (RST errors reported as expected)."

set -o pipefail

# Examples which should pass
echo "========="
echo "Negatives"
echo "========="
echo "flake8 --select RST test_cases/"
flake8 --select RST test_cases/
echo "Good, no RST style violations reported, as expected."

echo "================"
echo "Extra directives"
echo "================"
# Checked this failed earlier in the RST303 tests
flake8 --select RST --rst-directives=req,spec,needfilter RST303/sphinx-directives.py
echo "Good, no RST303 style violations reported, as expected."

echo "==========="
echo "Extra roles"
echo "==========="
# Checked this failed earlier in the RST304 tests
flake8 --select RST --rst-roles need,need_incoming RST304/sphinx-roles.py
echo "Good, no RST304 style violations reported, as expected."

echo "========="
echo "Help text"
echo "========="
flake8 -h | grep -i RST
echo "Good, RST options appear in the help text"

echo "============"
echo "Tests passed"
echo "============"
