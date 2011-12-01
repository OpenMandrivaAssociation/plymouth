%define plymouthdaemon_execdir /sbin
%define plymouthclient_execdir /bin
%define plymouth_libdir /%{_lib}

%define _libexecdir %{_prefix}/libexec

%define lib_major 2
%define lib_name %mklibname %{name} %{lib_major}
%define lib_name_devel %mklibname %{name} -d

%define snapshot 0

%bcond_with uclibc

Summary: Graphical Boot Animation and Logger
Name: plymouth
Version: 0.8.3
Release: %mkrel 15
License: GPLv2+
Group: System/Kernel and hardware
Source0: http://freedesktop.org/software/plymouth/releases/%{name}-%{version}.tar.bz2
Source1: boot-duration
Source2: charge.plymouth
# (fc) 0.8.3-2mdv fix tty staying locked after boot (GIT)
Patch0: plymouth-0.8.3-tty-lock.patch
# (fc) 0.8.3-3mdv do not switch VT when hiding plymouth (Mdv bug #59375)
Patch1: plymouth-0.8.3-retain-vt.patch
# (fc) 0.8.3-4mdv do not exit if details plugin isn't available
Patch2: plymouth-0.8.3-details-not-available.patch

# (bor) 0.8.3-5mdv fix "stair stepping" effect on terminal using systemd (GIT)
Patch3: plymouth-0.8.3-tty-OPOST-ONLCR.patch
# (bor) 0.8.3-6mdv be more liberal in accepting init= kernel parameter (GIT backport)
Patch4: plymouth-0.8.3-smarter_init_detection.patch
# (bor) 0.8.3-6mdv change socket name (GIT)
Patch5: plymouth-0.8.3-change_socket_path.patch
# (bor) 0.8.3-7mdv fix previous patch (submitted upstream)
Patch6: plymouth-0.8.3-change_socket_path-fix.patch

# (proyvind) 0.7.2-8mdv fix build with uclibc (should go upstream..)
Patch7:	plymouth-0.7.2-add-missing-header.patch
# (proyvind) 0.7.2-8mdv fix library link order for static linking (idem..)
Patch8: plymouth-0.8.3-library-link-order.patch
# (proyvind) 0.7.2-8mdv substitute /usr/lib with /lib rather than just stripping away
# /usr. This so that ie. /usr/uclibc/usr/lib will be be /usr/uclibc/lib rather than
# /uclibc/usr/lib. (should probably go upstream as well)
Patch9: plymouth-0.7.2-less-greedy-usr_lib-substitution.patch
# (proyvind) 0.7.2-8mdv specify absolute path to /bin/plymouth to ensure install
# location with uclibc
Patch10: plymouth-0.8.3-initrd-absolute-path.patch
# (proyvind): /usr/libexec/mkinird-functions has been moved to /lib/mkinitrd/functions
#	      to be available, usable and /sbin/mkinitrd location sensible
Patch11: SOURCES/plymouth-0.8.3-move-mkinitrd-functions-under-root-lib.patch
# (bor) 0.8.3-9 "could not write bytes" is not error (GIT)
Patch12: plymouth-0.8.3-boot-server-don-t-print-error-when-client-goes-away.patch
# (bor) 0.8.3-10 fix password request on boot (GIT)
#       ref: https://bugzilla.redhat.com/show_bug.cgi?id=655538
Patch13: plymouth-0.8.3-terminal-unlock-tty-before-muc.patch
# (bor) 0.8.3-13 do not wait forver for non-existing daemon to quit
Patch14: plymouth-0.8.3-do_not_hang_on_wait_without_daemon.patch
Patch15: plymouth-0.8.3-libpng14.patch
URL: http://freedesktop.org/software/plymouth/releases
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

Requires(post): plymouth-scripts = %{version}-%{release}
Requires: initscripts >= 8.83
Requires: desktop-common-data >= 2010.0-1mdv
BuildRequires: gtk2-devel
BuildRequires: libdrm-devel
%if %{with uclibc}
BuildRequires: uClibc-devel
BuildRequires: libpng-static-devel
%endif
Obsoletes: splashy
Provides: splashy

%description
Plymouth provides an attractive graphical boot animation in
place of the text messages that normally get shown.  Text
messages are instead redirected to a log file for viewing
after boot.

%package system-theme
Group: System/Kernel and hardware
Summary: Plymouth default theme
Requires: plymouth(system-theme)
Requires: plymouth = %{version}-%{release}

