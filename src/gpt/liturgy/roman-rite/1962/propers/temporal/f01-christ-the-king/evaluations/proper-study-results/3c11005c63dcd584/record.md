# Actual engine results

Workflow `proper-study`, version 12, digest `e6d49782e4c62eb282fbb9ce1e18a27f1e74c81170f26533f5efea288ebf4ff5`.
Run `3c11005c63dcd584`; seed commit `dbaed43763020c5deea78e4cf4fcbba124edf58a`. Terminal disposition **BLOCKED**.

The JSON files are exact engine-retained result bytes, copied after the run reached its terminal disposition. A stage's PASS records only its own completed work; publication acceptance is the terminal gate's. The engine supplies any `review_inputs` seal; workers do not author it. The interventions are the driver's records of host facts the packets do not carry, and the driver's account of every cycle is in `workflows/reviews/gpt-1962-f01-production-2026-10-19/CYCLES.md`.

| Stage | Iteration | Disposition | Packet SHA-256 | Accepted result SHA-256 |
| --- | ---: | --- | --- | --- |
| scope-gate | 0 | PASS | `151ca846dbbcbc28baad8990dea7ad8d59cf3e055975caee8cab653eb4181c02` | `c2c5dc73384dcaa82e6a0b0b6d655a49fd9f0d8345607513add762f6826c4e2d` |
| resolve-context | 0 | PASS | `e61211d395842ebbe4ca0035ecf1fef52400e7bdde3a602a4034270fa55ebac0` | `477a612121fbf7b427ba81468fde6639fb4571cc087d8c20ccaa65121ef5db31` |
| research | 0 | BLOCKED | `54268de70b4b827b140d39be8f380615ba446e1478f29d21a01e8ccc507a877d` | `7fd87694857663b009e1cd556d889a54c0f44a479c793ba245434a8ae2326a5c` |

The run recorded 3 results over 3 packets, all of which are preserved verbatim under `packets/`.

The run recorded no manual intervention, so there is no `interventions/` directory.

`terminal-status.json` and `terminal-replay.json` are the engine's own terminal records. A terminal replay reports `deterministic: null` by design and checks the saved packet's integrity, which it confirms.
