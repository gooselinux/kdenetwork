Summary: KDE Network Applications
Name: kdenetwork
Epoch: 7
Version: 4.3.4
Release: 11%{?dist}.1
License: GPLv2
Group: Applications/Internet
Url: http://www.kde.org
# Source0: ftp://ftp.kde.org/pub/kde/stable/%{version}/src/%{name}-%{version}.tar.bz2
# remove skype wrapper/icons because of trademark issue
Source0: kdenetwork-4.3.4-patched.tar.bz2
# part of oxygen-icons-theme
Source1: krdc-icons.tar.bz2
# consolehelper
Source2: kppp.console 
Source3: kppp.pam

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# add missing hicolor icons for kdrc
Patch1: kdenetwork-4.2.98-kdrc-icon.patch

# rhbz#540433 - KPPP is unable to add DNS entries to /etc/resolv.conf
Patch2: kdenetwork-4.3.3-resolv-conf-path.patch

# upstream patches (4.3 branch):
Patch100: kdenetwork-4.3.5.patch

# upstream patches (4.4 branch):
Patch200: kdenetwork-4.3.0-jabber-kde#111537.patch

## security patches
# rhbz#591967 -  CVE-2010-1000 CVE-2010-1511 kdenetwork: improper sanitization 
# of metalink attribute for downloading files
Patch300: kdenetwork-4.3.4-cve-2010-1000_1511.patch
Patch301: kdenetwork-4.3-CVE-2010-1000.patch

BuildRequires: boost-devel
BuildRequires: giflib-devel
BuildRequires: glib2-devel
BuildRequires: gmp-devel
BuildRequires: kdelibs4-devel >= %{version}
BuildRequires: kdelibs-experimental-devel >= %{version}
BuildRequires: kdepimlibs-devel >= %{version}
BuildRequires: libidn-devel
BuildRequires: libmsn-devel >= 4.0-0.4.beta2
BuildRequires: libvncserver-devel
BuildRequires: libxslt-devel libxml2-devel
BuildRequires: meanwhile-devel
BuildRequires: openldap-devel
BuildRequires: pcre-devel
BuildRequires: qca2-devel
BuildRequires: qimageblitz-devel
BuildRequires: soprano-devel >= 2.0.97
BuildRequires: speex-devel
BuildRequires: sqlite-devel
BuildRequires: libv4l-devel
BuildRequires: alsa-lib-devel
BuildRequires: sed

Requires: kdepimlibs%{?_isa} >= %{version}
Requires: %{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}

# kopete/yahoo
Requires(hint): jasper

# kopete/jabber
Requires(hint): qca-ossl

# kppp
Requires: ppp

# krdc
Requires(hint): rdesktop

# consolehelper
Requires: usermode-gtk

%description
Networking applications, including:
* kget: downloader manager
* kopete: chat client
* kppp: dialer and front end for pppd
* krdc: a client for Desktop Sharing and other VNC servers
* krfb: Desktop Sharing server, allow others to access your desktop via VNC

%package libs
Summary: Runtime libraries for %{name}
Group:   System Environment/Libraries

%description libs
%{summary}.

%package devel
Group:    Development/Libraries
Summary:  Development files for %{name}
Requires: %{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}
Requires: kdelibs4-devel

%description devel
%{summary}.


%prep
%setup -q -n %{name}-%{version}-patched -a 1

%patch1 -p1 -b .icon
%patch2 -p1 -b .resolv-conf-path

# 4.3 upstream patches
chmod +x kopete/kopete/kconf_update/kopete-update_yahoo_server.pl
%patch100 -p1 -b .kde435

# 4.4 upstream patches
%patch200 -p0 -b .bz#515586-kopete

# security patches
%patch300 -p0 -b .cve-2010-1000_1511
%patch301 -p1 -b .cve-2010-1000

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde4} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
rm -rf %{buildroot}

make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

# get rid of time stamp which causes multilib conflicts
sed -i -e 's!** Created:.*!** Created!' \
     %{buildroot}%{_kde4_includedir}/kopete/ui/ui_kopete*.h

# run kppp through consolehelper
mkdir -p %{buildroot}%{_sbindir} \
         %{buildroot}%{_sysconfdir}/security/console.apps \
         %{buildroot}%{_sysconfdir}/pam.d

chmod 0755 %{buildroot}%{_bindir}/kppp
mv %{buildroot}%{_bindir}/kppp %{buildroot}%{_sbindir}
ln -s consolehelper %{buildroot}%{_bindir}/kppp
install -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/security/console.apps/kppp
install -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/pam.d/kppp

%clean
rm -rf %{buildroot}


%post
touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null ||:
touch --no-create %{_kde4_iconsdir}/oxygen &> /dev/null ||:

