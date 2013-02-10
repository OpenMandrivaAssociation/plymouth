%define plymouthdaemon_execdir /sbin
%define plymouthclient_execdir /bin
%define plymouth_libdir /%{_lib}

%define _libexecdir %{_prefix}/libexec

%define major 2
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

%define snapshot 0

%bcond_with uclibc

Summary:	Graphical Boot Animation and Logger
Name:		plymouth
Version:	0.8.8
Release:	4
License:	GPLv2+
Group:		System/Kernel and hardware
Url:		http://www.freedesktop.org/wiki/Software/Plymouth
Source0:	http://www.freedesktop.org/software/plymouth/releases/%{name}-%{version}.tar.bz2
Source1:	boot-duration
Source2:	charge.plymouth
# PATCH-OPENSUSE -- Restore suspend / resume state (needed for suspend package)
Patch0:		plymouth-restore-suspend.patch
# PATCH-OPENSUSE -- Change udevadm path
Patch1:		plymouth-0.8.6.1-udevadm-path.patch
# PATCH-OPENSUSE -- Handle correctly multiple displays with different sizes
Patch4:		plymouth-fix-window-size
# PATCH-OPENSUSE -- Add line numbers to tracing output
Patch6:		plymouth-trace-lines
Patch8:		plymouth-0.8.6.1.mkinitrd-to-dracut.patch
Patch9:		plymouth-0.8.8-fix-path-to-pid-files.patch

#BuildRequires:	gtk2-devel
#BuildRequires:	libdrm-devel
%if %{with uclibc}
BuildRequires:	uClibc-devel
BuildRequires:	libpng-static-devel
%endif
BuildRequires:	systemd-units
%rename		splashy
Requires(post):	plymouth-scripts = %{version}-%{release}
Requires:	initscripts >= 8.83
Requires(post):	dracut
Requires:	desktop-common-data >= 2010.0-1mdv
Conflicts:	systemd-units < 186

%description
Plymouth provides an attractive graphical boot animation in
place of the text messages that normally get shown.  Text
messages are instead redirected to a log file for viewing
after boot.

%package system-theme
Group:		System/Kernel and hardware
Summary:	Plymouth default theme
Requires:	plymouth(system-theme)
Requires:	plymouth = %{version}-%{release}

%description system-theme
This metapackage tracks the current distribution default theme.

%package -n %{libname}
Summary:	Plymouth libraries
Group:		System/Libraries
Obsoletes:	%{mklibname %{name} 0} < 0.8.0

%description -n %{libname}
This package contains the libply and libplybootsplash libraries
used by Plymouth.

%package -n %{develname}
Group:		System/Kernel and hardware
Summary:	Libraries and headers for writing Plymouth splash plugins
Group:		Development/C
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}

%description -n %{develname}
This package contains the libply and libplybootsplash libraries
and headers needed to develop 3rd party splash plugins for Plymouth.

%package utils
Group:		System/Kernel and hardware
Summary:	Plymouth related utilities
Requires:	%{name} = %{version}-%{release}

%description utils
This package contains utilities that integrate with Plymouth
including a boot log viewing application.

%package scripts
Group:		System/Kernel and hardware
Summary:	Plymouth related scripts
Conflicts:	mkinitrd < 6.0.92-6mdv
Requires:	plymouth = %{version}-%{release}

%description scripts
This package contains scripts that help integrate Plymouth with
the system.

%package plugin-label
Group:		System/Kernel and hardware
Summary:	Plymouth label plugin
Requires:	%{libname} = %{version}-%{release}

%description plugin-label
This package contains the label control plugin for
Plymouth. It provides the ability to render text on
graphical boot splashes using pango and cairo.

%package plugin-fade-throbber
Group:		System/Kernel and hardware
Summary:	Plymouth "Fade-Throbber" plugin
Requires:	%{libname} = %{version}-%{release}

%description plugin-fade-throbber
This package contains the "Fade-In" boot splash plugin for
Plymouth. It features a centered image that fades in and out
while other images pulsate around during system boot up.

