from setuptools import setup, find_packages
from pkg_resources import DistributionNotFound

import sys
import os

if sys.version_info < (2, 4):
    raise SystemExit("Python 2.4 or later is required")

setup(
    name="netrek-client-pygame",
    version="0.6",
    description= "Netrek, a multi-player real-time 2D strategy game.",
    author="James Cameron",
    author_email="quozl@us.netrek.org",
    license="GNU General Public License (GPL)",
    long_description="Your team starts with ten planets.  Each player flies a starship.  You shoot at enemy ships with torpedos and phasers.  You fly to, scan and bomb enemy planets to deny their use by the enemy team.  You protect your own planets by preventing the enemy from reaching them.  Once you make a kill, and don't die, you beam up armies from the planets you protected, and drop them on the enemy planets that have been bombed.  Your team wins when all the enemy planets are taken.  Your team loses if all your planets are taken from you.  Strategies include escorting, controlling space, and coordinated attacks.",
    keywords = "netrek client pygame",
    url = "http://quozl.linux.org.au/netrek-client-pygame/",
    download_url = "http://james.tooraweenah.com/darcs/netrek-client-pygame/",
    entry_points = {},
    py_modules=[],
    scripts=["netrek-client-pygame"],
    packages=["netrek"],
    install_requires = [
	'Pygame>=1.7.1',
    ],
    classifiers = [
            'Development Status :: 4 - Beta',
            'Environment :: MacOS X',
            'Environment :: X11 Applications',
            'Intended Audience :: End Users/Desktop',
            'License :: OSI Approved :: GNU General Public License (GPL)',
            'Natural Language :: English',
            'Operating System :: POSIX :: Linux',
            'Operating System :: MacOS :: MacOS X',
            'Operating System :: Microsoft :: Windows',
            'Operating System :: Microsoft :: Windows :: Windows 95/98/2000',
            'Operating System :: Microsoft :: Windows :: Windows NT/2000',
            'Programming Language :: Python',
            'Topic :: Games/Entertainment :: Arcade'
    ]
#
# FIXME: include graphics assets in sdist
# http://docs.python.org/release/2.5.2/dist/node12.html
#    package_dir = { 'netrek' : [ 'netrek', 'images' ] },
#    package_data = { 'netrek' : [ 'images/*.png', 'images/*.jpg' ] }
#
)
