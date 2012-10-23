%define plymouthdaemon_execdir /sbin
%define plymouthclient_execdir /bin
%define plymouth_libdir /%{_lib}

%define _libexecdir %{_prefix}/libexec

%define major 2
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

%bcond_without	uclibc

Summary:	Graphical Boot Animation and Logger
Name:		plymouth
Version:	0.8.6.1
Release:	2
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
# PATCH-FIX-UPSTREAM -- Create targets for plymouth systemd services
Patch2:		plymouth-systemd-target.patch
Patch3:		plymouth-0.8.6.1-fix-systemd-service-patch.patch
# PATCH-OPENSUSE -- Handle correctly multiple displays with different sizes
Patch4:		plymouth-fix-window-size
# PATCH-FIX-UPSTREAM -- Recognize quotes often used in sysconfig-style files
Patch5:		0001-ply-text-progress-bar-strip-quotes-if-present.patch
# PATCH-OPENSUSE -- Add line numbers to tracing output
Patch6:         plymouth-trace-lines
Patch7:		plymouth-0.8.6.1-less-greedy-usr_lib-substitution.patch
BuildRequires:	gtk2-devel
BuildRequires:	libdrm-devel
%if %{with uclibc}
BuildRequires:	uClibc-devel >= 0.9.33.2-14
%endif
BuildRequires:	systemd-units
%rename		splashy
Requires(post):	plymouth-scripts = %{version}-%{release}
Requires:	initscripts >= 8.83
Requires:	desktop-common-data >= 2010.0-1mdv
Conflicts:	systemd-units < 186

%description
Plymouth provides an attractive graphical boot animation in
place of the text messages that normally get shown.  Text
messages are instead redirected to a log file for viewing
after boot.

%package -n	uclibc-%{name}
Summary:	uClibc build of %{name}
Group:		System/Kernel and hardware
Requires:	%{name} = %{EVRD}

%description -n	uclibc-%{name}
uClibc linked build of %{name}.

%package	system-theme
Group:		System/Kernel and hardware
Summary:	Plymouth default theme
Requires:	plymouth(system-theme)
Requires:	plymouth = %{version}-%{release}

%description	system-theme
This metapackage tracks the current distribution default theme.

%package -n	%{libname}
Summary:	Plymouth libraries
Group:		System/Libraries
Obsoletes:	%{mklibname %{name} 0} < 0.8.0

%description -n	%{libname}
This package contains the libply and libplybootsplash libraries
used by Plymouth.

%package -n	uclibc-%{libname}
Summary:	Plymouth libraries (uClibc builld)
Group:		System/Libraries

%description -n	uclibc-%{libname}
This package contains the libply and libplybootsplash libraries
used by Plymouth.

%package -n	%{develname}
Group:		System/Kernel and hardware
Summary:	Libraries and headers for writing Plymouth splash plugins
Group:		Development/C
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
%if %{with uclibc}
Requires:	uclibc-%{libname} = %{version}
%endif

%description -n	%{develname}
This package contains the libply and libplybootsplash libraries
and headers needed to develop 3rd party splash plugins for Plymouth.

%package	utils
Group:		System/Kernel and hardware
Summary:	Plymouth related utilities
Requires:	%{name} = %{version}-%{release}

%description	utils
This package contains utilities that integrate with Plymouth
including a boot log viewing application.

%package	scripts
Group:		System/Kernel and hardware
Summary:	Plymouth related scripts
Conflicts:	mkinitrd < 6.0.92-6mdv
Requires:	plymouth = %{version}-%{release}

%description	scripts
This package contains scripts that help integrate Plymouth with
the system.

%package	plugin-label
Group:		System/Kernel and hardware
Summary:	Plymouth label plugin
Requires:	%{libname} = %{version}-%{release}

%description	plugin-label
This package contains the label control plugin for
Plymouth. It provides the ability to render text on
graphical boot splashes using pango and cairo.

%package	plugin-fade-throbber
Group:		System/Kernel and hardware
Summary:	Plymouth "Fade-Throbber" plugin
Requires:	%{libname} = %{version}-%{release}

%description	plugin-fade-throbber
This package contains the "Fade-In" boot splash plugin for
Plymouth. It features a centered image that fades in and out
while other images pulsate around during system boot up.

%package -n	uclibc-%{name}-plugin-fade-throbber
Group:		System/Kernel and hardware
Summary:	Plymouth "Fade-Throbber" plugin (uClibc build)
Requires:	uclibc-%{libname} = %{version}-%{release}

%description -n	uclibc-%{name}-plugin-fade-throbber
This package contains the "Fade-In" boot splash plugin for
Plymouth. It features a centered image that fades in and out
while other images pulsate around during system boot up.

%package	plugin-script
Group:		System/Kernel and hardware
Summary:	Plymouth "Script" plugin
Requires:	%{libname} = %{version}-%{release}
Requires:	plymouth-plugin-label = %{version}-%{release}

%description	plugin-script
This package contains the "Script" plugin for Plymouth. 

