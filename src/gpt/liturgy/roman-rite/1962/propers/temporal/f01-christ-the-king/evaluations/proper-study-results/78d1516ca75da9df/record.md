# Actual engine results

Workflow `proper-study`, version 13, digest `7568a7728ef8a16e5a7c65475e9a3ae0d24c695caab6faa5d0c0c7ec52621d16`.
Run `78d1516ca75da9df`; seed commit `e8d76b1266990caa5eb18b50d1862af3453483bc`. Terminal disposition **BLOCKED**.

The JSON files are exact engine-retained result bytes, copied after the run reached its terminal disposition. A stage's PASS records only its own completed work; publication acceptance is the terminal gate's. The engine supplies any `review_inputs` seal; workers do not author it. The interventions are the driver's records of host facts the packets do not carry, and the driver's account of every cycle is in `workflows/reviews/gpt-1962-f01-production-2026-10-19/CYCLES.md`.

| Stage | Iteration | Disposition | Packet SHA-256 | Accepted result SHA-256 |
| --- | ---: | --- | --- | --- |
| scope-gate | 0 | PASS | `e5abf082113df541ae2c1476e02ccf7519a517cfefec8e33c5653e55d78a63ed` | `c2c5dc73384dcaa82e6a0b0b6d655a49fd9f0d8345607513add762f6826c4e2d` |
| resolve-context | 0 | PASS | `72d73812f713c27f65136ac5bd9518fb2a33e368ff5f462cb2c5d8c2f97341ce` | `e2c7b66afaf97c89c5c1c397b6f211b223dac1df5c3cea291948efeb923c86af` |
| research | 0 | BLOCKED | `408043e134033a174b991927b9179b8048e9a11953a858b8f9c3a0c4a38c0239` | `70607448f3cb916634aca8d9d12cd0082698460d95351eafa7c64a95771b1ac4` |

The run recorded 3 results over 3 packets, all of which are preserved verbatim under `packets/`.

The run recorded no manual intervention, so there is no `interventions/` directory.

`terminal-status.json` and `terminal-replay.json` are the engine's own terminal records. A terminal replay reports `deterministic: null` by design and checks the saved packet's integrity, which it confirms.
