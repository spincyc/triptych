#!/usr/bin/env python3
"""The portable executable command representation, and the classifier that
proves a recorded command is one.

WHY THIS FILE EXISTS. The V15 independent review found that `checks.txt`
called all twenty-four command rows `LITERAL` -- "the exact string handed to
the shell; re-runnable" -- while seven load-bearing rows carried single-quoted
`'$WORKSPACE/...'` or `'$REPO/...'` anchors that a shell cannot expand, with
no assignments supplied anywhere. Sixteen of twenty-four rows were replayable
with their recorded context. The label was computed by a classifier that
answered a different question from the one the label claimed to answer.

THE REAL CAUSE, NAMED. `battery.sh` composed its command strings by
interpolating REAL ABSOLUTE PATHS inside SINGLE QUOTES -- correct at the
instant of execution, because a single-quoted absolute path is exactly right
-- and the sanitizer then rewrote those absolute paths into `$WORKSPACE/...`
tokens IN PLACE, inside the quotes that were put there to stop expansion.
Neither half was wrong on its own. The composition of the two produced a
string that is not the string the shell was handed and cannot be made into
one by any local edit: the quoting says "do not expand" about a token whose
only meaning is its expansion.

Two consequences follow, and this module answers both.

  ONE. A RECORDED COMMAND IS A STRUCTURE, NOT A STRING. The record carries
  `cwd`, `argv` (or `shell`), and `env`, with filesystem roots named by
  variable and never by absolute path. Nothing has to guess where a quote
  belongs, because the structure has no quoting: `argv` is a list. The shell
  rendering is DERIVED from the structure for a reader, and the structure is
  what a replay executes.

  TWO. A LABEL IS EARNED BY A STRUCTURE, NOT BY A PREFIX MATCH. V15's
  classifier asked "does the first token start with one of these strings"
  -- which accepts `format` (`for`), `installing` (`install`) and `zipcode`
  (`zip`) as commands, and accepts `python3 would be run here to check the
  tree` as LITERAL. `EXECUTABLE` is now said only about a validated exec
  record. A bare string can never earn it.

THE ROOT VARIABLES ARE DISTINCT AND DEFINED ONCE. V15's parent-replay row read

    cp '$REPO/tools/tests/test_catena_wave_1.py' tools/tests/... && python3 ...

with `cwd : $REPO`. `$REPO` there is the PARENT checkout; `$REPO` inside the
quotes is the CANDIDATE checkout, because the sanitizer's `--repo` root was
the candidate. One name, two filesystem locations, in one row -- so even
removing the quotes could not recover the execution. The names below are
disjoint by construction and every one of them is defined exactly once in the
record's `variables` block. A row that uses an undefined name, or a record
that binds one name to two values, is refused here.

DETERMINISM IS PRESERVED. `checks.txt` is a shipped, byte-stable member: a
reviewer re-composing it off-host must get the same bytes. Every table in this
module is a literal; nothing probes `PATH`, the filesystem, the clock or the
environment. `COMMAND_HEADS` remains a fixed tuple for exactly the reason V15
gave, and the membership test that reads it is now exact rather than prefix.
"""

from __future__ import annotations

import json
import re
import shlex

SCHEMA = "catena-exec-command/1"
VARIABLES_SCHEMA = "catena-exec-roots/1"

# ---- the root variables ----------------------------------------------------
#
# ONE NAME, ONE FILESYSTEM ROOT, FOREVER. `$REPO` is deliberately NOT among
# them: it is the name V15 overloaded, and reusing it would make a V15 record
# and a V16 record look alike while meaning different things. `$WORKSPACE` is
# gone for the same reason -- it named the workspace root, which is one level
# above three of the roots below and therefore invites exactly the ambiguity
# this table exists to remove.
#
# The values are DESCRIPTIONS, not paths. A record carries the description;
# the operator supplies the path at replay time, and `resolve()` refuses a
# replay that leaves one unbound.
ROOT_VARS: dict[str, str] = {
    "CANDIDATE_REPO":
        "the implementation checkout under review -- the head side",
    "PARENT_REPO":
        "the comparison checkout -- the parent side",
    "PACKAGE_ROOT":
        "the extracted handoff package directory",
    "TOOLS_ANCHOR":
        "the out-of-package handoff-tools checkout this lane ran from",
    "EVIDENCE_ROOT":
        "the staged package source directory the batteries wrote into",
}

