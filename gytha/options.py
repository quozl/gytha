from argparse import ArgumentParser

parser = ArgumentParser(description='Gytha — Netrek client (Pygame)')
parser.add_argument("-F", "--fullscreen",
                    action="store_true", dest="fullscreen", default=True,
                    help="force fullscreen mode on")
parser.add_argument("--no-fullscreen", "--no-full-screen",
                    action="store_false", dest="fullscreen",
                    help="force fullscreen mode off")
parser.add_argument("-s", "--server", "--host", dest="server",
                    help="netrek server to connect to")
parser.add_argument("-p", "--port", type=int, dest="port", default=2592,
                    help="netrek player port number to connect to")
parser.add_argument("--name", dest="name", default="",
                    help="character name, default guest")
parser.add_argument("--password", dest="password", default="",
                    help="password for character name")
parser.add_argument("--login", dest="login", default="gytha",
                    help="username to show on player list")
parser.add_argument("--team", dest="team",
                    help="team to join")
parser.add_argument("--mercenary",
                    action="store_true", dest="mercenary", default=False,
                    help="automatically join the least represented team")
parser.add_argument("--ship", dest="ship",
                    help="ship class to request")
parser.add_argument("--updates",
                    type=int, dest="updates", default=10,
                    help="updates per second from server, default 10")
parser.add_argument("--tcp-only",
                    action="store_true", dest="tcp_only", default=False,
                    help="only use TCP, avoid UDP")
parser.add_argument("--dump-server",
                    action="store_true", dest="sp", default=False,
                    help="dump server packet stream")
parser.add_argument("--dump-client",
                    action="store_true", dest="cp", default=False,
                    help="dump client packet stream")
parser.add_argument("--screenshots",
                    action="store_true", dest="screenshots", default=False,
                    help="generate publicity screenshots")
parser.add_argument("--metaserver", action="store",
                    default='metaserver.netrek.org',
                    help="metaserver to query for games.")
parser.add_argument("--metaserver-refresh-interval",
                    type=int, dest="metaserver_refresh_interval", default=30,
                    help="how many seconds between metaserver queries, default 30")
parser.add_argument("--splash-time",
                    type=int, dest="splashtime", default=1000,
                    help="viewing delay for splash screen in milliseconds")
parser.add_argument("--width",
                    type=int, dest="manual_width",
                    help="force specific resolution for testing")
parser.add_argument("--height",
                    type=int, dest="manual_height",
                    help="force specific resolution for testing")
parser.add_argument("--no-backgrounds",
                    action="store_true", dest="no_backgrounds", default=False,
                    help="turn off the background images")
parser.add_argument("--halos",
                    action="store_true", dest="halos", default=False,
                    help="show experimental target navigation halos")
parser.add_argument("--debug",
                    action="store_true", dest="debug", default=False,
                    help="display debugging data")
parser.add_argument("--ubertweak",
                    action="store_true", dest="ubertweak", default=False,
                    help="enable ubertweak modifications")
parser.add_argument("--sounds", dest="sounds", default="/usr/share/gytha/sounds",
                    help="path to sound effects")
