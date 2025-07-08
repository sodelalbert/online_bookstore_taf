#!/bin/bash

# Set reports directory variable
REPORTS_DIR="reports"

black_status=0
pylint_status=0
mypy_status=0

# Run Black
uv run black . > "$REPORTS_DIR/black_output.txt" 2>&1
black_status=$?

# Run Pylint
uv run pylint **/*.py > "$REPORTS_DIR/pylint_report.txt" 2>&1
pylint_status=$?

# Run Mypy
uv run mypy . > "$REPORTS_DIR/mypy_report.txt" 2>&1
mypy_status=$?

# Print Summary
printf "%-8s %s\n" "Black:"  "$([ $black_status -eq 0 ] && echo '✅' || echo '❌')"
printf "%-8s %s\n" "Pylint:" "$([ $pylint_status -eq 0 ] && echo '✅' || echo '❌')"
printf "%-8s %s\n" "Mypy:"   "$([ $mypy_status -eq 0 ] && echo '✅' || echo '❌')"

# Show output of failing checks
if [ $black_status -ne 0 ]; then
    echo -e "\n--- Black Output ---"
    cat "$REPORTS_DIR/black_output.txt"
fi
if [ $pylint_status -ne 0 ]; then
    echo -e "\n--- Pylint Output ---"
    cat "$REPORTS_DIR/pylint_report.txt"
fi
if [ $mypy_status -ne 0 ]; then
    echo -e "\n--- Mypy Output ---"
    cat "$REPORTS_DIR/mypy_report.txt"
fi

echo
if [ $black_status -eq 0 ] && [ $pylint_status -eq 0 ] && [ $mypy_status -eq 0 ]; then
    echo "🎉 All checks passed!"
else
    echo "⚠️  Some checks failed. See above for details."
fi

# Clean up reports
rm -f reports/black_output.txt reports/pylint_report.txt reports/mypy_report.txt 2>/dev/null