# The names a `cwd` may take. A row's cwd is a ROOT, never a path below one:
# every command below runs from the top of a checkout or of the package, and
# admitting `$CANDIDATE_REPO/tools` would reintroduce the question of which
# root a relative path is relative to.
CWD_NAMES = tuple(sorted(ROOT_VARS))

# ---- the command heads -----------------------------------------------------
#
# EXACT MEMBERSHIP, NOT A PREFIX MATCH. V15 tested `first.startswith(HEADS)`,
# which is true of `format`, `installing`, `zipcode`, `testify`, `iffy`,
# `forward`, `envelope`, `settle`, `nodejs-is-not-here` and every other word
# that happens to begin with a short head. The review found three of those by
# hand. The test below is `in`, and the path-shaped heads -- which really are
# prefixes, because `tools/tpt` is a path -- are a separate, explicit tuple.
COMMAND_HEADS = (
    "python3", "python", "bash", "sh", "make", "git", "node", "npm",
    "cd", "env", "printf", "echo", "set", "true", "false", "test",
    "cp", "mv", "rm", "mkdir", "install", "ln", "cat", "sed", "awk",
    "grep", "find", "sort", "tee", "chmod", "sha256sum", "wc", "date",
    "zip", "unzip", "tar", "gzip", "for", "if", "while", "exec", "exit",
)
# A head that is a PATH is matched by prefix, because the rest of it is the
# rest of the path. These are the only prefixes in the whole test.
PATH_HEAD_PREFIXES = ("./", "../", "/", "tools/", "logs/", "scripts/",
                      "build/", "bin/")
# A leading shell grouping or an assignment prefix. `TRIPTYCH_CHROME=... node`
# is a command whose head is the assignment; the head test looks past it.
ASSIGNMENT = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*=")

# ---- prose detection -------------------------------------------------------
#
# A STRING THAT BEGINS WITH A COMMAND AND CONTINUES IN ENGLISH IS ENGLISH.
# The review's two examples are `python3 would be run here to ...` and `cp is
# used to ...`: both prefix-match a real head, and V15 labelled both
# re-runnable. The second token settles it. No invocation of `cp` has `is` as
# its first argument; no invocation of anything has `would`.
PROSE_CONNECTORS = frozenset("""
    a an the is are was were be been being am
    would will shall should could can may might must
    does did do done has have had
    here there then thus therefore however because since while
    and or but nor so yet
    this that these those it its
    used uses using run runs ran runnable
    described describes describing means meaning
    of for to from with without into onto about above below
    not no none nothing every each all any some
""".split())

# A trailing full stop after a real word, with no shell metacharacter anywhere
# in the string, is prose punctuation. A command may end in `.` only as part
# of a path (`cp x .`), which the metacharacter and single-token tests below
# already separate out.
SHELL_METACHARACTERS = frozenset("|&;<>()$`\\\"'*?[]{}")

# `$NAME` or `${NAME}`. Deliberately does not accept `$1`, `$?`, `$@`, `$$`:
# those are positional and status expansions, they are not roots, and a
# recorded shell fragment is allowed to contain them.
VARIABLE = re.compile(r"\$(?:\{([A-Za-z_][A-Za-z0-9_]*)\}|([A-Za-z_][A-Za-z0-9_]*))")

