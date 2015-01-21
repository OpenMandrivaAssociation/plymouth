%define plymouthdaemon_execdir /sbin
%define plymouthclient_execdir /bin
%define plymouth_libdir /%{_lib}
%define _libexecdir %{_prefix}/libexec
%define major 4
%define libname %mklibname %{name} %{major}
%define libply %mklibname ply %{major}
%define libply_boot_client %mklibname ply-boot-client %{major}
%define libply_splash_graphics %mklibname ply-splash-graphics %{major}
%define libply_splash_core %mklibname ply-splash-core %{major}
%define devname %mklibname %{name} -d

%define snapshot 0

%bcond_with uclibc

Summary:	Graphical Boot Animation and Logger
Name:		plymouth
Version:	0.9.0
%if %snapshot
Release:	0.%snapshot.1
Source0:	%{name}-%{snapshot}.tar.xz
%else
Release:	15
Source0:	http://www.freedesktop.org/software/plymouth/releases/%{name}-%{version}.tar.bz2
%endif
License:	GPLv2+
Group:		System/Kernel and hardware
Url:		http://www.freedesktop.org/wiki/Software/Plymouth
Source1:	boot-duration
Source2:	charge.plymouth


# UPSTREAM GIT PATCHES
Patch100:	0100-scripts-change-out-uncrustify-config.patch
Patch101:	0101-Reindent.patch
Patch102:	0102-device-manager-only-call-ply_terminal_free.patch
Patch103:	0103-main-fix-typo-in-debug-message.patch
Patch104:	0104-systemd-give-plymouth-quit-wait-a-better-description.patch
Patch105:	0105-splash-remove-pixel_display-in-sprite-lib-when-notif.patch
Patch106:	0106-libply-splash-core-fix-typo-in-logs.patch
Patch107:	0107-splash-do-not-process-display-lists-if-it-is-empty-o.patch
Patch109:	0109-libply-splash-core-also-monitor-for-file-removal-in-.patch
Patch110:	0110-configure-bump-point-release-and-ABI-versions-of-lib.patch
Patch111:	0111-seat-be-a-little-more-forgiving-in-the-case-there-s-.patch
Patch112:	0112-text-step-bar-use-correct-utf-8-multibyte-sequence-f.patch
Patch113:	0113-Revert-systemd-add-WantedBy-snippets.patch
Patch114:	0114-main-show-splash-even-when-user-has-init-bin-sh.patch
Patch115:	0115-main-fix-incorrectly-sized-buffer-for-proc-cmdline.patch
Patch116:	0116-client-fix-incorrectly-sized-buffer-for-proc-cmdline.patch
Patch117:	0117-script-support-system-update-events.patch
Patch118:	0118-main-fix-up-mode-confusion.patch
Patch119:	0119-main-fix-up-spacing-in-previous-commit-to-match-codi.patch
Patch120:	0120-script-Add-SetRefreshRate-function.patch
Patch121:	0121-utils-Don-t-create-unix-sockets-non-blocking.patch
Patch122:	0122-device-manager-try-fb-device-if-drm-device-failed.patch

# PATCH-OPENSUSE -- Restore suspend / resume state (needed for suspend package)
Patch500:		plymouth-restore-suspend.patch
# Fix complaints about ply_logger_is_tracing_enabled being undefined
Patch501:		plymouth-0.8.9-export-ply_logger_is_tracing_enabled.patch
# PATCH-OPENSUSE -- Handle correctly multiple displays with different sizes
Patch502:		plymouth-fix-window-size.patch
Patch503:		plymouth-0.8.9-set-delay-to-0.patch

BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(pangocairo)
BuildRequires:	pkgconfig(libdrm)
BuildRequires:	pkgconfig(systemd)
BuildRequires:	pkgconfig(libudev)
BuildRequires:	xsltproc
BuildRequires:	docbook-style-xsl
BuildRequires:	docbook-dtd45-xml
%if %{with uclibc}
BuildRequires:	uClibc-devel
BuildRequires:	%{_lib}png-static-devel
%endif
BuildRequires:	systemd-units
%rename		splashy
Requires(posttrans):	plymouth-scripts = %{EVRD}
Requires(posttrans):	dracut
Conflicts:	systemd-units < 186
%rename plymouth-utils

%description
Plymouth provides an attractive graphical boot animation in
place of the text messages that normally get shown.  Text
messages are instead redirected to a log file for viewing
after boot.

