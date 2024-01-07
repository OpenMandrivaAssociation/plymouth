%global optflags %{optflags} -O2

%define major 5
%define libname %mklibname %{name} %{major}
%define libply %mklibname ply %{major}
%define libply_boot_client %mklibname ply-boot-client %{major}
%define libply_splash_graphics %mklibname ply-splash-graphics %{major}
%define libply_splash_core %mklibname ply-splash-core %{major}
%define devname %mklibname %{name} -d

#define snapshot %{nil}

%bcond_with x11_renderer

Summary:	Graphical Boot Animation and Logger
Name:		plymouth
Version:	24.004.60
#if %snapshot
#Release:	0.%{snapshot}.4
# git clone https://gitlab.freedesktop.org/plymouth/plymouth.git
# git archive --format=tar --prefix plymouth-22.02.122-$(date +%Y%m%d)/ HEAD | xz -vf -T0 -9e > plymouth-22.02.122-$(date +%Y%m%d).tar.xz
#Source0:	%{name}-%{version}-%{snapshot}.tar.xz
#else
Release:	1
Source0:	http://www.freedesktop.org/software/plymouth/releases/%{name}-%{version}.tar.xz
#endif
License:	GPLv2+
Group:		System/Kernel and hardware
Url:		http://www.freedesktop.org/wiki/Software/Plymouth
Source2:	charge.plymouth
# use kernel-install if systemd-boot is used
Patch0:		plymouth-0.9.3-use-kernel-install.patch
# OpenMandriva default theme
%ifnarch %{armx} %{riscv}
Patch2:		%{name}-0.9.3-set-OpenMandriva-theme.patch
%else
Patch2:		%{name}-0.9.3-set-OpenMandriva-theme-armx.patch
%endif
#(tpg) these days nobody even does not know what is /var/log/boot.log
Patch3:		plymouth-0.9.4-by-default-disable-boot-log.patch
Patch4:		plymouth-fix-generate-version-script.patch

# UPSTREAM GIT PATCHES

BuildRequires:	meson
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(libdrm)
BuildRequires:	pkgconfig(libudev)
BuildRequires:	pkgconfig(libevdev)
BuildRequires:	pkgconfig(xkbcommon)
BuildRequires:	pkgconfig(xkeyboard-config)
%if %{with x11_renderer}
BuildRequires:	pkgconfig(gtk+-3.0)
%endif
BuildRequires:	pkgconfig(libsystemd)
BuildRequires:	systemd-rpm-macros
# (tpg) needed for udevadm and systemd-tty-ask-password-agent
BuildRequires:	systemd
# (tpg) needed for watermark.png and bgrt-fallback.png
BuildRequires:	distro-release-theme
#if %{snapshot}
#BuildRequires:	intltool
#BuildRequires:	xsltproc
#BuildRequires:	git
#endif
%rename		splashy
Conflicts:	systemd-units < 186
%rename	plymouth-utils
Requires:	%{name}-scripts

%description
Plymouth provides an attractive graphical boot animation in
place of the text messages that normally get shown.  Text
messages are instead redirected to a log file for viewing
after boot.

%package system-theme
Group:		System/Kernel and hardware
Summary:	Plymouth default theme
Requires:	plymouth(system-theme)
Requires:	%{name} = %{EVRD}

%description system-theme
This metapackage tracks the current distribution default theme.

%package -n %{libply}
Summary:	Plymouth libraries
Group:		System/Libraries
Obsoletes:	%{_lib}ply2 < 0.9.0-11
Provides:	%{_lib}ply2 = 0.9.0-11
Requires:	%{libply_boot_client} = %{EVRD}

%description -n %{libply}
This package contains the libply library used by Plymouth.

%package -n %{libply_boot_client}
Summary:	Plymouth libraries
Group:		System/Libraries
Obsoletes:	%{_lib}ply-boot-client2 < 0.9.0-11
Provides:	%{_lib}ply-boot-client2 = 0.9.0-11

%description -n %{libply_boot_client}
This package contains the libply-boot-client library used by Plymouth.

%package -n %{libply_splash_graphics}
Summary:	Plymouth libraries
Group:		System/Libraries
Obsoletes:	%{_lib}ply-splash-graphics2 < 0.9.0-11
Provides:	%{_lib}ply-splash-graphics2 = 0.9.0-11