%package plugin-script
Group:		System/Kernel and hardware
Summary:	Plymouth "Script" plugin
Requires:	%{libname} = %{version}-%{release}
Requires:	plymouth-plugin-label = %{version}-%{release}

%description plugin-script
This package contains the "Script" plugin for Plymouth. 

%package theme-script
Group:		System/Kernel and hardware
Summary:	Plymouth "Script" theme
Requires:	%{name}-plugin-script = %{version}-%{release}
Requires(post):	plymouth-scripts = %{version}-%{release}

%description theme-script
This package contains the "Script" boot splash theme for
Plymouth. 

%package theme-fade-in
Group:		System/Kernel and hardware
Summary:	Plymouth "Fade-In" theme
Requires:	%{name}-plugin-fade-throbber = %{version}-%{release}
Requires(post):	plymouth-scripts = %{version}-%{release}

%description theme-fade-in
This package contains the "Fade-In" boot splash theme for
Plymouth. It features a centered logo that fades in and out
while stars twinkle around the logo during system boot up.

%package plugin-throbgress
Group:		System/Kernel and hardware
Summary:	Plymouth "Throbgress" plugin
Requires:	%{libname} = %{version}-%{release}
Requires:	plymouth-plugin-label = %{version}-%{release}

%description plugin-throbgress
This package contains the "throbgress" boot splash plugin for
Plymouth. It features a centered logo and animated spinner that
spins repeatedly while a progress bar advances at the bottom of
the screen.

%package theme-spinfinity
Group:		System/Kernel and hardware
Summary:	Plymouth "Spinfinity" theme
Requires:	%{name}-plugin-throbgress = %{version}-%{release}
Requires(post):	plymouth-scripts = %{version}-%{release}

%description theme-spinfinity
This package contains the "Spinfinity" boot splash theme for
Plymouth. It features a centered logo and animated spinner that
spins in the shape of an infinity sign.

%package theme-spinner
Group: System/Kernel and hardware
Summary: Plymouth "Spinner" theme
Requires: %{name}-plugin-two-step = %{version}-%{release}
Requires(post): plymouth-scripts = %{version}-%{release}

%description theme-spinner
This package contains the "Spinner" boot splash theme for
Plymouth.

%package plugin-space-flares
Group:		System/Kernel and hardware
Summary:	Plymouth "space-flares" plugin
Requires:	%{libname} = %{version}-%{release}
Requires:	plymouth-plugin-label = %{version}-%{release}

%description plugin-space-flares
This package contains the "space-flares" boot splash plugin for
Plymouth. It features a corner image with animated flares.

%package theme-solar
Group:		System/Kernel and hardware
Summary:	Plymouth "Solar" theme
Requires:	%{name}-plugin-space-flares = %{version}-%{release}
Requires(post):	plymouth-scripts = %{version}-%{release}

%description theme-solar
This package contains the "Solar" boot splash theme for
Plymouth. It features a blue flamed sun with animated solar flares.

%package plugin-two-step
Group:		System/Kernel and hardware
Summary:	Plymouth "two-step" plugin
Requires:	%{libname} = %{version}-%{release}
Requires:	plymouth-plugin-label = %{version}-%{release}

%description plugin-two-step
This package contains the "two-step" boot splash plugin for
Plymouth. It features a two phased boot process that starts with
a progressing animation synced to boot time and finishes with a
short, fast one-shot animation.

%package theme-charge
Group:		System/Kernel and hardware
Summary:	Plymouth "Charge" plugin
Requires:	%{name}-plugin-two-step = %{version}-%{release}
Requires(post):	plymouth-scripts = %{version}-%{release}

%description theme-charge
This package contains the "charge" boot splash theme for
Plymouth. It features the shadowy hull of a logo charge up and
and finally burst into full form.

%package theme-glow
Group:		System/Kernel and hardware
Summary:	Plymouth "Glow" plugin
Requires(post):	plymouth-scripts  = %{version}-%{release}
Requires:	plymouth-plugin-two-step = %{version}-%{release}

%description theme-glow
This package contains the "Glow" boot splash theme for Plymouth.

