"""Replay the calendar-to-DOM review against a running Triptych site using Selenium 4."""

import argparse
import collections
import datetime as dt
import json
from pathlib import Path
import statistics
import sys
from urllib.parse import urlencode

from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait


PLAN = """
const [base, calendar, dates, done] = arguments;
(async () => {
  const load = async file => {
    const response = await fetch(base + '/structure/' + file + '.json');
    if (!response.ok) throw new Error(response.status + ' ' + response.url);
    return response.json();
  };
  const [rubrics, reader] = await Promise.all([
    load('rubrics/' + calendar), load('propers/reader/' + calendar)
  ]);
  const masses = new Map(reader.masses.map(m => [m.key, m]));
  const years = new Map(), plan = {};
  for (const date of dates) {
    const yearId = date.slice(0, 4);
    if (!years.has(yearId)) years.set(yearId, await load('calendar/' + calendar + '/' + yearId));
    const day = MassAssembly.derive({date, rubrics, year: years.get(yearId)});
    plan[date] = day.options.flatMap(branch => branch.readable.flatMap(reading => {
      const mass = masses.get(reading.key);
      if (!mass) throw new Error(date + ': missing calendar Mass ' + reading.key);
      const forms = mass.forms?.length ? mass.forms.map(f => f.id) : ['main'];
      return forms.map(form => [branch.option || null, mass.key, form]);
    }));
  }
  return plan;
})().then(done, e => done({error: String(e)}));
"""

