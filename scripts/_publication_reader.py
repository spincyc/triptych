"""Progressive publication navigation around immutable, source-owned bodies.

The caller supplies admitted outputs and their declared source owners. This
module never discovers publications, grants admission, or rewrites body HTML.
"""
from __future__ import annotations

from html import escape
from html.parser import HTMLParser
import posixpath
import re
from urllib.parse import quote


def treatment_label(role: str, kind: str) -> str:
    if role == "synthesis":
        return "Synthesis"
    if role == "homily":
        return "Homily"
    if role == "canonical":
        return "Full Study Guide" if kind.startswith("proper-") else "Full Text"
    return role.replace("-", " ").replace("_", " ").title()


def contexts(records: dict, admitted: set, products: dict, routes: set) -> dict:
    """Derive browse groups from provider, source parent and declared kind.

    Treatment identity comes from the output role within its source owner;
    filenames and similar titles never establish a companion relationship.
    """
    groups = {}
    for key, (record, output) in sorted(records.items()):
        if key not in admitted:
            continue
        provider, leaf = key
        reader = f"web/{provider}/{leaf}.html"
        printer = f"print/{provider}/{leaf}.html"
        target = reader if reader in routes else printer if printer in routes else None
        if target is None:
            continue
        owner = record["id"]
        group = groups.setdefault(owner, {
            "owner": owner, "provider": provider, "kind": record["kind"],
            "collection": (provider, posixpath.dirname(owner), record["kind"]),
            "outputs": [],
        })
        product = products.get(f"publication:{provider}/{leaf}", {})
        group["outputs"].append({
            "key": key, "role": output["role"], "href": target,
            "label": treatment_label(output["role"], record["kind"]),
            "title": product.get("title") or leaf.rsplit("/", 1)[-1].replace("-", " ").title(),
        })
    priority = {"canonical": 0, "synthesis": 1, "homily": 2}
    for group in groups.values():
        group["outputs"].sort(key=lambda row: (priority.get(row["role"], 3), row["role"], row["key"]))
        group["title"] = group["outputs"][0]["title"]
    result = {}
    for group in groups.values():
        siblings = sorted((candidate for candidate in groups.values()
                           if candidate["collection"] == group["collection"]), key=lambda row: row["owner"])
        for output in group["outputs"]:
            choices = []
            for sibling in siblings:
                selected = next((row for row in sibling["outputs"] if row["role"] == output["role"]), None)
                fallback = selected is None
                selected = selected or sibling["outputs"][0]
                choices.append({"owner": sibling["owner"], "href": selected["href"],
                                "title": sibling["title"], "fallback": fallback,
                                "label": selected["label"]})
            result[output["key"]] = {**group, "current": output, "choices": choices}
    return result


class _Sections(HTMLParser):
    """Read real section anchors without mutating sealed print-part DOM."""
    VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}

    def __init__(self, content):
        super().__init__(convert_charrefs=True)
        self.stack, self.sections, self.active, self.seen, self.ids = [], [], None, set(), set()
        self.feed(content)
        self.close()

    def handle_starttag(self, tag, pairs):
        attrs = dict(pairs)
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        if tag in {"h2", "h3", "h4"}:
            target = attrs.get("id") or next((row[1] for row in reversed(self.stack) if row[1]), None)
            self.active = {"tag": tag, "id": target, "text": []}
        if tag not in self.VOID:
            self.stack.append((tag, attrs.get("id")))

    def handle_data(self, data):
        if self.active is not None:
            self.active["text"].append(data)

    def handle_endtag(self, tag):
        if self.active and tag == self.active["tag"]:
            item = self.active
            label = re.sub(r"\s+", " ", "".join(item["text"])).strip()
            if item["id"] and label and item["id"] not in self.seen:
                self.sections.append((int(tag[1]), item["id"], label))
                self.seen.add(item["id"])
            self.active = None
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index][0] == tag:
                del self.stack[index:]
                break


def wrap(content: str, context: dict, route: str) -> str:
    """Surround the exact source rendering with static, accessible navigation."""
    def link(target):
        return escape(posixpath.relpath(target, posixpath.dirname(route) or "."), quote=True)

    current = context["current"]
    provider = {"gpt": "ChatGPT", "claude": "Claude"}.get(context["provider"], context["provider"])
    proper = context["kind"].startswith("proper-")
    choices = context["choices"]
    position = next(index for index, row in enumerate(choices) if row["owner"] == context["owner"])
    browse = []
    for index, direction in ((position - 1, "Previous"), (position + 1, "Next")):
        if 0 <= index < len(choices):
            choice = choices[index]
            suffix = f" — {choice['label']}" if choice["fallback"] else ""
            text = direction + (" celebration" if proper else " document")
            browse.append((direction, '<a class="publication-reader__adjacent" rel="' +
                           ("prev" if direction == "Previous" else "next") + '" href="' + link(choice["href"]) +
                           '" title="' + escape(choice["title"] + suffix, quote=True) + '">' +
                           escape(text + suffix) + '</a>'))
    options = []
    for choice in choices:
        selected = ' selected' if choice["owner"] == context["owner"] else ''
        label = choice["title"] + (" — " + choice["label"] if choice["fallback"] else '')
        options.append('<option value="' + link(choice["href"]) + '"' + selected + '>' + escape(label) + '</option>')
    before = next((markup for direction, markup in browse if direction == "Previous"), '')
    after = next((markup for direction, markup in browse if direction == "Next"), '')
    selector_label = "Sunday / celebration" if proper else "Document"
    selector = ('<label class="publication-reader__document publication-reader__select-label" hidden>' + selector_label +
                '<select data-reader-document-select aria-label="' + selector_label + '">' + ''.join(options) + '</select></label>')
    treatments = ''.join('<a href="' + link(output["href"]) + '"' +
                         (' aria-current="page"' if output["key"] == current["key"] else '') + '>' +
                         escape(output["label"]) + '</a>' for output in context["outputs"])
    parsed = _Sections(content)
    sections = parsed.sections
    content_id = "reader-content"
    suffix = 2
    while content_id in parsed.ids:
        content_id = "reader-content-" + str(suffix)
        suffix += 1
    contents = ''.join('<li class="publication-reader__section-level-' + str(level) + '"><a data-reader-section href="#' +
                       escape(quote(identifier, safe=''), quote=True) + '">' + escape(label) + '</a></li>'
                       for level, identifier, label in sections)
    if not contents:
        contents = '<li><a data-reader-section href="#' + content_id + '">Document</a></li>'
    return (
        '<div class="publication-reader">'
        '<div class="publication-reader__toolbar">'
        '<div class="publication-reader__browse">' + before + selector + after + '</div>'
        '<div class="publication-reader__actions"><button type="button" data-reader-copy-link hidden>Copy section link</button>'
        '<span data-reader-status role="status" aria-live="polite"></span></div>'
        '<progress data-reader-progress max="100" value="0" aria-label="Reading progress"></progress></div>'
        '<p class="publication-reader__identity">' + escape(provider) + ' · ' + escape(current["label"]) + '</p>'
        '<nav class="publication-reader__treatments" aria-label="Treatments">' + treatments + '</nav>'
        '<div class="publication-reader__layout">'
        '<details class="publication-reader__toc" data-reader-toc data-reader-contents open><summary>Contents</summary>'
        '<nav aria-label="Document sections"><ol>' + contents + '</ol></nav></details>'
        '<div class="publication-reader__content" data-reader-content id="' + content_id + '">' + content + '</div>'
        '</div></div>'
    )
