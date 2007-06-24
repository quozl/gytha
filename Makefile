PACKAGE=netrek-client-pygame
VERSION=0.1

all: 

clean:

distclean:

dist:
	mkdir $(PACKAGE)-$(VERSION)
	mkdir $(PACKAGE)-$(VERSION)/images
	cp -p netrek.py Makefile COPYING $(PACKAGE)-$(VERSION)/
	cp -p ChangeLog $(PACKAGE)-$(VERSION)/
	cp -p images/*.png $(PACKAGE)-$(VERSION)/images/
	GZIP=--best tar cfz $(PACKAGE)-$(VERSION).tar.gz $(PACKAGE)-$(VERSION)
	rm -rf $(PACKAGE)-$(VERSION)

install:
	mkdir -p $(DESTDIR)/usr/bin/
	cp -p netrek.py $(DESTDIR)/usr/bin/netrek-client-pygame
	chmod +x $(DESTDIR)/usr/bin/netrek-client-pygame
	mkdir -p $(DESTDIR)/usr/share/netrek-client-pygame/images
	cp -p images/*.png $(DESTDIR)/usr/share/netrek-client-pygame/images/
	chmod +r $(DESTDIR)/usr/share/netrek-client-pygame/images/*.png
	mkdir -p $(DESTDIR)/usr/share/doc/netrek-client-pygame
	cp ChangeLog $(DESTDIR)/usr/share/doc/netrek-client-pygame