# A NAME THE COMMAND ITSELF SETS IS NOT A REFERENCE TO ANYTHING OUTSIDE IT.
# The browser-gate row saves the gate's exit with `gate=$?` and reads it back
# as `$gate` two commands later. That is a shell local, it is bound inside the
# recorded string, and demanding that the record define it as a filesystem
# root would be demanding nonsense. Assignments are recognised at a command
# boundary -- start of string, after `;`, `&`, `|`, `(` or `&&`/`||`, or after
# whitespace -- which is where a shell recognises them too.
LOCAL_ASSIGNMENT = re.compile(
    r"(?:^|[;&|(\n]|\s)\s*([A-Za-z_][A-Za-z0-9_]*)=")


def locally_assigned(text: str) -> set[str]:
    """Every name the recorded shell text binds for itself."""
    return set(LOCAL_ASSIGNMENT.findall(text or ""))


class ExecProblem(Exception):
    """A recorded command that cannot be replayed as recorded.

    Carries the machine-readable `code` as well as the sentence, so a caller
    can refuse on a class of fault rather than on a substring of English.
    """

    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code
        self.message = message


# The complete refusal vocabulary. Every code a validation can raise appears
# here, and every one has a test. A caller that wants to enumerate what can go
# wrong reads this and not the code below it.
PROBLEM_CODES: dict[str, str] = {
    "missing-schema":
        "the exec record does not declare the schema this validator owns",
    "malformed-record":
        "the exec record is not an object with the required shape",
    "missing-cwd":
        "the exec record names no working directory",
    "undefined-cwd":
        "the exec record's cwd is not one of the defined root variables",
    "malformed-argv":
        "argv is not a non-empty list of non-empty strings",
    "argv-and-shell":
        "the record carries both an argv and a shell form; it must carry one",
    "neither-argv-nor-shell":
        "the record carries neither an argv nor a shell form",
    "no-command-head":
        "the first token is not a command this record set recognises",
    "prose-prefix":
        "the string begins with a command word and continues in English",
    "quoted-variable":
        "a variable reference sits inside single quotes and cannot expand",
    "undefined-variable":
        "the command uses a root variable the record does not define",
    "overloaded-variable":
        "one variable name is bound to two different roots",
    "malformed-env":
        "env is not a mapping of variable names to string values",
    "unbound-root":
        "a replay was asked for with a root variable left unbound",
    "reserved-variable":
        "the record defines a variable name reserved by an earlier schema",
    "misdeclared-uses":
        "the record's `uses` names a different set of roots from the ones "
        "its own command references",
}

# The names V15 overloaded. Defining either of them again would let a V16
# record repeat the exact defect under the exact old spelling.
RESERVED_VARIABLES = frozenset({"REPO", "WORKSPACE", "EVIDENCE", "SCRATCH"})


# ---- quoting ---------------------------------------------------------------

def quote_state_scan(text: str) -> list[tuple[int, str, str]]:
    """Walk `text` as `sh` would, reporting every variable reference and the
    quoting it sits inside.

    Returns `(offset, name, state)` where state is `"bare"`, `"double"` or
    `"single"`. A `"single"` state is the V15 defect: the shell will pass the
    dollar sign through literally, so the recorded string names a path that
    does not exist.

    This is a lexer for exactly one question and deliberately not a shell
    parser. It tracks the three quoting states and backslash escaping, which
    is the whole of what decides whether a `$` expands.
    """
    found: list[tuple[int, str, str]] = []
    state = "bare"
    i = 0
    n = len(text)
    while i < n:
        ch = text[i]
        if state == "bare" and ch == "\\":
            i += 2
            continue
        if state == "double" and ch == "\\":
            i += 2
            continue
        if state == "bare" and ch == "'":
            state = "single"
            i += 1
            continue
        if state == "single" and ch == "'":
            state = "bare"
            i += 1
            continue
        if state == "bare" and ch == '"':
            state = "double"
            i += 1
            continue
        if state == "double" and ch == '"':
            state = "bare"
            i += 1
            continue
        if ch == "$":
            match = VARIABLE.match(text, i)
            if match:
                found.append((i, match.group(1) or match.group(2), state))
                i = match.end()
                continue
        i += 1
    return found