%description system-theme
This metapackage tracks the current distribution default theme.

%package -n %{lib_name}
Summary: Plymouth libraries
Group: System/Libraries
Obsoletes: %{mklibname %{name} 0} < 0.8.0

%description -n %{lib_name}
This package contains the libply and libplybootsplash libraries
used by Plymouth.

%package -n %{lib_name_devel}
Group: System/Kernel and hardware
Summary: Libraries and headers for writing Plymouth splash plugins
Group: Development/C
Provides: %{name}-devel = %{version}-%{release}
Provides: lib%{name}-devel = %{version}-%{release}
Requires: %{lib_name} = %{version}-%{release}

%description -n %{lib_name_devel}
This package contains the libply and libplybootsplash libraries
and headers needed to develop 3rd party splash plugins for Plymouth.

%package utils
Group: System/Kernel and hardware
Summary: Plymouth related utilities
Requires: %{name} = %{version}-%{release}

%description utils
This package contains utilities that integrate with Plymouth
including a boot log viewing application.

%package scripts
Group: System/Kernel and hardware
Summary: Plymouth related scripts
Requires: mkinitrd >= 6.0.92-6mdv
Requires: plymouth = %{version}-%{release}

%description scripts
This package contains scripts that help integrate Plymouth with
the system.

%package plugin-label
Group: System/Kernel and hardware
Summary: Plymouth label plugin
Requires: %{lib_name} = %{version}-%{release}

%description plugin-label
This package contains the label control plugin for
Plymouth. It provides the ability to render text on
graphical boot splashes using pango and cairo.

%package plugin-fade-throbber
Group: System/Kernel and hardware
Summary: Plymouth "Fade-Throbber" plugin
Requires: %{lib_name} = %{version}-%{release}

%description plugin-fade-throbber
This package contains the "Fade-In" boot splash plugin for
Plymouth. It features a centered image that fades in and out
while other images pulsate around during system boot up.

%package plugin-script
Group: System/Kernel and hardware
Summary: Plymouth "Script" plugin
Requires: %{lib_name} = %{version}-%{release}
Requires: plymouth-plugin-label = %{version}-%{release}

%description plugin-script
This package contains the "Script" plugin for Plymouth. 

%package theme-script
Group: System/Kernel and hardware
Summary: Plymouth "Script" theme
Requires: %{name}-plugin-script = %{version}-%{release}
Requires(post): plymouth-scripts = %{version}-%{release}

%description theme-script
This package contains the "Script" boot splash theme for
Plymouth. 

%package theme-fade-in
Group: System/Kernel and hardware
Summary: Plymouth "Fade-In" theme
Requires: %{name}-plugin-fade-throbber = %{version}-%{release}
Requires(post): plymouth-scripts = %{version}-%{release}

%description theme-fade-in
This package contains the "Fade-In" boot splash theme for
Plymouth. It features a centered logo that fades in and out
while stars twinkle around the logo during system boot up.

%package plugin-throbgress
Group: System/Kernel and hardware
Summary: Plymouth "Throbgress" plugin
Requires: %{lib_name} = %{version}-%{release}
Requires: plymouth-plugin-label = %{version}-%{release}

%description plugin-throbgress
This package contains the "throbgress" boot splash plugin for
Plymouth. It features a centered logo and animated spinner that
spins repeatedly while a progress bar advances at the bottom of
the screen.

%package theme-spinfinity
Group: System/Kernel and hardware
Summary: Plymouth "Spinfinity" theme
Requires: %{name}-plugin-throbgress = %{version}-%{release}
Requires(post): plymouth-scripts = %{version}-%{release}

%description theme-spinfinity
This package contains the "Spinfinity" boot splash theme for
Plymouth. It features a centered logo and animated spinner that
spins in the shape of an infinity sign.

%package plugin-space-flares
Group: System/Kernel and hardware
Summary: Plymouth "space-flares" plugin
Requires: %{lib_name} = %{version}-%{release}
Requires: plymouth-plugin-label = %{version}-%{release}

%description plugin-space-flares
This package contains the "space-flares" boot splash plugin for
Plymouth. It features a corner image with animated flares.

%package theme-solar
Group: System/Kernel and hardware
Summary: Plymouth "Solar" theme
Requires: %{name}-plugin-space-flares = %{version}-%{release}
Requires(post): plymouth-scripts = %{version}-%{release}