%package -n	uclibc-%{name}-plugin-script
Group:		System/Kernel and hardware
Summary:	Plymouth "Script" plugin (uClibc build)
Requires:	uclibc-%{libname} = %{version}-%{release}

%description	plugin-script
This package contains the "Script" plugin for Plymouth. 

%package	theme-script
Group:		System/Kernel and hardware
Summary:	Plymouth "Script" theme
Requires:	%{name}-plugin-script = %{version}-%{release}
Requires(post):	plymouth-scripts = %{version}-%{release}

%description	theme-script
This package contains the "Script" boot splash theme for
Plymouth. 

%package	theme-fade-in
Group:		System/Kernel and hardware
Summary:	Plymouth "Fade-In" theme
Requires:	%{name}-plugin-fade-throbber = %{version}-%{release}
Requires(post):	plymouth-scripts = %{version}-%{release}

%description	theme-fade-in
This package contains the "Fade-In" boot splash theme for
Plymouth. It features a centered logo that fades in and out
while stars twinkle around the logo during system boot up.

%package	plugin-throbgress
Group:		System/Kernel and hardware
Summary:	Plymouth "Throbgress" plugin
Requires:	%{libname} = %{version}-%{release}
Requires:	plymouth-plugin-label = %{version}-%{release}

%description	plugin-throbgress
This package contains the "throbgress" boot splash plugin for
Plymouth. It features a centered logo and animated spinner that
spins repeatedly while a progress bar advances at the bottom of
the screen.

%package -n	uclibc-%{name}-plugin-throbgress
Group:		System/Kernel and hardware
Summary:	Plymouth "Throbgress" plugin (uClibc build)
Requires:	uclibc-%{libname} = %{version}-%{release}

%description -n	uclibc-%{name}-plugin-throbgress
This package contains the "throbgress" boot splash plugin for
Plymouth. It features a centered logo and animated spinner that
spins repeatedly while a progress bar advances at the bottom of
the screen.

%package	theme-spinfinity
Group:		System/Kernel and hardware
Summary:	Plymouth "Spinfinity" theme
Requires:	%{name}-plugin-throbgress = %{version}-%{release}
Requires(post):	plymouth-scripts = %{version}-%{release}

%description	theme-spinfinity
This package contains the "Spinfinity" boot splash theme for
Plymouth. It features a centered logo and animated spinner that
spins in the shape of an infinity sign.

%package	theme-spinner
Group:		System/Kernel and hardware
Summary:	Plymouth "Spinner" theme
Requires:	%{name}-plugin-two-step = %{version}-%{release}
Requires(post):	plymouth-scripts = %{version}-%{release}

%description	theme-spinner
This package contains the "Spinner" boot splash theme for
Plymouth.

%package	plugin-space-flares
Group:		System/Kernel and hardware
Summary:	Plymouth "space-flares" plugin
Requires:	%{libname} = %{version}-%{release}
Requires:	plymouth-plugin-label = %{version}-%{release}

%description	plugin-space-flares
This package contains the "space-flares" boot splash plugin for
Plymouth. It features a corner image with animated flares.

%package -n	uclibc-%{name}-plugin-space-flares
Group:		System/Kernel and hardware
Summary:	Plymouth "space-flares" plugin (uClibc build)
Requires:	uclibc-%{libname} = %{version}-%{release}

%description -n	uclibc-%{name}-plugin-space-flares
This package contains the "space-flares" boot splash plugin for
Plymouth. It features a corner image with animated flares.

%package	theme-solar
Group:		System/Kernel and hardware
Summary:	Plymouth "Solar" theme
Requires:	%{name}-plugin-space-flares = %{version}-%{release}
Requires(post):	plymouth-scripts = %{version}-%{release}

%description	theme-solar
This package contains the "Solar" boot splash theme for
Plymouth. It features a blue flamed sun with animated solar flares.

%package	plugin-two-step
Group:		System/Kernel and hardware
Summary:	Plymouth "two-step" plugin
Requires:	%{libname} = %{version}-%{release}
Requires:	plymouth-plugin-label = %{version}-%{release}

%description	plugin-two-step
This package contains the "two-step" boot splash plugin for
Plymouth. It features a two phased boot process that starts with
a progressing animation synced to boot time and finishes with a
short, fast one-shot animation.

%package -n	uclibc-%{name}-plugin-two-step
Group:		System/Kernel and hardware
Summary:	Plymouth "two-step" plugin (uClibc build)
Requires:	uclibc-%{libname} = %{version}-%{release}

%description -n	uclibc-%{name}-plugin-two-step
This package contains the "two-step" boot splash plugin for
Plymouth. It features a two phased boot process that starts with
a progressing animation synced to boot time and finishes with a
short, fast one-shot animation.

%package	theme-charge
Group:		System/Kernel and hardware
Summary:	Plymouth "Charge" plugin
Requires:	%{name}-plugin-two-step = %{version}-%{release}
Requires(post):	plymouth-scripts = %{version}-%{release}

