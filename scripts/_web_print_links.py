"""Href-only route projection for already rendered canonical print parts.

No converter, Pandoc, TeX, source acquisition or shared-cache write occurs.
"""
from __future__ import annotations
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
import hashlib
import html
from html.parser import HTMLParser
import posixpath
import re
from types import MappingProxyType
from urllib.parse import quote, unquote, urlsplit, urlunsplit


class LinkError(ValueError):
    pass


def need(test, message):
    if not test:
        raise LinkError(message)


def path(value):
    need(isinstance(value, str) and value and not value.startswith("/")
         and "\\" not in value and "\0" not in value, "unsafe repository/site path")
    normalized = posixpath.normpath(value)
    need(normalized != ".." and not normalized.startswith("../"), "path escapes repository")
    return normalized


@dataclass(frozen=True, slots=True, init=False, eq=False)
class RoutingContext:
    """A private, immutable copy of one held catalog's validated route policy."""
    _publication_routes: Mapping[str, str]
    _site_routes: Mapping[str, str]
    _repository_paths: frozenset[str]
    _repository_ref: str
    _site_ids: Mapping[str, frozenset[str]]
    _repository_ids: Mapping[str, frozenset[str]]
    _repository_origin: str
    _live_repository_navigation: bool
    _inert_source_urls: Mapping[str, frozenset[str]]

    def __init__(self, *, publication_routes, site_routes, repository_paths,
                 repository_ref, site_ids=None, repository_ids=None,
                 repository_origin="https://github.com/spincyc/triptych",
                 live_repository_navigation=False, inert_source_urls=None):
        need(type(live_repository_navigation) is bool,
             "live source navigation requires an explicit boolean opt-in")
        need(isinstance(repository_ref, str) and (
            re.fullmatch(r"[0-9a-f]{40}", repository_ref)
            or live_repository_navigation and repository_ref == "main"),
            "source-repository links require an exact published commit or explicitly enabled main navigation")
        need(isinstance(repository_origin, str), "source-repository origin must be a string")
        need(isinstance(repository_paths, Iterable) and not isinstance(repository_paths, (str, bytes)),
             "public repository paths must be a collection of paths")

        def routes(values):
            need(isinstance(values, Mapping), "route policy must be a mapping")
            return MappingProxyType({path(key): path(value) for key, value in values.items()})

        def identifiers(values):
            values = {} if values is None else values
            need(isinstance(values, Mapping), "anchor policy must be a mapping")
            copied = {}
            for route, ids in values.items():
                need(path(route) == route and isinstance(ids, (list, tuple, set, frozenset))
                     and all(isinstance(identifier, str) for identifier in ids),
                     "invalid route-qualified anchor policy")
                copied[route] = frozenset(ids)
            return MappingProxyType(copied)

        inert_source_urls = {} if inert_source_urls is None else inert_source_urls
        need(isinstance(inert_source_urls, dict), "inert source URLs require an explicit source-qualified map")
        inert = {}
        for source, targets in inert_source_urls.items():
            need(path(source) == source and isinstance(targets, (list, tuple, set, frozenset))
                 and all(isinstance(target, str) and re.fullmatch(
                     r"[a-z0-9][a-z0-9.-]*\.[a-z]{2,}(?:/[A-Za-z0-9][A-Za-z0-9._~-]*)*", target)
                         for target in targets), "invalid source-qualified inert URL policy")
            inert[source] = frozenset(targets)
        object.__setattr__(self, "_publication_routes", routes(publication_routes))
        object.__setattr__(self, "_site_routes", routes(site_routes))
        object.__setattr__(self, "_repository_paths", frozenset(path(value) for value in repository_paths))
        object.__setattr__(self, "_repository_ref", repository_ref)
        object.__setattr__(self, "_site_ids", identifiers(site_ids))
        object.__setattr__(self, "_repository_ids", identifiers(repository_ids))
        object.__setattr__(self, "_repository_origin", repository_origin)
        object.__setattr__(self, "_live_repository_navigation", live_repository_navigation)
        object.__setattr__(self, "_inert_source_urls", MappingProxyType(inert))


_UNSET = object()