%description -n %{libply_splash_graphics}
This package contains the libply-splash-graphic library used by Plymouth.

%package -n %{libply_splash_core}
Summary:	Plymouth libraries
Group:		System/Libraries
Obsoletes:	%{_lib}ply-splash-core2 < 0.9.0-11
Provides:	%{_lib}ply-splash-core2 = 0.9.0-11

%description -n %{libply_splash_core}
This package contains the libply-splash-core library used by Plymouth.

%package -n %{devname}
Summary:	Libraries and headers for writing Plymouth splash plugins
Group:		Development/C
Provides:	%{name}-devel = %{EVRD}
Requires:	%{libply} = %{EVRD}
Requires:	%{libply_boot_client} = %{EVRD}
Requires:	%{libply_splash_graphics} = %{EVRD}
Requires:	%{libply_splash_core} = %{EVRD}

%description -n %{devname}
This package contains the libply and libplybootsplash libraries
and headers needed to develop 3rd party splash plugins for Plymouth.

%package scripts
Group:		System/Kernel and hardware
Summary:	Plymouth related scripts
BuildArch:	noarch
Requires:	findutils
Requires:	coreutils
Requires:	pigz
Requires:	cpio
Requires:	dracut
Requires:	awk
Requires:	%{name} = %{EVRD}
Provides:	bootsplash = 3.4.3
Obsoletes:	bootsplash < 3.4.3
Conflicts:	bootsplash < 3.4.3

%description scripts
This package contains scripts that help integrate Plymouth with
the system.

%package plugin-label
Group:		System/Kernel and hardware
Summary:	Plymouth label plugin
Requires:	%{name}
Requires:	%{libply_splash_graphics}

%description plugin-label
This package contains the label control plugin for
Plymouth. It provides the ability to render text on
graphical boot splashes using freetype.

%package plugin-fade-throbber
Group:		System/Kernel and hardware
Summary:	Plymouth "Fade-Throbber" plugin
Requires:	%{name}
Requires:	%{libply_splash_core}
Requires:	%{libply_splash_graphics}

%description plugin-fade-throbber
This package contains the "Fade-In" boot splash plugin for
Plymouth. It features a centered image that fades in and out
while other images pulsate around during system boot up.

%package plugin-script
Group:		System/Kernel and hardware
Summary:	Plymouth "Script" plugin
Requires:	%{libply_splash_core}
Requires:	%{libply_splash_graphics}

%description plugin-script
This package contains the "Script" plugin for Plymouth. 

%package plugin-two-step
Group:		System/Kernel and hardware
Summary:	Plymouth "two-step" plugin
Requires:	%{libply_splash_core}
Requires:	%{name}-plugin-label = %{version}
%rename %{name}-plugin-throbgress

%description plugin-two-step
This package contains the "two-step" boot splash plugin for
Plymouth. It features a two phased boot process that starts with
a progressing animation synced to boot time and finishes with a
short, fast one-shot animation.

%package plugin-space-flares
Group:		System/Kernel and hardware
Summary:	Plymouth "space-flares" plugin
Requires:	%{libply_splash_core}
Requires:	%{name}-plugin-label = %{version}

%description plugin-space-flares
This package contains the "space-flares" boot splash plugin for
Plymouth. It features a corner image with animated flares.

%package plugin-tribar
Group:		System/Kernel and hardware
Summary:	Plymouth "Tribar" plugin
Requires:	%{libply_splash_core}
Requires:	%{libply_splash_graphics}

%description plugin-tribar
This package contains the "tribar" boot splash plugin for
Plymouth.

%package theme-script
Group:		System/Kernel and hardware
Summary:	Plymouth "Script" theme
BuildArch:	noarch
Requires:	%{name}-plugin-script = %{version}
Requires(post):	%{name}-scripts

%description theme-script
This package contains the "Script" boot splash theme for
Plymouth.

%package theme-fade-in
Group:		System/Kernel and hardware
Summary:	Plymouth "Fade-In" theme
BuildArch:	noarch
Requires:	%{name}-plugin-fade-throbber = %{version}
Requires:	%{name}-plugin-label = %{version}
Requires(post):	%{name}-scripts

