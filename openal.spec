%define name		openal
%define version		0.0.8
%define	release		%mkrel 3
%define lib_name_orig	lib%{name}
%define lib_major	0
%define lib_name	%mklibname %{name} %{lib_major}
%define	lib_name_devel	%mklibname %{name} %{lib_major} -d

Name:		%{name}
Summary:	3D Sound Library
Version:	%{version}
Release:	%{release}
License:	LGPL
Source:		http://www.openal.org/openal_webstf/downloads/%{name}-%{version}.tar.gz
Patch0:		openal-0.0.8-requirements.patch
URL:		http://www.openal.org/
Group:		Sound
Requires(post):	info-install
Requires(preun):	info-install
BuildRequires:	esound-devel arts-devel smpeg-devel texinfo SDL-devel oggvorbis-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
OpenAL is a free 3D-audio library, with a programming interface similar
to that of OpenGL.

%package -n	%{lib_name}
Summary:	Main library for OpenAL, a free 3D sound library
Group:		Sound
Provides:	%{name} = %{version}-%{release}

%description -n	%{lib_name}
This package contains the library needed to run programs dynamically
linked with OpenAL.

%package -n	%{lib_name_devel}
Summary:	Headers for developing programs that will use OpenAL
Group:		Development/C

Requires:	%{lib_name} = %{version}
Provides:	%{lib_name_orig}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{lib_name_devel}
This package contains the headers that programmers will need to develop
applications which will use OpenAL, a free 3D audio library.

%prep
%setup -q
%patch0 -p1 -b .requirements

%build
CFLAGS="$RPM_OPT_FLAGS -O3" \
%configure2_5x	--enable-alsa \
		--enable-alsa-dlopen \
		--enable-arts \
		--enable-arts-dlopen \
		--enable-esd \
		--enable-esd-dlopen \
		--enable-waveout \
		--enable-null \
		--enable-sdl \
		--enable-vorbis \
		--enable-smpeg \
		--enable-capture \
		--enable-optimization \
		--disable-debug
%make

%install
rm -rf %{buildroot}
%makeinstall
%multiarch_binaries $RPM_BUILD_ROOT%{_bindir}/%{name}-config

install -d %{buildroot}%{_sysconfdir}
cat << EOF > %{buildroot}%{_sysconfdir}/openalrc
(define devices '(native alsa sdl esd arts null))
EOF

%clean
rm -rf %{buildroot}

%post -n	%{lib_name} -p /sbin/ldconfig

%post -n	%{lib_name}-devel
%_install_info %{name}.info

%preun -n	%{lib_name}-devel
%_remove_install_info %{name}.info

%postun -n	%{lib_name} -p /sbin/ldconfig

%files -n	%{lib_name}
%defattr(644,root,root,0755)
%doc AUTHORS ChangeLog NEWS NOTES README TODO
%config(noreplace) %{_sysconfdir}/openalrc
%defattr(755,root,root,0755)
%{_libdir}/*.so.*

%files -n	%{lib_name_devel}
%defattr(644,root,root,0755)
%{_includedir}/AL
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/pkgconfig/%{name}.pc
%defattr(755,root,root,0755)
%{_libdir}/*.so
%{_bindir}/%{name}-config
%{multiarch_bindir}/%{name}-config