class Identity(HTMLParser):
    def __init__(self, fragment):
        super().__init__(convert_charrefs=True)
        self.ids, self.units, self.tags, self.words = [], [], [], []
        self.feed(fragment)
    def handle_starttag(self, tag, attrs):
        self.tags.append(tag)
        values = dict(attrs)
        if "id" in values:
            self.ids.append(values["id"])
        if "data-print-unit" in values:
            self.units.append(values["data-print-unit"])
    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
    def handle_data(self, value):
        self.words.append(value)
    @property
    def text_sha256(self):
        # Match the controller's ECMAScript /\s+/gu exactly, without changing
        # any source text. Python str.split has additional control characters.
        text = re.sub("[\u0009-\u000d\u0020\u00a0\u1680\u2000-\u200a\u2028\u2029\u202f\u205f\u3000\ufeff]+",
                      " ", "".join(self.words)).strip(" ")
        return hashlib.sha256(text.encode()).hexdigest()


def anchor_index(parts):
    result = {}
    part_ids = set()
    for part in parts:
        need(part["id"] not in part_ids, "duplicate print part identity")
        part_ids.add(part["id"])
        path(part["route"])
        for identifier in Identity(part["html"]).ids:
            need(identifier and identifier not in result, "ambiguous repeated HTML anchor: " + str(identifier))
            result[identifier] = (part["id"], part["route"])
    return result


def href_spans(raw):
    """Locate href value spans without reserializing any other HTML bytes."""
    begin = re.match(r"<\s*[A-Za-z][\w:-]*", raw)
    need(begin is not None, "invalid start tag")
    cursor, found = begin.end(), []
    while cursor < len(raw):
        while cursor < len(raw) and raw[cursor].isspace():
            cursor += 1
        if raw[cursor:cursor + 1] == ">" or raw[cursor:cursor + 2] == "/>":
            break
        attribute_start = cursor
        name = re.match(r"[^\s=/>]+", raw[cursor:])
        need(name is not None, "invalid attribute")
        attribute = name[0].casefold()
        cursor += len(name[0])
        while cursor < len(raw) and raw[cursor].isspace():
            cursor += 1
        if raw[cursor:cursor + 1] != "=":
            need(attribute != "href", "href has no value")
            continue
        cursor += 1
        while cursor < len(raw) and raw[cursor].isspace():
            cursor += 1
        delimiter = raw[cursor:cursor + 1]
        if delimiter in {'"', "'"}:
            start = cursor + 1
            end = raw.find(delimiter, start)
            need(end >= start, "unterminated href/attribute")
            cursor = end + 1
        else:
            start = cursor
            while cursor < len(raw) and not raw[cursor].isspace() and raw[cursor] != ">":
                cursor += 1
            end = cursor
            delimiter = ""
        if attribute == "href":
            found.append((start, end, delimiter, html.unescape(raw[start:end]), attribute_start, cursor))
    need(len(found) <= 1, "duplicate href attribute")
    return found


class AnchorRewriter(HTMLParser):
    def __init__(self, fragment, resolve, *, inert_title=False):
        super().__init__(convert_charrefs=False)
        self.fragment, self.resolve, self.edits = fragment, resolve, []
        self.inert_title = inert_title
        self.lines = [0] + [i + 1 for i, char in enumerate(fragment) if char == "\n"]
    def handle_starttag(self, tag, attrs):
        if tag != "a":
            return
        line, column = self.getpos()
        offset = self.lines[line - 1] + column
        for start, end, delimiter, old, attribute_start, attribute_end in href_spans(self.get_starttag_text()):
            new = self.resolve(old)
            if new is None:
                replacement = ('title="' + html.escape("Source URL: " + old, quote=True) + '"'
                               if self.inert_title and "title" not in dict(attrs) else "")
                self.edits.append((offset + attribute_start, offset + attribute_end, replacement))
                continue
            if new == old:
                continue
            escaped = html.escape(new, quote=True)
            if not delimiter:
                escaped = '"' + escaped + '"'
            self.edits.append((offset + start, offset + end, escaped))
    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
    def result(self):
        self.feed(self.fragment)
        output = self.fragment
        for start, end, value in reversed(self.edits):
            output = output[:start] + value + output[end:]
        return output


