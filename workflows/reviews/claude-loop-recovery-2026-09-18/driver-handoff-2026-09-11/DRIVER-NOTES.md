# Driver notes for the three proper-finish v5 runs (session 2026-09-09)

Order: 55 (35/22 pp, three findings short) -> 56 (canonical passed under v4; companion to derive) -> 54 (76/45 pp).

Per stage:
- SINGLE: one fresh subagent (Agent tool, general-purpose), packet handed by absolute path + sha256, result JSON written by the agent to .scratch/tpt/<run>/<stage>-<iter>.result.json; validate shape before advance.
- FANOUT: one fresh subagent per lane, all five in one message; each gets its own lane packet path + lane_packet_hash; results to .scratch/tpt/<run>/<stage>-<iter>-lane-<nn>-<lane>.result.json.
- GATE: tools/tpt proper-finish <doc> advance <run> --run-gate.
- Effort: host exposes no per-dispatch effort; subagents inherit the session level (xhigh). Record one intervention per run at seed (as run efff3a6f did).
- Never summarize lane results; never write a finding myself; verify reviser claims against the built PDFs before advancing (grep + page counts).
- Evaluators are never told the budget position; revisers are told a false `repaired` is the worse outcome.

Baseline page counts (merged tree, before any run): 54 76/45, 55 35/22, 56 45/29.
