#!/bin/bash
echo "=== Test 1: Config dump ==="
./run.sh --package test --repo tests/test_repo.json --test-mode

echo -e "\n=== Test 2: ASCII tree ==="
./run.sh --package A --repo tests/test_repo.json --test-mode --ascii-tree --max-depth 2

echo -e "\n=== Test 3: Reverse deps ==="
./run.sh --package D --repo tests/test_repo.json --test-mode

echo -e "\n=== Test 4: Error handling ==="
./run.sh --package test --repo nonexistent.json --test-mode

echo -e "\n=== All tests completed ==="
