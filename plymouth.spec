%define plymouthdaemon_execdir /sbin
%define plymouthclient_execdir /bin
%define plymouth_libdir /%{_lib}

%define snapshot 20090515
%define build_gdm 0

%define lib_major 0
%define lib_name %mklibname %{name} %{lib_major}
%define lib_name_devel %mklibname %{name} -d

Summary: Graphical Boot Animation and Logger
Name: plymouth
Version: 0.7.0
Release: %mkrel 0.%{snapshot}.1
License: GPLv2+
Group: System/Kernel and hardware
Source0: http://freedesktop.org/software/plymouth/releases/%{name}-%{version}.tar.bz2
Source1: boot-duration
Source2: charge.plymouth

URL: http://freedesktop.org/software/plymouth/releases
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

Requires(post): plymouth-scripts
Requires: initscripts >= 8.83-1
BuildRequires: gtk2-devel
BuildRequires: pango-devel >= 1.21.0
BuildRequires: cairo-devel
BuildRequires: libpng-devel

%description
Plymouth provides an attractive graphical boot animation in
place of the text messages that normally get shown.  Text
messages are instead redirected to a log file for viewing
after boot.

%package system-theme
Group: System/Kernel and hardware
Summary: Plymouth default theme
Requires: plymouth(system-theme) = %{version}-%{release}

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
Requires: %{name} = %{version}-%{release}

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
Requires: nash

%description scripts
This package contains scripts that help integrate Plymouth with
the system.

%if %{build_gdm}
%package gdm-hooks
Group: System/Kernel and hardware
Summary: Plymouth GDM integration
Requires: gdm >= 2.22.0
Requires: plymouth-utils
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

%package theme-fade-in
Group: System/Kernel and hardware
Summary: Plymouth "Fade-In" theme
Requires: %{name}-plugin-fade-throbber = %{version}-%{release}
Requires(post): plymouth-scripts

%description theme-fade-in
This package contains the "Fade-In" boot splash theme for
Plymouth. It features a centered logo that fades in and out
while stars twinkle around the logo during system boot up.

%package plugin-throbgress
Group: System/Kernel and hardware
Summary: Plymouth "Throbgress" plugin
Requires: %{lib_name} = %{version}-%{release}
Requires: plymouth-plugin-label

%description plugin-throbgress
This package contains the "throbgress" boot splash plugin for
Plymouth. It features a centered logo and animated spinner that
spins repeatedly while a progress bar advances at the bottom of
the screen.

%package theme-spinfinity
Group: System/Kernel and hardware
Summary: Plymouth "Spinfinity" theme
Requires: %{name}-plugin-throbgress = %{version}-%{release}
Requires(post): plymouth-scripts

%description theme-spinfinity
This package contains the "Spinfinity" boot splash theme for
Plymouth. It features a centered logo and animated spinner that
spins in the shape of an infinity sign.

%package plugin-space-flares
Group: System/Kernel and hardware
Summary: Plymouth "space-flares" plugin
Requires: %{lib_name} = %{version}-%{release}
Requires: plymouth-plugin-label

%description plugin-space-flares
This package contains the "space-flares" boot splash plugin for
Plymouth. It features a corner image with animated flares.

%package theme-solar
Group: System/Kernel and hardware
Summary: Plymouth "Solar" theme
Requires: %{name}-plugin-space-flares = %{version}-%{release}
Requires(post): plymouth-scripts

%description theme-solar
This package contains the "Solar" boot splash theme for
Plymouth. It features a blue flamed sun with animated solar flares.

%package plugin-two-step
Group: System/Kernel and hardware
Summary: Plymouth "two-step" plugin
Requires: %{lib_name} = %{version}-%{release}
Requires: plymouth-plugin-label

%description plugin-two-step
This package contains the "two-step" boot splash plugin for
Plymouth. It features a two phased boot process that starts with
a progressing animation synced to boot time and finishes with a
short, fast one-shot animation.

%package theme-charge
Group: System/Kernel and hardware
Summary: Plymouth "Charge" plugin
Requires: %{name}-plugin-two-step = %{version}-%{release}
Requires(post): plymouth-scripts
Provides: plymouth(system-theme) = %{version}-%{release}

%description theme-charge
This package contains the "charge" boot splash theme for
Plymouth. It features the shadowy hull of a logo charge up and
and finally burst into full form.

%package theme-glow
Group: System/Kernel and hardware
Summary: Plymouth "Glow" plugin
Requires(post): plymouth-scripts

%description theme-glow
This package contains the "Glow" boot splash theme for Plymouth.

%prep
%setup -q

%build
%configure2_5x --enable-tracing --disable-tests --without-boot-entry	\
	--without-default-plugin					\
	--with-logo=%{_datadir}/pixmaps/system-logo-white.png		\
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
	--with-system-root-install

%make

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall_std

find $RPM_BUILD_ROOT -name '*.a' -exec rm -f {} \;
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} \;

