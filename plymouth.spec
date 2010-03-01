%define plymouthdaemon_execdir /sbin
%define plymouthclient_execdir /bin
%define plymouth_libdir /%{_lib}

%define _libexecdir %{_prefix}/libexec

%define build_gdm 0

%define lib_major 0
%define lib_name %mklibname %{name} %{lib_major}
%define lib_name_devel %mklibname %{name} -d

%define snapshot 0

%define         build_uclibc 0
%{?_with_uclibc: %global build_uclibc 1}

Summary: Graphical Boot Animation and Logger
Name: plymouth
Version: 0.7.2
Release: %mkrel 8
License: GPLv2+
Group: System/Kernel and hardware
Source0: http://freedesktop.org/software/plymouth/releases/%{name}-%{version}.tar.bz2
Source1: boot-duration
Source2: charge.plymouth
# (fc) 0.7.0-6mdv text support (Charlie Brej)
Patch2: text.patch
# (fc) 0.7.2-5mdv handle init= for shutdown and allow to force splash (fdo bug #22180)
Patch3: plymouth-0.7.2-handle-init.patch
# (fc) 0.7.2-6mdv backport array support (GIT)
Patch4: plymouth-0.7.2-array.patch
# (fc) 0.7.2-7mdv add onquit support (GIT)
Patch5: plymouth-0.7.2-onquit.patch
# (fc) 0.7.2-7mdv optimize image operations (Charles Brej)
Patch6: plymouth-0.7.2-optimize-image.patch
# (proyvind) 0.7.2-8mdv fix build with uclibc (should go upstream..)
Patch7:	plymouth-0.7.2-add-missing-header.patch
# (proyvind) 0.7.2-8mdv fix library link order for static linking (idem..)
Patch8: plymouth-0.7.2-library-link-order.patch
# (proyvind) 0.7.2-8mdv substitute /usr/lib with /lib rather than just stripping away
# /usr. This so that ie. /usr/uclibc/usr/lib will be be /usr/uclibc/lib rather than
# /uclibc/usr/lib. (should probably go upstream as well)
Patch9: plymouth-0.7.2-less-greedy-usr_lib-substitution.patch
# (proyvind) 0.7.2-8mdv specify absolute path to /bin/plymouth to ensure install
# location with uclibc
Patch10: plymouth-0.7.2-initrd-absolute-path.patch
# (fc) 0.7.2-8mdv shutdown tty should be tty1 (Mdv bug #55077)
Patch11: plymouth-0.7.2-shutdown-tty.patch

URL: http://freedesktop.org/software/plymouth/releases
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

Requires(post): plymouth-scripts = %{version}-%{release}
Requires: initscripts >= 8.83
Requires: desktop-common-data >= 2010.0-1mdv
BuildRequires: gtk2-devel
%if %{build_uclibc}
BuildRequires: uClibc-devel
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

%description -n %{lib_name}
This package contains the libply and libplybootsplash libraries
used by Plymouth.

%package -n %{lib_name_devel}
Group: System/Kernel and hardware
Summary: Libraries and headers for writing Plymouth splash plugins
Group: Development/C
Provides: %{name}-devel = %{version}-%{release}
Provides: lib%{name}-devel = %{version}-%{release}

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

%if %{build_gdm}
%package gdm-hooks
Group: System/Kernel and hardware
Summary: Plymouth GDM integration
Requires: gdm >= 2.22.0
Requires: plymouth-utils = %{version}-%{release}
Requires: %{name} = %{version}-%{release}

%description gdm-hooks
This package contains support files for integrating Plymouth with GDM
Namely, it adds hooks to show boot messages at the login screen in the
event start-up services fail.
%endif

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
%patch2 -p1 -b .text
%patch3 -p1 -b .handle-init
%patch4 -p1 -b .array
%patch5 -p1 -b .onquit
%patch6 -p1 -b .optimize-image
%patch11 -p1 -b .shutdown-tty
%if %{build_uclibc}
%patch7 -p1 -b .header~
%patch8 -p1 -b .link_order~
%patch9 -p1 -b .usrlib_subst~
%patch10 -p1 -b .abspath~
autoreconf --install --symlink
%endif


%build
export CONFIGURE_TOP=`pwd`
%if %{build_uclibc}
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
	--without-default-plugin					\
	--with-logo=%{_datadir}/icons/large/mandriva.png 		\
	--with-background-start-color-stop=0x0073B3			\
	--with-background-end-color-stop=0x00457E			\
	--with-background-color=0x3391cd				\
%if %{build_gdm}
	--enable-gdm-transition						\
%else
	--disable-gdm-transition					\
	--without-gdm-autostart-file					\
%endif
	--without-rhgb-compat-link					\
	--with-system-root-install 					\
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
	--without-default-plugin					\
	--with-logo=%{_datadir}/icons/large/mandriva.png 		\
	--with-background-start-color-stop=0x0073B3			\
	--with-background-end-color-stop=0x00457E			\
	--with-background-color=0x3391cd				\
%if %{build_gdm}
	--enable-gdm-transition						\
%else
	--disable-gdm-transition					\
	--without-gdm-autostart-file					\
