Name:		unifont
Version:	6.3.20140214
Release:	1
License:	GPLv2+ and GFDL
Url:		https://savannah.gnu.org/projects/unifont
Summary:	Tools and glyph descriptions in a very simple text format
Group:		System/Fonts/True type
Source0:	http://ftp.gnu.org/gnu/%{name}/%{name}-%{version}/%{name}-%{version}.tar.gz

BuildRequires:	pkgconfig(fontutil)
BuildRequires:	fontforge
BuildRequires:	fontpackages-devel

%description
Unifont is a Unicode font with a glyph for every visible Unicode Basic
Multilingual Plane code point and more, with supporting utilities to
modify the font. This package contains tools and glyph descriptions.

%package	fonts
BuildArch:	noarch
Summary:	Unicode font with a glyph for every visible BMP code point
Requires:	fontpackages-filesystem

%description	fonts
Unifont is a fixed-width Unicode font with a glyph for every visible
Unicode Basic Multilingual Plane code point and more. The latest
version of Unifont includes approximately 54,700 glyphs for all the
visible Unicode BMP code points.

This font strives for very wide coverage rather than beauty, so use it
only as fallback or for special purposes.

%prep
%setup -q
# Disable rebuilding during installation
sed -i 's/^install: .*/install:/' Makefile
sed -i 's/install -s/install/' src/Makefile

%build
# Makefile is broken with parallel builds
%make CFLAGS='%{optflags}' || %make CFLAGS='%{optflags}'
%make -C doc unifont.info

%install
%makeinstall_std USRDIR=%{_prefix} COMPRESS=0 TTFDEST='$(DESTDIR)%{_fontdir}'
find %{buildroot}/usr/share/unifont/ -type f \! -name %{name}.hex -delete
install -p -m644 doc/unifont.info -D %{buildroot}%{_infodir}/unifont.info

%files
%{_bindir}/*
%{_datadir}/%{name}/
%doc NEWS README COPYING
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_infodir}/%{name}.info*

%files fonts
%{_datadir}/consolefonts/Unifont-APL8x16.psf.gz
%dir %{_fontdir}/
%{_fontdir}/%{name}*.ttf
%dir %{_fontbasedir}/X11/misc
%{_fontbasedir}/X11/misc/%{name}*.pcf.gz