def unexpandable_variables(text: str) -> list[tuple[int, str]]:
    """Every variable reference in `text` that a shell cannot expand.

    This is the check V15's classifier did not have and the reason seven rows
    shipped labelled re-runnable. It is `checks.py`'s refusal and it is also
    the replay tool's, so a row cannot pass one and fail the other.
    """
    return [(at, name) for at, name, state in quote_state_scan(text)
            if state == "single"]


def referenced_variables(text: str) -> set[str]:
    """Every root-shaped variable a string names, whatever its quoting.

    Quoting is a separate fault with a separate code; a name inside single
    quotes is still a name the record has to define, or the row is wrong twice
    rather than once and the reader is told both.
    """
    return {name for _at, name, _state in quote_state_scan(text)}


# ---- the head test ---------------------------------------------------------

def head_of(text: str) -> str:
    """The first token that is not an environment assignment.

    `TRIPTYCH_CHROME='/usr/bin/chromium' node tools/...` has head `node`. V15
    treated the assignment itself as the head via the `"=" in first` escape,
    which meant `NOTES=this is a note about what ran` classified as a command.
    """
    for token in text.strip().split():
        if ASSIGNMENT.match(token):
            continue
        return token
    return ""


def is_command_head(token: str) -> bool:
    """Exact membership, plus the explicitly path-shaped prefixes.

    THE PREFIX OVERMATCH, CLOSED. `format`, `installing` and `zipcode` are not
    commands and no longer test as commands. `tools/tpt` still is, because a
    path head really is a prefix and `PATH_HEAD_PREFIXES` says which prefixes
    are paths rather than leaving every short word to act as one.
    """
    if not token:
        return False
    if token in COMMAND_HEADS:
        return True
    return token.startswith(PATH_HEAD_PREFIXES)


def looks_like_prose(text: str) -> tuple[bool, str]:
    """Is this English about a command rather than a command?

    Returns `(verdict, why)`. Three independent tests, any of which is enough:

      * the token after the head is an English connector -- `python3 would`,
        `cp is`, `make will`. This is the review's own pair of examples;
      * the head is not a command at all;
      * the string carries no shell metacharacter, no flag, no path and no
        assignment, ends in a full stop, and runs to five words or more. That
        is a sentence, and a command that looked like one would have to be
        five bare words with a period glued to the last.
    """
    stripped = text.strip()
    if not stripped:
        return True, "the string is empty"
    tokens = stripped.split()
    head = head_of(stripped)
    if not is_command_head(head):
        return True, (f"the first token {head!r} is not a command head this "
                      f"record set recognises")
    try:
        after = tokens[tokens.index(head) + 1]
    except (ValueError, IndexError):
        after = ""
    bare = after.strip(",.;:").lower()
    if bare and bare in PROSE_CONNECTORS:
        return True, (f"the token after {head!r} is {after!r}, an English "
                      f"connector rather than an argument")
    if (len(tokens) >= 5
            and stripped.endswith(".")
            and not any(ch in SHELL_METACHARACTERS for ch in stripped)
            and not any(one.startswith("-") for one in tokens)
            and not any("/" in one for one in tokens[1:])
            and not any(ASSIGNMENT.match(one) for one in tokens)):
        return True, ("the string is a full sentence: five or more words, a "
                      "closing full stop, and no flag, path, assignment or "
                      "shell metacharacter anywhere in it")
    return False, ""


# ---- the record ------------------------------------------------------------