%package system-theme
Group:		System/Kernel and hardware
Summary:	Plymouth default theme
Requires:	plymouth(system-theme)
Requires:	plymouth = %{EVRD}

%description system-theme
This metapackage tracks the current distribution default theme.

%package -n %{libply}
Summary:	Plymouth libraries
Group:		System/Libraries
Obsoletes:	%{_lib}plymouth2 < 0.9.0-11
Requires:	%{libply_boot_client}
Requires:	%{libply_boot_client} = %{EVRD}
Requires:	%{libply_splash_graphics} = %{EVRD}
Requires:	%{libply_splash_core} = %{EVRD}

%description -n %{libply}
This package contains the libply library used by Plymouth.

%package -n %{libply_boot_client}
Summary:	Plymouth libraries
Group:		System/Libraries
Requires:	%{libply} = %{EVRD}
Obsoletes:	%{_lib}ply-boot-client2 < 0.9.0-11

%description -n %{libply_boot_client}
This package contains the libply-boot-client library used by Plymouth.

%package -n %{libply_splash_graphics}
Summary:	Plymouth libraries
Group:		System/Libraries
Requires:	%{libply} = %{EVRD}
Obsoletes:	%{_lib}ply-splash-graphics2 < 0.9.0-11

%description -n %{libply_splash_graphics}
This package contains the libply-splash-graphic library used by Plymouth.

%package -n %{libply_splash_core}
Summary:	Plymouth libraries
Group:		System/Libraries
Requires:	%{libply} = %{EVRD}
Obsoletes:	%{_lib}ply-splash-core2 < 0.9.0-11

%description -n %{libply_splash_core}
This package contains the libply-splash-core library used by Plymouth.

%package -n uclibc-%{libname}
Summary:	Plymouth libraries
Group:		System/Libraries
Conflicts:	%{_lib}plymouth2 < 0.9.0-11

%description -n uclibc-%{libname}
This package contains the libply and libplybootsplash libraries
used by Plymouth.

%package -n %{devname}
Group:		System/Kernel and hardware
Summary:	Libraries and headers for writing Plymouth splash plugins
Group:		Development/C
Provides:	%{name}-devel = %{EVRD}
Requires:	%{libply} = %{EVRD}
Requires:	%{libply_boot_client} = %{EVRD}
Requires:	%{libply_splash_graphics} = %{EVRD}
Requires:	%{libply_splash_core} = %{EVRD}
%if %{with uclibc}
Requires:	uclibc-%{libname} = %{EVRD}
%endif

%description -n %{devname}
This package contains the libply and libplybootsplash libraries
and headers needed to develop 3rd party splash plugins for Plymouth.

%package scripts
Group:		System/Kernel and hardware
Summary:	Plymouth related scripts
Conflicts:	mkinitrd < 6.0.92-6mdv
Requires(pre):	%{name} = %{EVRD}

%description scripts
This package contains scripts that help integrate Plymouth with
the system.

%package plugin-label
Group:		System/Kernel and hardware
Summary:	Plymouth label plugin

%description plugin-label
This package contains the label control plugin for
Plymouth. It provides the ability to render text on
graphical boot splashes using pango and cairo.

%package plugin-fade-throbber
Group:		System/Kernel and hardware
Summary:	Plymouth "Fade-Throbber" plugin

%description plugin-fade-throbber
This package contains the "Fade-In" boot splash plugin for
Plymouth. It features a centered image that fades in and out
while other images pulsate around during system boot up.

%package plugin-script
Group:		System/Kernel and hardware
Summary:	Plymouth "Script" plugin
Requires:	plymouth-plugin-label = %{EVRD}

%description plugin-script
This package contains the "Script" plugin for Plymouth. 

%package theme-script
Group:		System/Kernel and hardware
Summary:	Plymouth "Script" theme
Requires:	%{name}-plugin-script = %{EVRD}
Requires(post):	plymouth-scripts = %{EVRD}

%description theme-script
This package contains the "Script" boot splash theme for
Plymouth.

%package theme-fade-in
Group:		System/Kernel and hardware
Summary:	Plymouth "Fade-In" theme
Requires:	%{name}-plugin-fade-throbber = %{EVRD}
Requires(post):	plymouth-scripts = %{EVRD}

%description theme-fade-in
This package contains the "Fade-In" boot splash theme for
Plymouth. It features a centered logo that fades in and out
while stars twinkle around the logo during system boot up.

%package plugin-throbgress
Group:		System/Kernel and hardware
Summary:	Plymouth "Throbgress" plugin
Requires:	plymouth-plugin-label = %{EVRD}

