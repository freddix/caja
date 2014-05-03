Summary:	File manager for the MATE desktop environment
Name:		caja
Version:	1.8.1
Release:	1
License:	GPL v2+
Group:		X11/Applications
Source0:	http://pub.mate-desktop.org/releases/1.8/%{name}-%{version}.tar.xz
# Source0-md5:	e81bbec307c8aafd9663f4927f309ba4
URL:		http://wiki.mate-desktop.org/mate-file-manager
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	exempi-devel
BuildRequires:	freetype-devel
BuildRequires:	gettext-devel
BuildRequires:	mate-desktop-devel >= 1.8
BuildRequires:	intltool
BuildRequires:	libexif-devel
BuildRequires:	librsvg-devel
BuildRequires:	libtool
BuildRequires:	libunique-devel
BuildRequires:	libxml2-devel
BuildRequires:	pkg-config
BuildRequires:	startup-notification-devel
Requires(post,postun):	/usr/bin/gtk-update-icon-cache
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	hicolor-icon-theme
Requires(post,postun):	shared-mime-info
Requires(post,postun):	glib-gio-gsettings
Requires:	gdk-pixbuf-rsvg
Requires:	gvfs-fuse
Requires:	mate-desktop
Requires:	xdg-icon-theme
# for previewing audio files
Suggests:	gstreamer010
Suggests:	gstreamer010-plugins-base
Suggests:	gstreamer010-plugins-good
# useful gvfs backends
Suggests:	gvfs-archive
Suggests:	gvfs-cdio
Suggests:	gvfs-gphoto2
Suggests:	gvfs-mtp
Suggests:	gvfs-smb
Requires:	%{name}-libs = %{version}-%{release}
Provides:	mate-file-manager = %{version}-%{release}
Obsoletes:	mate-file-manager < %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir	%{_libdir}/caja

%description
Caja (mate-file-manager) is the file manager and graphical shell for
the MATE desktop, that makes it easy to manage your files and the rest
of your system. It allows to browse directories on local and remote
file systems, preview files and launch applications associated with
them. It is also responsible for handling the icons on the MATE
desktop.

%package libs
Summary:	Caja libraries
Group:		X11/Libraries
Provides:	mate-file-manager-libs = %{version}-%{release}
Obsoletes:	mate-file-manager-libs < %{version}-%{release}

%description libs
Caja libraries.

%package devel
Summary:	Libraries and include files for developing Caja components
Group:		X11/Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Provides:	mate-file-manager-devel = %{version}-%{release}
Obsoletes:	mate-file-manager-devel < %{version}-%{release}

%description devel
This package provides the necessary development libraries and include
files to allow you to develop Caja components.

%package apidocs
Summary:	libcaja-extension API documentation
Group:		Documentation
Requires:	gtk-doc-common
Provides:	mate-file-manager-apidocs = %{version}-%{release}
Obsoletes:	mate-file-manager-apidocs < %{version}-%{release}

%description apidocs
libcaja-extension API documentation.

%prep
%setup -q

%build
%{__gtkdocize}
%{__glib_gettextize}
%{__intltoolize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
%configure \
	--disable-introspection	\
	--disable-silent-rules	\
	--disable-static	\
	--disable-update-mimedb	\
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_datadir}/caja-extensions,%{_libdir}/caja/extensions-2.0}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_datadir}/MateConf/gsettings/*.convert
%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/locale/{ca@valencia,en@shaw,crh,ha,ig,io,ps}

%find_lang caja

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database
%update_gsettings_cache
%update_icon_cache hicolor
%update_mime_database

%postun
%update_desktop_database
%update_gsettings_cache
%update_icon_cache hicolor
%update_mime_database

%post	libs -p /usr/sbin/ldconfig
%postun libs -p /usr/sbin/ldconfig

%files -f caja.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog MAINTAINERS NEWS README THANKS
%attr(755,root,root) %{_bindir}/caja
%attr(755,root,root) %{_bindir}/caja-autorun-software
%attr(755,root,root) %{_bindir}/caja-connect-server
%attr(755,root,root) %{_bindir}/caja-file-management-properties
%attr(755,root,root) %{_libexecdir}/caja-convert-metadata

%dir %{_libdir}/caja/extensions-2.0
%dir %{_datadir}/caja-extensions
%{_datadir}/caja
%{_datadir}/glib-2.0/schemas/org.mate.*.gschema.xml
%{_datadir}/mime/packages/*.xml

%{_desktopdir}/caja-autorun-software.desktop
%{_desktopdir}/caja-browser.desktop
%{_desktopdir}/caja-computer.desktop
%{_desktopdir}/caja-file-management-properties.desktop
%{_desktopdir}/caja-folder-handler.desktop
%{_desktopdir}/caja-home.desktop
%{_desktopdir}/caja.desktop
%{_desktopdir}/mate-network-scheme.desktop
%{_pixmapsdir}/caja
%{_iconsdir}/hicolor/*/apps/caja.png
%{_iconsdir}/hicolor/*/apps/caja.svg
%{_iconsdir}/hicolor/*/emblems/*.png
%{_datadir}/dbus-1/services/org.mate.freedesktop.FileManager1.service

%{_mandir}/man1/caja*.1*

%files libs
%defattr(644,root,root,755)
%dir %{_libdir}/caja
%attr(755,root,root) %ghost %{_libdir}/libcaja-extension.so.?
%attr(755,root,root) %{_libdir}/libcaja-extension.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcaja-extension.so
%{_includedir}/caja
%{_pkgconfigdir}/libcaja-extension.pc

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/libcaja-extension

