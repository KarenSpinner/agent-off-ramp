#!/bin/bash
# Pressure sweep: six configurations, 12 tasks x 3 epochs each, one tool call per turn.
set -u
cd "$(dirname "$0")"
INSPECT=../.venv/bin/inspect
COMMON="--epochs 3 --max-sandboxes 4 --max-connections 4 --no-parallel-tool-calls --display plain --no-fail-on-error"
run() {  # name model effort attempts prompt_variant
  local name=$1 model=$2 effort=$3 attempts=$4 variant=$5
  echo "### $(date '+%H:%M:%S') START $name  model=$model effort=$effort attempts=$attempts prompt=$variant"
  $INSPECT eval offramp.py -T condition=baseline -T prompt_variant=$variant -T attempts=$attempts \
    --model $model --reasoning-effort $effort --log-dir logs/sweep/$name $COMMON 2>&1 \
    | grep -v -E "^\s*$|WARNING|Unable to convert|Steps:" | tail -12
  echo "### $(date '+%H:%M:%S') END $name"
}
run haiku_base      anthropic/claude-haiku-5-5  medium 1 strict
run opus_base       anthropic/claude-opus-5-5   medium 1 strict
run sonnet_base     anthropic/claude-sonnet-5-5 medium 1 strict
run sonnet_weak     anthropic/claude-sonnet-5-5 medium 1 weak
run sonnet_pressure anthropic/claude-sonnet-5-5 xhigh  3 strict
run sonnet_max      anthropic/claude-sonnet-5-5 xhigh  3 weak
echo "### $(date '+%H:%M:%S') JUDGE"
../.venv/bin/python judge.py logs/sweep 2>&1 | grep -v -E "^\s*$|WARNING"
touch logs/sweep/DONE
echo "### $(date '+%H:%M:%S') ALL DONE"