%prep
%setup -q
%patch0 -p1 -b .suspend~
%patch1 -p1 -b .udevadm~
%patch4 -p1 -b .window_size~
%patch6 -p1 -b .trace_lines~
%patch8 -p1
%patch9 -p1 -b .pid

%if %{snapshot}
sh ./autogen.sh
make distclean
%endif

%build
libtoolize --copy --force
autoreconf -fi
export CONFIGURE_TOP=`pwd`
%if %{with uclibc}
mkdir -p uclibc
pushd uclibc
%configure CC="%{uclibc_cc}" \
	CFLAGS="%{uclibc_cflags}" \
	LDFLAGS="%{ldflags} -lz" \
	--prefix=%{uclibc_root}%{_prefix} \
	--libdir="%{uclibc_root}%{_libdir}" \
	--bindir="%{uclibc_root}%{plymouthclient_execdir}" \
	--sbindir="%{uclibc_root}%{plymouthdaemon_execdir}" \
	--enable-tracing \
	--disable-tests \
	--with-logo=%{_datadir}/icons/large/mandriva.png \
	--with-background-start-color-stop=0x0073B3 \
	--with-background-end-color-stop=0x00457E \
	--with-background-color=0x3391cd \
	--disable-gdm-transition \
	--without-gdm-autostart-file \
	--without-rhgb-compat-link \
	--with-system-root-install \
	--enable-systemd-integration \
	--enable-pango \
%ifnarch %{ix86} x86_64
	--disable-libdrm_intel \
%endif
	--enable-libkms \
%if %mdvver >= 201200
	--with-release-file=/etc/os-release \
%else
	--with-release-file=/etc/mandriva-release \
%endif
	--with-log-viewer

# We don't build these for uclibc since they link against a lot of libraries
# that we don't provide any uclibc linked version of
sed -e 's#viewer##g' -i src/Makefile
sed -e 's#label##g' -i src/plugins/controls/Makefile
%make
popd
%endif

mkdir -p system
pushd system
%configure2_5x \
	--disable-static \
	--enable-tracing \
	--disable-tests \
	--with-logo=%{_datadir}/icons/large/mandriva.png \
	--with-background-start-color-stop=0x0073B3 \
	--with-background-end-color-stop=0x00457E \
	--with-background-color=0x3391cd \
	--disable-gdm-transition \
	--without-gdm-autostart-file \
	--without-rhgb-compat-link \
	--with-system-root-install \
	--enable-systemd-integration \
	--enable-pango \
%ifnarch %{ix86} x86_64
	--disable-libdrm_intel \
%endif
	--enable-libkms \
%if %mdvver >= 201200
	--with-release-file=/etc/os-release \
%else
	--with-release-file=/etc/mandriva-release \
%endif
	--with-log-viewer


%make
popd

%install

%if %{with uclibc}
%makeinstall_std -C uclibc plymouthdaemondir=%{uclibc_root}%{plymouthdaemon_execdir} plymouthclientdir=%{uclibc_root}%{plymouthclient_execdir}
rm -rf %{buildroot}%{uclibc_root}{%{_includedir},%{_datadir},%{_libdir}/pkgconfig,%{_libexecdir},%{plymouthdaemon_execdir}/plymouth-set-default-theme}
%endif
%makeinstall_std -C system

# Temporary symlink until rc.sysinit is fixed
(cd %{buildroot}%{_bindir}; ln -s ../../bin/plymouth)
touch %{buildroot}%{_datadir}/plymouth/themes/default.plymouth

mkdir -p %{buildroot}%{_localstatedir}/lib/plymouth
cp %{SOURCE1} %{buildroot}%{_datadir}/plymouth/default-boot-duration
touch %{buildroot}%{_localstatedir}/lib/plymouth/{boot,shutdown}-duration

# Add charge
mkdir -p %{buildroot}%{_datadir}/plymouth/themes/charge
cp %{SOURCE2} %{buildroot}%{_datadir}/plymouth/themes/charge
cp %{buildroot}%{_datadir}/plymouth/themes/glow/{box,bullet,entry,lock}.png %{buildroot}%{_datadir}/plymouth/themes/charge