%description plugin-throbgress
This package contains the "throbgress" boot splash plugin for
Plymouth. It features a centered logo and animated spinner that
spins repeatedly while a progress bar advances at the bottom of
the screen.

%package theme-spinfinity
Group:		System/Kernel and hardware
Summary:	Plymouth "Spinfinity" theme
Requires:	%{name}-plugin-throbgress = %{EVRD}
Requires(post):	plymouth-scripts = %{EVRD}

%description theme-spinfinity
This package contains the "Spinfinity" boot splash theme for
Plymouth. It features a centered logo and animated spinner that
spins in the shape of an infinity sign.

%package theme-spinner
Group:		System/Kernel and hardware
Summary:	Plymouth "Spinner" theme
Requires:	%{name}-plugin-two-step = %{EVRD}
Requires(post):	plymouth-scripts = %{EVRD}

%description theme-spinner
This package contains the "Spinner" boot splash theme for
Plymouth.

%package plugin-two-step
Group:		System/Kernel and hardware
Summary:	Plymouth "two-step" plugin
Requires:	plymouth-plugin-label = %{EVRD}

%description plugin-two-step
This package contains the "two-step" boot splash plugin for
Plymouth. It features a two phased boot process that starts with
a progressing animation synced to boot time and finishes with a
short, fast one-shot animation.

%package plugin-space-flares
Group:		System/Kernel and hardware
Summary:	Plymouth "space-flares" plugin
Requires:	plymouth-plugin-label = %{EVRD}

%description plugin-space-flares
This package contains the "space-flares" boot splash plugin for
Plymouth. It features a corner image with animated flares.

%package theme-solar
Group:		System/Kernel and hardware
Summary:	Plymouth "Solar" theme
Requires:	%{name}-plugin-space-flares = %{EVRD}
Requires(post):	plymouth-scripts = %{EVRD}

%description theme-solar
This package contains the "Solar" boot splash theme for
Plymouth. It features a blue flamed sun with animated solar flares.

%package theme-charge
Group:		System/Kernel and hardware
Summary:	Plymouth "Charge" plugin
Requires:	%{name}-plugin-two-step = %{EVRD}
Requires(post):	plymouth-scripts = %{EVRD}

%description theme-charge
This package contains the "charge" boot splash theme for
Plymouth. It features the shadowy hull of a logo charge up and
and finally burst into full form.

%package theme-glow
Group:		System/Kernel and hardware
Summary:	Plymouth "Glow" plugin
Requires(post):	plymouth-scripts  = %{EVRD}
Requires:	plymouth-plugin-two-step = %{EVRD}

%description theme-glow
This package contains the "Glow" boot splash theme for Plymouth.

%package plugin-tribar
Group:		System/Kernel and hardware
Summary:	Plymouth "tribar" plugin
Requires:	plymouth-plugin-label = %{EVRD}

%description plugin-tribar
This package contains the "tribar" boot splash plugin for
Plymouth.

%package theme-tribar
Group:		System/Kernel and hardware
Summary:	Plymouth "Tribar" plugin
Requires(post):	plymouth-scripts  = %{EVRD}
Requires:	plymouth-plugin-tribar = %{EVRD}

%description theme-tribar
This package contains the "Tribar" boot splash theme for Plymouth.

%prep
%setup -q
%apply_patches

%if %{snapshot}
sh ./autogen.sh
libtoolize --copy --force
autoreconf -fi
make distclean
%endif


%build
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
	--disable-tests \
	--with-logo=%{_datadir}/plymouth/themes/OpenMandriva/openmandriva-logo.png \
	--with-background-start-color-stop=0x0073B3 \
	--with-background-end-color-stop=0x00457E \
	--with-background-color=0x3391cd \
	--disable-gdm-transition \
	--without-gdm-autostart-file \
	--without-rhgb-compat-link \
	--with-system-root-install \
	--enable-systemd-integration \
	--enable-pango \
	--enable-gtk=no \
%if %mdvver >= 201200
	--with-release-file=/etc/os-release \
%else
	--with-release-file=/etc/mandriva-release \
%endif
	--without-log-viewer

# We don't build these for uclibc since they link against a lot of libraries
# that we don't provide any uclibc linked version of
sed -e 's#viewer##g' -i src/Makefile
sed -e 's#label##g' -i src/plugins/controls/Makefile
%make
popd
%endif

