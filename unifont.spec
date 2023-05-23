Name:		unifont
Version:	15.0.03
Release:	1
License:	GPLv2+ and GFDL
Url:		https://savannah.gnu.org/projects/unifont
Summary:	Tools and glyph descriptions in a very simple text format
Group:		System/Fonts/True type
Source0:	http://ftp.gnu.org/gnu/%{name}/%{name}-%{version}/%{name}-%{version}.tar.gz
Source1:	https://src.fedoraproject.org/rpms/unifont/raw/rawhide/f/unifont.metainfo.xml
BuildRequires:	pkgconfig(fontutil)
BuildRequires:	fontforge
BuildRequires:	fontpackages-devel
BuildRequires:	fontconfig
BuildRequires:	freetype-tools
BuildRequires:	texinfo
BuildRequires:	pkgconfig(libbsd)

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

%package	viewer
Summary:	Graphical viewer for unifont
BuildArch:	noarch

%description	viewer
A graphical viewer for unifont.

%package -n fonts-ttf-%{name}
Summary:	GNU Unifont glyphs
BuildArch:	noarch

%description -n fonts-ttf-%{name}
GNU Unifont provides glyphs for every printable code point in the
Unicode 5.1 Basic Multilingual Plane (BMP).  The BMP occupies the
first 65,536 code points of the Unicode space, denoted as
U+0000..U+FFFF.

%package -n fonts-otf-%{name}
Summary:	GNU Unifont glyphs
BuildArch:	noarch

%description -n fonts-otf-%{name}
GNU Unifont provides glyphs for every printable code point in the
Unicode 5.1 Basic Multilingual Plane (BMP).  The BMP occupies the
first 65,536 code points of the Unicode space, denoted as
U+0000..U+FFFF.

%prep
%autosetup -p1
# Disable rebuilding during installation
sed -i 's/^install: .*/install:/' Makefile
sed -i 's/install -s/install/' src/Makefile

%build
# Makefile is broken with parallel builds
%make_build -j1 CFLAGS="%{optflags} -lbsd" CC=%{__cc} LDFLAGS="%{build_ldflags} -lbsd" CONSOLEDEST=%{_prefix}/lib/kbd/consolefonts
%make_build -C doc unifont.info CC=%{__cc}

%install
%make_install USRDIR=%{_prefix} COMPRESS=0 TTFDEST='$(DESTDIR)%{_fontdir}/%{name}' CONSOLEDEST='$(DESTDIR)/%{_prefix}/lib/kbd/consolefonts'

find %{buildroot}/usr/share/unifont/ -type f \! -name %{name}.hex -delete
install -p -m644 doc/unifont.info -D %{buildroot}%{_infodir}/unifont.info
install -Dm0644 %{SOURCE1} %{buildroot}%{_datadir}/appdata/unifont.metainfo.xml

mkdir -p %{buildroot}%{_datadir}/fonts/TTF/%{name}
mv %{buildroot}%{_fontdir}/%{name}/*.ttf %{buildroot}%{_datadir}/fonts/TTF/%{name}/
ttmkfdir %{buildroot}/%{_datadir}/fonts/TTF/%{name}  > %{buildroot}%{_datadir}/fonts/TTF/%{name}/fonts.dir
ln -s fonts.dir %{buildroot}%{_datadir}/fonts/TTF/%{name}/fonts.scale

mkdir -p %{buildroot}%{_sysconfdir}/X11/fontpath.d/
ln -s ../../..%{_datadir}/fonts/TTF/%{name} \
	%{buildroot}%{_sysconfdir}/X11/fontpath.d/ttf-%{name}:pri=50

%files
%doc NEWS README COPYING
%{_bindir}/*
%{_datadir}/%{name}/
%doc %{_mandir}/man1/*
%doc %{_mandir}/man5/*
%doc %{_infodir}/%{name}.info*
%{_datadir}/appdata/%{name}.metainfo.xml
%exclude %{_bindir}/unifont-viewer

%files fonts
%{_prefix}/lib/kbd/consolefonts/Unifont-APL8x16.psf.gz
%dir %{_fontbasedir}/X11/misc
%{_fontbasedir}/X11/misc/%{name}*.pcf.gz

%files viewer
%{_bindir}/unifont-viewer

%files -n fonts-ttf-%{name}
%dir %{_datadir}/fonts/TTF/%{name}
%{_datadir}/fonts/TTF/%{name}/*.ttf
%verify(not mtime) %{_datadir}/fonts/TTF/%{name}/fonts.dir
%{_datadir}/fonts/TTF/%{name}/fonts.scale
%{_sysconfdir}/X11/fontpath.d/ttf-%{name}:pri=50

%files -n fonts-otf-%{name}
%{_datadir}/fonts/opentype/unifont
