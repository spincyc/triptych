# Actual engine results

Workflow `proper-study`, version 13, digest `7568a7728ef8a16e5a7c65475e9a3ae0d24c695caab6faa5d0c0c7ec52621d16`.
Run `8d637d6f2f9160aa`; seed commit `0b318d4007e01f0be65399fd75863732dedf2372`. Terminal disposition **BLOCKED**.

The JSON files are exact engine-retained result bytes, copied after the run reached its terminal disposition. A stage's PASS records only its own completed work; publication acceptance is the terminal gate's. The engine supplies any `review_inputs` seal; workers do not author it. The interventions are the driver's records of host facts the packets do not carry, and the driver's account of every cycle is in `workflows/reviews/gpt-1962-f01-production-2026-10-19/CYCLES.md`.

| Stage | Iteration | Disposition | Packet SHA-256 | Accepted result SHA-256 |
| --- | ---: | --- | --- | --- |
| scope-gate | 0 | PASS | `a8778aa1976e36c954ce6d553b844ba53543f522a41d8be41ddf63ddd45ed313` | `c2c5dc73384dcaa82e6a0b0b6d655a49fd9f0d8345607513add762f6826c4e2d` |
| resolve-context | 0 | PASS | `a39c6b75ba7c9e454c6d81c0f97cdb5239beea1cabd02d9ebd347c229af5e87e` | `2fe35dd181ddc13270084293b8b22ab0757a7fbc9bde63a8dba5ecd66d60ae54` |
| research | 0 | BLOCKED | `fe8dee4a70fba5caa52ad6a3e037dea43bedee0a214f6936f02dd0c931b76fce` | `b076e88d0b7d42816b90f2614fc62375f843b94eb573d84cf499b52eb93d2331` |

The run recorded 3 results over 3 packets, all of which are preserved verbatim under `packets/`.

`interventions/` holds the 1 manual intervention this run recorded. It is unencoded workflow debt, not an acceptance.

`terminal-status.json` and `terminal-replay.json` are the engine's own terminal records. A terminal replay reports `deterministic: null` by design and checks the saved packet's integrity, which it confirms.
