%define	oname	openal-soft
%define	major	1
%define	libname	%mklibname %{name} %{major}
%define	devname	%mklibname %{name} -d
%bcond_without	ffmpeg

Summary:	3D Sound Library
Name:		openal
Version:	1.16.0
Release:	3
License:	LGPLv2
Group:		Sound
Url:		http://www.openal.org
Source0:	http://kcat.strangesoft.net/openal-releases/%{oname}-%{version}.tar.bz2
BuildRequires:	cmake
BuildRequires:	alsa-oss-devel
%if %{with ffmpeg}
BuildRequires:	ffmpeg-devel
%endif
BuildRequires:	pkgconfig(libpulse)
BuildRequires:	pkgconfig(portaudio-2.0)
Requires:	%{name}-config >= %{version}-%{release}
Provides:	%{oname} = %{version}-%{release}

%description
OpenAL is a free 3D-audio library, with a programming interface similar
to that of OpenGL.

%package	config
Summary:	Configuration for openal
Group:		Sound
BuildArch:	noarch

%description	config
This package contains the configuration of the library needed to run programs
dynamically linked with OpenAL.

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
%setup -q -n %{oname}-%{version}

%build
export CC=gcc
export CXX=g++

%cmake -DALSOFT_CONFIG=ON -DALSOFT_EXAMPLES=ON
%make

%install
%makeinstall_std -C build
mkdir -p %{buildroot}/%{_sysconfdir}/%{name}
install -m 0644 alsoftrc.sample %{buildroot}/%{_sysconfdir}/%{name}/alsoft.conf

%files
%dir %{_datadir}/openal
%dir %{_datadir}/openal/hrtf
%if %{with ffmpeg}
%{_bindir}/alstream
%{_bindir}/allatency
%{_bindir}/alreverb
%endif
%{_bindir}/openal-info
%{_bindir}/makehrtf
%{_datadir}/%{name}/alsoftrc.sample
%{_datadir}/openal/hrtf/*.mhr
%{_datadir}/openal/hrtf/default-48000.mhr
    
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