def make_variables(**bindings: str) -> dict:
    """The `variables` block: each root name defined EXACTLY ONCE.

    `bindings` maps a root name to the SYMBOLIC description of what it is, not
    to a path. Refuses a name outside `ROOT_VARS` and refuses any of the names
    V15 overloaded.
    """
    out: dict[str, str] = {}
    for name, meaning in bindings.items():
        if name in RESERVED_VARIABLES:
            raise ExecProblem(
                "reserved-variable",
                f"{name} is reserved: V15 bound it to two different roots in "
                f"one record, and a V16 record that defines it again would "
                f"repeat that defect under the same spelling")
        if name not in ROOT_VARS:
            raise ExecProblem(
                "undefined-variable",
                f"{name} is not one of the defined root variables "
                f"({', '.join(CWD_NAMES)})")
        if name in out:
            raise ExecProblem(
                "overloaded-variable",
                f"{name} is defined twice; a root variable is defined once")
        out[name] = str(meaning or ROOT_VARS[name])
    return {"schema": VARIABLES_SCHEMA, "roots": out}


def make_record(cwd: str, argv: list[str] | None = None,
                shell: str | None = None,
                env: dict[str, str] | None = None,
                uses: list[str] | None = None) -> dict:
    """Build an exec record and validate it in the same breath.

    Nothing in this toolchain constructs one of these by hand in a string.
    `battery.sh` and `assemble.sh` emit the fields they already hold at the
    instant of execution and this assembles them, so the record is derived
    from what ran rather than typed beside it.

    `uses` IS DERIVED HERE AND NOT TAKEN FROM THE CALLER. It was a parameter
    no caller passed, and this function threw away `validate()`'s return value
    -- which is exactly the sorted list of roots the command references -- so
    every record this toolchain has ever written carries `uses: []`, including
    rows that provably use three roots. A field in the shipped schema that is
    empty on every row is a lie of omission, and the cure is to derive it from
    the same walk that validates the record rather than to ask a caller to
    restate what the record already says. A caller that passes `uses` is
    making a CLAIM, and `validate()` refuses one that disagrees.
    """
    record = {
        "schema": SCHEMA,
        "cwd": cwd,
        "env": dict(env or {}),
        "argv": list(argv) if argv is not None else None,
        "shell": shell,
        "uses": sorted(set(uses or [])),
    }
    record["uses"] = validate(record, defined=set(ROOT_VARS))
    return record