READ = """
const [hash, entrance, done] = arguments;
const state = entrance === 'day' ? dayReaderDebug : propersReaderDebug;
const start = performance.now(), previous = state.renders;
history.replaceState(null, '', '#' + hash);
dispatchEvent(new PopStateEvent('popstate'));
async function inspect() {
  const doc = document.getElementById('reader-document');
  if (!state.ready || state.renders <= previous || doc.getAttribute('aria-busy') !== 'false') {
    if (performance.now() - start > 60000) return done({error: 'navigation timed out'});
    return setTimeout(inspect, 10);
  }
  try {
    if (entrance === 'day' && state.state?.civilDate !== new URLSearchParams(hash).get('date'))
      throw new Error('reader is showing a different civil date');
    if (state.error || !['ready','unresolved'].includes(state.outcome))
      throw new Error(state.error ? JSON.stringify(state.error) : state.outcome);
    if (document.documentElement.scrollWidth > innerWidth + 1) throw new Error('horizontal overflow');
    if (/\\bundefined\\b|\\[object Object\\]|\\bNaN\\b/.test(doc.innerText)) throw new Error('invalid text');
    const elapsed = performance.now() - start;
    const calendar = new URLSearchParams(hash).get('missal');
    const data = new URLSearchParams(location.search).get('data').replace(/\\/$/, '');
    const sources = window.decadeVerifierSources ||= new Map();
    const words = text => String(text).normalize('NFC').replaceAll('℟', 'R').replaceAll('℣', 'V')
      .match(/[\\p{L}\\p{M}]+/gu)?.join(' ');
    const localEvents = [];
    const branches = Array.isArray(state.semantic) ? state.semantic : [{document: state.semantic}];
    const appointments = [];
    for (const branch of branches) {
      const result = branch.document;
      if (!result?.events?.length) continue;
      const host = branch.territory ? Array.from(doc.querySelectorAll('[data-territorial-branch]'))
        .find(node => node.dataset.territorialBranch === branch.territory) : doc;
      const ids = Array.from(new Set(Array.from(host.querySelectorAll('[data-semantic-event-id]'),
        node => node.dataset.semanticEventId)));
      if (JSON.stringify(ids) !== JSON.stringify(result.events.map(event => event.id)))
        throw new Error('semantic event sequence differs from document');
      if (calendar === 'roman-1962') {
        const creed = ['credo-heading','credo-in-unum-deum','et-in-unum-dominum','et-in-spiritum-sanctum']
          .filter(key => ids.includes('ordinary-element/oblatio/' + key));
        if (creed.length !== 0 && creed.length !== 4) throw new Error('partial Creed in the Ordinary');
      }
      if (calendar === 'roman-1962' && result.resolved.formulary === 'easter-vigil') {
        const english = 'https://extraordinaryform.org/masses/EasterVigilM20.pdf#page=';
        const latin = 'https://media.churchmusicassociation.org/pdf/missale62.pdf#page=';
        for (const [role, en, la] of [['Preface of the Easter Vigil',2,315],
            ['Communicantes of the Easter Vigil',2,294],['Easter dismissal',3,296]]) {
          const link = Array.from(host.querySelectorAll('[data-published-proper]')).find(a => a.dataset.publishedProper === role);
          const original = link?.closest('.proper')?.querySelector('.missal-rite-source');
          if (link?.href !== english + en || original?.href !== latin + la ||
              !link.title.includes('private bilingual hand missal'))
            throw new Error('Vigil source mismatch for ' + role);
        }
      }
      if (calendar === 'postconciliar' || result.resolved.formulary === 'easter-vigil') {
        const mass = result.resolved.formulary;
        const url = data + '/structure/propers/mass/' + calendar + '/' + encodeURIComponent(mass) + '.json';
        if (!sources.has(url)) sources.set(url, fetch(url).then(response => {
          if (!response.ok) throw new Error('failed to read ' + url);
          return response.json();
        }).then(json => json.mass));
        const source = await sources.get(url);
        for (const section of host.querySelectorAll('[data-semantic-event-id], [data-proper-choice-member-event]')) {
          const id = section.dataset.properChoiceMemberEvent || section.dataset.semanticEventId;
          const [type, edition, owner, ordinal] = id.split('/');
          if (type !== 'proper' || edition !== calendar || owner !== mass || !/^\\d+$/.test(ordinal)) continue;
          const row = source.propers[Number(ordinal)-1];
          const vigil = calendar === 'roman-1962' && ['Preface of the Easter Vigil',
            'Communicantes of the Easter Vigil','Easter dismissal'].includes(row.name);
          const antiphon = row.latin?.publication?.source_ids?.some(s => s.includes('2026-11-24-historical-antiphons'));
          if (!vigil && !antiphon) continue;
          const english = row.translations.find(t => t.lang === 'en');
          for (const [lang, expected] of [['la', row.text], ['en', english?.text]]) {
            const body = section.querySelector('.composed[lang="' + lang + '"]')?.cloneNode(true);
            if (!body || !expected) throw new Error('missing local ' + lang + ' body for ' + id);
            body.querySelectorAll('.composed-label, .visually-hidden').forEach(node => node.remove());
            if (words(body.textContent) !== words(expected)) throw new Error('wording differs in ' + lang + ' for ' + id);
          }
          localEvents.push(id);
        }
      }
      appointments.push([branch.territory || null, result.resolved.formulary, result.resolved.form || 'main']);
    }
    const choices = Array.from(doc.querySelectorAll('form[data-choice]'), form => ({
      id: form.dataset.choice,
      values: Array.from(form.querySelectorAll('input[data-choice-option]'), input => input.value)
    }));
    done({appointments, choices, events: branches.reduce((n, branch) => n + (branch.document?.events?.length || 0), 0),
      optionalPrayer: Boolean(doc.querySelector('[data-proper-choice="prayer-over-the-people"]')),
      localEvents, ms: elapsed});
  } catch (e) { done({error: String(e)}); }
}
inspect();
"""


OPTIONAL_PRAYER = r"""
const [entrance, done] = arguments;
const debug = entrance === 'day' ? dayReaderDebug : propersReaderDebug;
const selector = '#reader-document [data-proper-choice="prayer-over-the-people"]';
(async () => {
  for (const choice of ['pray','omit']) {
    let host = document.querySelector(selector);
    const radio = host?.querySelector('input[value="' + choice + '"]');
    if (!radio || radio.disabled) throw new Error('optional prayer lacks an available ' + choice + ' control');
    if (!radio.checked) {
      for (let node = radio.parentElement; node; node = node.parentElement) {
        if (node.tagName === 'DETAILS') node.open = true;
      }
      const previous = debug.renders, deadline = performance.now() + 15000;
      radio.click();
      while (debug.renders <= previous || document.querySelector('#reader-document').getAttribute('aria-busy') !== 'false') {
        if (performance.now() > deadline) throw new Error('optional prayer navigation timed out');
        await new Promise(resolve => setTimeout(resolve, 10));
      }
    }
    host = document.querySelector(selector);
    const active = host?.querySelector('[data-choice-status="selected"]');
    if (debug.error || host?.dataset.choiceSelection !== choice || active?.dataset.properChoiceOption !== choice)
      throw new Error('reader lost its selected optional prayer');
    if (Boolean(active.querySelector('[data-proper-choice-member-event]')) !== (choice === 'pray'))
      throw new Error('reading does not follow use or omission');
    if (choice === 'pray' && (!active.querySelector('[data-published-proper]') ||
        !active.querySelector('[data-published-latin-proper]'))) throw new Error('optional prayer lost a published source');
  }
  return true;
})().then(done, error => done({error:String(error)}));
"""


