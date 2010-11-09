PACKAGE=gytha
VERSION=0.7

all:
	@echo $(PACKAGE)-$(VERSION)
	echo "To start this Netrek client, run the file gytha.py"

clean:
	rm -rf debian/gytha build-stamp debian/files

distclean:

dist:
	mkdir $(PACKAGE)-$(VERSION)
	cp -p ChangeLog Makefile COPYING INSTALL $(PACKAGE)-$(VERSION)/
	cp -p gytha.png gytha.desktop $(PACKAGE)-$(VERSION)/
	mkdir $(PACKAGE)-$(VERSION)/images
	cp -p images/*.png $(PACKAGE)-$(VERSION)/images/
	cp -p images/*.jpg $(PACKAGE)-$(VERSION)/images/
	mkdir $(PACKAGE)-$(VERSION)/netrek
	cp -p netrek/*.py $(PACKAGE)-$(VERSION)/netrek
	cp -p gytha.py $(PACKAGE)-$(VERSION)/
	GZIP=--best tar cfz $(PACKAGE)-$(VERSION).tar.gz $(PACKAGE)-$(VERSION)
	rm -rf $(PACKAGE)-$(VERSION)

install:
	mkdir -p $(DESTDIR)/usr/bin/
	cp -p gytha.py $(DESTDIR)/usr/games/gytha
	chmod +x $(DESTDIR)/usr/games/gytha
	mkdir -p $(DESTDIR)/usr/share/gytha/images
	cp -p gytha.png $(DESTDIR)/usr/share/gytha/
	chmod +r $(DESTDIR)/usr/share/gytha/gytha.png
	cp -p images/*.png $(DESTDIR)/usr/share/gytha/images/
	chmod +r $(DESTDIR)/usr/share/gytha/images/*.png
	cp -p images/*.jpg $(DESTDIR)/usr/share/gytha/images/
	chmod +r $(DESTDIR)/usr/share/gytha/images/*.jpg
	mkdir -p $(DESTDIR)/usr/share/doc/gytha
	cp ChangeLog $(DESTDIR)/usr/share/doc/gytha

#
# Maintainer's Debian packaging section
#
DEBIAN_VERSION=$(shell head -1 debian/changelog|cut -f2 -d\(|cut -f1 -d\))
DEBIAN_PACKAGE=$(shell head -1 debian/changelog|cut -f1 -d\ )

package:
	fakeroot dpkg-buildpackage -us -uc

newpackage:
	python2.6 setup.py bdist_deb

TARGET=~/public_html/external/mine/gytha/
upload:
	cp $(PACKAGE)-$(VERSION).tar.gz $(TARGET)
	mv ../$(DEBIAN_PACKAGE)_$(DEBIAN_VERSION)*.deb $(TARGET)
	cp doc/index.phtml doc/*.jpg $(TARGET)

update:
	(cd $(TARGET);rm -f db;make)

release: dist package upload update