def project_parts(parts, *, entrypoint, context=_UNSET, publication_routes=_UNSET,
                  site_routes=_UNSET, repository_paths=_UNSET, repository_ref=_UNSET,
                  site_ids=_UNSET, repository_ids=_UNSET, route_overrides=None,
                  repository_origin=_UNSET, live_repository_navigation=_UNSET,
                  inert_source_urls=_UNSET):
    """Project links after splitting and before computing HTML transport hashes.

    Route/admission maps are supplied by the publisher, not inferred from a
    title or an arbitrary directory listing. Repository fallback is permitted
    only for explicitly public canonical files; PDFs never use that fallback.

    Exact commits remain the default. An explicit live_repository_navigation
    opt-in permits only the literal main ref for ordinary repository source
    navigation (README, manifests and audit records). That moving destination
    is not a scholarly citation, primary evidence or an archived payload pin.
    It keeps navigation output reproducible from plaintext without Git HEAD or
    a prior publication commit; source/selection/audit digests remain the
    independent authority for the edition. Existing external citations are
    returned unchanged and never pass through this repository fallback.

    A caller may declare exact bare-host literals under exact source entrypoints
    in inert_source_urls. Those source-qualified links retain their anchor and
    wording but lose href, with a source-URL title if no title already exists.
    This records an unresolved source URL without inventing a protocol. Other
    bare hosts and the same literal outside its declared source still refuse.

    A held catalog may supply one RoutingContext instead of the raw global
    policy arguments. Every entrypoint, part, anchor and link is still checked
    on each projection. Raw arguments and a context must never be mixed.
    """
    entrypoint = path(entrypoint)
    raw = (publication_routes, site_routes, repository_paths, repository_ref,
           site_ids, repository_ids, repository_origin, live_repository_navigation,
           inert_source_urls)
    if context is not _UNSET:
        need(type(context) is RoutingContext, "expected a validated routing context")
        need(all(value is _UNSET for value in raw), "routing context cannot be mixed with raw policy arguments")
    else:
        need(all(value is not _UNSET for value in raw[:4]), "raw routing requires all route maps, paths and revision")
        context = RoutingContext(
            publication_routes=publication_routes, site_routes=site_routes,
            repository_paths=repository_paths, repository_ref=repository_ref,
            site_ids=None if site_ids is _UNSET else site_ids,
            repository_ids=None if repository_ids is _UNSET else repository_ids,
            repository_origin="https://github.com/spincyc/triptych" if repository_origin is _UNSET else repository_origin,
            live_repository_navigation=False if live_repository_navigation is _UNSET else live_repository_navigation,
            inert_source_urls=None if inert_source_urls is _UNSET else inert_source_urls)
    index = anchor_index(parts)
    publication_routes, site_routes = context._publication_routes, context._site_routes
    repository_paths, repository_ref = context._repository_paths, context._repository_ref
    site_ids, repository_ids = context._site_ids, context._repository_ids
    repository_origin = context._repository_origin
    route_overrides = route_overrides or {}
    inert_targets = context._inert_source_urls.get(entrypoint, frozenset())
    original_routes = {part["route"]: part["id"] for part in parts}
    events, projected = [], []
    for part in parts:
        current = path(route_overrides.get(part["id"], part["route"]))
        before = Identity(part["html"])
        if "text_sha256" in part:
            need(part["text_sha256"] == before.text_sha256, "part text digest changed before link projection")

        def local_href(destination, fragment, query=""):
            relative = posixpath.relpath(destination, posixpath.dirname(current) or ".")
            return urlunsplit(("", "", relative, query, quote(fragment, safe=":._-~")))

        def resolve(target):
            if target in inert_targets:
                events.append({"part": part["id"], "from": target, "to": None, "kind": "inert-source-url"})
                return None
            uri = urlsplit(target)
            if uri.scheme.casefold() == "urn":
                # Inert source identifiers are citations, not navigable file
                # paths. Keep a finite ASCII URN shape and reject controls,
                # including percent-encoded controls; never admit a general
                # unknown URI scheme through this exception.
                need(re.fullmatch(r"urn:[A-Za-z0-9][A-Za-z0-9-]{0,30}[A-Za-z0-9]:[A-Za-z0-9._~!$&'()*+,;=:@/?#%+-]+", target, re.I)
                     and not re.search(r"%(?![0-9A-Fa-f]{2})", target)
                     and not any(char.isspace() or ord(char) < 33 or 127 <= ord(char) <= 159 for char in unquote(target)),
                     "unsafe or malformed source URN citation")
                return target
            need(uri.scheme.casefold() in {"", "http", "https", "mailto"}, "unsafe link protocol")
            if uri.scheme or uri.netloc:
                return target
            fragment = unquote(uri.fragment)
            if not uri.path:
                need(not uri.query, "unscoped query-only source link")
                if not fragment:
                    return target
                need(fragment in index, "unresolved print anchor: " + fragment)
                owner, destination = index[fragment]
                rewritten = "#" + quote(fragment, safe=":._-~") if owner == part["id"] else local_href(destination, fragment)
            else:
                decoded = unquote(uri.path)
                need(not decoded.startswith("/") and "\\" not in decoded and "\0" not in decoded,
                     "nonportable or unsafe source link")
                # A source-relative link can climb more levels than the print
                # route has: main.tex lives one directory below leaf.html.
                # This optional idempotence lookup must not reject that valid
                # source-context link before the canonical lookup below.
                transported = posixpath.normpath(posixpath.join(posixpath.dirname(part["route"]), decoded))
                if transported in original_routes and fragment in index and index[fragment][1] == transported:
                    rewritten = local_href(transported, fragment, uri.query)
                    if rewritten != target:
                        events.append({"part": part["id"], "from": target, "to": rewritten})
                    return rewritten
                # Prefer the source entrypoint's actual directory. An explicit
                # repository-root token is considered only when recognized.
                candidates = [path(posixpath.join(posixpath.dirname(entrypoint), decoded))]
                if not decoded.startswith("../"):
                    candidates.append(path(decoded))
                destination = None
                chosen = None
                for candidate in dict.fromkeys(candidates):
                    if candidate in publication_routes or candidate in site_routes or candidate in repository_paths:
                        chosen = candidate
                        destination = publication_routes.get(candidate, site_routes.get(candidate))
                        break
                if chosen is None and transported in site_routes:
                    # Already-authored browser navigation may be relative to
                    # the public page rather than main.tex. Only a supplied
                    # admitted public route may establish this final fallback.
                    chosen, destination = transported, site_routes[transported]
                need(chosen is not None, "unresolved source-relative link: " + target)
                if destination is not None:
                    if fragment:
                        need(fragment in site_ids.get(destination, set()), "unresolved target-page fragment: " + target)
                    rewritten = local_href(destination, fragment, uri.query)
                else:
                    need(not chosen.lower().endswith(".pdf"), "unadmitted PDF has no source-repository fallback")
                    if fragment:
                        need(re.fullmatch(r"L[1-9][0-9]*(?:-L[1-9][0-9]*)?", fragment)
                             or fragment in repository_ids.get(chosen, set()),
                             "unproved source-repository fragment")
                    need(not uri.query, "source-repository link has an unproved query")
                    rewritten = (repository_origin.rstrip("/") + "/blob/" + quote(repository_ref, safe="")
                                 + "/" + quote(chosen, safe="/._-~"))
                    if fragment:
                        rewritten += "#" + quote(fragment, safe=":._-~")
            if rewritten != target:
                events.append({"part": part["id"], "from": target, "to": rewritten})
            return rewritten

        output = AnchorRewriter(part["html"], resolve, inert_title=True).result()
        after = Identity(output)
        need((before.text_sha256, before.ids, before.units, before.tags)
             == (after.text_sha256, after.ids, after.units, after.tags),
             "href projection changed source text, anchors or semantic units")
        projected.append({**part, "route": current, "html": output,
                          "text_sha256": before.text_sha256,
                          "html_sha256": hashlib.sha256(output.encode()).hexdigest()})
    return projected, events
