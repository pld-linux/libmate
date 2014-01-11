# NOTE: this package is deprecated, meant for MATE <= 1.4 compatibility only
#
# Conditional build:
%bcond_with	esd		# EsounD support (obsolete)
%bcond_with	static_libs	# static library
#
Summary:	MATE base library
Summary(pl.UTF-8):	Podstawowa biblioteka MATE
Name:		libmate
Version:	1.4.0
Release:	1
License:	LGPL v2+
Group:		Libraries
Source0:	http://pub.mate-desktop.org/releases/1.4/%{name}-%{version}.tar.xz
# Source0-md5:	12cbd0c29abf817501ce8c5233f5aa4e
Patch0:		%{name}-load-config.patch
Patch1:		%{name}-glib.patch
URL:		http://mate-desktop.org/
%{?with_esd:BuildRequires:	audiofile-devel >= 0.2.3}
BuildRequires:	autoconf >= 2.54
BuildRequires:	automake >= 1:1.9
BuildRequires:	docbook-dtd412-xml
%{?with_esd:BuildRequires:	esound-devel >= 0.2.26}
BuildRequires:	gettext-devel >= 0.10.40
BuildRequires:	glib2-devel >= 1:2.16.0
BuildRequires:	gtk-doc >= 1.0
BuildRequires:	intltool >= 0.40.0
BuildRequires:	libcanberra-devel
BuildRequires:	libmatecomponent-devel >= 1.1.0
BuildRequires:	libtool >= 1:1.4.3
BuildRequires:	mate-common
BuildRequires:	mate-conf-devel >= 1.1.0
BuildRequires:	mate-vfs-devel >= 1.1.0
BuildRequires:	perl-base >= 5
BuildRequires:	pkgconfig
BuildRequires:	popt-devel >= 1.5
BuildRequires:	rpmbuild(macros) >= 1.197
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires(post,preun):	mate-conf >= 1.1.0
Requires:	%{name}-libs = %{version}-%{release}
Requires:	mate-conf >= 1.1.0
Suggests:	mate-vfs >= 1.1.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define	mateconf_schema_install() \
	umask 022; \
	MATECONF_CONFIG_SOURCE="xml:readwrite:/etc/mateconf/mateconf.xml.defaults" /usr/bin/mateconftool-2 --makefile-install-rule /etc/mateconf/schemas/%{?1}%{!?1:*.schemas} > /dev/null ; \
	%{nil}

%define mateconf_schema_uninstall() \
	if [ $1 = 0 -a -x /usr/bin/mateconftool-2 ]; then \
		umask 022; \
		MATECONF_CONFIG_SOURCE="xml:readwrite:/etc/mateconf/mateconf.xml.defaults" /usr/bin/mateconftool-2 --makefile-uninstall-rule /etc/mateconf/schemas/%{?1} > /dev/null \
	fi ; \
	%{nil}

%description
libmate is the non-GUI part of base MATE libraries. It's a fork of
libgnome.

%description -l pl.UTF-8
libmate to nie związana z graficznym interfejsem użytkownika część
podstawowych bibliotek MATE. Jest to odgałęzienie libgnome.

%package libs
Summary:	Base libmate library and matecomponent modules
Summary(pl.UTF-8):	Podstawowa biblioteka libmate oraz moduły matecomponent
Group:		Libraries
Requires:	libmatecomponent >= 1.1.0
Requires:	mate-conf-libs >= 1.1.0
Requires:	mate-vfs-libs >= 1.1.0
Requires:	popt >= 1.5

%description libs
Base libmate library and matecomponent modules.

%description libs -l pl.UTF-8
Podstawowa biblioteka libmate oraz moduły matecomponent.

%package devel
Summary:	Headers for libmate
Summary(pl.UTF-8):	Pliki nagłówkowe libmate
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	libcanberra-devel
Requires:	libmatecomponent-devel >= 1.1.0
Requires:	mate-conf-devel >= 1.1.0
Requires:	mate-vfs-devel >= 1.1.0
Requires:	popt-devel >= 1.5

%description devel
This package includes the header files for libmate applications
development.

%description devel -l pl.UTF-8
Pliki nagłówkowe potrzebne do kompilowania programów korzystających z
libmate.

%package static
Summary:	Static libmate library
Summary(pl.UTF-8):	Statyczna biblioteka libmate
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static version of libmate library.

%description static -l pl.UTF-8
Statyczna wersja biblioteki libmate.

