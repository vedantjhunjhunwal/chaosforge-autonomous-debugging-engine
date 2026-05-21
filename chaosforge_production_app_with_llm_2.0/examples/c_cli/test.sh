#!/usr/bin/env bash
set -euo pipefail
gcc main.c -o main
./main '{"amount":100,"price":5}' >/dev/null
