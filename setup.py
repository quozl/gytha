from setuptools import setup, find_packages
from pkg_resources import DistributionNotFound

import sys
import os

if sys.version_info < (2, 4):
    raise SystemExit("Python 2.4 or later is required")

setup(
    name="netrek-client-pygame",
    version="0.3",
    description= "This is a client for the multi-player game of Netrek",
    author="James Cameron",
    author_email="quozl@us.netrek.org",
    license="GNU General Public License (GPL)",
    long_description="Netrek is the probably the first video game which can accurately be described as a sport.  It has more in common with basketball than with arcade games or Quake.  Its vast and expanding array of tactics and strategies allows for many different play styles; the best players are the ones who think fastest, not necessarily the ones who twitch most effectively.  It can be enjoyed as a twitch game, since the dogfighting system is extremely robust, but the things that really set Netrek apart from other video games are the team and strategic aspects.  Team play is dynamic and varied, with roles constantly changing as the game state changes.  Strategic play is explored in organized league games; after 6+ years of league play, strategies are still being invented and refined.",
    keywords = "netrek client pygame",
    url = "http://quozl.linux.org.au/netrek-client-pygame/",
    download_url = "http://james.tooraweenah.com/darcs/netrek-client-pygame/",
    entry_points = {},
    py_modules=[],
    packages=["netrek-client-pygame"],
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
)