def validate(record, defined: set[str] | None = None) -> list[str]:
    """Refuse a record that cannot be replayed as recorded.

    Returns the set of root variables the record USES, so a caller can prove
    the record's variables block covers them. Raises `ExecProblem` on the
    first fault, with a code from `PROBLEM_CODES`.

    `defined` is the set of names the surrounding record defines. Passing
    `None` skips the undefined-variable test -- which is only ever right for a
    caller that is about to run that test itself against a larger scope.
    """
    if not isinstance(record, dict):
        raise ExecProblem("malformed-record",
                          "the exec record is not a JSON object")
    if record.get("schema") != SCHEMA:
        raise ExecProblem(
            "missing-schema",
            f"the exec record declares schema {record.get('schema')!r}; this "
            f"validator owns {SCHEMA!r} and refuses to guess at another")

    cwd = record.get("cwd")
    if not cwd or not isinstance(cwd, str):
        raise ExecProblem("missing-cwd",
                          "the exec record names no working directory; a "
                          "relative path in it is relative to nothing")
    if not cwd.startswith("$") or cwd[1:] not in ROOT_VARS:
        raise ExecProblem(
            "undefined-cwd",
            f"the exec record's cwd is {cwd!r}; it must be one of "
            + ", ".join("$" + one for one in CWD_NAMES))

    env = record.get("env")
    if env is None:
        env = {}
    if not isinstance(env, dict) or any(
            not isinstance(k, str) or not isinstance(v, str)
            or not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", k)
            for k, v in env.items()):
        raise ExecProblem("malformed-env",
                          "env must map variable NAMES to string values")

    argv, shell = record.get("argv"), record.get("shell")
    if argv is not None and shell is not None:
        raise ExecProblem(
            "argv-and-shell",
            "the record carries both argv and shell; two renderings of one "
            "execution cannot both be the one that ran, and nothing here can "
            "tell which")
    if argv is None and shell is None:
        raise ExecProblem("neither-argv-nor-shell",
                          "the record carries no executable form at all")

    used: set[str] = set()
    for value in env.values():
        used |= referenced_variables(value)

    if argv is not None:
        if (not isinstance(argv, list) or not argv
                or any(not isinstance(one, str) or not one for one in argv)):
            raise ExecProblem(
                "malformed-argv",
                "argv must be a non-empty list of non-empty strings; an "
                "empty element is an argument the shell never received and a "
                "non-string is not an argument at all")
        head = argv[0]
        if not is_command_head(head):
            raise ExecProblem(
                "no-command-head",
                f"argv[0] is {head!r}, which is not a command head this "
                f"record set recognises")
        prose, why = looks_like_prose(" ".join(argv))
        if prose:
            raise ExecProblem("prose-prefix",
                              f"argv reads as a description, not an "
                              f"invocation: {why}")
        # AN ARGV ELEMENT IS NEVER QUOTED, so a variable in one always
        # expands and there is no quoting fault to find. The check that
        # matters here is that the name is defined.
        for one in argv:
            used |= referenced_variables(one)
    else:
        if not isinstance(shell, str) or not shell.strip():
            raise ExecProblem("malformed-argv",
                              "the shell form is empty; there is nothing to "
                              "hand to a shell")
        prose, why = looks_like_prose(shell)
        if prose:
            raise ExecProblem("prose-prefix",
                              f"the shell form reads as a description, not an "
                              f"invocation: {why}")
        trapped = unexpandable_variables(shell)
        if trapped:
            names = ", ".join(sorted({name for _at, name in trapped}))
            raise ExecProblem(
                "quoted-variable",
                f"the shell form quotes {names} inside SINGLE quotes, where a "
                f"shell passes the dollar sign through literally: the "
                f"recorded string names a path that does not exist and the "
                f"row is not re-runnable as written")
        used |= referenced_variables(shell)
        # The row's own locals are bound by the row; they are not roots and
        # they are not undefined.
        used -= locally_assigned(shell)

    used |= {cwd[1:]}
    # A name that is not a root and is not something the record's own env
    # sets is a reference to nothing. `$?`, `$1` and friends never reach here:
    # `VARIABLE` does not match them.
    unknown = {one for one in used
               if one not in ROOT_VARS and one not in env}
    if unknown:
        raise ExecProblem(
            "undefined-variable",
            "the command references " + ", ".join(sorted(unknown))
            + ", which is neither a defined root nor set by this row's env")
    if defined is not None:
        missing = {one for one in used
                   if one in ROOT_VARS and one not in defined}
        if missing:
            raise ExecProblem(
                "undefined-variable",
                "the command uses the root(s) " + ", ".join(sorted(missing))
                + " which the record's variables block does not define")
    roots_used = sorted(used & set(ROOT_VARS))
    # `uses` IS A CLAIM, AND A CLAIM IS CHECKED AGAINST THE DERIVATION.
    #
    # The walk above has just computed the roots this record references. A
    # record that ALSO states them is stating something a tool can derive, and
    # the whole of the V15 defect is a label nothing compared to what it
    # described -- so it is compared here. An ABSENT or EMPTY `uses` is not a
    # false claim and is not refused: every record written before this field
    # was derived carries `[]`, and those records are correct about everything
    # they do say. `make_record` fills it in from this same return value, so a
    # record composed by this module never has to make the claim by hand.
    declared = record.get("uses")
    if declared:
        if (not isinstance(declared, list)
                or any(not isinstance(one, str) for one in declared)):
            raise ExecProblem(
                "malformed-record",
                "`uses` must be a list of root variable names")
        if sorted(set(declared)) != roots_used:
            raise ExecProblem(
                "misdeclared-uses",
                "the record says it uses " + ", ".join(sorted(set(declared)))
                + " and its own cwd, argv or shell and env reference "
                + (", ".join(roots_used) or "no root at all")
                + "; the field is derivable from the record and a record that "
                  "disagrees with itself cannot be replayed on the strength "
                  "of either half")
    return roots_used


