# Assistive-technology limitation — corrected record

**No real assistive-technology session was possible in this environment, so the
real-AT requirement is not satisfied by this package.** Nothing in this evidence
set, or in the V2 evidence set it supersedes, may be described as a
screen-reader pass, an AT session, or an observed announcement.

That conclusion is unchanged. What was wrong, and is corrected here, is the
stated reason.

## 1. The V2 statement this record corrects

`20260811T212656Z-catena-e1-corrections-v2/screenshots/AT-LIMITATION.md`,
line 17, in the "What the environment actually is" table:

    | the AT-SPI accessibility bus | no — no `at-spi2-core` bus launcher on the system | filesystem check for the launcher |

and, consequentially, the same file's lines 21–24:

    A screen reader needs a running accessibility bus, a speech or braille output
    channel, and a windowed browser to attach to. None of the three exists here, so
    there was no AT to run, and no announcement was heard, timed, or transcribed by
    anything.

**Both are false as written.** An AT-SPI bus launcher does exist, and the bus
was running at capture time. The sealed V2 package is left byte-identical — its
`MANIFEST.sha256` and its ZIP digest `e4083de5…6a96b` still verify — and this
record carries the correction.

The same error is inherited, in the weaker form "no accessibility bus", by the
V2 package's `LIMITATIONS.md:9`, `EVIDENCE-INDEX.md:223`, `HANDOFF.md:193`,
`UNRESOLVED-BLOCKERS.md:16`, `REVIEW_REQUEST.md:37`, and
`screenshots/INDEX.md:89` and `:254`. No tracked durable record in the
repository ever carried the claim, so no tracked file needed correcting for it.

## 2. What actually exists

An AT-SPI bus launcher is installed, and was installed before the V2 capture:

    $ pacman -Qi at-spi2-core | grep -E 'Version|Install Date'
    Version         : 2.60.6-1
    Install Date    : Sat 08 Aug 2026 01:03:45 PM CDT

    $ ls -la /usr/lib/at-spi-bus-launcher /usr/lib/at-spi2-registryd
    -rwxr-xr-x 1 root root 26800 Aug  1 14:43 /usr/lib/at-spi-bus-launcher
    -rwxr-xr-x 1 root root 84624 Aug  1 14:43 /usr/lib/at-spi2-registryd

    $ cat /usr/share/dbus-1/services/org.a11y.Bus.service
    [D-BUS Service]
    Name=org.a11y.Bus
    Exec=/usr/lib/at-spi-bus-launcher
    SystemdService=at-spi-dbus-bus.service

It is not merely installed: the bus was **running**, and had been since before
the V2 capture on 2026-08-11:

    $ busctl --user list --no-pager | grep org.a11y
    org.a11y.Bus  3442168  at-spi-bus-laun  ksh  :1.7  user@1000.service - -

    $ ps -o pid,lstart,cmd -p 3442168
        PID                  STARTED CMD
    3442168 Sat Aug  8 13:05:55 2026 /usr/lib/at-spi-bus-launcher

    $ systemctl --user is-active at-spi-dbus-bus.service
    active

**Why the V2 check was wrong.** It probed GNOME/Fedora-style locations that
Arch does not use — `/usr/lib/at-spi2-core/`, `/usr/libexec/at-spi-bus-launcher`,
`/usr/lib/at-spi2/` — all of which are genuinely absent here. Arch's
`at-spi2-core` installs the launcher directly in `/usr/lib`. A negative
filesystem probe of the wrong paths was reported as the absence of the
component.

## 3. What is actually missing

| Requirement | Present? | Check and result |
| --- | --- | --- |
| AT-SPI bus launcher | **yes** | `/usr/lib/at-spi-bus-launcher`, `at-spi2-core 2.60.6-1` |
| Accessibility bus, running | **yes** | org.a11y.Bus owned; `at-spi-dbus-bus.service` active |
| Session D-Bus | **yes** | `DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus` |
| Display server | **no** | `DISPLAY` and `WAYLAND_DISPLAY` unset; `XDG_SESSION_TYPE=tty` |
| Virtual display | **no** | `Xvfb`, `xvfb-run` not found |
| Screen reader | **no** | `orca` absent as command and as package |
| Speech synthesis | **no** | `speech-dispatcher`, `spd-say`, `espeak`, `espeak-ng`, `festival`, `flite` all absent; no `/etc/speech-dispatcher`, no runtime socket |
| Braille stack | **no** | `brltty` absent as command and as package; no `brl*` device node |
| AT-SPI registry daemon | not running | binary present; nothing has requested a registry, because no AT client exists |

## 4. The accurate limitation

- An AT-SPI bus launcher **exists** on this host, and the accessibility bus was
  running throughout the capture.
- The review environment nevertheless provided **no usable display, session or
  assistive-technology client stack** sufficient for real AT testing.
- **No usable screen-reader, speech or braille session was available.**
- **Therefore no successful real-assistive-technology evidence was produced**,
  and none is claimed.

A running bus with no screen reader, no speech channel, no braille stack and no
display is a bus with nothing on either end of it. The corrected fact does not
soften the conclusion; it only stops the package from asserting a
system-configuration fact that is untrue.

## 5. What the existing evidence actually is, and remains

The accessibility artifacts in the V2 package — the Chromium accessibility
trees, the landmark and heading listing, the keyboard traversal transcript —
are **real captures of a real browser** made over the DevTools protocol, and
they are **not** assistive-technology output. Their existing "SUPPLEMENT ONLY"
labelling is accurate and is preserved, not weakened, by this correction. The
repository's own gate assertion
(`tools/tests/corpus_browser_gate.mjs`, `interactive-controls-have-accessible-names`)
reads Chromium's computed accessibility tree; it proves a control **has** an
accessible name and proves nothing about what any AT would announce.

The real-device-or-AT review remains a **pre-release evidence prerequisite**
owned outside this lane, exactly as the independent review recorded it, and not
a Catena code defect. This lane did not attempt to install, configure or
otherwise create an AT environment; doing so was explicitly out of scope.