%posttrans
gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &> /dev/null ||:
gtk-update-icon-cache %{_kde4_iconsdir}/oxygen &> /dev/null ||:
update-desktop-database -q &> /dev/null ||:

%postun
if [ $1 -eq 0 ] ; then
  touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null ||:
  touch --no-create %{_kde4_iconsdir}/oxygen &> /dev/null ||:
  gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &> /dev/null ||:
  gtk-update-icon-cache %{_kde4_iconsdir}/oxygen &> /dev/null ||:
  update-desktop-database -q &> /dev/null ||:
fi

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc COPYING README
%config(noreplace) %{_sysconfdir}/security/console.apps/kppp
%config(noreplace) %{_sysconfdir}/pam.d/kppp
%{_kde4_bindir}/*
%{_kde4_appsdir}/kconf_update/*
%{_kde4_appsdir}/kget/
%{_kde4_appsdir}/khtml/kpartplugins/kget_plug_in.rc
%{_kde4_appsdir}/kopete*
%{_kde4_appsdir}/kppp/
%{_kde4_appsdir}/krfb/
%{_kde4_appsdir}/krdc/
%{_kde4_appsdir}/remoteview/
%{_kde4_appsdir}/desktoptheme/default/widgets/kget.svg
%{_kde4_configdir}/kopeterc
%{_kde4_datadir}/applications/kde4/*
%{_kde4_datadir}/config.kcfg/*
%{_datadir}/dbus-1/interfaces/*
%{_kde4_datadir}/kde4/services/*
%{_kde4_datadir}/kde4/servicetypes/*
%{_kde4_datadir}/sounds/*
%{_kde4_docdir}/HTML/en/*/
%{_kde4_iconsdir}/hicolor/*/*/*
%{_kde4_iconsdir}/oxygen/*/*/*
%{_kde4_libdir}/kde4/*.so
%{_sbindir}/kppp

%files libs
%doc COPYING README
%defattr(-,root,root,-)
%{_kde4_libdir}/libqgroupwise.so
%{_kde4_libdir}/lib*.so.*

%files devel
%defattr(-,root,root,-)
%{_kde4_includedir}/kopete/
%{_kde4_includedir}/krdc/
%{_kde4_libdir}/lib*.so
%exclude %{_kde4_libdir}/libqgroupwise.so


%changelog
* Tue Apr 19 2011 Than Ngo <than@redhat.com> - 7:4.3.4-11.1
- CVE-2010-1000, improper sanitization of metalink attribute for downloading files

* Fri Jul 02 2010 Than Ngo <than@redhat.com> - 7:4.3.4-10
- Resolves: bz#606884, add missing COPYING in kdenetwork-libs

* Tue Jun 08 2010 Than Ngo <than@redhat.com> - 7:4.3.4-9
- Resolves: bz#587237, fix multilib conflicts

* Thu May 13 2010 Jaroslav Reznik <jreznik@redhat.com> - 7:4.3.4-8
- Resolves: #591967,
    CVE-2010-1000, CVE-2010-1511: improper sanitization of metalink 
    attribute

* Tue Mar 30 2010 Than Ngo <than@redhat.com> - 7:4.3.4-7
- rebuilt against qt 4.6.2

* Thu Mar 11 2010 Than Ngo <than@redhat.com> - 7:4.3.4-6
- drop skype wrapper because of trademark issue

* Wed Mar 10 2010 Than Ngo <than@redhat.com> 7:4.3.4-5
- drop skype wrapper

* Fri Jan 22 2010 Than Ngo <than@redhat.com> - 7:4.3.4-4
- backport 4.3.5 fixes

* Tue Dec 15 2009 Than Ngo <than@redhat.com> - 7:4.3.4-3
- drop BR ortp

* Sat Dec 12 2009 Than Ngo <than@redhat.com> - 4.3.4-2
- cleanup

* Tue Dec 01 2009 Than Ngo <than@redhat.com> - 4.3.4-1
- 4.3.4

* Mon Nov 23 2009 Jaroslav Reznik <jreznik@redhat.com> - 4.3.3-6
- KPPP fix to read resolv.conf from /var/run/ppp (#540433)

* Wed Nov 11 2009 Than Ngo <than@redhat.com> - 4.3.3-5
- rhel cleanup, drop BR on libotr-devel, openslp-devel, libgadu-devel

* Mon Nov 09 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.3-4
- BR: webkitpart-devel >= 0.0.2

* Mon Nov  9 2009 Lukáš Tinkl <ltinkl@redhat.com> - 4.3.3-3
- Compile with latest WebKitKDE

* Tue Nov 03 2009 Than Ngo <than@redhat.com> - 4.3.3-2
- respin

* Sat Oct 31 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.3-1
- 4.3.3

* Mon Oct 26 2009 Than Ngo <than@redhat.com> - 4.3.2-4
- rhel cleanup

* Fri Oct 09 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.3.2-3
- fix BR to be on kdelibs-experimental-devel, not kdelibs-experimental

* Wed Oct 07 2009 Than Ngo <than@redhat.com> - 4.3.2-2
- enable jingle

* Mon Oct 05 2009 Than Ngo <than@redhat.com> - 4.3.2-1
- 4.3.2

* Sun Sep 17 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.1-3
- %%?_isa'ize -libs deps
- BR: webkitpart-devel

* Mon Sep 14 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.1-2
- kopete/bonjour patch
- krfb produces garbled display (#523131, kde#162493)

* Fri Aug 28 2009 Than Ngo <than@redhat.com> - 4.3.1-1
- 4.3.1

* Mon Aug 24 2009 Than Ngo <than@redhat.com> - 4.3.0-2
- fix bz#515586, backport patch to fix this issue

* Thu Jul 30 2009 Than Ngo <than@redhat.com> - 4.3.0-1
- 4.3.0

* Wed Jul 22 2009 Than Ngo <than@redhat.com> - 4.2.98-1
- 4.3rc3

* Sat Jul 11 2009 Than Ngo <than@redhat.com> - 4.2.96-1
- 4.3rc2

* Fri Jun 26 2009 Than Ngo <than@redhat.com> - 4.2.95-1
- 4.3rc1

* Thu Jun 25 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.2.90-3
- BR: kdelibs-experimental

* Thu Jun 25 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.2.90-2
- implement YMSG 16 protocol to allow logging into Yahoo! again (upstream patch)

* Thu Jun 04 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.2.90-1
- KDE-4.3 beta2 (4.2.90)

* Wed May 13 2009 Lukáš Tinkl <ltinkl@redhat.com> - 4.2.85-1
- KDE 4.3 beta 1

* Wed Apr 01 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.2.2-2
- optimize scriptlets

* Tue Mar 31 2009 Lukáš Tinkl <ltinkl@redhat.com> - 4.2.2-1
- KDE 4.2.2

* Fri Feb 27 2009 Than Ngo <than@redhat.com> - 4.2.1-1
- 4.2.1

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7:4.2.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Feb 21 2009 Tejas Dinkar <tejas@gja.in> - 4.2.0-8
- Added patch to add View History to Kopete (backport from trunk)

* Tue Feb 17 2009 Lorenzo Villani <lvillani@binaryhelix.net> - 7:4.2.0-7
- Make GCC 4.4 happy (patch)

* Tue Feb 17 2009 Lorenzo Villani <lvillani@binaryhelix.net> - 7:4.2.0-6
- adjust patch level

* Tue Feb 17 2009 Lorenzo Villani <lvillani@binaryhelix.net> - 7:4.2.0-5
- KPPP Crash fix backported patch (KDE BZ: #176645 - BZ: #485890)

* Fri Feb 06 2009 Than Ngo <than@redhat.com> - 4.2.0-4
- fix yahoo protocol to show contact list correctly

* Wed Feb 04 2009 Jaroslav Reznik <jreznik@redhat.com> - 4.2.0-3
- port kopete video to libv4l (#475623)

* Mon Jan 26 2009 Jaroslav Reznik <jreznik@redhat.com> - 4.2.0-2
- fix kopete jabber protocol encrypted messages handling (#473412)

* Thu Jan 22 2009 Than Ngo <than@redhat.com> - 4.2.0-1
- 4.2.0

* Fri Jan 16 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.1.96-3
- rebuild for new OpenSSL

* Mon Jan 12 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.1.96-2
- build against system libgadu (trivial patch backported from 4.3)

* Wed Jan 07 2009 Than Ngo <than@redhat.com> - 4.1.96-1
- 4.2rc1

* Fri Dec 12 2008 Than Ngo <than@redhat.com> 4.1.85-1
- 4.2beta2
- BR: libmsn-devel

* Thu Dec 11 2008 Rex Dieter <rdieter@fedoraproject.org> 7:4.1.80-7
- Obsoletes/Provides: kopete-bonjour (#451302)

* Thu Dec 04 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 7:4.1.80-6
- rebuild for fixed kde-filesystem (macros.kde4) (get rid of rpaths)

* Thu Dec 04 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 7:4.1.80-5
- add missing BR meanwhile-devel (#474592)
- add missing BR ortp-devel and speex-devel (for Jingle protocol)

* Mon Dec 01 2008 Rex Dieter <rdieter@fedoraproject.org> 7:4.1.80-4
- fix up %%description
- versioned Obsoletes
- scriptlets fixes
- BR: plasma-devel

* Fri Nov 28 2008 Lorenzo Villani <lvillani@binaryhelix.net> 7:4.1.80-3
- fix build (updated file lists)

* Thu Nov 20 2008 Than Ngo <than@redhat.com> 4.1.80-2
- merged

* Thu Nov 20 2008 Lorenzo Villani <lvillani@binaryhelix.net> 7:4.1.72-1
- 4.1.80
- BR cmake 2.6
- make install/fast

* Wed Nov 12 2008 Than Ngo <than@redhat.com> 4.1.3-1
- 4.1.3

* Mon Oct 20 2008 Lukáš Tinkl <ltinkl@redhat.com> 4.1.2-3
- fix kopete crashes on logout (kdebug:172011), in the account editor
  (kdebug:172985) and during login (kdebug:172997)

* Mon Sep 29 2008 Rex Dieter <rdieter@fedoraproject.org> 4.1.2-2
- make VERBOSE=1
- respin against new(er) kde-filesystem

* Fri Sep 26 2008 Rex Dieter <rdieter@fedoraproject.org> 4.1.2-1
- 4.1.2

* Fri Aug 29 2008 Than Ngo <than@redhat.com> 4.1.1-1
- 4.1.1

* Fri Jul 25 2008 Than Ngo <than@redhat.com> 4.1.0-2
- respun

* Wed Jul 23 2008 Than Ngo <than@redhat.com> 4.1.0-1
- 4.1.0

* Fri Jul 18 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.99-1
- 4.0.99

* Fri Jul 11 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.98-1
- 4.0.98

* Sun Jul 06 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.85-1
- 4.0.85

* Fri Jun 27 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.84-1
- 4.0.84

* Thu Jun 19 2008 Than Ngo <than@redhat.com> 4.0.83-1
- 4.0.83 (beta2)

* Sun Jun 15 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.82-1
- 4.0.82

* Mon May 26 2008 Than Ngo <than@redhat.com> 4.0.80-1
- 4.1 beta1

* Wed May 07 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0.72-2
- add BR gmp-devel, libotr-devel, soprano-devel

* Wed May 07 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0.72-1
- update to 4.0.72
- drop backported kde#160728 patch
- update file list

* Thu Apr 17 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.3-6
- omit BR: xmms-devel, for now, save pulling in xmms-lib, gtk+ lib stack

* Sat Apr 12 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0.3-5
- fix segfault in krdc VNC on remote server disconnection (#442127, kde#160728)

* Thu Apr 03 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0.3-4
- rebuild (again) for the fixed %%{_kde4_buildtype}

* Mon Mar 31 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0.3-3
- rebuild for NDEBUG and _kde4_libexecdir
- drop libidn patch (fixed in libidn)

* Sat Mar 29 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0.3-2
- look for libidn in default path if pkgconfig lies (see #439549) (#439465)

* Fri Mar 28 2008 Than Ngo <than@redhat.com> 4.0.3-1
- 4.0.3
- drop kdenetwork-4.0.2-kopete-crash.patch, it's included in 4.0.3

* Tue Mar 18 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.2-3
- Requires(hint): qca-ossl (kopete/jabber)

* Thu Mar 13 2008 Than Ngo <than@redhat.com> 4.0.2-2
- apply upstream patch to fix crash in kopete

* Thu Feb 28 2008 Than Ngo <than@redhat.com> 4.0.2-1
- 4.0.2

* Fri Feb 01 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.1-2
- enable krfb, BR: libvncserver-devel

* Thu Jan 31 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.1-1
- kde-4.0.1

* Mon Jan 21 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.0-2
- BR: avahi-compat-libdns_sd-devel glib2-devel openslp-devel libxslt-devel xmms-devel

* Tue Jan 08 2008 Rex Dieter <rdieter[AT]fedoraproject.org> 4.0.0-1
- kde-4.0.0

* Fri Dec 14 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 3.97.0-5
- Obsoletes: -extras ...
- Requires: rdesktop (#420801), for krdc
- Requires: ppp , for kppp
- Requires: jasper , for kopete

* Wed Dec 12 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> 3.97.0-4
- rebuild for changed _kde4_includedir

* Fri Dec 07 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> 3.97.0-3
- BR: openldap-devel, it's needed in kopete

* Fri Dec 07 2007 Than Ngo <than@redhat.com> 3.97.0-2
- BR: qimageblitz-devel, it's needed in kopete

* Wed Dec 05 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 3.97.0-1
- kde-3.97.0

* Wed Dec 05 2007 Than Ngo <than@redhat.com> 3.96.2-2
- fix building kopete

* Sat Dec 01 2007 Sebastian Vahl <fedora@deadbabylon.de> 7:3.96.2-1
- kde-3.96.2

* Sat Nov 24 2007 Sebastian Vahl <fedora@deadbabylon.de> 7:3.96.1-1
- kde-3.96.1

* Sat Nov 17 2007 Sebastian Vahl <fedora@deadbabylon.de> 7:3.96.0-1
- Initial version for Fedora
