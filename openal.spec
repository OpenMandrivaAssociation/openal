%define oname openal-soft
%define major 1
%define libname %mklibname %{name} %{major}
%define devname %mklibname %{name} -d

Summary:	3D Sound Library
Name:		openal
Version:	1.20.0
Release:	1
License:	LGPLv2
Group:		Sound
Url:		http://www.openal.org
Source0:	https://github.com/kcat/openal-soft/archive/%{oname}-%{version}.tar.gz
Source1:	openal.rpmlintrc
BuildRequires:	cmake
BuildRequires:	alsa-oss-devel
BuildRequires:	ffmpeg-devel
BuildRequires:	glibc-devel
BuildRequires:	pkgconfig(libpulse)
BuildRequires:	pkgconfig(portaudio-2.0)
BuildRequires:	pkgconfig(sdl2)
BuildRequires:	SDL_sound-devel
BuildRequires:	qmake5
BuildRequires:	cmake(Qt5Widgets)
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

%description -n	%{devname}
This package contains the headers that programmers will need to develop
applications which will use OpenAL, a free 3D audio library.

%prep
%setup -q -n %{oname}-%{oname}-%{version}
%autopatch -p1

%build
export CC=gcc
export CXX=g++
%cmake -DALSOFT_CONFIG=ON -DALSOFT_EXAMPLES=ON -DQT_QMAKE_EXECUTABLE=%{_prefix}/lib/qt5/bin/qmake
%make_build

%install
%make_install -C build
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
