# Result Format

Your structured result must be valid JSON. The required schema depends on
your stage type.

## Say which packet you are answering

Every result must carry `packet_hash`, copied verbatim from the
`SOURCE_DIGEST`-bearing packet you were given. It is the value `tpt` recorded
when it issued that packet, and it is how the engine knows your result answers
the guidance you actually received rather than some earlier packet. A result
without it, or with the wrong one, is refused and the run does not advance.

You are given the packet's hash by whoever handed you the packet. If you do
not have it, ask for it; do not guess.

## Worker (linear or revision) stages

```json
{
  "packet_hash": "<the hash of the packet you were given>",
  "disposition": "PASS",
  "summary": "One or two sentences describing what you did.",
  "artifact_path": "src/gpt/liturgy/roman-rite/1962/propers/temporal/46-ninth-after-pentecost/main.tex"
}
```

`disposition` must be `"PASS"` when you completed the work. If you cannot
complete it, set `disposition` to `"BLOCKED"` and explain why in
`block_reason`; the workflow stops there for an operator to look at. Never
report `PASS` for work you did not do: nothing downstream reads your
`summary`, so a false `PASS` advances the run as though the stage had
succeeded.

## Evaluator stages

```json
{
  "packet_hash": "<the hash of the packet you were given>",
  "disposition": "PASS" | "CHANGES_REQUIRED" | "BLOCKED",
  "summary": "One or two sentences.",
  "findings": [
    {
      "id": "VIS-001",
      "severity": "blocking",
      "location": "page 4",
      "problem": "Description of the issue.",
      "required_result": "What the reviser must produce to resolve this finding."
    }
  ]
}
```

- `PASS`: no blocking findings. The workflow advances.
- `CHANGES_REQUIRED`: blocking findings present. The workflow enters a
  bounded revision loop. Findings are forwarded verbatim to the reviser.
- `BLOCKED`: a finding cannot be resolved by revision. The workflow stops.

Finding IDs must be stable across iterations (e.g., `VIS-001` refers to the
same issue every time it appears). Use a prefix matching the evaluator type:
`CON-` for content, `VIS-` for visual.

Only `blocking` severity findings trigger revision. `advisory` findings are
recorded but do not block.

## Gate stages

Gates are run by `tpt` directly. No AI worker result is needed, and no
`packet_hash` is required: the engine composes the gate's result itself. The
parent driver runs `tpt ... advance <run-id> --run-gate`.

## Fail closed

A malformed or missing result causes the workflow to stop with an error. No
transition occurs. The run remains inspectable but cannot advance until a
valid result is submitted.