mkdir -p system
pushd system
%configure \
	--disable-static \
	--disable-tests \
	--disable-tracing \
	--with-logo=%{_datadir}/plymouth/themes/OpenMandriva/openmandriva-logo.png \
	--with-background-start-color-stop=0x0073B3 \
	--with-background-end-color-stop=0x00457E \
	--with-background-color=0x3391cd \
	--enable-drm-renderer \
	--disable-gdm-transition \
	--without-gdm-autostart-file \
	--without-rhgb-compat-link \
	--with-system-root-install \
	--enable-systemd-integration \
	--enable-pango \
	--enable-gtk=no \
%if %mdvver >= 201200
	--with-release-file=/etc/os-release \
%else
	--with-release-file=/etc/mandriva-release \
%endif
	--without-log-viewer

%make
popd

%install
%if %{with uclibc}
%makeinstall_std -C uclibc plymouthdaemondir=%{uclibc_root}%{plymouthdaemon_execdir} plymouthclientdir=%{uclibc_root}%{plymouthclient_execdir}
rm -rf %{buildroot}%{uclibc_root}{%{_includedir},%{_datadir},%{_libdir}/pkgconfig,%{_libexecdir},%{plymouthdaemon_execdir}/plymouth-set-default-theme}
# What the.....
mv %{buildroot}/uclibc/usr/%{_lib}/* %{buildroot}%{uclibc_root}%{_libdir}/
rm -rf %{buildroot}/uclibc
%endif
%makeinstall_std -C system

# Temporary symlink until rc.sysinit is fixed
touch %{buildroot}%{_datadir}/plymouth/themes/default.plymouth

mkdir -p %{buildroot}%{_localstatedir}/lib/plymouth
cp %{SOURCE1} %{buildroot}%{_datadir}/plymouth/default-boot-duration
touch %{buildroot}%{_localstatedir}/lib/plymouth/{boot,shutdown}-duration

# Add charge
mkdir -p %{buildroot}%{_datadir}/plymouth/themes/charge
cp %{SOURCE2} %{buildroot}%{_datadir}/plymouth/themes/charge
cp %{buildroot}%{_datadir}/plymouth/themes/glow/{box,bullet,entry,lock}.png %{buildroot}%{_datadir}/plymouth/themes/charge

find %{buildroot} -name \*.a -delete -o -name \*.la -delete

%posttrans
[ -f %{_localstatedir}/lib/plymouth/boot-duration ] || cp -f %{_datadir}/plymouth/default-boot-duration %{_localstatedir}/lib/plymouth/boot-duration
if [ "x$DURING_INSTALL" = "x" ]; then
  if [ $1 -eq 1 ]; then
   /usr/libexec/plymouth/plymouth-update-initrd
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
%{_libdir}/plymouth/details.so
%{_libdir}/plymouth/text.so
%{_mandir}/man1/plymouth.1*
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

%files -n %{libply}
%{plymouth_libdir}/libply.so.%{major}*

%files -n %{libply_boot_client}
%{_libdir}/libply-boot-client.so.%{major}*

%files -n %{libply_splash_graphics}
%{_libdir}/libply-splash-graphics.so.%{major}*

%files -n %{libply_splash_core}
/%{_lib}/libply-splash-core.so.%{major}*

%if %{with uclibc}
%files -n uclibc-%{libname}
%dir %{uclibc_root}%{_libdir}/plymouth
%{uclibc_root}%{plymouth_libdir}/libply.so*
%{uclibc_root}%{_libdir}/libply-boot-client.so*
%{uclibc_root}%{_libdir}/libply-splash-core.so*
%{uclibc_root}%{_libdir}/libply-splash-graphics.so*
%{uclibc_root}%{_libdir}/plymouth/renderers
%endif

%files -n %{devname}
%{plymouth_libdir}/libply.so
%{_libdir}/libply-boot-client.so
%{_libdir}/libply-splash-graphics.so
/%{_lib}/libply-splash-core.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/plymouth-1

%files scripts
%{_sbindir}/plymouth-set-default-theme
%{_libexecdir}/plymouth
%{_mandir}/man1/plymouth-set-default-theme.1*

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

%files plugin-tribar
%{_libdir}/plymouth/tribar.so
%if %{with uclibc}
%{uclibc_root}%{_libdir}/plymouth/tribar.so
%endif

%files theme-tribar
%{_datadir}/plymouth/themes/tribar

%files theme-charge
%{_datadir}/plymouth/themes/charge

%files theme-glow
%{_datadir}/plymouth/themes/glow

%files system-theme

