#!/usr/bin/env python3
"""Replay a recorded command, or prove that every recorded command replays.

THE DEFECT THIS ANSWERS. V15's `checks.txt` labelled all twenty-four command
rows "the exact string handed to the shell; re-runnable" while seven of them
carried `'$WORKSPACE/...'` or `'$REPO/...'` inside SINGLE QUOTES, which a
shell does not expand, with no assignments supplied anywhere in the package.
The label was not checked against anything. Nothing in the toolchain had ever
taken a recorded row and tried to run it.

WHAT THIS DOES, IN THREE MODES.

  --check      Validate every row against `catena_command`'s schema without
               running anything: cwd present and a defined root, argv or
               shell but not both, no variable trapped inside single quotes,
               no undefined root, no prose wearing a command's first word.
               Read-only, needs no checkout, and is what `checks.py` and
               `handoff-inventory.py` run internally.

  --replay     Bind the roots to real directories and EXECUTE a row, exactly
               as recorded, then compare the exit status against the one the
               record carries.

               AN EXIT STATUS ALONE IS NOT A NON-VACUITY PROOF, AND THIS
               DOCSTRING USED TO SAY IT WAS. It claimed the run "confirms the
               head named in the record is the process that ran"; nothing in
               the code confirmed anything of the kind, and the command-replay
               lane demonstrated a false pass on the most important row in the
               set. Binding both roots of `head-tests-against-parent` to an
               empty directory makes its `cp` fail, `&&` short-circuits,
               `python3 -m unittest` never runs, the shell exits 1, the record
               says 1, and this tool reported a match. A failed `cp` and a
               wave-1 suite with 288 failures both exit 1.

               So the claim is withdrawn and replaced by a check. Pass
               `--witness SUBSTRING`, repeatable: every substring must appear
               in the replayed output or the row is reported VACUOUS and the
               tool exits 1 even though the exit status matched. The recorded
               transcript's own headline is the witness to use -- `checks.txt`
               prints it on each row's `result :` slot for exactly this. With
               no `--witness` the tool says on its own output that the match
               rests on the exit status alone.

  --render     Print the shell rendering of a row, for a reader who wants to
               paste it. The rendering DERIVES from the record; it is never
               the stored truth, and every root reference in it is double
               quoted so it expands.

THE ROOTS ARE BOUND ON THE COMMAND LINE, ONCE EACH. A package records
`$CANDIDATE_REPO`, `$PARENT_REPO`, `$PACKAGE_ROOT`, `$TOOLS_ANCHOR` and
`$EVIDENCE_ROOT` and never a path. `--root NAME=PATH` binds one. An unbound
root that a row uses is a refusal, not an empty substitution: substituting
nothing would run the command in the wrong directory and report success.
"""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import subprocess
import sys

# NO BYTECODE, EVER, AND THIS IS NOT HOUSEKEEPING.
#
# `assemble.sh` runs `$PKG/logs/checks.py` at P5 -- AFTER the P3 freeze and
# BEFORE the P6 manifest -- and the import below would write
# `$PKG/logs/__pycache__/catena_command.cpython-3NN.pyc` into the tree that is
# about to be sealed. The manifest would then cover a binary member, and the
# archive's strict-UTF-8 check would refuse the package it just produced.
# Nothing imported across files in this anchor before V16, so this hazard did
# not exist and there was nothing guarding against it.
sys.dont_write_bytecode = True
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import catena_command as CC  # noqa: E402