%description	theme-charge
This package contains the "charge" boot splash theme for
Plymouth. It features the shadowy hull of a logo charge up and
and finally burst into full form.

%package	theme-glow
Group:		System/Kernel and hardware
Summary:	Plymouth "Glow" plugin
Requires(post):	plymouth-scripts  = %{version}-%{release}
Requires:	plymouth-plugin-two-step = %{version}-%{release}

%description	theme-glow
This package contains the "Glow" boot splash theme for Plymouth.

%prep
%setup -q
%patch0 -p1 -b .suspend~
%patch1 -p1 -b .udevadm~
%patch2 -p1 -b .systemd~
%patch3 -p1 -b .dashes~
%patch4 -p1 -b .window_size~
%patch5 -p1 -b .strip_quotes~
%patch6 -p1 -b .trace_lines~
%patch7 -p1 -b .sysroot_subst~
autoreconf -f

%build
export CONFIGURE_TOP=`pwd`
%if %{with uclibc}
mkdir -p uclibc
cd uclibc
%uclibc_configure \
	LDFLAGS="%{ldflags} -lz -lpciaccess" \
	--bindir="%{uclibc_root}%{plymouthclient_execdir}" \
	--sbindir="%{uclibc_root}%{plymouthdaemon_execdir}" \
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
	--disable-pango \
	--disable-gtk \
%ifnarch %{ix86} x86_64
	--disable-libdrm_intel \
%else
	--enable-libdrm_intel \
%endif
	--enable-libdrm_radeon \
	--enable-libkms \
%if %mdvver >= 201200
	--with-release-file=/etc/os-release \
%else
	--with-release-file=/etc/mandriva-release \
%endif
	--without-log-viewer

%make
cd ..
%endif

mkdir -p system
cd system
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
cd ..

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
%files -n uclibc-plymouth
%{uclibc_root}%{plymouthdaemon_execdir}/plymouthd
%{uclibc_root}%{plymouthclient_execdir}/plymouth
%dir %{uclibc_root}%{_libdir}/plymouth
%{uclibc_root}%{_libdir}/plymouth/details.so
%{uclibc_root}%{_libdir}/plymouth/text.so
%dir %{uclibc_root}%{_libdir}/plymouth/renderers
%{uclibc_root}%{_libdir}/plymouth/renderers/drm*
%{uclibc_root}%{_libdir}/plymouth/renderers/frame-buffer*
%endif

%files -n %{develname}
/%{_lib}/libply.so
/%{_lib}/libply-splash-core.so
%{_libdir}/libply-boot-client.so
%{_libdir}/libply-splash-graphics.so
%if %{with uclibc}
%{uclibc_root}/%{_lib}/libply.so
%{uclibc_root}/%{_lib}/libply-splash-core.so
%{uclibc_root}%{_libdir}/libply-boot-client.so
%{uclibc_root}%{_libdir}/libply-splash-graphics.so
%endif
%{_libdir}/plymouth/renderers/x11*
%{_libdir}/pkgconfig/*.pc
%{_includedir}/plymouth-1

%files -n %{libname}
/%{_lib}/libply.so.%{major}*
/%{_lib}/libply-splash-core.so.%{major}*
%{_libdir}/libply-boot-client.so.%{major}*
%{_libdir}/libply-splash-graphics.so.%{major}*

%if %{with uclibc}
%files -n uclibc-%{libname}
%{uclibc_root}/%{_lib}/libply.so.%{major}*
%{uclibc_root}/%{_lib}/libply-splash-core.so.%{major}*
%{uclibc_root}%{_libdir}/libply-boot-client.so.%{major}*
%{uclibc_root}%{_libdir}/libply-splash-graphics.so.%{major}*
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
%files -n uclibc-%{name}-plugin-fade-throbber
%{uclibc_root}%{_libdir}/plymouth/fade-throbber.so
%endif

%files theme-fade-in
%{_datadir}/plymouth/themes/fade-in

%files plugin-throbgress
%{_libdir}/plymouth/throbgress.so

%if %{with uclibc}
%files -n uclibc-%{name}-plugin-throbgress
%{uclibc_root}%{_libdir}/plymouth/throbgress.so
%endif

%files plugin-script
%{_libdir}/plymouth/script.so

%if %{with uclibc}
%files -n uclibc-%{name}-plugin-script
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
%files -n uclibc-%{name}-plugin-space-flares
%{uclibc_root}%{_libdir}/plymouth/space-flares.so
%endif

%files theme-solar
%{_datadir}/plymouth/themes/solar

%files plugin-two-step
%{_libdir}/plymouth/two-step.so

%if %{with uclibc}
%files -n uclibc-%{name}-plugin-two-step
%{uclibc_root}%{_libdir}/plymouth/two-step.so
%endif

%files theme-charge
%{_datadir}/plymouth/themes/charge

%files theme-glow
%{_datadir}/plymouth/themes/glow

%files system-theme