def inspect_optional_prayer(driver, entrance):
    result = driver.execute_async_script(OPTIONAL_PRAYER, entrance)
    if result is not True:
        raise ValueError(result.get("error", "optional prayer inspection failed"))


def dates_inclusive(first, last):
    return [(first + dt.timedelta(days=i)).isoformat() for i in range((last - first).days + 1)]


def inspect_day(driver, defaults, expected):
    pending = collections.deque([{}])
    seen, rendered, times = set(), set(), []
    events, local_bodies = 0, 0
    for _, mass, form in expected:
        pending.append(dict(mass=mass, **({"form": form} if form != "main" else {})))
    while pending:
        selection = pending.popleft()
        key = urlencode(defaults | selection)
        if key in seen:
            continue
        seen.add(key)
        result = driver.execute_async_script(READ, key, 'day')
        if result.get("error"):
            raise ValueError(f"{key}: {result['error']}")
        if result.get("optionalPrayer"):
            inspect_optional_prayer(driver, "day")
        times.append(result["ms"])
        events += result["events"]
        local_bodies += 2 * len(result["localEvents"])
        rendered.update(map(tuple, result["appointments"]))
        for choice in result["choices"]:
            for value in choice["values"]:
                if choice["id"].startswith("proper-form:"):
                    pending.append(dict(mass=choice["id"].split("/")[-1], form=value))
                else:
                    pending.append(dict(mass=value))
    planned = set(map(tuple, expected))
    if rendered != planned:
        raise ValueError(f"{defaults['date']}: missing {sorted(planned - rendered, key=str)}, "
                         f"unexpected {sorted(rendered - planned, key=str)}")
    return len(rendered), times, events, local_bodies