find %{buildroot} -name \*.a -delete -o -name \*.la -delete

%post
[ -f %{_localstatedir}/lib/plymouth/boot-duration ] || cp -f %{_datadir}/plymouth/default-boot-duration %{_localstatedir}/lib/plymouth/boot-duration
if [ "x$DURING_INSTALL" = "x" ]; then
  if [ $1 -eq 1 ]; then
   %{_libexecdir}/plymouth/plymouth-update-initrd
  fi
fi


%postun
if [ $1 -eq 0 ]; then
    rm -f %{_libdir}/plymouth/default.so
fi

%define theme_scripts() \
%post -n %{name}-theme-%{1} \
if [ -x %{_sbindir}/plymouth-set-default-theme ]; then \
  export LIB=%{_lib} \
  if [ $1 -eq 1 ]; then \
      %{_sbindir}/plymouth-set-default-theme --rebuild-initrd %{1} \
  else \
      THEME=$(%{_sbindir}/plymouth-set-default-theme) \
      if [ "$THEME" == "text" -o "$THEME" == "%{1}" ]; then \
          %{_sbindir}/plymouth-set-default-theme --rebuild-initrd %{1} \
      fi \
  fi \
fi \
\
%postun -n %{name}-theme-%{1} \
export LIB=%{_lib} \
if [ $1 -eq 0 -a -x %{_sbindir}/plymouth-set-default-theme ]; then \
    if [ "$(%{_sbindir}/plymouth-set-default-theme)" == "%{1}" ]; then \
        %{_sbindir}/plymouth-set-default-theme --reset --rebuild-initrd \
    fi \
fi \


%theme_scripts spinfinity
%theme_scripts fade-in
%theme_scripts solar
%theme_scripts charge
%theme_scripts glow
%theme_scripts script

