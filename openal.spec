%define major 0
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

Name:		openal
Summary:	3D Sound Library
Version:	0.0.8
Release:	%mkrel 10
License:	LGPLv2
Group:		Sound
URL:		http://www.openal.org
Source:		http://www.openal.org/openal_webstf/downloads/%{name}-%{version}.tar.gz
Patch0:		%{name}-0.0.8-arch.patch
Patch1:		%{name}-0.0.8-pthread.patch
Patch2:		%{name}-0.0.8-pkgconfig.patch
Patch3:		%{name}-pause.patch
Patch4:		%{name}-x86_64-mmx.patch
Patch5:		fix_gcc-4.2.diff
# (fc) 0.0.8-8mdv fix dlopen for audio backends
Patch6:		openal-0.0.8-dlopen.patch
Patch7:		openal-0.0.8-fix-str-fmt.patch
Requires(post):	info-install
Requires(preun): info-install
BuildRequires:	esound-devel
BuildRequires:	smpeg-devel
BuildRequires:	texinfo
BuildRequires:	SDL-devel
BuildRequires:	oggvorbis-devel
Suggests:	libSDL
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
OpenAL is a free 3D-audio library, with a programming interface similar
to that of OpenGL.

%package -n %{libname}
Summary:	Main library for OpenAL, a free 3D sound library
Group:		Sound
Provides:	%{name} = %{version}-%{release}

%description -n %{libname}
This package contains the library needed to run programs dynamically
linked with OpenAL.

%package -n %{develname}
Summary:	Headers for developing programs that will use OpenAL
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%mklibname %{name} 0 -d
Provides:	%mklibname %{name} 0 -d

%description -n	%{develname}
This package contains the headers that programmers will need to develop
applications which will use OpenAL, a free 3D audio library.

%prep
%setup -q
%patch0 -p1 -b .arch
%patch1 -p1 -b .pthread
%patch2 -p1 -b .pkgconfig
%patch3 -p1 -b .pause
%patch4 -p1 -b .nommx
%patch5 -p1 -b .fixgcc
%patch6 -p1 -b .dlopen
%patch7 -p1 -b .str

%build
export CFLAGS="%{optflags} -O3"
export CXXLAGS="%{optflags} -O3"

./autogen.sh

%configure2_5x	--enable-alsa \
		--enable-alsa-dlopen \
		--disable-arts \
		--disable-arts-dlopen \
		--enable-esd \
		--enable-esd-dlopen \
		--enable-waveout \
		--enable-null \
		--enable-sdl \
		--enable-vorbis \
		--enable-mp3 \
		--enable-mp3-dlopen \
		--enable-optimization \
		--disable-debug
%make

%install
rm -rf %{buildroot}
%makeinstall_std
%multiarch_binaries %{buildroot}%{_bindir}/%{name}-config

install -d %{buildroot}%{_sysconfdir}
cat << EOF > %{buildroot}%{_sysconfdir}/openalrc
(define devices '(sdl alsa native esd null))
EOF

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%post -n %{develname}
%_install_info %{name}.info

%preun -n %{develname}
%_remove_install_info %{name}.info

%files -n %{libname}
%defattr(-,root,root)
%doc AUTHORS NEWS NOTES README TODO
%config(noreplace) %{_sysconfdir}/openalrc
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%doc ChangeLog
%{_includedir}/AL
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/*.so
%{_bindir}/%{name}-config
%{multiarch_bindir}/%{name}-config