MEMORIAL_SOURCES = """
const [data, calendar, mass, roles, groups, done] = arguments;
(async () => {
  const controls = Array.from(document.querySelectorAll('[data-memorial-prayer]'));
  if (controls.length !== roles.length) throw new Error('missing independent prayer source controls');
  const eventCount = document.querySelectorAll('[data-semantic-event-id]').length;
  const hrefs = new Set(), fetched = new Map();
  const target = key => {
    if (!fetched.has(key)) fetched.set(key, fetch(data+'/structure/propers/mass/'+calendar+'/'+key+'.json')
      .then(r => { if (!r.ok) throw new Error(r.status); return r.json(); }).then(r => r.mass));
    return fetched.get(key);
  };
  const waitFor = async test => {
    const end = performance.now() + 15000;
    while (!test()) {
      if (performance.now() > end) throw new Error('source picker timed out');
      await new Promise(r => setTimeout(r, 10));
    }
  };
  let choices = 0, occurrences = 0;
  for (const control of controls) {
    const role = control.dataset.memorialPrayer;
    if (!roles.includes(role)) throw new Error('unknown source role '+role);
    control.open = true;
    const select = control.querySelector(':scope > label select');
    await waitFor(() => select.options.length > 1);
    const expected = groups.flatMap(g => g.form_ids.map(f => [g.id,g.mass,f].join('/')));
    const actual = Array.from(select.options, o => o.value).filter(Boolean);
    if (JSON.stringify(actual) !== JSON.stringify(expected)) throw new Error('Common source list differs from its witness');
    for (const value of actual) {
      const [,key,form] = value.split('/');
      const source = await target(key);
      const rows = source.propers.map((p,i) => ({p,i})).filter(r => r.p.form_id === form && r.p.name === role);
      if (!rows.length) throw new Error('no source prayer in '+value);
      select.value = value;
      select.dispatchEvent(new Event('change', {bubbles:true}));
      const preview = control.querySelector('.memorial-prayer-preview');
      await waitFor(() => preview.querySelector('a') && (preview.querySelector('.proper') || preview.querySelector('select')));
      const href = preview.querySelector('a').href, params = new URLSearchParams(new URL(href).hash.slice(1));
      const disposition = rows[0].p.ordinary_disposition;
      const position = disposition?.kind === 'alternative'
        ? ['proper-choice',calendar,key,form,disposition.group].join('/')
        : ['proper',calendar,key,String(rows[0].i+1).padStart(3,'0')].join('/');
      if (params.get('mass') !== key || params.get('form') !== form || params.get('location') !== position)
        throw new Error('incorrect prayer location '+href);
      hrefs.add(href);
      if (rows.length > 1) {
        const variants = preview.querySelector('select');
        if (!variants || variants.options.length !== rows.length + 1) throw new Error('missing prayer alternatives');
        for (let i=0; i<rows.length; ++i) {
          variants.value = String(i);
          variants.dispatchEvent(new Event('change', {bubbles:true}));
          await waitFor(() => preview.querySelector('.proper'));
        }
      }
      ++choices;
      occurrences += rows.length;
    }
    control.open = false;
  }
  if (document.querySelectorAll('[data-semantic-event-id]').length !== eventCount ||
      propersReaderDebug.semantic.resolved.formulary !== mass) throw new Error('memorial identity changed');
  return {choices, occurrences, hrefs:[...hrefs]};
})().then(done, e => done({error:String(e)}));
"""


PUBLISHED_PRAYERS = r"""
const [url, key, form, done] = arguments;
(async () => {
  const response = await fetch(url);
  if (!response.ok) throw new Error('formulary HTTP '+response.status);
  const {mass} = await response.json();
  if (mass.key !== key) throw new Error('incorrect source owner');
  const seen = new Set();
  let count = 0, latinCount = 0, otherCount = 0, otherLatinCount = 0;
  const events = document.querySelector('#reader-document').querySelectorAll('[data-semantic-event-id], [data-proper-choice-member-event]');
  for (const section of events) {
    const eventId = section.dataset.properChoiceMemberEvent || section.dataset.semanticEventId;
    const [,calendar,owner,ordinal] = eventId.split('/');
    if (calendar !== 'postconciliar' || owner !== key || !/^\d+$/.test(ordinal || '')) continue;
    const proper = mass.propers[Number(ordinal)-1];
    if (!proper) continue;
    if (proper.published_english_source) {
      const link = section.querySelector('[data-published-proper]');
      if (!link || link.href !== proper.published_english_source.url) throw new Error('incorrect published Proper '+eventId);
      ++otherCount;
    }
    if (proper.published_latin_source) {
      const link = section.querySelector('[data-published-latin-proper]');
      if (!link || link.href !== proper.published_latin_source.url) throw new Error('incorrect Latin Proper '+eventId);
      ++otherLatinCount;
    }
    if (!['Collect','Prayer over the Offerings','Prayer after Communion'].includes(proper.name)) continue;
    const form = (mass.forms || []).find(f => f.id === proper.form_id);
    const witnesses = [...(form?.missal_witness_links || []), ...(mass.missal_witness_links || [])];
    const latin = witnesses.filter(w => w.language === 'la' && w.scope === 'form');
    if (!proper.text && latin.length) {
      const a = section.querySelector('.published-latin-link');
      if (!a || !latin.some(w => w.url === a.href)) throw new Error('incorrect Latin formulary '+eventId);
      ++latinCount;
    }
    const sources = witnesses.filter(w => (w.prayer_roles || []).includes(proper.name));
    if (!sources.length) continue;
    const links = Array.from(section.querySelectorAll('.published-prayer-link'));
    if (links.length !== 1 || !sources.some(w => w.url === links[0].href))
      throw new Error('published prayer is missing or belongs to another formulary: '+eventId);
    ++count;
    seen.add(links[0].href);
  }
  const recovered = [];
  mass.propers.forEach((row, i) => {
    if (row.form_id !== form || !row.latin?.publication?.source_ids?.some(id => id.includes('2026-11-24-historical-antiphons'))) return;
    const d = row.ordinary_disposition;
    recovered.push({id:['proper','postconciliar',key,String(i+1).padStart(3,'0')].join('/'),
      choice:d?.kind === 'alternative' ? {['proper-choice/postconciliar/'+key+'/'+form+'/'+d.group]:d.option} : null});
  });
  return {count, latinCount, otherCount, otherLatinCount, recovered, urls:[...seen]};
})().then(done, e => done({error:String(e)}));
"""