%endif
	--without-rhgb-compat-link					\
	--with-system-root-install 					\
	--with-release-file=/etc/mandriva-release

%make
cd ..

%install
rm -rf $RPM_BUILD_ROOT

%if %{build_uclibc}
%makeinstall_std -C uclibc plymouthdaemondir=%{uclibc_root}%{plymouthdaemon_execdir} plymouthclientdir=%{uclibc_root}%{plymouthclient_execdir}
rm -rf %{buildroot}%{uclibc_root}{%{_includedir},%{_datadir},%{_libdir}/pkgconfig,%{_libexecdir},%{plymouthdaemon_execdir}/plymouth-set-default-theme}
%endif
%makeinstall_std -C system

find $RPM_BUILD_ROOT -name \*.a -delete -o -name \*.la -delete

# Temporary symlink until rc.sysinit is fixed
(cd $RPM_BUILD_ROOT%{_bindir}; ln -s ../../bin/plymouth)
touch $RPM_BUILD_ROOT%{_datadir}/plymouth/themes/default.plymouth

mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/lib/plymouth
cp %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/plymouth/default-boot-duration
touch $RPM_BUILD_ROOT%{_localstatedir}/lib/plymouth/{boot,shutdown}-duration

# Add charge
mkdir -p $RPM_BUILD_ROOT%{_datadir}/plymouth/themes/charge
cp %{SOURCE2} $RPM_BUILD_ROOT%{_datadir}/plymouth/themes/charge
cp $RPM_BUILD_ROOT%{_datadir}/plymouth/themes/glow/{box,bullet,entry,lock}.png $RPM_BUILD_ROOT%{_datadir}/plymouth/themes/charge

%clean
rm -rf $RPM_BUILD_ROOT

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
%dir %{_datadir}/plymouth
%dir %{_datadir}/plymouth/themes
%{_datadir}/plymouth/default-boot-duration
%dir %{_localstatedir}/lib/plymouth
%{plymouthdaemon_execdir}/plymouthd
%{plymouthclient_execdir}/plymouth
%{_bindir}/plymouth
%{_libdir}/plymouth/details.so
%{_libdir}/plymouth/text.so
%ghost %{_datadir}/plymouth/themes/default.plymouth
%{_datadir}/plymouth/themes/details
%{_datadir}/plymouth/themes/text
%{_localstatedir}/run/plymouth
%{_localstatedir}/spool/plymouth
%ghost %{_localstatedir}/lib/plymouth/shutdown-duration
%ghost %{_localstatedir}/lib/plymouth/boot-duration
%if %{build_uclibc}
%{uclibc_root}%{plymouthdaemon_execdir}/plymouthd
%{uclibc_root}%{plymouthclient_execdir}/plymouth
%{uclibc_root}%{_libdir}/plymouth/details.so
%{uclibc_root}%{_libdir}/plymouth/text.so
%endif

%files -n %{lib_name_devel}
%defattr(-, root, root)
%{plymouth_libdir}/libply.so
%{_libdir}/libplybootsplash.so
%{_libdir}/pkgconfig/plymouth-1.pc
%{_includedir}/plymouth-1

%files -n %{lib_name}
%defattr(-, root, root)
%{plymouth_libdir}/libply.so.*
%{_libdir}/libplybootsplash.so.*
%dir %{_libdir}/plymouth
%if %{build_uclibc}
%dir %{uclibc_root}%{_libdir}/plymouth
%{uclibc_root}%{plymouth_libdir}/libply.so*
%{uclibc_root}%{_libdir}/libplybootsplash.so*
%endif

%files scripts
%defattr(-, root, root)
%{_sbindir}/plymouth-set-default-theme
%{_libexecdir}/plymouth

%files utils
%defattr(-, root, root)
%{_bindir}/plymouth-log-viewer

%if %{build_gdm}
%files gdm-hooks
%defattr(-, root, root)
%{_datadir}/gdm/autostart/LoginWindow/plymouth-log-viewer.desktop
%endif

%files plugin-label
%defattr(-, root, root)
%{_libdir}/plymouth/label.so

%files plugin-fade-throbber
%defattr(-, root, root)
%{_libdir}/plymouth/fade-throbber.so
%if %{build_uclibc}
%{uclibc_root}%{_libdir}/plymouth/fade-throbber.so
%endif

%files theme-fade-in
%defattr(-, root, root)
%{_datadir}/plymouth/themes/fade-in

%files plugin-throbgress
%defattr(-, root, root)
%{_libdir}/plymouth/throbgress.so
%if %{build_uclibc}
%{uclibc_root}%{_libdir}/plymouth/throbgress.so
%endif

%files plugin-script
%defattr(-, root, root)
%{_libdir}/plymouth/script.so
%if %{build_uclibc}
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
%if %{build_uclibc}
%{uclibc_root}%{_libdir}/plymouth/space-flares.so
%endif

%files theme-solar
%defattr(-, root, root)
%{_datadir}/plymouth/themes/solar

%files plugin-two-step
%defattr(-, root, root)
%{_libdir}/plymouth/two-step.so
%if %{build_uclibc}
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