%description theme-fade-in
This package contains the "Fade-In" boot splash theme for
Plymouth. It features a centered logo that fades in and out
while stars twinkle around the logo during system boot up.

%package theme-spinfinity
Group:		System/Kernel and hardware
Summary:	Plymouth "Spinfinity" theme
BuildArch:	noarch
Requires:	%{name}-plugin-two-step = %{version}
Requires(post):	%{name}-scripts

%description theme-spinfinity
This package contains the "Spinfinity" boot splash theme for
Plymouth. It features a centered logo and animated spinner that
spins in the shape of an infinity sign.

%package theme-bgrt
Group:		System/Kernel and hardware
Summary:	Plymouth "BGRT" and "Spinner" theme
BuildArch:	noarch
Requires:	abattis-cantarell-fonts
Requires:	%{name}-plugin-two-step = %{version}
Requires(post):	%{name}-scripts
%ifarch %{armx} %{riscv}
Provides:	plymouth(system-theme) = %{EVRD}
%endif
# no need to provide a separate package for this, ass difference is on one file
%rename %{name}-theme-spinner

%description theme-bgrt
This package contains the "BGRT" and "Spinner" boot splash theme for
Plymouth.

%package theme-solar
Group:		System/Kernel and hardware
Summary:	Plymouth "Solar" theme
BuildArch:	noarch
Requires:	%{name}-plugin-space-flares = %{version}
Requires(post):	%{name}-scripts

%description theme-solar
This package contains the "Solar" boot splash theme for
Plymouth. It features a blue flamed sun with animated solar flares.

%package theme-charge
Group:		System/Kernel and hardware
Summary:	Plymouth "Charge" plugin
BuildArch:	noarch
Requires:	%{name}-plugin-two-step = %{version}
Requires(post):	%{name}-scripts

%description theme-charge
This package contains the "charge" boot splash theme for
Plymouth. It features the shadowy hull of a logo charge up and
and finally burst into full form.

%package theme-glow
Group:		System/Kernel and hardware
Summary:	Plymouth "Glow" plugin
BuildArch:	noarch
Requires:	%{name}-plugin-two-step = %{version}
Requires(post):	%{name}-scripts

%description theme-glow
This package contains the "Glow" boot splash theme for Plymouth.

%package theme-tribar
Group:		System/Kernel and hardware
Summary:	Plymouth "Tribar" plugin
BuildArch:	noarch
Requires:	%{name}-plugin-tribar = %{version}
Requires(post):	%{name}-scripts

%description theme-tribar
This package contains the "Tribar" boot splash theme for Plymouth.

%prep
#if %{snapshot}
#autosetup -n %{name}-%{version}-%{snapshot} -p1
#else
%autosetup -p1
#endif

%build
%meson \
    -Dlogo="%{_datadir}/pixmaps/system-logo-white.png" \
    -Dtracing=false \
    -Dpango=disabled \
%if %{without x11_renderer}
    -Dgtk=disabled \
%endif
    -Ddocs=false

%meson_build -C build

%install
%meson_install -C build

# Add charge
mkdir -p %{buildroot}%{_datadir}/plymouth/themes/charge
cp %{SOURCE2} %{buildroot}%{_datadir}/plymouth/themes/charge
cp %{buildroot}%{_datadir}/plymouth/themes/glow/{box,bullet,entry,lock}.png %{buildroot}%{_datadir}/plymouth/themes/charge

find %{buildroot} -name \*.a -delete -o -name \*.la -delete

# (tpg) add watermark to all the themes that relies on two-step plugin
for i in bgrt charge glow spinfinity spinner; do
    cp %{_datadir}/pixmaps/system-logo-white.png %{buildroot}%{_datadir}/plymouth/themes/$i/watermark.png
done

# (tpg) display something if BGRT image is empty
for i in bgrt spinner; do
    cp %{_datadir}/pixmaps/system-logo-white.png %{buildroot}%{_datadir}/plymouth/themes/$i/bgrt-fallback.png
done

%find_lang %{name}

