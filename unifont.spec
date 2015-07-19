Name:		unifont
Version:	8.0.01
Release:	2
License:	GPLv2+ and GFDL
Url:		https://savannah.gnu.org/projects/unifont
Summary:	Tools and glyph descriptions in a very simple text format
Group:		System/Fonts/True type
Source0:	http://ftp.gnu.org/gnu/%{name}/%{name}-%{version}/%{name}-%{version}.tar.gz
#Source1:	http://ftp.gnu.org/gnu/%{name}/%{name}-%{version}/%{name}-%{version}.ttf

BuildRequires:	pkgconfig(fontutil)
BuildRequires:	fontforge
BuildRequires:	fontpackages-devel
BuildRequires:	fontconfig
BuildRequires:	freetype-tools

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

%package -n fonts-ttf-%{name}
Summary:	GNU Unifont glyphs
BuildArch:	noarch

%description -n fonts-ttf-%{name}
GNU Unifont provides glyphs for every printable code point in the
Unicode 5.1 Basic Multilingual Plane (BMP).  The BMP occupies the
first 65,536 code points of the Unicode space, denoted as
U+0000..U+FFFF.

%prep
%setup -q
# Disable rebuilding during installation
sed -i 's/^install: .*/install:/' Makefile
sed -i 's/install -s/install/' src/Makefile

%build
# Makefile is broken with parallel builds
make CFLAGS='%{optflags}'
%make -C doc unifont.info

%install
%makeinstall_std USRDIR=%{_prefix} COMPRESS=0 TTFDEST='$(DESTDIR)%{_fontdir}/%{name}'
find %{buildroot}/usr/share/unifont/ -type f \! -name %{name}.hex -delete
install -p -m644 doc/unifont.info -D %{buildroot}%{_infodir}/unifont.info

mkdir -p %{buildroot}%{_datadir}/fonts/TTF/%{name}
mv %{buildroot}%{_fontdir}/%{name}/*.ttf %{buildroot}%{_datadir}/fonts/TTF/%{name}/
ttmkfdir %{buildroot}/%{_datadir}/fonts/TTF/%{name}  > %{buildroot}%{_datadir}/fonts/TTF/%{name}/fonts.dir
ln -s fonts.dir %{buildroot}%{_datadir}/fonts/TTF/%{name}/fonts.scale

mkdir -p %{buildroot}%{_sysconfdir}/X11/fontpath.d/
ln -s ../../..%{_datadir}/fonts/TTF/%{name} \
        %{buildroot}%{_sysconfdir}/X11/fontpath.d/ttf-%{name}:pri=50

%files
%{_bindir}/*
%{_datadir}/%{name}/
%doc NEWS README COPYING
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_infodir}/%{name}.info*

%files fonts
%{_datadir}/consolefonts/Unifont-APL8x16.psf.gz
%dir %{_fontbasedir}/X11/misc
%{_fontbasedir}/X11/misc/%{name}*.pcf.gz

%files -n fonts-ttf-%{name}
%dir %{_datadir}/fonts/TTF/%{name}
%{_datadir}/fonts/TTF/%{name}/*.ttf
%verify(not mtime) %{_datadir}/fonts/TTF/%{name}/fonts.dir
%{_datadir}/fonts/TTF/%{name}/fonts.scale
%{_sysconfdir}/X11/fontpath.d/ttf-%{name}:pri=50