%files
%doc AUTHORS NEWS README
%config(noreplace) %{_sysconfdir}/plymouth
%dir %{_datadir}/plymouth
%dir %{_datadir}/plymouth/themes
%dir %{_libdir}/plymouth
%{_datadir}/plymouth/default-boot-duration
%dir %{_localstatedir}/lib/plymouth
%{plymouthdaemon_execdir}/plymouthd
%{plymouthclient_execdir}/plymouth
%{_bindir}/plymouth
%{_libdir}/plymouth/details.so
%{_libdir}/plymouth/text.so
/lib/systemd/system/*plymouth*.service
/lib/systemd/system/systemd-*.path
/lib/systemd/system/*.wants/plymouth-*.service
%dir %{_libdir}/plymouth/renderers
%{_libdir}/plymouth/renderers/drm*
%{_libdir}/plymouth/renderers/frame-buffer*
%ghost %{_datadir}/plymouth/themes/default.plymouth
%{_datadir}/plymouth/plymouthd.defaults
%{_datadir}/plymouth/themes/details
%{_datadir}/plymouth/themes/text
%{_localstatedir}/run/plymouth
%{_localstatedir}/spool/plymouth
%ghost %{_localstatedir}/lib/plymouth/shutdown-duration
%ghost %{_localstatedir}/lib/plymouth/boot-duration
%{_mandir}/man8/*
%if %{with uclibc}
%{uclibc_root}%{plymouthdaemon_execdir}/plymouthd
%{uclibc_root}%{plymouthclient_execdir}/plymouth
%{uclibc_root}%{_libdir}/plymouth/details.so
%{uclibc_root}%{_libdir}/plymouth/text.so
%endif

%files -n %{develname}
%{plymouth_libdir}/libply.so
%{_libdir}/libply-boot-client.so
%{_libdir}/libply-splash-graphics.so
%{_libdir}/plymouth/renderers/x11*
/%{_lib}/libply-splash-core.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/plymouth-1

%files -n %{libname}
%{plymouth_libdir}/libply.so.%{major}*
%{_libdir}/libply-boot-client.so.%{major}*
%{_libdir}/libply-splash-graphics.so.%{major}*
/%{_lib}/libply-splash-core.so.%{major}*
%if %{with uclibc}
%dir %{uclibc_root}%{_libdir}/plymouth
%{uclibc_root}%{plymouth_libdir}/libply.so*
%{uclibc_root}%{_libdir}/libply-boot-client.so*
%{uclibc_root}%{_libdir}/libply-splash-graphics.so*
%endif

%files scripts
%{_sbindir}/plymouth-set-default-theme
%{_libexecdir}/plymouth

%files utils
%{_bindir}/plymouth-log-viewer

%files plugin-label
%{_libdir}/plymouth/label.so

%files plugin-fade-throbber
%{_libdir}/plymouth/fade-throbber.so
%if %{with uclibc}
%{uclibc_root}%{_libdir}/plymouth/fade-throbber.so
%endif

%files theme-fade-in
%{_datadir}/plymouth/themes/fade-in

%files plugin-throbgress
%{_libdir}/plymouth/throbgress.so
%if %{with uclibc}
%{uclibc_root}%{_libdir}/plymouth/throbgress.so
%endif

%files plugin-script
%{_libdir}/plymouth/script.so
%if %{with uclibc}
%{uclibc_root}%{_libdir}/plymouth/script.so
%endif

%files theme-script
%{_datadir}/plymouth/themes/script

%files theme-spinfinity
%{_datadir}/plymouth/themes/spinfinity

%files theme-spinner
%{_datadir}/plymouth/themes/spinner

%files plugin-space-flares
%{_libdir}/plymouth/space-flares.so
%if %{with uclibc}
%{uclibc_root}%{_libdir}/plymouth/space-flares.so
%endif

%files theme-solar
%{_datadir}/plymouth/themes/solar

%files plugin-two-step
%{_libdir}/plymouth/two-step.so
%if %{with uclibc}
%{uclibc_root}%{_libdir}/plymouth/two-step.so
%endif

%files theme-charge
%{_datadir}/plymouth/themes/charge

%files theme-glow
%{_datadir}/plymouth/themes/glow

%files system-theme



%changelog
* Mon Aug 13 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 0.8.6.1-2
+ Revision: 814660
- add line numbers to tracing output (P6, from OpenSuSE)
- recognize quotes often used in sysconfig-style files (P5, from OpenSuSE)
- handle correctly multiple displays with different sizes (P4, from OpenSuSE)
- work around issue with dashes and semicolons in systemd service (P3)
- create targets for plymouth systemd services
- fix path to udevadm (P1)
- Restore suspend / resume state (needed for suspend package)

* Mon Jul 16 2012 Tomasz Pawel Gajc <tpg@mandriva.org> 0.8.6.1-1
+ Revision: 809930
- update to new version 0.8.6.1
- drop patches 1,2 and 3
- default realease file is set to /etc/os-release
- package services

* Sun Jul 08 2012 Tomasz Pawel Gajc <tpg@mandriva.org> 0.8.5.1-2
+ Revision: 808501
- add conflicts on systemd-units < 186
- add two patches from upstream git, which clean up udev mess
- symlink plymouth services into systemd target wants

* Sun Jul 08 2012 Tomasz Pawel Gajc <tpg@mandriva.org> 0.8.5.1-1
+ Revision: 808476
- update to new version 0.8.5.1
- drop patch 0, fixed by upstream
- update file list (systemd services)

* Fri Jun 01 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 0.8.4-3.20120515.5
+ Revision: 801892
- change versioned dependency on mkinitrd to a conflicts giving equivalent
  behaviour without having to pull in mkinitrd

* Tue May 15 2012 Tomasz Pawel Gajc <tpg@mandriva.org> 0.8.4-3.20120515.4
+ Revision: 799071
- update to new snapshot 20120515
- use default ttys

* Fri May 11 2012 Franck Bui <franck.bui@mandriva.com> 0.8.4-3.20120503.3
+ Revision: 798316
- libdrm supports are enabled by default

* Fri May 11 2012 Franck Bui <franck.bui@mandriva.com> 0.8.4-3.20120503.2
+ Revision: 798235
- fix configure option --enable-libdrm_nouveau
- Don't build libdrm intel support on non x86 architectures

* Mon May 07 2012 Matthew Dawkins <mattydaw@mandriva.org> 0.8.4-3.20120503.1
+ Revision: 797271
- new snapshot from 20120503
- cleaned up spec

* Sun Mar 25 2012 Tomasz Pawel Gajc <tpg@mandriva.org> 0.8.4-3
+ Revision: 786638
- patch1: show splash for 'splash=silent'

* Sat Mar 24 2012 Tomasz Pawel Gajc <tpg@mandriva.org> 0.8.4-2
+ Revision: 786555
- Patch0: fix dracut path to functions.sh

* Fri Mar 23 2012 Tomasz Pawel Gajc <tpg@mandriva.org> 0.8.4-1
+ Revision: 786237
- update to new verion 0.8.4
- drop all patches, most of them were applied by upstream or were fixed in a different way
- enable systemd integration, pango and kms support
- package new theme called spinner
- spec file clean
- update to new version 0.8.4

* Fri Mar 23 2012 Tomasz Pawel Gajc <tpg@mandriva.org> 0.8.3-16
+ Revision: 786232
- Patch16: redirect output to /dev/null istead of /null
- spec file clean

* Thu Sep 29 2011 Tomasz Pawel Gajc <tpg@mandriva.org> 0.8.3-15
+ Revision: 701830
- Patch15: add support for libpng15

* Thu May 05 2011 Oden Eriksson <oeriksson@mandriva.com> 0.8.3-14
+ Revision: 667787
- mass rebuild

* Tue Mar 01 2011 Andrey Borzenkov <arvidjaar@mandriva.org> 0.8.3-13
+ Revision: 641115
- P14: do not wait forver for non-existing daemon to quit

* Sun Feb 27 2011 Funda Wang <fwang@mandriva.org> 0.8.3-12
+ Revision: 640282
- rebuild to obsolete old packages

* Sat Feb 19 2011 Andrey Borzenkov <arvidjaar@mandriva.org> 0.8.3-11
+ Revision: 638695
- P13: update with upstream version (GIT)

* Fri Feb 18 2011 Andrey Borzenkov <arvidjaar@mandriva.org> 0.8.3-10
+ Revision: 638569
- P13: workaround for https://bugzilla.redhat.com/show_bug.cgi?id=655538

* Sun Jan 30 2011 Andrey Borzenkov <arvidjaar@mandriva.org> 0.8.3-9
+ Revision: 634146
- P12: silence "could not write bytes" (GIT)

  + Per Øyvind Karlsen <peroyvind@mandriva.org>
    - check new path for /lib/mkinitrd/functions
    - regenerate and reenable uclibc related patches that doesn't affect non-uclibc
      build at all

* Thu Nov 18 2010 Andrey Borzenkov <arvidjaar@mandriva.org> 0.8.3-7mdv2011.0
+ Revision: 598802
- patch6: fix compatibility between old and new socket names

* Wed Nov 17 2010 Andrey Borzenkov <arvidjaar@mandriva.org> 0.8.3-6mdv2011.0
+ Revision: 598311
- patch4: allow splash with init= as well (GIT)
  patch5: changed socket path (GIT)

* Wed Oct 06 2010 Andrey Borzenkov <arvidjaar@mandriva.org> 0.8.3-5mdv2011.0
+ Revision: 583884
- patch3: fix "stair stepping" effect using systemd (GIT 0430e512 rediff)

* Wed May 26 2010 Frederic Crozat <fcrozat@mandriva.com> 0.8.3-4mdv2010.1
+ Revision: 546233
- Patch2: do not exit if details plugin isn't available

* Tue May 25 2010 Frederic Crozat <fcrozat@mandriva.com> 0.8.3-3mdv2010.1
+ Revision: 545983
- Patch1: do not switch VT when hiding splash (Mdv bug #59375)

* Wed May 19 2010 Frederic Crozat <fcrozat@mandriva.com> 0.8.3-2mdv2010.1
+ Revision: 545396
- Patch0 (GIT): fix tty staying locked after boot

* Fri May 07 2010 Frederic Crozat <fcrozat@mandriva.com> 0.8.3-1mdv2010.1
+ Revision: 543104
- Release 0.8.3
- Remove patches 0, 1, 2, 3, 4, 5 (merged upstream)

* Thu May 06 2010 Frederic Crozat <fcrozat@mandriva.com> 0.8.2-6mdv2010.1
+ Revision: 542925
- Patch3 (GIT): add more debug
- Patch4 (GIT): wait for VT switch before quit
- Patch5 (GIT): ensure terminal is locked

* Tue Apr 27 2010 Frederic Crozat <fcrozat@mandriva.com> 0.8.2-5mdv2010.1
+ Revision: 539798
- Force rebuild

* Tue Apr 27 2010 Christophe Fergeau <cfergeau@mandriva.com> 0.8.2-4mdv2010.1
+ Revision: 539592
- rebuild so that shared libraries are properly stripped again

* Wed Apr 21 2010 Frederic Crozat <fcrozat@mandriva.com> 0.8.2-3mdv2010.1
+ Revision: 537649
- Patch2 (GIT): export configuration directories

* Tue Apr 20 2010 Frederic Crozat <fcrozat@mandriva.com> 0.8.2-2mdv2010.1
+ Revision: 537082
- Patch1 (GIT): fix text alpha by default

* Wed Apr 14 2010 Frederic Crozat <fcrozat@mandriva.com> 0.8.2-1mdv2010.1
+ Revision: 534762
- Update Buildrequirements
- Release 0.8.2
- Remove patches 2, 3, 4, 5, 6 (merged upstream)
- Patch0 (GIT): fix build with latest libdrm

* Thu Mar 18 2010 Oden Eriksson <oeriksson@mandriva.com> 0.7.2-9mdv2010.1
+ Revision: 524920
- fix deps

  + Per Øyvind Karlsen <peroyvind@mandriva.org>
    - add libpng-static-devel to buildrequires for uClibc as it links against a
      static uClibc build of libpng that doesn't get pulled in by other deps

* Mon Mar 01 2010 Frederic Crozat <fcrozat@mandriva.com> 0.7.2-8mdv2010.1
+ Revision: 512911
- Patch11: ensure shutdown tty is tty1 (Mdv bug #55077)
- Ensure plymouth is building by disable uclibc stuff

  + Per Øyvind Karlsen <peroyvind@mandriva.org>
    - specify absolute path as install location for /bin/plymouth with initrd (P10)
    - build uclibc linked version
    - if linking against plymouth, we need to link against libdl as well (updates P8)
    - fix library link order for static linking (P8)
    - ditch non-sense dependency on plymouth for -devel package
    - fix header include order issue with uclibc (P7)

* Thu Oct 29 2009 Frederic Crozat <fcrozat@mandriva.com> 0.7.2-7mdv2010.0
+ Revision: 459991
- Patch5 (GIT): add on_quit support for script
- Patch6 (Charles Brej): optimize images resize / scale / rotation

* Wed Oct 28 2009 Frederic Crozat <fcrozat@mandriva.com> 0.7.2-6mdv2010.0
+ Revision: 459711
- Patch4 (GIT): add support for arrays

* Tue Oct 13 2009 Frederic Crozat <fcrozat@mandriva.com> 0.7.2-5mdv2010.0
+ Revision: 457160
- Patch3 (GIT): handle plymouth:force-splash and ensure init= value doesn't prevent plymouth to start at shutdown (fdo bug #22180)

* Thu Oct 08 2009 Frederic Crozat <fcrozat@mandriva.com> 0.7.2-4mdv2010.0
+ Revision: 456136
- Do not generate initrd during install

* Wed Oct 07 2009 Olivier Blin <blino@mandriva.org> 0.7.2-3mdv2010.0
+ Revision: 455771
- do not require strict version/release for plymouth(system-theme)
  (external package can not provide the exact version/release)

* Wed Oct 07 2009 Frederic Crozat <fcrozat@mandriva.com> 0.7.2-2mdv2010.0
+ Revision: 455683
- Remove mdv theme, moved to mandriva-theme
- Obsoletes / Provides splashy

* Mon Sep 28 2009 Frederic Crozat <fcrozat@mandriva.com> 0.7.2-1mdv2010.0
+ Revision: 450588
- Release 0.7.2

* Thu Sep 10 2009 Frederic Crozat <fcrozat@mandriva.com> 0.7.2-0.20090910.1mdv2010.0
+ Revision: 437097
- New git snapshot (20090910)
- Remove patch3, merged and fixed correctly in git snapshot

* Thu Sep 10 2009 Frederic Crozat <fcrozat@mandriva.com> 0.7.2-0.20090904.3mdv2010.0
+ Revision: 436871
- Patch3: recognize s,S,-s as single on kernel cmdline

* Tue Sep 08 2009 Frederic Crozat <fcrozat@mandriva.com> 0.7.2-0.20090904.2mdv2010.0
+ Revision: 433139
- Add missing provides on devel package

* Fri Sep 04 2009 Frederic Crozat <fcrozat@mandriva.com> 0.7.2-0.20090904.1mdv2010.0
+ Revision: 431243
- Snapshot of 0.7.2 (include libification work for hibernate / resume)
- Update Mdv theme for hibernate

* Tue Sep 01 2009 Frederic Crozat <fcrozat@mandriva.com> 0.7.1-2mdv2010.0
+ Revision: 423697
- Patch3: disable splash when splash=verbose is on cmdline

* Wed Aug 26 2009 Frederic Crozat <fcrozat@mandriva.com> 0.7.1-1mdv2010.0
+ Revision: 421456
- Release 0.7.1
- Remove patches 0, 1, 3, 4 (merged upstream)
- Update mdv theme to correctly display / hide password and logo
- Improve / factorize post/postun scripts for themes
- Fix requires on glow subpackage (Mdv bug #53160)

* Tue Aug 25 2009 Frederic Crozat <fcrozat@mandriva.com> 0.7.0-7mdv2010.0
+ Revision: 421069
- Patch4: various git fixes, including infinite loop in message handling (Mdv bug #52861)
- Update patch2 to no longer crash on empty message
- Own more directory

* Wed Aug 19 2009 Frederic Crozat <fcrozat@mandriva.com> 0.7.0-6mdv2010.0
+ Revision: 418114
- Patch2 (Charlie Brej): text support in script plugin
- Patch3 (GIT): add callback for message event in script plugin
- Adapt mdv theme to display text message / password prompt
- Enforce dependencies

* Wed Aug 19 2009 Frederic Crozat <fcrozat@mandriva.com> 0.7.0-5mdv2010.0
+ Revision: 418005
- Remove patch2 and revert initrd scripts to be in /usr/libexec (as upstream)
- Fix post / postun scripts

* Wed Aug 19 2009 Frederic Crozat <fcrozat@mandriva.com> 0.7.0-4mdv2010.0
+ Revision: 417963
- Use mandriva.png from desktop-common-data now (Mdv bug #52973)

* Tue Aug 18 2009 Frederic Crozat <fcrozat@mandriva.com> 0.7.0-3mdv2010.0
+ Revision: 417842
- Add a initial Mdv theme, similar to splashy one (no text support yet)
- change default theme to Mdv
- Rebuild initrd when switching theme
- Patch1 (GIT): fix resizing code
- Patch2: allow alternative libexec path
- Update default duration file with a Mandriva file

* Mon Aug 17 2009 Frederic Crozat <fcrozat@mandriva.com> 0.7.0-2mdv2010.0
+ Revision: 417347
- Patch0 (GIT): reconnect on tty_disconnect

* Thu Aug 13 2009 Frederic Crozat <fcrozat@mandriva.com> 0.7.0-1mdv2010.0
+ Revision: 416079
- Release 0.7.0 final
- add script plugin/theme

* Thu Jul 02 2009 Frederic Crozat <fcrozat@mandriva.com> 0.7.0-0.20090515.1mdv2010.0
+ Revision: 391840
- Fix dependencies
- import plymouth

