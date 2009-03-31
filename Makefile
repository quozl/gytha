PACKAGE=`head -1 debian/changelog|cut -f1 -d\ `
VERSION=`head -1 debian/changelog|cut -f2 -d\(|cut -f1 -d-`

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

package:
	fakeroot dpkg-buildpackage -us -uc

upload:
	cp $(PACKAGE)-$(VERSION).tar.gz ~/public_html/external/mine/netrek-client-pygame/
	mv ../$(PACKAGE)_$(VERSION)*.deb ~/public_html/external/mine/netrek-client-pygame/
	cp doc/index.phtml ~/public_html/external/mine/netrek-client-pygame/
	cp doc/*.{jpg,png,gif} ~/public_html/external/mine/netrek-client-pygame/

update:
	(cd ~/public_html/external/mine/netrek-client-pygame/;rm -f db;make)

release: dist package upload update
