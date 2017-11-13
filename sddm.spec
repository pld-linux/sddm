%define		qtver	5.6.0

Summary:	QML based X11 desktop manager
Name:		sddm
Version:	0.16.0
Release:	1
License:	GPLv2+ and CC-BY-SA
Group:		X11/Applications
Source0:	https://github.com/sddm/sddm/archive/v%{version}.tar.gz
# Source0-md5:	8d41b09ff9197b182b093af82e3958d5
Source10:	%{name}.pam
Source11:	%{name}-autologin.pam
Source12:	tmpfiles-%{name}.conf
# sample sddm.conf generated with sddm --example-config, and entries commented-out
Source13:	%{name}.conf
Source14:	Xsession
URL:		https://github.com/sddm/sddm
BuildRequires:	Qt5Core-devel >= %{qtver}
BuildRequires:	Qt5DBus-devel >= %{qtver}
BuildRequires:	Qt5Network-devel >= %{qtver}
BuildRequires:	Qt5Qml-devel >= %{qtver}
BuildRequires:	Qt5Quick-devel >= %{qtver}
BuildRequires:	Qt5Test-devel >= %{qtver}
BuildRequires:	cmake >= 2.8.8
BuildRequires:	docutils
BuildRequires:	kf5-extra-cmake-modules
BuildRequires:	libstdc++-devel
BuildRequires:	libxcb-devel
BuildRequires:	pam-devel
BuildRequires:	pkgconfig
BuildRequires:	python-docutils
BuildRequires:	qt5-build >= %{qtver}
BuildRequires:	qt5-linguist >= %{qtver}
BuildRequires:	qt5-qmake >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.202
BuildRequires:	systemd-devel
BuildRequires:	systemd-units
Provides:	XDM
Provides:	group(sddm)
Provides:	service(graphical-login) = sddm
Provides:	user(sddm)
Requires(post,preun,postun):	systemd-units >= 38
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires:	Qt5Core >= %{qtver}
Requires:	Qt5DBus >= %{qtver}
Requires:	Qt5Network >= %{qtver}
Requires:	Qt5Qml >= %{qtver}
Requires:	Qt5Quick >= %{qtver}
Requires:	systemd-units >= 38
Requires:	xinitrc-ng >= 1.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SDDM is a modern display manager for X11 aiming to be fast, simple and
beautiful. It uses modern technologies like QtQuick, which in turn
gives the designer the ability to create smooth, animated user
interfaces.

%prep
%setup -q

%build
install -d build
cd build
%cmake \
	-DBUILD_MAN_PAGES:BOOL=ON \
	-DENABLE_JOURNALD:BOOL=ON \
	-DUSE_QT5:BOOL=ON \
	..
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_localstatedir}/{lib,run}/sddm
%{__make} -C build install/fast \
	DESTDIR=$RPM_BUILD_ROOT

install -Dpm 644 %{SOURCE10} $RPM_BUILD_ROOT/etc/pam.d/sddm
install -Dpm 644 %{SOURCE11} $RPM_BUILD_ROOT/etc/pam.d/sddm-autologin
install -Dpm 644 %{SOURCE12} $RPM_BUILD_ROOT%{systemdtmpfilesdir}/sddm.conf
install -Dpm 644 %{SOURCE13} $RPM_BUILD_ROOT%{_sysconfdir}/sddm.conf
install -Dpm 644 %{SOURCE14} $RPM_BUILD_ROOT%{_datadir}/sddm/scripts/Xsession

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 323 -r -f sddm
%useradd -u 323 -r -d %{_localstatedir}/lib/sddm -s /bin/false -c "Simple Desktop Display Manager" -g sddm sddm

%preun
%systemd_preun sddm.service

%post
%systemd_post sddm.service

%postun
if [ "$1" = "0" ]; then
	%userremove sddm
	%groupremove sddm
fi
%systemd_reload

%files
%defattr(644,root,root,755)
%doc README.md CONTRIBUTORS
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/sddm.conf
%config(noreplace) %verify(not md5 mtime size) /etc/pam.d/sddm
%config(noreplace) %verify(not md5 mtime size) /etc/pam.d/sddm-autologin
%config(noreplace) %verify(not md5 mtime size) /etc/pam.d/sddm-greeter
# it's under %{_sysconfdir}, sure, but it's not a config file
/etc/dbus-1/system.d/org.freedesktop.DisplayManager.conf
%attr(755,root,root) %{_bindir}/sddm
%attr(755,root,root) %{_bindir}/sddm-greeter
%attr(755,root,root) %{_libexecdir}/sddm-helper
%{systemdtmpfilesdir}/sddm.conf
%attr(711, root, sddm) %dir %{_localstatedir}/run/sddm
%attr(1770, sddm, sddm) %dir %{_localstatedir}/lib/sddm
%{systemdunitdir}/sddm.service
%{_libdir}/qt5/qml/SddmComponents/
%dir %{_datadir}/sddm
%{_datadir}/sddm/faces
%{_datadir}/sddm/flags
%dir %{_datadir}/sddm/scripts
%attr(755,root,root) %{_datadir}/sddm/scripts/*
%{_datadir}/sddm/themes
%{_datadir}/sddm/translations
%{_mandir}/man1/sddm.1*
%{_mandir}/man1/sddm-greeter.1*
%{_mandir}/man5/sddm.conf.5*
%{_mandir}/man5/sddm-state.conf.5*
