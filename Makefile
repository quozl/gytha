PACKAGE=netrek-client-pygame
VERSION=0.5

all:
	@echo $(PACKAGE)-$(VERSION)
	echo "To start this Netrek client, run the file netrek-client-pygame"

clean:
	rm -rf debian/netrek-client-pygame/ build-stamp debian/files

distclean:

dist:
	mkdir $(PACKAGE)-$(VERSION)
	cp -p ChangeLog Makefile COPYING INSTALL $(PACKAGE)-$(VERSION)/
	mkdir $(PACKAGE)-$(VERSION)/images
	cp -p images/*.png images/*.jpg $(PACKAGE)-$(VERSION)/images/
	mkdir $(PACKAGE)-$(VERSION)/netrek
	cp -p netrek/*.py $(PACKAGE)-$(VERSION)/netrek
	cp -p netrek-client-pygame $(PACKAGE)-$(VERSION)/
	GZIP=--best tar cfz $(PACKAGE)-$(VERSION).tar.gz $(PACKAGE)-$(VERSION)
	rm -rf $(PACKAGE)-$(VERSION)

install:
	mkdir -p $(DESTDIR)/usr/bin/
	cp -p netrek-client-pygame $(DESTDIR)/usr/bin/
	chmod +x $(DESTDIR)/usr/bin/netrek-client-pygame
	mkdir -p $(DESTDIR)/usr/share/netrek-client-pygame/images
	cp -p images/*.png $(DESTDIR)/usr/share/netrek-client-pygame/images/
	chmod +r $(DESTDIR)/usr/share/netrek-client-pygame/images/*.png
	cp -p images/*.jpg $(DESTDIR)/usr/share/netrek-client-pygame/images/
	chmod +r $(DESTDIR)/usr/share/netrek-client-pygame/images/*.jpg
	mkdir -p $(DESTDIR)/usr/share/doc/netrek-client-pygame
	cp ChangeLog $(DESTDIR)/usr/share/doc/netrek-client-pygame

#
# Maintainer's Debian packaging section
#
DEBIAN_VERSION=$(shell head -1 debian/changelog|cut -f2 -d\(|cut -f1 -d\))
DEBIAN_PACKAGE=$(shell head -1 debian/changelog|cut -f1 -d\ )

package:
	fakeroot dpkg-buildpackage -us -uc

newpackage:
	python2.6 setup.py bdist_deb

TARGET=~/public_html/external/mine/netrek-client-pygame/
upload:
	cp $(PACKAGE)-$(VERSION).tar.gz $(TARGET)
	mv ../$(DEBIAN_PACKAGE)_$(DEBIAN_VERSION)*.deb $(TARGET)
	cp doc/index.phtml doc/*.jpg $(TARGET)

update:
	(cd $(TARGET);rm -f db;make)

release: dist package upload update
