#!/bin/bash
IFS=$'\n\t'
set -eu
# Note not using "set -o pipefile" until after check error message with grep

# Examples which should fail
for code in RST??? ; do
    echo "======"
    echo $code
    echo "======"
    flake8 --select RST $code/ 2>&1 | grep $code
    echo "Return code $? from $code tests"
done
# echo "Positive tests passed (RST errors reported as expected)."

set -o pipefail

# Examples which should pass
echo "========="
echo "Negatives"
echo "========="
flake8 --select RST test_cases/
#echo "Negative tests passed (no RST errors reported as expected)."

echo "============"
echo "Tests passed"
echo "============"