# Temporary symlink until rc.sysinit is fixed
(cd $RPM_BUILD_ROOT%{_bindir}; ln -s ../../bin/plymouth)

mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/lib/plymouth
cp %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/plymouth/default-boot-duration
cp %{SOURCE1} $RPM_BUILD_ROOT%{_localstatedir}/lib/plymouth

# Add charge
mkdir -p $RPM_BUILD_ROOT%{_datadir}/plymouth/themes/charge
cp %{SOURCE2} $RPM_BUILD_ROOT%{_datadir}/plymouth/themes/charge
cp $RPM_BUILD_ROOT%{_datadir}/plymouth/themes/glow/{box,bullet,entry,lock}.png $RPM_BUILD_ROOT%{_datadir}/plymouth/themes/charge

#rm -rf $RPM_BUILD_ROOT%{_datadir}/plymouth/themes/glow

%clean
rm -rf $RPM_BUILD_ROOT

%postun
if [ $1 -eq 0 ]; then
    rm -f %{_libdir}/plymouth/default.so
fi

%postun theme-spinfinity
export LIB=%{_lib}
if [ $1 -eq 0 ]; then
    if [ "$(%{_sbindir}/plymouth-set-default-theme)" == "spinfinity" ]; then
        %{_sbindir}/plymouth-set-default-theme text
    fi
fi

%postun theme-fade-in
export LIB=%{_lib}
if [ $1 -eq 0 ]; then
    if [ "$(%{_sbindir}/plymouth-set-default-theme)" == "fade-in" ]; then
        %{_sbindir}/plymouth-set-default-theme --reset
    fi
fi

%postun theme-solar
export LIB=%{_lib}
if [ $1 -eq 0 ]; then
    if [ "$(%{_sbindir}/plymouth-set-default-theme)" == "solar" ]; then
        %{_sbindir}/plymouth-set-default-theme --reset
    fi
fi

%post theme-charge
export LIB=%{_lib}
if [ $1 -eq 1 ]; then
    %{_sbindir}/plymouth-set-default-theme charge
else
    if [ "$(%{_sbindir}/plymouth-set-default-theme)" == "solar" ]; then
        %{_sbindir}/plymouth-set-default-theme charge
    fi
fi

%postun theme-charge
export LIB=%{_lib}
if [ $1 -eq 0 ]; then
    if [ "$(%{_sbindir}/plymouth-set-default-theme)" == "charge" ]; then
        %{_sbindir}/plymouth-set-default-theme --reset
    fi
fi

%post theme-glow
export LIB=%{_lib}
if [ $1 -eq 1 ]; then
    %{_sbindir}/plymouth-set-default-theme glow
else
    if [ "$(%{_sbindir}/plymouth-set-default-theme)" == "solar" ]; then
        %{_sbindir}/plymouth-set-default-theme glow
    fi
fi

%postun theme-glow
export LIB=%{_lib}
if [ $1 -eq 0 ]; then
    if [ "$(%{_sbindir}/plymouth-set-default-theme)" == "glow" ]; then
        %{_sbindir}/plymouth-set-default-theme --reset
    fi
fi

%files
%defattr(-, root, root)
%doc AUTHORS NEWS README
%dir %{_datadir}/plymouth
%dir %{_datadir}/plymouth/themes
%dir %{_libexecdir}/plymouth
%dir %{_localstatedir}/lib/plymouth
%{plymouthdaemon_execdir}/plymouthd
%{plymouthclient_execdir}/plymouth
%{_bindir}/plymouth
%{_libdir}/plymouth/details.so
%{_libdir}/plymouth/text.so
%{_datadir}/plymouth/default-boot-duration
%{_datadir}/plymouth/themes/details/details.plymouth
%{_datadir}/plymouth/themes/text/text.plymouth
%{_localstatedir}/run/plymouth
%{_localstatedir}/spool/plymouth
%ghost %{_localstatedir}/lib/plymouth/boot-duration

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

%files scripts
%defattr(-, root, root)
%{_sbindir}/plymouth-set-default-theme
%{_libexecdir}/plymouth/plymouth-update-initrd
%{_libexecdir}/plymouth/plymouth-populate-initrd

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

%files theme-fade-in
%defattr(-, root, root)
%{_datadir}/plymouth/themes/fade-in

%files plugin-throbgress
%defattr(-, root, root)
%{_libdir}/plymouth/throbgress.so

%files theme-spinfinity
%defattr(-, root, root)
%{_datadir}/plymouth/themes/spinfinity

%files plugin-space-flares
%defattr(-, root, root)
%{_libdir}/plymouth/space-flares.so

%files theme-solar
%defattr(-, root, root)
%{_datadir}/plymouth/themes/solar

%files plugin-two-step
%defattr(-, root, root)
%{_libdir}/plymouth/two-step.so

%files theme-charge
%defattr(-, root, root)
%{_datadir}/plymouth/themes/charge

%files theme-glow
%defattr(-, root, root)
%{_datadir}/plymouth/themes/glow

%files system-theme
%defattr(-, root, root)
