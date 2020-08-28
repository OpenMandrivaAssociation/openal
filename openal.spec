# wine uses openal
%ifarch %{x86_64}
%bcond_without compat32
%else
%bcond_with compat32
%endif

%define oname openal-soft
%define major 1
%define libname %mklibname %{name} %{major}
%define devname %mklibname %{name} -d
%define lib32name %mklib32name %{name} %{major}
%define dev32name %mklib32name %{name} -d

Summary:	3D Sound Library
Name:		openal
Version:	1.20.1
Release:	3
License:	LGPLv2
Group:		Sound
Url:		http://www.openal.org
Source0:	https://github.com/kcat/openal-soft/archive/%{oname}-%{version}.tar.gz
Source1:	openal.rpmlintrc
# As of LLVM 10.0, OpenAL 1.20.1, allowing __attribute__((visibility("protected")))
# results in ffmpeg failing to build, complaining it "cannot preempt symbol" alGetError
# Same behavior observed when building with gcc 10.1, regardless of linker.
Patch0:		openal-1.20.1-no-visibility-protected.patch
BuildRequires:	cmake
BuildRequires:	pkgconfig(alsa)
BuildRequires:	ffmpeg-devel
BuildRequires:	glibc-devel
BuildRequires:	pkgconfig(libpulse)
BuildRequires:	pkgconfig(portaudio-2.0)
BuildRequires:	pkgconfig(sdl2)
BuildRequires:	SDL_sound-devel
BuildRequires:	qmake5
BuildRequires:	cmake(Qt5Widgets)
BuildRequires:	ninja
Requires:	%{name}-config >= %{version}-%{release}
Provides:	%{oname} = %{version}-%{release}

%description
OpenAL is a free 3D-audio library, with a programming interface similar
to that of OpenGL.

%package config
Summary:	Configuration tool for openal
Group:		Sound

%description config
This package contains a configuration tool and configuration files for OpenAL

%package -n %{libname}
Summary:	Main library for OpenAL, a free 3D sound library
Group:		System/Libraries
Suggests:	%{name} >= %{version}-%{release}

%description -n %{libname}
This package contains the library needed to run programs dynamically
linked with OpenAL.

%package -n %{devname}
Summary:	Headers for developing programs that will use OpenAL
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	%{oname}-devel = %{version}-%{release}

%description -n %{devname}
This package contains the headers that programmers will need to develop
applications which will use OpenAL, a free 3D audio library.

%if %{with compat32}
%package -n %{lib32name}
Summary:	Main library for OpenAL, a free 3D sound library (32-bit)
Group:		System/Libraries
Suggests:	%{name} >= %{version}-%{release}

%description -n %{lib32name}
This package contains the library needed to run programs dynamically
linked with OpenAL.

%package -n %{dev32name}
Summary:	Headers for developing programs that will use OpenAL (32-bit)
Group:		Development/C
Requires:	%{devname} = %{version}-%{release}
Requires:	%{lib32name} = %{version}-%{release}

%description -n %{dev32name}
This package contains the headers that programmers will need to develop
applications which will use OpenAL, a free 3D audio library.
%endif

%prep
%autosetup -n %{oname}-%{oname}-%{version} -p1
%if %{with compat32}
%cmake32 -DALSOFT_CONFIG=ON -DALSOFT_EXAMPLES=ON -DQT_QMAKE_EXECUTABLE=%{_prefix}/lib/qt5/bin/qmake -G Ninja
cd ..
%endif
%cmake -DALSOFT_CONFIG=ON -DALSOFT_EXAMPLES=ON -DQT_QMAKE_EXECUTABLE=%{_prefix}/lib/qt5/bin/qmake -G Ninja

%build
%if %{with compat32}
%ninja_build -C build32
%endif
%ninja_build -C build

%install
%if %{with compat32}
%ninja_install -C build32
%endif
%ninja_install -C build
mkdir -p %{buildroot}/%{_sysconfdir}/%{name}
install -m 0644 alsoftrc.sample %{buildroot}/%{_sysconfdir}/%{name}/alsoft.conf

%files
%dir %{_datadir}/openal
%dir %{_datadir}/openal/hrtf
%{_bindir}/alffplay
%{_bindir}/almultireverb
%{_bindir}/alplay
%{_bindir}/allatency
%{_bindir}/alloopback
%{_bindir}/alrecord
%{_bindir}/alreverb
%{_bindir}/alstream
%{_bindir}/altonegen
%{_bindir}/alhrtf
%{_bindir}/openal-info
%{_datadir}/%{name}/alsoftrc.sample
%{_datadir}/%{name}/hrtf/*.mhr
%{_datadir}/%{name}/presets

%files config
%dir %{_sysconfdir}/openal
%config(noreplace) %{_sysconfdir}/openal/alsoft.conf
%{_bindir}/alsoft-config

%files -n %{libname}
%{_libdir}/libopenal.so.%{major}*

%files -n %{devname}
%{_includedir}/AL
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/*.so
%{_libdir}/cmake/OpenAL

%if %{with compat32}
%files -n %{lib32name}
%{_prefix}/lib/libopenal.so.%{major}*

%files -n %{dev32name}
%{_prefix}/lib/pkgconfig/%{name}.pc
%{_prefix}/lib/*.so
%{_prefix}/lib/cmake/OpenAL
%endif
