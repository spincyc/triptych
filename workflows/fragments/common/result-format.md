# Result Format

Your structured result must be valid JSON. The required schema depends on
your stage type.

## Name the packet you are answering

Every result must repeat, exactly, the `STAGE` and `ITERATION` values from
this packet's header:

```json
{
  "stage": "<the STAGE line of this packet>",
  "iteration": <the ITERATION line of this packet, as a number>
}
```

The engine rejects a result that names any other packet. That is how it tells
your work from a result submitted for a different stage, or from an earlier
result resubmitted.

## Worker (linear or revision) stages

```json
{
  "stage": "author-proper",
  "iteration": 0,
  "disposition": "PASS",
  "summary": "One or two sentences describing what you did.",
  "artifact_path": "src/gpt/liturgy/roman-rite/1962/propers/temporal/46-ninth-after-pentecost/main.tex"
}
```

Use `disposition: "PASS"` when you completed the stage's work. If you could
not complete it, use `disposition: "BLOCKED"` with a `summary` naming what
stopped you: the run stops there. Do not report `PASS` for work you did not
do; the engine has no other way to tell the difference.

## Evaluator stages

```json
{
  "stage": "content-evaluation",
  "iteration": 0,
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

Gates are run by `tpt` directly. No AI worker result is needed. The parent
driver runs `tpt ... advance <run-id> --run-gate`.

## Fail closed

A malformed or missing result, or one naming a different packet, causes the
workflow to stop with an error. No transition occurs. The run remains
inspectable but cannot advance until a valid result for the current packet is
submitted.
