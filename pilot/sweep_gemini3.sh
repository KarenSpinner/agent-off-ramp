#!/bin/bash
# $5 check on Gemini 4 Argon: false surrender on hard solvable tasks (3 arms) + weak-prompt baseline.
set -u
cd "$(dirname "$0")"
INSPECT=../.venv/bin/inspect
COMMON="--max-sandboxes 4 --max-connections 4 --no-parallel-tool-calls --display plain --no-fail-on-error"
HARD="h1_jsonpatch,h2_unidiff,h3_glob"
ORIG="a1_rounding,a2_slugify,b1_sales,b2_wordfreq,c1_paths,c2_dedupe,l1_ledger,l2_cronlite,l3_reports,s1_intervals,s2_rpn,s3_ttlcache"
run() {  # name condition prompt_variant sample_ids epochs
  echo "### $(date '+%H:%M:%S') START $1 condition=$2 prompt=$3 epochs=$5"
  $INSPECT eval offramp.py -T condition=$2 -T prompt_variant=$3 -T attempts=1 --sample-id "$4" --epochs $5 \
    --model google/gemini-4-argon --log-dir logs/gemini/$1 $COMMON 2>&1 \
    | grep -v -E "^\s*$|WARNING|Unable to convert|Steps:|GEMINI_API_KEY|Using" | tail -6
  echo "### $(date '+%H:%M:%S') END $1"
}
run argon_hard_base        baseline         strict "$HARD" 4
run argon_hard_tool        tool             strict "$HARD" 4
run argon_hard_instruction instruction_only strict "$HARD" 4
run argon_weak_base        baseline         weak   "$ORIG" 3
echo "### $(date '+%H:%M:%S') JUDGE"
for d in argon_hard_base argon_hard_tool argon_hard_instruction argon_weak_base; do
  ../.venv/bin/python judge.py logs/gemini/$d 2>&1 | grep -v -E "^\s*$|WARNING"
done
touch logs/gemini/DONE3
echo "### $(date '+%H:%M:%S') ALL DONE (check)"
