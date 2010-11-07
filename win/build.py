from distutils.core import setup
import py2exe, pygame
import glob, shutil
import sys, os
import operator, fnmatch, zlib

data_files = [('images',
['images\\activity-stop.png',

'images\\close.png',

'images\\exp-00.png',

'images\\exp-01.png',

'images\\exp-02.png',

'images\\exp-03.png',

'images\\exp-04.png',

'images\\exp-05.png',

'images\\exp-06.png',

'images\\exp-07.png',

'images\\exp-08.png',

'images\\exp-09.png',

'images\\exp-10.png',

'images\\explosion.png',

'images\\fed-8x8.png',

'images\\fed-as-40x40.png',

'images\\fed-as.png',

'images\\fed-bb-40x40.png',

'images\\fed-bb.png',

'images\\fed-ca-40x40.png',

'images\\fed-ca.png',

'images\\fed-dd-40x40.png',

'images\\fed-dd.png',

'images\\fed-sb-40x40.png',

'images\\fed-sb.png',

'images\\fed-sc-40x40.png',

'images\\fed-sc.png',

'images\\go-previous.png',

'images\\help.png',

'images\\hubble-crab.jpg',

'images\\hubble-helix.jpg',

'images\\hubble-orion.jpg',

'images\\hubble-spire.jpg',

'images\\ind-8x8.png',

'images\\kli-8x8.png',

'images\\kli-as-40x40.png',

'images\\kli-as.png',

'images\\kli-bb-40x40.png',

'images\\kli-bb.png',

'images\\kli-ca-40x40.png',

'images\\kli-ca.png',

'images\\kli-dd-40x40.png',

'images\\kli-dd.png',

'images\\kli-sb-40x40.png',

'images\\kli-sb.png',

'images\\kli-sc-40x40.png',

'images\\kli-sc.png',

'images\\locator.png',

'images\\netrek.png',

'images\\ori-8x8.png',

'images\\ori-as-40x40.png',

'images\\ori-as.png',

'images\\ori-bb-40x40.png',

'images\\ori-bb.png',

'images\\ori-ca-40x40.png',

'images\\ori-ca.png',

'images\\ori-dd-40x40.png',

'images\\ori-dd.png',

'images\\ori-sb-40x40.png',

'images\\ori-sb.png',

'images\\ori-sc-40x40.png',

'images\\ori-sc.png',

'images\\planet-fed-30x30.png',

'images\\planet-fed.png',

'images\\planet-ind-30x30.png',

'images\\planet-ind.png',

'images\\planet-kli-30x30.png',

'images\\planet-kli.png',

'images\\planet-ori-30x30.png',

'images\\planet-ori.png',

'images\\planet-overlay-army.png',

'images\\planet-overlay-attack.png',

'images\\planet-overlay-fuel.png',

'images\\planet-overlay-lock.png',

'images\\planet-overlay-repair.png',

'images\\planet-rom-30x30.png',

'images\\planet-rom.png',

'images\\plasma-explode.png',

'images\\plasma-move.png',

'images\\ring-36x36.png',

'images\\rom-8x8.png',

'images\\rom-as-40x40.png',

'images\\rom-as.png',

'images\\rom-bb-40x40.png',

'images\\rom-bb.png',

'images\\rom-ca-40x40.png',

'images\\rom-ca.png',

'images\\rom-dd-40x40.png',

'images\\rom-dd.png',

'images\\rom-sb-40x40.png',

'images\\rom-sb.png',

'images\\rom-sc-40x40.png',

'images\\rom-sc.png',

'images\\servers-icon.png',

'images\\servers-player.png',

'images\\shield-80x80.png',

'images\\ship-cloak.png',

'images\\stars.png',

'images\\system-logout.png',

'images\\system-restart.png',

'images\\team-box-fed.png',

'images\\team-box-kli.png',

'images\\team-box-ori.png',

'images\\team-box-rom.png',

'images\\torp-det.png',

'images\\torp-explode-100.png',

'images\\torp-explode-120.png',

'images\\torp-explode-140.png',

'images\\torp-explode-160.png',

'images\\torp-explode-180.png',

'images\\torp-explode-20.png',

'images\\torp-explode-200.png',

'images\\torp-explode-40.png',

'images\\torp-explode-60.png',

'images\\torp-explode-80.png',

'images\\torp-explode.png',

'images\\torp-fed.png',

'images\\torp-ind.png',

'images\\torp-kli.png',

'images\\torp-me.png',

'images\\torp-off.png',

'images\\torp-ori.png',

'images\\torp-rom.png'])]

setup(
windows=[
         {
           "script": "start.py",
           "icon_resources": [(0, "gytha.ico")]
         }
         ],
data_files = data_files,
name='gytha',
version='0.3.1',
description='gytha - a netrek client',
author='James Cameron',
author_email='',
url='www.netrek.org',
      py_modules=['netrek\\__init__','netrek\\cache','netrek\\cap','netrek\\client','netrek\\constants','netrek\\mercenary','netrek\\meta','netrek\\rcd','netrek\\repair','netrek\\mis','netrek\\motd','netrek\\options','netrek\\util']
)

import zipfile
font = os.path.join(os.path.dirname(sys.executable), 'lib', 'site-packages', 'pygame', 'freesansbold.ttf')
zip = zipfile.ZipFile('dist/library.zip', 'a')
zip.write(font, 'pygame/freesansbold.ttf')
zip.close()