def load(path: pathlib.Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def rows_of(blob: dict) -> list[dict]:
    rows = blob.get("commands")
    return rows if isinstance(rows, list) else []


def check(blob: dict, stream) -> int:
    """Validate every row. Zero problems is exit 0."""
    try:
        defined = set(CC.check_variables(blob.get("variables")))
    except CC.ExecProblem as problem:
        print(f"REFUSING: [{problem.code}] {problem.message}", file=stream)
        return 1
    print(f"roots defined: {', '.join('$' + one for one in sorted(defined))}",
          file=stream)
    problems = 0
    executable = 0
    for row in rows_of(blob):
        where = f"{row.get('side', '?')}/{row.get('slug', '?')}"
        record = row.get("exec")
        if record is None:
            print(f"  {where}: no exec record ({row.get('recorded', '?')})",
                  file=stream)
            continue
        verdict, why = CC.classify(row.get("command"), record, defined=defined)
        if verdict != CC.VERDICT_EXECUTABLE:
            print(f"  {where}: {verdict} -- {why}", file=stream)
            problems += 1
        else:
            executable += 1
    # THREE FIGURES, THREE NAMES. V15 printed one -- "LITERAL: 24" -- over a
    # set in which seven rows were not what the one figure said they were.
    print(f"rows with an exec record: {sum(1 for r in rows_of(blob) if r.get('exec'))}",
          file=stream)
    print(f"rows validated EXECUTABLE: {executable}", file=stream)
    print(f"rows refused             : {problems}", file=stream)
    return 1 if problems else 0


def find(blob: dict, side: str | None, slug: str) -> dict | None:
    for row in rows_of(blob):
        if row.get("slug") != slug:
            continue
        if side and row.get("side") != side:
            continue
        return row
    return None


def run_and_echo(form, cwd: str, env: dict, stream) -> tuple[int, str]:
    """Run the resolved form, echoing its output AND keeping it.

    The output is what a witness is checked against, so it has to be held; it
    is echoed line by line as it arrives so a reviewer watching a twenty-minute
    suite still sees it happen. `stderr` is folded into `stdout` because the
    thing being tested is what the run SAID, and the recorded transcripts the
    witnesses come from are themselves `> log 2>&1`.
    """
    argv = form if isinstance(form, list) else ["/bin/sh", "-c", form]
    done = subprocess.Popen(argv, cwd=cwd, env=env, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, text=True,
                            errors="replace", bufsize=1)
    captured: list[str] = []
    assert done.stdout is not None
    for line in done.stdout:
        captured.append(line)
        stream.write(line)
        stream.flush()
    return done.wait(), "".join(captured)


def replay(row: dict, roots: dict[str, str], stream, dry: bool = False,
           witness: list[str] | None = None) -> int:
    record = row.get("exec")
    if record is None:
        print(f"REFUSING: {row.get('slug')} carries no exec record; there is "
              f"nothing to replay", file=stream)
        return 2
    try:
        cwd, overlay, form = CC.resolve(record, roots)
    except CC.ExecProblem as problem:
        print(f"REFUSING: [{problem.code}] {problem.message}", file=stream)
        return 2
    if not pathlib.Path(cwd).is_dir():
        print(f"REFUSING: the bound root for {record['cwd']} is not a "
              f"directory", file=stream)
        return 2
    env = dict(os.environ)
    env.update(overlay)
    if isinstance(form, list):
        shown = " ".join(CC.quote_token(one) for one in form)
        head = form[0]
    else:
        shown = form
        head = CC.head_of(form)
    print(f"cwd  : {record['cwd']}", file=stream)
    print(f"env  : {json.dumps(overlay, sort_keys=True)}", file=stream)
    print(f"head : {head}", file=stream)
    print(f"run  : {shown}", file=stream)
    wanted = list(witness or [])
    for one in wanted:
        print(f"want : {one!r} in the replayed output", file=stream)
    if dry:
        return 0
    status, said = run_and_echo(form, cwd, env, stream)
    recorded = row.get("exit")
    print(f"exit : {status} (recorded {recorded})", file=stream)

    # THE EXIT STATUS IS NECESSARY AND IT IS NOT SUFFICIENT.
    #
    # A replay that cannot distinguish "the tool ran and returned 1" from "the
    # shell fell over and returned 1" is not evidence, and this tool used to
    # claim it was. Each witness is a substring of what the intended tool
    # itself printed, taken from the recorded transcript; a run in which the
    # tool never started cannot contain one.
    missing = [one for one in wanted if one not in said]
    for one in wanted:
        print(f"witness: {'FOUND  ' if one in said else 'MISSING'} {one!r}",
              file=stream)
    if recorded is None and not wanted:
        return 0
    diverged = recorded is not None and int(recorded) != status
    if diverged:
        print(f"DIVERGED: {row.get('slug')} recorded exit {recorded} and "
              f"replayed exit {status}", file=stream)
    if missing:
        # VACUOUS, NOT DIVERGED, and the two words mean different things. The
        # exit may well have matched; what is missing is any evidence that the
        # process the record names is the process that produced it.
        print(f"VACUOUS: {row.get('slug')} replayed to exit {status} without "
              + ("any of" if len(missing) > 1 else "")
              + " the recorded output " + ", ".join(repr(one)
                                                    for one in missing)
              + "; the exit status was reproduced and the run was not",
              file=stream)
    if diverged or missing:
        return 1
    if not wanted:
        # SAID OUT LOUD, ON THE TOOL'S OWN OUTPUT, EVERY TIME. A reader who
        # takes this run as proof that the row re-ran is entitled to know what
        # was actually compared.
        print("note : this row matched on EXIT STATUS ALONE. Nothing here "
              "proves the tool named in the record is what produced it -- "
              "pass --witness with a line from the recorded transcript "
              "(checks.txt prints one on each row's `result :` slot) to "
              "require that too", file=stream)
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--commands", type=pathlib.Path, required=True,
                        metavar="COMMANDS.JSON",
                        help="the machine-readable command record")
    parser.add_argument("--check", action="store_true",
                        help="validate every row; run nothing")
    parser.add_argument("--render", metavar="SLUG",
                        help="print one row's shell rendering")
    parser.add_argument("--replay", metavar="SLUG",
                        help="bind the roots and execute one row")
    parser.add_argument("--side", default=None,
                        help="which battery side the slug belongs to")
    parser.add_argument("--root", action="append", default=[],
                        metavar="NAME=PATH",
                        help="bind one root variable; repeat per root")
    parser.add_argument("--dry-run", action="store_true",
                        help="with --replay, resolve and print but do not run")
    parser.add_argument("--witness", action="append", default=[],
                        metavar="SUBSTRING",
                        help="with --replay, require this text in the "
                             "replayed output; repeat per witness. Without "
                             "one the row is compared on exit status alone")
    args = parser.parse_args(argv)

    try:
        blob = load(args.commands)
    except (OSError, ValueError) as problem:
        print(f"cannot read {args.commands}: {problem}", file=sys.stderr)
        return 2

    if args.check:
        return check(blob, sys.stdout)

    roots: dict[str, str] = {}
    for one in args.root:
        if "=" not in one:
            print(f"--root wants NAME=PATH, got {one!r}", file=sys.stderr)
            return 2
        name, path = one.split("=", 1)
        if name not in CC.ROOT_VARS:
            print(f"--root {name} is not a known root; known roots are "
                  + ", ".join(sorted(CC.ROOT_VARS)), file=sys.stderr)
            return 2
        roots[name] = str(pathlib.Path(path).resolve())

    slug = args.render or args.replay
    if not slug:
        parser.print_help()
        return 2
    row = find(blob, args.side, slug)
    if row is None:
        print(f"no row named {slug!r}"
              + (f" on side {args.side}" if args.side else ""),
              file=sys.stderr)
        return 2
    if args.render:
        record = row.get("exec")
        if record is None:
            print(f"{slug}: no exec record", file=sys.stderr)
            return 2
        print(CC.render_shell(record))
        return 0
    return replay(row, roots, sys.stdout, dry=args.dry_run,
                  witness=args.witness)


if __name__ == "__main__":
    raise SystemExit(main())
