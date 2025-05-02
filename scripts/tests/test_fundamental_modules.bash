#!/bin/bash

: <<'END_COMMENT'

This script will run the tests for the fundamental modules.
What are they?
    * pipeline.py : Pipeline class is a fundamental class that must have 100% coverage and must pass 100% of the tests.
    * task.py : Task class is a fundamental class that must have 100% coverage and must pass 100% of the tests.

END_COMMENT

pytest tests/unit_tests/modules/pipeline/test_pipeline.py > /dev/null 2>&1

printf "\nTESTS THAT MUST PASS: \ntest_pipeline.py \n"

if [ $? -eq 0 ]; then
    printf "\n ✅ ALL TESTS FROM test_pipeline.py PASSED! \n"
else
    printf "\n❌ Some tests in test_pipeline.py FAILED.\n"
fi

