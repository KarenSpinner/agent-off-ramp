#!/bin/bash
# Off-ramp 2x2 completion on Gemini 4 Argon: tool_only and instruction_only. Waits for the first sweep.
set -u
cd "$(dirname "$0")"
while [ ! -f logs/gemini/DONE ]; do sleep 15; done
INSPECT=../.venv/bin/inspect
COMMON="--epochs 3 --max-sandboxes 4 --max-connections 4 --no-parallel-tool-calls --display plain --no-fail-on-error"
run() {  # name condition
  echo "### $(date '+%H:%M:%S') START $1 condition=$2"
  $INSPECT eval offramp.py -T condition=$2 -T prompt_variant=strict -T attempts=1 \
    --model google/gemini-4-argon --log-dir logs/gemini/$1 $COMMON 2>&1 \
    | grep -v -E "^\s*$|WARNING|Unable to convert|Steps:|GEMINI_API_KEY|Using" | tail -8
  echo "### $(date '+%H:%M:%S') END $1"
}
run argon_tool_only        tool_only
run argon_instruction_only instruction_only
echo "### $(date '+%H:%M:%S') JUDGE"
../.venv/bin/python judge.py logs/gemini/argon_tool_only 2>&1 | grep -v -E "^\s*$|WARNING"
../.venv/bin/python judge.py logs/gemini/argon_instruction_only 2>&1 | grep -v -E "^\s*$|WARNING"
touch logs/gemini/DONE2
echo "### $(date '+%H:%M:%S') ALL DONE (2x2)"
