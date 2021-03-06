datarootdir = ${prefix}/share
srcdir=.


prefix=/usr/local
exec_prefix=${prefix}
bindir=${exec_prefix}/bin
mandir=${datarootdir}/man
INSTALLCMD=/usr/bin/install -c
PACKAGE_NAME=ccache-swig
# Soft link test can be skipped on systems that don't support soft linking
NOSOFTLINKSTEST=

CC=gcc
CFLAGS=-g -O2 -Wall -W -I.
SWIG=swig
SWIG_LIB=../$(srcdir)/../Lib
EXEEXT=

# Use standard autoconf approach to transform executable name using --program-prefix and --program-suffix
transform = s,x,x,

LIBS= 
OBJS= ccache.o mdfour.o hash.o execute.o util.o args.o stats.o \
	cleanup.o snprintf.o unify.o
HEADERS = ccache.h mdfour.h

all: $(PACKAGE_NAME)$(EXEEXT)

# Regenerate Makefile if Makefile.in or config.status have changed.
Makefile: $(srcdir)/Makefile.in ./config.status
	$(SHELL) ./config.status

# Note that HTML documentation is actually generated and used from the main SWIG documentation Makefile
docs: $(srcdir)/$(PACKAGE_NAME).1 $(srcdir)/web/ccache-man.html

$(PACKAGE_NAME)$(EXEEXT): $(OBJS) $(HEADERS)
	$(CC) $(CFLAGS) $(LDFLAGS) -o $@ $(OBJS) $(LIBS)

$(srcdir)/$(PACKAGE_NAME).1: $(srcdir)/ccache.yo
	-yodl2man -o $(srcdir)/$(PACKAGE_NAME).1 $(srcdir)/ccache.yo

$(srcdir)/web/ccache-man.html: $(srcdir)/ccache.yo
	yodl2html -o $(srcdir)/web/ccache-man.html $(srcdir)/ccache.yo

install: $(PACKAGE_NAME)$(EXEEXT)
	@echo "Installing $(PACKAGE_NAME)"
	@echo "Installing $(DESTDIR)${bindir}/`echo $(PACKAGE_NAME) | sed '$(transform)'`$(EXEEXT)"
	${INSTALLCMD} -d $(DESTDIR)${bindir}
	${INSTALLCMD} -m 755 $(PACKAGE_NAME)$(EXEEXT) $(DESTDIR)${bindir}/`echo $(PACKAGE_NAME) | sed '$(transform)'`$(EXEEXT)

install-docs: $(srcdir)/$(PACKAGE_NAME).1
	@echo "Installing $(DESTDIR)${mandir}/man1/`echo $(PACKAGE_NAME) | sed '$(transform)'`.1"
	${INSTALLCMD} -d $(DESTDIR)${mandir}/man1
	${INSTALLCMD} -m 644 $(srcdir)/$(PACKAGE_NAME).1 $(DESTDIR)${mandir}/man1/`echo $(PACKAGE_NAME) | sed '$(transform)'`.1

uninstall: $(PACKAGE_NAME)$(EXEEXT)
	rm -f $(DESTDIR)${bindir}/`echo $(PACKAGE_NAME) | sed '$(transform)'`$(EXEEXT)

uninstall-docs: $(srcdir)/$(PACKAGE_NAME).1
	rm -f $(DESTDIR)${mandir}/man1/`echo $(PACKAGE_NAME) | sed '$(transform)'`.1

clean:
	/bin/rm -f $(OBJS) *~ $(PACKAGE_NAME)$(EXEEXT)

test: test.sh
	SWIG_LIB='$(SWIG_LIB)' PATH=../..:$$PATH SWIG='$(SWIG)' CC='$(CC)' NOSOFTLINKSTEST='$(NOSOFTLINKSTEST)' $(srcdir)/test.sh

check: test

distclean: clean
	/bin/rm -f Makefile config.h config.sub config.log build-stamp config.status ccache_swig_config.h
	/bin/rm -rf autom4te.cache

maintainer-clean: distclean
	/bin/rm -f $(srcdir)/$(PACKAGE_NAME).1 $(srcdir)/web/ccache-man.html


# FIXME: To fix this, test.sh needs to be able to take ccache from the
# installed prefix, not from the source dir.
installcheck:
	@echo "WARNING!  This is not really \"installcheck\" yet."
	$(MAKE) check