def render_shell(record: dict, env: bool = True) -> str:
    """The reader's rendering: one line a person can look at.

    DERIVED, NEVER STORED AS THE TRUTH. `argv` is the truth for an argv row;
    this is what it looks like. The quoting here is `shlex.quote`'s, with one
    deliberate exception: a token whose whole content is a root reference, or
    a root reference followed by a path, is rendered in DOUBLE quotes so the
    rendering a reader copies expands exactly as the replay does. That single
    rule is the whole of the V15 defect, stated as code.

    `env=False` renders the same line WITHOUT the environment prefix. It is
    not an option a reader should want -- a line missing an assignment the
    command needed is a line that may not reproduce the run -- and it exists
    for exactly one reason: `battery.sh`'s `run()` writes its `CMD:` line
    from the shell text it is handed, which carries no prefix, so this is the
    second of the two strings a battery can legitimately have logged for one
    record. `checks.py` compares a ledger's string against both and refuses
    anything else.
    """
    argv, shell = record.get("argv"), record.get("shell")
    prefix = "".join(f"{k}={quote_token(v)} "
                     for k, v in sorted((record.get("env") or {}).items())
                     ) if env else ""
    if shell is not None:
        return prefix + shell
    return prefix + " ".join(quote_token(one) for one in argv or [])


def quote_token(token: str) -> str:
    """Quote one token so a shell receives it, expansions intact.

    A token naming a root gets DOUBLE quotes -- it must expand, and it must
    survive a space in the expansion. Everything else gets `shlex.quote`,
    which is single quotes and is right for everything that must NOT expand.
    """
    if referenced_variables(token):
        return '"' + token.replace("\\", "\\\\").replace('"', '\\"') + '"'
    return shlex.quote(token)


def resolve(record: dict, roots: dict[str, str]) -> tuple[str, dict, list[str] | str]:
    """Turn a record into something that can be handed to a process.

    Returns `(cwd, env_overlay, argv_or_shell)` with every root substituted.
    Refuses -- rather than substituting an empty string, which is how a replay
    silently runs in the wrong directory -- when a root the record uses is not
    bound.
    """
    used = validate(record, defined=set(roots) | set(ROOT_VARS))
    missing = [one for one in used if not roots.get(one)]
    if missing:
        raise ExecProblem(
            "unbound-root",
            "cannot replay: " + ", ".join(sorted(missing))
            + " is used by this row and was not bound. Pass --root NAME=PATH "
              "for each; an unbound root would run the command somewhere "
              "other than where it ran.")

    def swap(text: str) -> str:
        def one(match: re.Match) -> str:
            name = match.group(1) or match.group(2)
            if name in roots:
                return roots[name]
            return match.group(0)
        return VARIABLE.sub(one, text)

    cwd = roots[record["cwd"][1:]]
    env = {k: swap(v) for k, v in (record.get("env") or {}).items()}
    if record.get("argv") is not None:
        return cwd, env, [swap(one) for one in record["argv"]]
    return cwd, env, swap(record["shell"])


# ---- the verdict written into `checks.txt` ---------------------------------

VERDICT_EXECUTABLE = "EXECUTABLE"
VERDICT_ELIDED = "ELIDED"
VERDICT_PROSE = "PROSE"
VERDICT_NOT_RECORDED = "NOT RECORDED"
VERDICT_NON_EXECUTABLE = "NON-EXECUTABLE"

VERDICTS = (VERDICT_EXECUTABLE, VERDICT_ELIDED, VERDICT_PROSE,
            VERDICT_NOT_RECORDED, VERDICT_NON_EXECUTABLE)

# A standalone capitalised token is a placeholder until proved otherwise --
# `assemble.sh` writes PKG, ZIP, TOOLS and LEDGER for values it held. Carried
# over from V15 unchanged, including its lookarounds, because it was right:
# what it decides is whether a row is ELIDED, and that judgement never claimed
# executability.
PLACEHOLDER = re.compile(r"(?<![\w./$-])([A-Z][A-Z0-9_]{2,})(?![\w./=-])")


