#!/bin/sh
# The fully qualified FAIL/ERROR header identities of one unittest run,
# sorted and deduplicated. Two runs are compared by this set because the head
# runs more tests than the parent, so no literal count identity is claimable.
grep -E '^(FAIL|ERROR): ' "$1" | sed -E 's/^(FAIL|ERROR): [^(]*\((.*)\)$/\1 \2/' | sort -u