%define theme_scripts() \
%post -n %{name}-theme-%{1} \
if [ -x %{_sbindir}/plymouth-set-default-theme ]; then \
  export LIB=%{_lib} \
  if [ $1 -eq 1 ]; then \
      %{_sbindir}/plymouth-set-default-theme --rebuild-initrd %{1} \
  else \
      THEME=$(%{_sbindir}/plymouth-set-default-theme) \
      if [ "$THEME" = "text" ] || [ "$THEME" = "%{1}" ]; then \
          %{_sbindir}/plymouth-set-default-theme --rebuild-initrd %{1} \
      fi \
  fi \
fi \
\
%postun -n %{name}-theme-%{1} \
export LIB=%{_lib} \
if [ $1 -eq 0 ] && [ -x %{_sbindir}/plymouth-set-default-theme ]; then \
    if [ "$(%{_sbindir}/plymouth-set-default-theme)" = "%{1}" ]; then \
        %{_sbindir}/plymouth-set-default-theme --reset --rebuild-initrd \
    fi \
fi \

%theme_scripts spinfinity
%theme_scripts fade-in
%theme_scripts solar
%theme_scripts charge
%theme_scripts glow
%theme_scripts script

%files -f %{name}.lang
%doc AUTHORS README.md
%config(noreplace) %{_sysconfdir}/plymouth
%dir %{_datadir}/plymouth
%dir %{_datadir}/plymouth/themes
%dir %{_datadir}/plymouth/themes/details
%dir %{_datadir}/plymouth/themes/text
%dir %{_libdir}/plymouth
%dir %{_libdir}/plymouth/renderers
%dir %{_libexecdir}/plymouth
%dir %{_localstatedir}/lib/plymouth
%{_sbindir}/plymouthd
%{_bindir}/plymouth
%{_libexecdir}/plymouth/plymouthd-fd-escrow
%{_sysconfdir}/logrotate.d/bootlog
%{_libdir}/plymouth/details.so
%{_libdir}/plymouth/text.so
%{_unitdir}/*plymouth*.service
%{_unitdir}/systemd-*.path
%{_unitdir}/*.wants/plymouth-*.service
%{_datadir}/plymouth/plymouthd.defaults
%{_datadir}/plymouth/themes/details/details.plymouth
%{_datadir}/plymouth/themes/text/text.plymouth
%{_localstatedir}/spool/plymouth

%files -n %{libply}
%{_libdir}/libply.so.%{major}*

%files -n %{libply_boot_client}
%{_libdir}/libply-boot-client.so.%{major}*

%files -n %{libply_splash_graphics}
%{_libdir}/libply-splash-graphics.so.%{major}*
%{_libdir}/plymouth/renderers/drm*
%{_libdir}/plymouth/renderers/frame-buffer*
%if %{with x11_renderer}
%{_libdir}/plymouth/renderers/x11*
%endif

%files -n %{libply_splash_core}
%{_libdir}/libply-splash-core.so.%{major}*

%files -n %{devname}
%{_libdir}/libply.so
%{_libdir}/libply-boot-client.so
%{_libdir}/libply-splash-graphics.so
%{_libdir}/libply-splash-core.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/plymouth-1

%files scripts
%{_sbindir}/plymouth-set-default-theme
%{_libexecdir}/plymouth/plymouth-update-initrd
%{_libexecdir}/plymouth/plymouth-generate-initrd
%{_libexecdir}/plymouth/plymouth-populate-initrd

%files plugin-label
%{_libdir}/plymouth/label-freetype.so

%files plugin-fade-throbber
%{_libdir}/plymouth/fade-throbber.so

%files theme-fade-in
%{_datadir}/plymouth/themes/fade-in

%files plugin-script
%{_libdir}/plymouth/script.so

%files theme-script
%{_datadir}/plymouth/themes/script

%files theme-spinfinity
%{_datadir}/plymouth/themes/spinfinity

%files theme-bgrt
%{_datadir}/plymouth/themes/bgrt
%{_datadir}/plymouth/themes/spinner

%files plugin-space-flares
%{_libdir}/plymouth/space-flares.so

%files theme-solar
%{_datadir}/plymouth/themes/solar

%files plugin-two-step
%{_libdir}/plymouth/two-step.so

%files plugin-tribar
%{_libdir}/plymouth/tribar.so

%files theme-tribar
%{_datadir}/plymouth/themes/tribar

%files theme-charge
%{_datadir}/plymouth/themes/charge

%files theme-glow
%{_datadir}/plymouth/themes/glow

%files system-theme