%description theme-solar
This package contains the "Solar" boot splash theme for
Plymouth. It features a blue flamed sun with animated solar flares.

%package plugin-two-step
Group: System/Kernel and hardware
Summary: Plymouth "two-step" plugin
Requires: %{lib_name} = %{version}-%{release}
Requires: plymouth-plugin-label = %{version}-%{release}

%description plugin-two-step
This package contains the "two-step" boot splash plugin for
Plymouth. It features a two phased boot process that starts with
a progressing animation synced to boot time and finishes with a
short, fast one-shot animation.

%package theme-charge
Group: System/Kernel and hardware
Summary: Plymouth "Charge" plugin
Requires: %{name}-plugin-two-step = %{version}-%{release}
Requires(post): plymouth-scripts = %{version}-%{release}

%description theme-charge
This package contains the "charge" boot splash theme for
Plymouth. It features the shadowy hull of a logo charge up and
and finally burst into full form.

%package theme-glow
Group: System/Kernel and hardware
Summary: Plymouth "Glow" plugin
Requires(post): plymouth-scripts  = %{version}-%{release}
Requires: plymouth-plugin-two-step = %{version}-%{release}

%description theme-glow
This package contains the "Glow" boot splash theme for Plymouth.

%prep
%setup -q
%patch0 -p1 -b .tty-lock
%patch1 -p1 -b .retain-vt
%patch2 -p1 -b .details-not-available
%patch3 -p1 -b .tty-OPOST-ONLCR
%patch4 -p1 -b .smarter_init_detection
%patch5 -p1 -b .change_socket_path
%patch6 -p1 -b .change_socket_path-fix
%patch7 -p1 -b .header~
%patch8 -p1 -b .link_order~
%patch9 -p1 -b .usrlib_subst~
%patch10 -p1 -b .abspath~
%patch11 -p1 -b .mkinitrd_lib~
%patch12 -p1 -b .could-not-write-bytes
%patch13 -p1 -b .tty_locked_settings
%patch14 -p1 -b .do_not_hang_on_wait
%patch15 -p0 -b .png
autoreconf --install --symlink


%build
export CONFIGURE_TOP=`pwd`
%if %{with uclibc}
mkdir -p uclibc
cd uclibc
%configure2_5x CC="%{uclibc_cc}" \
	CFLAGS="%{uclibc_cflags}" \
	LDFLAGS="%{ldflags} -lz" \
	--prefix=%{uclibc_root}%{_prefix} \
	--libdir="%{uclibc_root}%{_libdir}" \
	--bindir="%{uclibc_root}%{plymouthclient_execdir}" \
	--sbindir="%{uclibc_root}%{plymouthdaemon_execdir}" \
	--enable-tracing --disable-tests \
	--with-logo=%{_datadir}/icons/large/mandriva.png 		\
	--with-background-start-color-stop=0x0073B3			\
	--with-background-end-color-stop=0x00457E			\
	--with-background-color=0x3391cd				\
	--disable-gdm-transition					\
	--without-gdm-autostart-file					\
	--without-rhgb-compat-link					\
	--with-system-root-install 					\
	--with-boot-tty=tty7						\
	--with-shutdown-tty=tty1					\
	--with-release-file=/etc/mandriva-release
# We don't build these for uclibc since they link against a lot of libraries
# that we don't provide any uclibc linked version of
sed -e 's#viewer##g' -i src/Makefile
sed -e 's#label##g' -i src/plugins/controls/Makefile
%make
cd ..
%endif

mkdir -p system
cd system
%configure2_5x \
	--enable-tracing --disable-tests \
	--with-logo=%{_datadir}/icons/large/mandriva.png 		\
	--with-background-start-color-stop=0x0073B3			\
	--with-background-end-color-stop=0x00457E			\
	--with-background-color=0x3391cd				\
	--disable-gdm-transition					\
	--without-gdm-autostart-file					\
	--without-rhgb-compat-link					\
	--with-system-root-install 					\
	--with-boot-tty=tty7						\
	--with-shutdown-tty=tty1					\
	--with-release-file=/etc/mandriva-release

%make
cd ..

%install
rm -rf %{buildroot}

