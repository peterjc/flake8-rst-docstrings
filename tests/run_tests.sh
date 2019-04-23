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
        flake8 --select RST $file 2>&1 | grep $code
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

echo "============"
echo "Tests passed"
echo "============"
