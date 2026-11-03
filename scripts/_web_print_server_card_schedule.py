"""Pure canonical card/deck schedule, derived before rendering any fragments.

The planner owns event encoding and canonical fragment normalization. This
module walks source calls and projects their source-owned fields into that
event vocabulary; it never inspects HTML or invokes a rendering method.
"""
from __future__ import annotations

import re


def plan_cards(p) -> list[dict]:
    """Plan every selected sheet, face, field, notice and terminal apparatus."""
    # Shared source parsers are loaded lazily; no rendering API is called.
    from _web_print_server import calls, web, Refusal

    m = p.model
    low = m.form == "low"
    owner = m.owner
    definitions = m.defs if hasattr(m, "defs") else m.definitions

    def origin(path, macro, start=0):
        setter = getattr(p, "origin", None)
        if setter is not None:
            setter(path, macro, start)

    def node_body(name):
        raw = definitions[name][2]
        match = re.search(r"at\s*\([^)]*\)\s*\{", raw)
        if match is None:
            raise Refusal("card schedule source text node is missing: " + name)
        return web.brace_group(raw, match.end() - 1)[0]

    def face_events(command, args, path, start):
        origin(path, command, start)
        if command.startswith("LowMass"):
            _, _, number, stage, body = args
            identity = "LM-F" + number
            back = command == "LowMassBackCard"
            header = (p.literal(number + " · " + ("BOTH" if back else "PRIEST"))
                      + p.literal("LOW MASS") + p.literal(stage))
            events = p.wrap("face-header", header)
            answer = p.text(("℟. " if back else "℣. ") + body)
            events += p.wrap("answer", answer) if back else answer
        else:
            identity = args[0]
            back = command not in {"integratedresponsefront", "flashfront"}
            marker = "MC" if m.form == "cantata" else "SOLEMN"
            printed_id = identity if command in {"flashfront", "actionflashback"} else identity + " · " + marker
            header = p.literal(printed_id) + p.literal("Answer" if back else "Cue")
            events = p.wrap("face-header", header)
            if command == "integratedresponsefront":
                events += p.text("℣. " + args[2])
            elif command == "flashfront":
                events += p.text(args[1])
            else:
                if command == "storedresponseback":
                    response_id = args[1]
                    item = m.bank[response_id]
                    args = [identity, item["latin"], item["learner"], item["sound"], item["meaning"],
                            "Lesson " + m.lookup["lesson", response_id] + " · " + response_id + "."]
                if command == "actionflashback":
                    events += p.text(r"\textit{" + args[1] + "}")
                    events += p.wrap("action-body", p.text(args[2]))
                    events += p.wrap("face-footer", p.text(args[3]))
                else:
                    dense = command == "denseintegratedresponseback"
                    for field, label, value in zip(
                            ("response", "learner", "sound", "meaning"),
                            ("RESPONSE", "LATIN CHUNKS", "SAY IT LIKE", "MEANING"), args[1:5]):
                        field_events = [] if dense and field in {"response", "meaning"} else p.literal(label)
                        field_events += p.text(("℟. " if field == "response" else "") + value)
                        events += p.wrap("field", field_events, field)
                    events += p.wrap("face-footer", p.text(args[5]))
        side = "back" if back else "front"
        return identity, side, p.wrap("face", events, identity + ":" + side)

    main_path = m.leaf / "main.tex"
    if low:
        sources = [(main_path, p.read(main_path))]
        commands = {"LowMassFrontCard": 5, "LowMassBackCard": 5}
    else:
        response_path = owner / "shared/response-reference.tex"
        action_path = owner / "shared" / (
            "missa-cantata-action-cards.tex" if m.form == "cantata" else "solemn-action-cards.tex")
        sources = [(path, m.select(p.read(path))) for path in (response_path, action_path)]
        commands = {"integratedresponsefront": 3, "storedresponseback": 2,
                    "integratedresponseback": 6, "denseintegratedresponseback": 6,
                    "flashfront": 2, "actionflashback": 4}
    environment = "tikzpicture" if low else "flashgrid"
    sheets = []
    for path, source in sources:
        for grid in re.finditer(
                r"\\begin\{" + environment + r"\}(.*?)\\end\{" + environment + r"\}", source, re.S):
            body = grid[1]
            invocations = sorted((start, command, args)
                                 for command, count in commands.items()
                                 for args, start, _ in calls(body, command, count))
            if not invocations:
                continue
            number = len(sheets) + 1
            side = "front" if number % 2 else "back"
            identities, contents = [], []
            for start, command, args in invocations:
                identity, source_side, events = face_events(
                    command, args, path, grid.start(1) + start)
                if source_side != side:
                    raise Refusal("card schedule source does not alternate front/back sheets")
                identities.append(identity)
                contents += events
            if len(identities) > (8 if low else 6):
                raise Refusal("card schedule exceeds its canonical grid capacity")
            if side == "back":
                prior = sheets[-1]["face_ids"]
                mirrored = [item for start in range(0, len(prior), 2)
                            for item in prior[start:start + 2][::-1]]
                if identities != mirrored:
                    raise Refusal("card schedule back is not the source's row-mirrored front")
            events = p.wrap("grid", contents, "4" if low else "3")
            if low:
                footers = calls(body, "LowMassSheetFooter", 1)
                if len(footers) > 1:
                    raise Refusal("card schedule repeats a source duplex instruction")
                for args, start, _ in footers:
                    origin(path, "LowMassSheetFooter", grid.start(1) + start)
                    events += p.wrap("sheet-duplex", p.text(args[0]),
                                     f"sheet-{number:02d}-duplex-instruction")
            sheets.append(dict(id=f"sheet-{number:02d}-{side}", kind="card-sheet",
                               events=events, face_ids=identities, side=side))
    if not sheets or len(sheets) % 2:
        raise Refusal("card schedule has an incomplete duplex source selection")

    # The revision/rights notice belongs inside the final back, after its grid
    # and any source duplex instruction, before the sheet closes.
    if low:
        origin(main_path, "LowMassFinalNotice")
        notice = p.text(node_body("LowMassFinalNotice").replace(
            r"\AIDocumentRevisionTimestampValue", m.revised))
    else:
        origin(m.leaf / "generation-metadata.tex", "AIDocumentRevisionTimestamp")
        notice = p.text(r"\textbf{Last revised (UTC):} " + m.revised)
        origin(owner.parents[5] / "common/preamble.tex",
               "TriptychRightsNotice")
        notice += p.tex(m.rights)
    sheets[-1]["events"] += p.wrap("sheet-notice", notice, "card-revision-rights")
    for number, sheet in enumerate(sheets, 1):
        sheet["events"] = p.wrap("sheet", sheet["events"],
                                 ("low" if low else "sung") + "/" + sheet["side"] + "/" + str(number))
        del sheet["face_ids"]
        del sheet["side"]
    if m.form in {"low", "cantata"}:
        origin(owner / "shared/server-guide-format.tex", "CardCompanionTerminalApparatus")
        events = p.wrap("apparatus", p.text(node_body("CardCompanionTerminalApparatus")),
                        "card-terminal-apparatus")
        sheets.append(dict(id="card-terminal-apparatus", kind="apparatus", events=events))
    return sheets
