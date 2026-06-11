# Gytha — Netrek Client (Pygame)

Gytha is a Python/Pygame client for [Netrek](https://www.netrek.org/), a real-time
multiplayer space combat game first played in 1988.  It connects to any standard
Netrek server over TCP/UDP.

**Version:** 0.9  
**Author:** James Cameron &lt;quozl@us.netrek.org&gt;  
**Licence:** GNU General Public Licence v2 (see `COPYING`)  
**Language:** Python 2.4+, Pygame 1.7.1+

---

## About Netrek

Netrek is a 16-player real-time space battle game.  Two teams of up to eight
ships fight for control of planets across a 100,000 × 100,000 coordinate galaxy.
Ships carry armies between planets to conquer them; the team that owns all planets
wins.  Gameplay involves torpedoes, phasers, plasma torpedoes, cloaking, tractor
beams, and structured team communication via distress calls.

## Features of this client

- Tactical view (your ship centred, 20,000-unit radius) and simultaneous galactic
  overview
- TCP and UDP protocol support with automatic upgrade after login
- Metaserver integration — queries `metaserver.netrek.org` on startup for a live
  server list
- Animated sprites: rotating ships, exploding torpedoes, phaser lines, tractor
  beams, shield bubbles, planet halos
- Structured distress / RCD (Receiver Configurable Distress) team-chat parsing
- Achievement system persisted to `~/.gytha.achievements`
- Mercenary auto-team-selection mode
- Fullscreen and windowed modes; Scale2x for high-DPI displays
- OGG sound effects (kills, death, phaser, shields, gains)
- Screenshots via the Print Screen key

---

## Requirements

| Dependency | Minimum version | Notes |
|---|---|---|
| Python | 2.4 | 2.6+ recommended |
| Pygame | 1.7.1 | For graphics, input, and audio |
| DejaVu fonts | any | Usually shipped with the OS |
| libX11 | any | Linux/X11 only; used for input-lag reduction |

The client connects to Netrek servers on TCP/UDP port 2592 and queries the
metaserver on UDP port 3521.

## Installation

```
git clone <repository>
cd netrek-client-pygame
# Optionally install to /usr/share/games/gytha:
make install
```

No build step is required; the package is pure Python.

## Running

```bash
python gytha.py                         # fullscreen, picks server from metaserver
python gytha.py --no-fullscreen         # windowed
python gytha.py -s netrek.server.org    # connect directly to a server
python gytha.py --name MyName --team fed
```

The splash screen appears briefly, then the server-list screen loads with live
data from the metaserver.  Click a server to connect.

---

## Controls

### Mouse

| Action | Control |
|---|---|
| Set heading | Right-click anywhere on tactical or galactic |
| Fire torpedo | Left-click |
| Fire phaser | Middle-click |
| Planet / ship info | Left-click on a planet or ship sprite |

### Keyboard — flight

| Key | Action |
|---|---|
| `1`–`9` | Set speed (1 = slow, 9 = max) |
| `0` | Stop |
| `S` | Toggle shields |
| `C` | Toggle cloak |
| `R` | Toggle repair |
| `O` | Orbit nearest planet |
| `B` | Bomb planet (must be in orbit) |
| `X` | Beam down armies |
| `Z` | Beam up armies |
| `P` | Fire plasma torpedo |
| `D` | Detonate enemy torpedoes nearby |
| `L` | Lock onto nearest planet |
| `Shift`+`F/R/K/O` | Lock onto nearest Fed/Rom/Kli/Ori planet |
| `M` | Open message composer |
| `Ctrl`+`T` | Send "I'm taking" distress |
| `Ctrl`+`E` | Send "I'll escort" distress |
| `?` or `H` | Toggle help/tips screen |
| `Q` or `Esc` | Quit |
| `Print Screen` | Save screenshot |

### Keyboard — message composer

| Key | Action |
|---|---|
| `T` / `A` / `F` / `R` / `K` / `O` | Address to Team / All / Federation / Romulan / Klingon / Orion |
| `Enter` | Send message |
| `Esc` | Cancel |

---

## Command-line options

```
-F, --fullscreen          Fullscreen mode (default)
    --no-fullscreen       Windowed mode
-s, --server HOST         Connect directly to this server
-p, --port PORT           Server port (default 2592)
    --name NAME           Character name (default: guest)
    --password PASS       Password for character name
    --login LOGIN         Username shown in player list (default: gytha)
    --team TEAM           Team to join (fed/rom/kli/ori)
    --mercenary           Auto-join the least represented team
    --ship CLASS          Ship class to request
    --updates N           Server update rate in Hz (default 10)
    --tcp-only            Disable UDP, use TCP only
    --metaserver HOST     Metaserver address (default metaserver.netrek.org)
    --metaserver-refresh-interval N
                          Seconds between metaserver polls (default 30)
    --splash-time MS      Splash screen duration in milliseconds (default 1000)
    --width W / --height H  Force a specific window resolution
    --no-backgrounds      Disable background images
    --halos               Show experimental target-distance halos
    --debug               Overlay FPS, UPS, and network statistics
    --ubertweak           Enable ubertweak mode (reduced event overhead)
    --sounds PATH         Path to sound effects directory
    --dump-server         Dump raw server packet stream to stdout
    --dump-client         Dump raw client packet stream to stdout
```

---

## Architecture (developer notes)

```
gytha.py                 Entry point — calls gytha.main()
gytha/
  __init__.py            Everything: game state, packet handlers, phases, rendering
  client.py              TCP + UDP socket management; select()-based event loop
  meta.py                UDP metaserver client
  cache.py               Image (IC) and font (FC) caches; Scale2x support
  sprites.py             Pygame sprite classes: Icon, Text, Field, buttons
  bouncer.py             Parametric-orbit animation for splash screen
  cap.py                 Ship capability tables (speed, turn rate, weapons)
  constants.py           Protocol and game constants (GWIDTH, TWIDTH, team IDs…)
  options.py             optparse option definitions
  util.py                Coordinate math helpers
  motd.py                MOTD buffer and display
  rcd.py                 RCD (distress call) decoding
  sound.py               pygame.mixer sound effect loader
  mercenary.py           Automatic team selection logic
images/                  PNG/JPG sprite and background assets (180+)
sounds/                  OGG audio files
doc/                     Screenshots and HTML documentation
```

### Coordinate systems

| System | Range | Description |
|---|---|---|
| Netrek | 0–100,000 | Server-authoritative galaxy coordinates (GWIDTH = 100,000) |
| Tactical screen | pixels | 20,000-unit window centred on the player's ship |
| Galactic screen | pixels | Full galaxy scaled to fit the galactic panel |
| Sub-galactic | pixels | Smaller inset map variant |

### Phase (screen) lifecycle

```
PhaseSplash → PhaseServers → PhaseQueue → PhaseLogin → PhaseOutfit → PhaseFlight
                   ↕
               PhaseTips
```

Each phase owns its own event handler tables (`eh_md`, `eh_mu`, `eh_mm`,
`eh_ue`) and `display_sink()` / `network_sink()` methods.  The `cycle_wait()`
method drives a `pygame.time.set_timer()`-based 100 Hz update loop.

### Network event loop

`client.Client.recv()` calls `select.select()` on a list of file descriptors:

1. The TCP socket to the game server
2. The UDP socket (after SP_PICKOK)
3. The X11 display socket (see below)

The `pg_fd()` function in `__init__.py` (line 5116) navigates SDL 1.2 private
C structures via `ctypes` to locate the X11 display file descriptor.  When
found, it is appended to the select list and the timeout is set to `None`
(blocking), giving zero-latency response to both network packets and user input.
When the fd cannot be found, a fallback timeout of 0.02 s is used instead,
which introduces up to 20 ms of input lag — noticeable when firing rapid torpedo
spreads.

---

## Porting to Python 3 and Pygame 2.6.1

This section documents the work required to port Gytha from Python 2 / Pygame 1
to Python 3 / Pygame 2.6.1.

### The X11 socket problem

This is the most architecturally significant issue.  The existing `pg_fd()`
function navigates SDL **1.2** private C structures at hard-coded byte offsets:

```python
w = pygame.display.get_wm_info()
w = w['display']
n = int(str(w)[23:-1], 16)            # parse ctypes repr for the raw pointer
n = ctypes.cast(n+8, ctypes.POINTER(ctypes.c_int)).contents.value  # SDL1.2 offset
n = ctypes.cast(n+8, ctypes.POINTER(ctypes.c_int)).contents.value  # _XDisplay.fd
```

Pygame 2 uses SDL **2**, whose internal layout is entirely different.  This
function will silently fail (the `except` clause catches all errors) and fall
back to the 0.02 s timeout on any Pygame 2 installation.

Three replacement strategies are described below, in order of increasing
architectural change.

#### Strategy A — Fix `pg_fd()` for SDL2 (X11 only)

Pygame 2 on X11 still populates `get_wm_info()['display']` with the actual
`Display*` pointer and sets `get_wm_info()['subsystem'] == 'x11'`.  The correct
way to extract the file descriptor from a `Display*` is the Xlib API call
`XConnectionNumber()`, which is exported as a real function symbol in
modern libX11:

```python
import ctypes

def pg_fd_sdl2():
    try:
        wm = pygame.display.get_wm_info()
        if wm.get('subsystem') != 'x11':
            return          # Wayland, macOS, Windows — no X fd
        display_ptr = wm['display']
        libX11 = ctypes.CDLL('libX11.so.6')
        libX11.XConnectionNumber.restype = ctypes.c_int
        libX11.XConnectionNumber.argtypes = [ctypes.c_void_p]
        n = libX11.XConnectionNumber(display_ptr)
    except Exception:
        print("unable to identify file descriptor of X socket, slowing")
        return
    nt.set_pg_fd(n)
    if mc:
        mc.set_pg_fd(n)
```

This is the minimal invasive fix.  It only works on X11; Wayland, macOS, and
Windows still fall back to the timeout.

**Important caveat:** Wayland is now the default compositor on many Linux
distributions (Fedora, Ubuntu 22.04+, Arch).  SDL2 running natively on Wayland
exposes no equivalent socket fd.  Strategy A is therefore incomplete for a fully
modern Linux deployment.

#### Strategy B — Accept the fallback (simplest, lowest risk)

Remove `pg_fd()` entirely and set `client.Client.timeout = 0.02` unconditionally.
The 20 ms maximum input lag is imperceptible to casual players.  Expert players
firing rapid torp spreads at 10 updates/second will experience occasional
one-frame delays.

This is a valid choice for an initial port that prioritises stability over
responsiveness, and can always be revisited later with Strategy A or C.

#### Strategy C — Background network thread (recommended for full portability)

Replace the `select()` integration with a dedicated network I/O thread.  The
thread blocks in `socket.select()` on the network fds alone and posts a
`pygame.event.post(pygame.event.Event(NETWORK_EVENT))` custom event whenever
data arrives.  The main thread runs `pygame.event.wait()` (blocking without a
timeout) and handles both UI events and the custom network event.

```
Main thread                         Network thread
────────────────────────────────    ────────────────────────────────
pygame.event.wait() ←─ blocks       select([tcp, udp], [], [], None)
                                    ↓ data ready
                                    recv and dispatch packets
                                    pygame.event.post(NETWORK_EVENT)
↓ woken by event
handle NETWORK_EVENT or UI event
```

Benefits:
- Works on X11, Wayland, macOS, Windows — no SDL internals needed
- The `set_pg_fd()` / timeout mechanism in `Client` can be removed entirely
- Idiomatic Python 3 (threading module is well-supported)

Drawbacks:
- Thread safety: game state updated by the network thread must be protected.
  The simplest approach is a `threading.Lock` around the `galaxy` state object,
  held briefly while updating and while rendering.
- Slightly more complex shutdown sequence.

This strategy is **recommended** for the Python 3 port because it removes a
platform-specific hack and makes the client portable to Wayland and non-Linux
platforms without any further effort.

---

### Python 2 → Python 3 migration

The changes fall into four categories.

#### 1. Syntax (`2to3` handles most of these automatically)

| Pattern (Python 2) | Replacement (Python 3) |
|---|---|
| `print expr` | `print(expr)` |
| `except Exc, e:` | `except Exc as e:` |
| `except socket.error, (r, m):` | `except OSError as e: r, m = e.args` |
| `raise "message"` | `raise RuntimeError("message")` |
| `xrange(n)` | `range(n)` |
| `dict.iteritems()` | `dict.items()` |
| `dict.itervalues()` | `dict.values()` |
| `dict.has_key(k)` | `k in dict` |
| `reduce(f, xs)` | `from functools import reduce; reduce(f, xs)` |
| `__metaclass__ = Foo` (class body) | `class X(metaclass=Foo):` |
| Integer division `/` on ints | Audit: replace with `//` where floor is intended |

Estimated scope: `__init__.py` alone contains approximately 117 print
statements and similar Python 2-isms spread across ~5,740 lines.  The `2to3`
command-line tool will handle the mechanical transformations; a careful manual
pass is required for division operators and exception unpacking.

#### 2. Bytes vs strings in the network layer (`client.py`)

The network code uses `array.array('B', …)` as a receive buffer and passes
slices to packet handlers.  Python 3 tightens the distinction between `str`
(text) and `bytes` (binary data), requiring specific fixes:

| Location | Python 2 | Python 3 |
|---|---|---|
| `client.py:24` | `array.array('B', bufsiz * '\0')` | `array.array('B', bytes(bufsiz))` |
| `client.py:144,199` | `buffer[a:b].tostring()` | `buffer[a:b].tobytes()` |
| `client.py:198` | `recv_into(self.buffer[length:], need)` | `recv_into(memoryview(self.buffer)[length:], need)` |
| `client.py:243–253` | `rest = ''` / `byte + rest` | `rest = b''` / bytes concatenation |
| `client.py:236` | `struct.unpack('b', byte[0])` | `struct.unpack('b', byte)` (byte is already `bytes`) |
| `client.py:58,129,163,179` | `except socket.error, (r, m):` | `except OSError as e: r, m = e.args` |

All `struct.pack` / `struct.unpack_from` calls produce and consume `bytes` in
Python 3, which is consistent with what they do in Python 2 on network data;
most will need no change beyond the exception-syntax fix.

#### 3. Metaclass syntax for packet classes (`__init__.py`)

The CP_* and SP_* packet classes use an old-style metaclass declaration:

```python
# Python 2
class CP_LOGIN(CP):
    __metaclass__ = ClientPacket
    ...

# Python 3
class CP_LOGIN(CP, metaclass=ClientPacket):
    ...
```

There are two metaclass declarations (lines 2412 and 2740) acting as base-class
defaults.  The most compatible approach is to have the base classes `CP` and
`SP` themselves declare the metaclass so all subclasses inherit it:

```python
class CP(metaclass=ClientPacket):
    ...
class SP(metaclass=ServerPacket):
    ...
```

Then remove `__metaclass__ = …` from every subclass body.

#### 4. `optparse` → `argparse`

`optparse` is present in Python 3 but deprecated since 3.2 and may be removed
in a future release.  The migration to `argparse` is mechanical; the option
names and defaults are preserved in `gytha/options.py`.

---

### Pygame 1 → Pygame 2 API changes

Most Pygame 2 APIs are backwards-compatible with Pygame 1.  The following
specifics apply to this codebase.

| Area | Status |
|---|---|
| `pygame.sprite.Sprite`, `Group`, `draw()` | Unchanged |
| `pygame.Surface(size, flags, depth)` with `SRCALPHA` | Unchanged |
| `pygame.display.update(rects)` | Unchanged |
| `pygame.draw.*` | Unchanged |
| `pygame.font.Font` / `render()` | Unchanged |
| `pygame.time.set_timer(event, ms)` | Unchanged; Pygame 2 adds an optional repeat-count argument, default is infinite (same as Pygame 1 behaviour) |
| `pygame.mixer` / OGG playback | Unchanged |
| `pygame.locals` constants | Unchanged |
| `pygame.display.get_wm_info()` | Present in Pygame 2 / SDL2; returns `subsystem` key in addition to `display` and `window` — see X11 discussion above |
| `pygame.SRCALPHA` surface flag | Unchanged |
| `pygame.Rect` | Unchanged |

The `Scale2x` path in `cache.py` uses `pygame.transform.scale2x()`, which is
present in Pygame 2 unchanged.

No Pygame 2 deprecation warnings are expected from this codebase other than the
X11 fd hack and the pygame 1-era `pygame.SRCALPHA` depth argument of `32` (now
ignored; Pygame 2 infers depth from the flags automatically).

---

### Recommended migration sequence

1. **Run `2to3 -w gytha/`** to apply all mechanical Python 2→3 transformations
   in place.  Commit the result as a starting point.

2. **Fix the network byte-handling** in `client.py` manually (the table in
   section 2 above covers all required changes).

3. **Fix the metaclass declarations** in `__init__.py` (section 3 above).

4. **Migrate `options.py`** from `optparse` to `argparse`.

5. **Run the client without a server** (`--metaserver localhost` with nothing
   listening) to exercise the splash and server-list screens.  Fix any remaining
   `TypeError`/`AttributeError` from Python 3 str/bytes confusion.

6. **Implement Strategy B** (remove `pg_fd()`, set `timeout = 0.02`) to get a
   working client under Pygame 2.  Verify game play end-to-end.

7. **Implement Strategy A or C** to restore low-latency input.  Strategy C is
   preferred for long-term maintainability and Wayland compatibility.

8. **Test on Wayland** by setting `SDL_VIDEODRIVER=wayland` and confirming the
   fallback path is taken gracefully.

---

## Known issues

- Input lag of up to 20 ms on non-X11 platforms (Windows, macOS, Wayland) due
  to the `select()` timeout fallback when the X11 socket fd cannot be identified.
- UDP path failure detection is not fully implemented (`FIXME` at `client.py:264`).
- Approximately 30 `FIXME` comments in `__init__.py` mark incomplete features,
  including: speed display on tactical, player proximity edge pointers, unknown
  planet scanning, and moving/turning achievements on the galactic map.
- The `tcp_read_more()` `raise "string"` on unknown packet type will not work
  even on Python 2 in new-style class contexts; it needs to be `raise
  RuntimeError(...)`.

## Licence

GNU General Public Licence, version 2 or later.  See `COPYING`.
