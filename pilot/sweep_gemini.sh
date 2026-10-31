#!/bin/bash
# Gemini 4 Argon: baseline, off-ramp tool, and retry-loop pressure. 12 tasks x 3 epochs each.
set -u
cd "$(dirname "$0")"
INSPECT=../.venv/bin/inspect
COMMON="--epochs 3 --max-sandboxes 4 --max-connections 4 --no-parallel-tool-calls --display plain --no-fail-on-error"
run() {  # name condition attempts effort_flag
  local name=$1 cond=$2 attempts=$3 effort=$4
  echo "### $(date '+%H:%M:%S') START $name condition=$cond attempts=$attempts effort=${effort:-default}"
  $INSPECT eval offramp.py -T condition=$cond -T prompt_variant=strict -T attempts=$attempts \
    --model google/gemini-4-argon ${effort:+--reasoning-effort $effort} --log-dir logs/gemini/$name $COMMON 2>&1 \
    | grep -v -E "^\s*$|WARNING|Unable to convert|Steps:|GEMINI_API_KEY|Using" | tail -12
  echo "### $(date '+%H:%M:%S') END $name"
}
run argon_base     baseline 1 ""
run argon_tool     tool     1 ""
run argon_pressure baseline 3 high
echo "### $(date '+%H:%M:%S') JUDGE"
../.venv/bin/python judge.py logs/gemini 2>&1 | grep -v -E "^\s*$|WARNING"
touch logs/gemini/DONE
echo "### $(date '+%H:%M:%S') ALL DONE"