def inspect_standalone(driver, url, data, defaults, mass_keys):
    driver.get(url + '?' + urlencode({'data': data}) + '#' + urlencode(defaults))
    WebDriverWait(driver, 60).until(lambda page: page.execute_script('return !!window.propersReaderDebug?.ready'))
    catalog = driver.execute_async_script('''
      const [url, done] = arguments;
      fetch(url).then(response => response.json()).then(data => done(data.masses.map(mass =>
        [mass.key, mass.kind, mass.forms?.map(form => form.id) || [], mass.memorial_prayer_sources || null])), error => done({error: String(error)}));
    ''', data.rstrip('/') + '/structure/propers/reader/' + defaults['missal'] + '.json')
    if not isinstance(catalog, list):
        raise ValueError(catalog)
    checked, failures = 0, []
    published = set()
    counts = collections.Counter()
    locations = set()
    unknown = mass_keys - {row[0] for row in catalog}
    if unknown:
        raise ValueError(f"Unknown formulary keys in this missal: {sorted(unknown)}")
    for mass, kind, forms, sources in catalog:
        if mass_keys and mass not in mass_keys:
            continue
        for form in forms or ['main']:
            request = defaults | {'mass': mass, 'type': kind}
            if form != 'main':
                request['form'] = form
            key = urlencode(request)
            result = driver.execute_async_script(READ, key, 'propers')
            if result.get('error') or [None, mass, form] not in result.get('appointments', []):
                failures.append(f"{key}: {result.get('error', 'no selected formulary')}")
            elif defaults['missal'] == 'postconciliar':
                url = data.rstrip('/') + '/structure/propers/mass/postconciliar/' + mass + '.json'
                checked_prayers = driver.execute_async_script(PUBLISHED_PRAYERS, url, mass, form)
                if checked_prayers.get('error'):
                    failures.append(f"{key}: {checked_prayers['error']}")
                else:
                    counts['published_prayer_positions'] += checked_prayers['count']
                    counts['published_latin_formulary_positions'] += checked_prayers['latinCount']
                    counts['other_published_english_positions'] += checked_prayers['otherCount']
                    counts['other_published_latin_positions'] += checked_prayers['otherLatinCount']
                    published.update(checked_prayers['urls'])
                    for target in checked_prayers['recovered']:
                        selected = result
                        if target['choice']:
                            params = request | {'proper-choices': json.dumps(target['choice'])}
                            selected = driver.execute_async_script(READ, urlencode(params), 'propers')
                        if target['id'] in selected.get('localEvents', []):
                            counts['bilingual_historical_antiphons'] += 1
                        else:
                            failures.append(f"{key}: {target['id']}: {selected.get('error', 'appointed antiphon absent')}")
                    if any(target['choice'] for target in checked_prayers['recovered']):
                        driver.execute_async_script(READ, key, 'propers')
            if result.get('optionalPrayer'):
                try:
                    inspect_optional_prayer(driver, 'propers')
                    counts['optional_prayers_exercised'] += 1
                except ValueError as error:
                    failures.append(f"{key}: {error}")
            if sources and not result.get('error'):
                sources_result = driver.execute_async_script(MEMORIAL_SOURCES, data.rstrip('/'),
                    defaults['missal'], mass, sources['roles'], sources['groups'])
                if sources_result.get('error'):
                    failures.append(f"{key}: {sources_result['error']}")
                else:
                    counts['memorial_prayer_positions'] += len(sources['roles'])
                    counts['memorial_source_choices'] += sources_result['choices']
                    counts['memorial_prayer_occurrences'] += sources_result['occurrences']
                    locations.update(sources_result['hrefs'])
            checked += 1
    for href in sorted(locations):
        result = driver.execute_async_script(READ, href.partition('#')[2], 'propers')
        if result.get('error'):
            failures.append(f"{href}: {result['error']}")
    counts['distinct_prayer_links_opened'] = len(locations)
    counts['distinct_published_prayer_links'] = len(published)
    return checked, failures, counts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("day_url", help="Day reader URL on the running site, excluding query or fragment")
    parser.add_argument("data_url", help="Browser product root on the same site")
    parser.add_argument("calendar", choices=["roman-1962", "postconciliar"])
    parser.add_argument("--first", type=dt.date.fromisoformat, default=dt.date(2026, 11, 24))
    parser.add_argument("--last", type=dt.date.fromisoformat, default=dt.date(2036, 11, 23))
    parser.add_argument("--mode", choices=["read", "missal"], default="missal")
    parser.add_argument("--propers-url", help="Also check each standalone formulary and named Common on this Propers reader")
    parser.add_argument("--mass", action="append", default=[], metavar="KEY",
                        help="Check every appointment on dates containing this formulary and its standalone forms. Repeat for more formularies.")
    parser.add_argument("--timings", type=Path, help="Write individual dated navigation times in milliseconds as JSON")
    args = parser.parse_args()
    if args.last < args.first:
        parser.error("--last precedes --first")
    dates = dates_inclusive(args.first, args.last)
    defaults = dict(missal=args.calendar, bible="douay-rheims", orations="en", ordinary="1" if args.mode == "missal" else "0", mode=args.mode,
                    **{"ordinary-lang": "en", "text-display": "latin-and-selected",
                       "scripture-companion": "clementine-vulgate"})
    options = ChromeOptions()
    for flag in ["--headless=new", "--no-sandbox", "--disable-ipc-flooding-protection", "--disable-dev-shm-usage", "--window-size=1280,900"]:
        options.add_argument(flag)
    appointments, events, local_bodies, times, failures = 0, 0, 0, [], []
    mass_keys = set(args.mass)
    standalone, source_counts = 0, {}
    with Chrome(options=options) as driver:
        driver.set_script_timeout(120)
        entry = args.day_url + "?" + urlencode({"data": args.data_url})
        driver.get(entry + "#" + urlencode(defaults | {"date": dates[0]}))
        WebDriverWait(driver, 60).until(lambda page: page.execute_script("return !!window.dayReaderDebug?.ready"))
        plan = driver.execute_async_script(PLAN, args.data_url.rstrip("/"), args.calendar, dates)
        if "error" in plan:
            raise ValueError(plan["error"])
        review_dates = [day for day in dates if not mass_keys or any(row[1] in mass_keys for row in plan[day])]
        for date in review_dates:
            try:
                count, timings, event_count, body_count = inspect_day(driver, defaults | {"date": date}, plan[date])
                appointments += count
                events += event_count
                local_bodies += body_count
                times.extend(timings)
            except ValueError as error:
                failures.append(str(error))
        if args.propers_url:
            standalone, additional, source_counts = inspect_standalone(driver, args.propers_url, args.data_url, defaults, mass_keys)
            failures.extend(additional)
        elif mass_keys and not review_dates:
            failures.append("None of the selected formularies is appointed in this date range")
    report = {"calendar": args.calendar, "mode": args.mode, "first": dates[0], "last": dates[-1], "dates": len(review_dates),
              "appointments": appointments, "views": len(times), "events": events, "verified_local_bodies": local_bodies, "standalone_forms": standalone,
              "failures": failures, **source_counts}
    if args.timings:
        args.timings.write_text(json.dumps(times) + "\n", encoding="utf-8")
    if times:
        report["navigation_ms_median"] = round(statistics.median(times), 1)
        if len(times) > 1:
            report["navigation_ms_p95"] = round(statistics.quantiles(times, n=100, method="inclusive")[94], 1)
    print(json.dumps(report, ensure_ascii=False))
    return bool(failures)


if __name__ == "__main__":
    sys.exit(main())
