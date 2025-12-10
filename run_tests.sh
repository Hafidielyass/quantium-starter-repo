#!/bin/bash

# Script to run the Pink Morsels Sales app test suite
# Activates the virtual environment and executes pytest
# Returns exit code 0 if all tests pass, 1 if any fail

set -e  # Exit on any error

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Activate the virtual environment
if [ -f "$SCRIPT_DIR/venv/Scripts/activate" ]; then
    source "$SCRIPT_DIR/venv/Scripts/activate"
elif [ -f "$SCRIPT_DIR/venv/bin/activate" ]; then
    source "$SCRIPT_DIR/venv/bin/activate"
else
    echo "Error: Virtual environment not found"
    exit 1
fi

# Run the test suite
echo "Running test suite..."
python -m pytest tests/test_app.py -v

# Capture the exit code
TEST_EXIT_CODE=$?

# Return the exit code from pytest
exit $TEST_EXIT_CODE