def classify(text, record=None, defined: set[str] | None = None
             ) -> tuple[str, str]:
    """The verdict, and the sentence that explains it.

    THE RULE THAT MAKES THIS DIFFERENT FROM V15. `EXECUTABLE` is said only
    about a VALIDATED EXEC RECORD. No string, however well-formed, earns it,
    because no string carries a cwd, an env or an unambiguous argument
    boundary, and those are what "re-runnable" means. A row with no record
    gets `ELIDED`, `PROSE` or `NOT RECORDED` -- all three of which are honest
    about not being re-runnable -- or `NON-EXECUTABLE`, which is what a row
    gets when it has a record that does not validate.
    """
    text = str(text or "")
    if record is not None:
        try:
            validate(record, defined=defined)
        except ExecProblem as problem:
            return VERDICT_NON_EXECUTABLE, (
                f"[{problem.code}] {problem.message}")
        return VERDICT_EXECUTABLE, (
            "a validated exec record: cwd, argv or shell, and env, with every "
            "filesystem root named by a variable this file defines. Replay it "
            "with logs/replay-command.py")
    if not text.strip():
        return VERDICT_NOT_RECORDED, (
            "no command string was recorded for this step; there is nothing "
            "to re-run and nothing to check it against")
    prose, why = looks_like_prose(text)
    if prose:
        return VERDICT_PROSE, (
            f"a description of what happened, not a string a shell was "
            f"handed: {why}")
    trapped = unexpandable_variables(text)
    if trapped:
        names = ", ".join(sorted({name for _at, name in trapped}))
        return VERDICT_NON_EXECUTABLE, (
            f"[quoted-variable] the string quotes {names} inside single "
            f"quotes, where a shell passes the dollar sign through "
            f"literally; it names a path that does not exist")
    found = sorted(set(PLACEHOLDER.findall(text)))
    if found:
        return VERDICT_ELIDED, (
            "the capitalised token(s) " + ", ".join(found)
            + " stand in for values this lane held; substitute them to re-run. "
              "Marked conservatively: a token that really was literal is "
              "marked the same way")
    return VERDICT_ELIDED, (
        "a plausible command string with no exec record beside it. Without a "
        "recorded cwd and env nothing here can say it re-runs, so it is not "
        "called executable")


def parse_record(blob):
    """Read an exec record out of a JSON string, refusing anything else."""
    if isinstance(blob, dict):
        return blob
    try:
        value = json.loads(blob)
    except (TypeError, ValueError) as problem:
        raise ExecProblem("malformed-record",
                          f"the exec record is not JSON: {problem}") from None
    if not isinstance(value, dict):
        raise ExecProblem("malformed-record",
                          "the exec record is not a JSON object")
    return value


def check_variables(block) -> dict[str, str]:
    """Validate a `variables` block and return its root table.

    A block that defines a name twice cannot exist in JSON -- the later key
    wins silently -- so the overloading test that matters is done where the
    block is BUILT (`make_variables`) and here against the reserved names and
    the known roots.
    """
    if not isinstance(block, dict) or block.get("schema") != VARIABLES_SCHEMA:
        raise ExecProblem("malformed-record",
                          f"the variables block does not declare "
                          f"{VARIABLES_SCHEMA}")
    roots = block.get("roots")
    if not isinstance(roots, dict):
        raise ExecProblem("malformed-record",
                          "the variables block carries no `roots` mapping")
    for name in roots:
        if name in RESERVED_VARIABLES:
            raise ExecProblem(
                "reserved-variable",
                f"the variables block defines {name}, which V15 bound to two "
                f"different roots in one record; it is reserved")
        if name not in ROOT_VARS:
            raise ExecProblem("undefined-variable",
                              f"the variables block defines {name}, which is "
                              f"not a known root")
    return {k: str(v) for k, v in roots.items()}