%if %{with uclibc}
%makeinstall_std -C uclibc plymouthdaemondir=%{uclibc_root}%{plymouthdaemon_execdir} plymouthclientdir=%{uclibc_root}%{plymouthclient_execdir}
rm -rf %{buildroot}%{uclibc_root}{%{_includedir},%{_datadir},%{_libdir}/pkgconfig,%{_libexecdir},%{plymouthdaemon_execdir}/plymouth-set-default-theme}
%endif
%makeinstall_std -C system

find %{buildroot} -name \*.a -delete -o -name \*.la -delete

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

%clean
rm -rf %{buildroot}

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
%defattr(-, root, root)
%doc AUTHORS NEWS README
%config(noreplace) %{_sysconfdir}/plymouth
%dir %{_datadir}/plymouth
%dir %{_datadir}/plymouth/themes
%{_datadir}/plymouth/default-boot-duration
%dir %{_localstatedir}/lib/plymouth
%{plymouthdaemon_execdir}/plymouthd
%{plymouthclient_execdir}/plymouth
%{_bindir}/plymouth
%{_libdir}/plymouth/details.so
%{_libdir}/plymouth/text.so
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
%{_mandir}/man8/
%if %{with uclibc}
%{uclibc_root}%{plymouthdaemon_execdir}/plymouthd
%{uclibc_root}%{plymouthclient_execdir}/plymouth
%{uclibc_root}%{_libdir}/plymouth/details.so
%{uclibc_root}%{_libdir}/plymouth/text.so
%endif

%files -n %{lib_name_devel}
%defattr(-, root, root)
%{plymouth_libdir}/libply.so
%{_libdir}/libply-boot-client.so
%{_libdir}/libply-splash-graphics.so
%{_libdir}/plymouth/renderers/x11*
/%{_lib}/libply-splash-core.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/plymouth-1

%files -n %{lib_name}
%defattr(-, root, root)
%{plymouth_libdir}/libply.so.%{lib_major}*
%{_libdir}/libply-boot-client.so.%{lib_major}*
%{_libdir}/libply-splash-graphics.so.%{lib_major}*
/%{_lib}/libply-splash-core.so.%{lib_major}*
%dir %{_libdir}/plymouth
%if %{with uclibc}
%dir %{uclibc_root}%{_libdir}/plymouth
%{uclibc_root}%{plymouth_libdir}/libply.so*
%{uclibc_root}%{_libdir}/libply-boot-client.so*
%{uclibc_root}%{_libdir}/libply-splash-graphics.so*
%endif

%files scripts
%defattr(-, root, root)
%{_sbindir}/plymouth-set-default-theme
%{_libexecdir}/plymouth

%files utils
%defattr(-, root, root)
%{_bindir}/plymouth-log-viewer

%files plugin-label
%defattr(-, root, root)
%{_libdir}/plymouth/label.so

%files plugin-fade-throbber
%defattr(-, root, root)
%{_libdir}/plymouth/fade-throbber.so
%if %{with uclibc}
%{uclibc_root}%{_libdir}/plymouth/fade-throbber.so
%endif

%files theme-fade-in
%defattr(-, root, root)
%{_datadir}/plymouth/themes/fade-in

%files plugin-throbgress
%defattr(-, root, root)
%{_libdir}/plymouth/throbgress.so
%if %{with uclibc}
%{uclibc_root}%{_libdir}/plymouth/throbgress.so
%endif

%files plugin-script
%defattr(-, root, root)
%{_libdir}/plymouth/script.so
%if %{with uclibc}
%{uclibc_root}%{_libdir}/plymouth/script.so
%endif

%files theme-script
%defattr(-, root, root)
%{_datadir}/plymouth/themes/script

%files theme-spinfinity
%defattr(-, root, root)
%{_datadir}/plymouth/themes/spinfinity

%files plugin-space-flares
%defattr(-, root, root)
%{_libdir}/plymouth/space-flares.so
%if %{with uclibc}
%{uclibc_root}%{_libdir}/plymouth/space-flares.so
%endif

%files theme-solar
%defattr(-, root, root)
%{_datadir}/plymouth/themes/solar

%files plugin-two-step
%defattr(-, root, root)
%{_libdir}/plymouth/two-step.so
%if %{with uclibc}
%{uclibc_root}%{_libdir}/plymouth/two-step.so
%endif

%files theme-charge
%defattr(-, root, root)
%{_datadir}/plymouth/themes/charge

%files theme-glow
%defattr(-, root, root)
%{_datadir}/plymouth/themes/glow

%files system-theme
%defattr(-, root, root)