%package apidocs
Summary:	libmate API documentation
Summary(pl.UTF-8):	Dokumentacja API libmate
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
libmate API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API libmate.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__gtkdocize}
%{__glib_gettextize}
%{__intltoolize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	MATECONFTOOL=/usr/bin/mateconftool-2 \
	%{?with_esd:--enable-esd} \
	--enable-gtk-doc \
	--disable-schemas-install \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static} \
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
#export _POSIX2_VERSION=199209

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# no static modules and *.la for matecomponent modules
# libraries .la obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib*.la \
	$RPM_BUILD_ROOT%{_libdir}/matecomponent/monikers/*.la
%if %{with static_libs}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/matecomponent/monikers/*.a
%endif

%{__mv} $RPM_BUILD_ROOT%{_datadir}/locale/{sr@ije,sr@ijekavian}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%mateconf_schema_install desktop_mate_accessibility_keyboard.schemas
%mateconf_schema_install desktop_mate_accessibility_startup.schemas
%mateconf_schema_install desktop_mate_applications_at_mobility.schemas
%mateconf_schema_install desktop_mate_applications_at_visual.schemas
%mateconf_schema_install desktop_mate_applications_browser.schemas
%mateconf_schema_install desktop_mate_applications_office.schemas
%mateconf_schema_install desktop_mate_applications_terminal.schemas
%mateconf_schema_install desktop_mate_applications_window_manager.schemas
%mateconf_schema_install desktop_mate_background.schemas
%mateconf_schema_install desktop_mate_file_views.schemas
%mateconf_schema_install desktop_mate_interface.schemas
%mateconf_schema_install desktop_mate_lockdown.schemas
%mateconf_schema_install desktop_mate_peripherals_keyboard.schemas
%mateconf_schema_install desktop_mate_peripherals_mouse.schemas
%mateconf_schema_install desktop_mate_sound.schemas
%mateconf_schema_install desktop_mate_thumbnail_cache.schemas
%mateconf_schema_install desktop_mate_thumbnailers.schemas
%mateconf_schema_install desktop_mate_typing_break.schemas

%preun
%mateconf_schema_uninstall desktop_mate_accessibility_keyboard.schemas
%mateconf_schema_uninstall desktop_mate_accessibility_startup.schemas
%mateconf_schema_uninstall desktop_mate_applications_at_mobility.schemas
%mateconf_schema_uninstall desktop_mate_applications_at_visual.schemas
%mateconf_schema_uninstall desktop_mate_applications_browser.schemas
%mateconf_schema_uninstall desktop_mate_applications_office.schemas
%mateconf_schema_uninstall desktop_mate_applications_terminal.schemas
%mateconf_schema_uninstall desktop_mate_applications_window_manager.schemas
%mateconf_schema_uninstall desktop_mate_background.schemas
%mateconf_schema_uninstall desktop_mate_file_views.schemas
%mateconf_schema_uninstall desktop_mate_interface.schemas
%mateconf_schema_uninstall desktop_mate_lockdown.schemas
%mateconf_schema_uninstall desktop_mate_peripherals_keyboard.schemas
%mateconf_schema_uninstall desktop_mate_peripherals_mouse.schemas
%mateconf_schema_uninstall desktop_mate_sound.schemas
%mateconf_schema_uninstall desktop_mate_thumbnail_cache.schemas
%mateconf_schema_uninstall desktop_mate_thumbnailers.schemas
%mateconf_schema_uninstall desktop_mate_typing_break.schemas

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog MAINTAINERS NEWS README
%attr(755,root,root) %{_bindir}/mate-open
%dir %{_datadir}/mate-background-properties
%{_datadir}/mate-background-properties/mate-default.xml
%{_mandir}/man7/mate-options*
%{_sysconfdir}/mateconf/schemas/desktop_mate_accessibility_keyboard.schemas
%{_sysconfdir}/mateconf/schemas/desktop_mate_accessibility_startup.schemas
%{_sysconfdir}/mateconf/schemas/desktop_mate_applications_at_mobility.schemas
%{_sysconfdir}/mateconf/schemas/desktop_mate_applications_at_visual.schemas
%{_sysconfdir}/mateconf/schemas/desktop_mate_applications_browser.schemas
%{_sysconfdir}/mateconf/schemas/desktop_mate_applications_office.schemas
%{_sysconfdir}/mateconf/schemas/desktop_mate_applications_terminal.schemas
%{_sysconfdir}/mateconf/schemas/desktop_mate_applications_window_manager.schemas
%{_sysconfdir}/mateconf/schemas/desktop_mate_background.schemas
%{_sysconfdir}/mateconf/schemas/desktop_mate_file_views.schemas
%{_sysconfdir}/mateconf/schemas/desktop_mate_interface.schemas
%{_sysconfdir}/mateconf/schemas/desktop_mate_lockdown.schemas
%{_sysconfdir}/mateconf/schemas/desktop_mate_peripherals_keyboard.schemas
%{_sysconfdir}/mateconf/schemas/desktop_mate_peripherals_mouse.schemas
%{_sysconfdir}/mateconf/schemas/desktop_mate_sound.schemas
%{_sysconfdir}/mateconf/schemas/desktop_mate_thumbnail_cache.schemas
%{_sysconfdir}/mateconf/schemas/desktop_mate_thumbnailers.schemas
%{_sysconfdir}/mateconf/schemas/desktop_mate_typing_break.schemas
%dir %{_sysconfdir}/sound
%dir %{_sysconfdir}/sound/events
%{_sysconfdir}/sound/events/gtk2-mate-events.soundlist
%{_sysconfdir}/sound/events/mate.soundlist

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmate-2.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmate-2.so.0
%attr(755,root,root) %{_libdir}/matecomponent/monikers/libmoniker_extra_2.so
%{_libdir}/matecomponent/servers/MATE_Moniker_std.server

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmate-2.so
%{_includedir}/libmate-2.0
%{_pkgconfigdir}/libmate-2.0.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libmate-2.a
%endif

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/libmate
