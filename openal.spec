%define major 1
%define libname %mklibname %{name} %{major}
%define devname %mklibname %{name} -d
%define oname openal-soft

Summary:	3D Sound Library
Name:		openal
Version:	1.14
Release:	1
License:	LGPLv2
Group:		Sound
URL:		http://www.openal.org
Source0:	http://connect.creativelabs.com/openal/Downloads/%{oname}-%{version}.tar.bz2
Provides:	%{oname} = %{version}-%{release}
Conflicts:	openal1 < 1.7.411-2
BuildRequires:	portaudio-devel
BuildRequires:	libalsa-devel
BuildRequires:	cmake
BuildRequires:	pulseaudio-devel

%description
OpenAL is a free 3D-audio library, with a programming interface similar
to that of OpenGL.

%package -n %{libname}
Summary:	Main library for OpenAL, a free 3D sound library
Group:		Sound

%description -n %{libname}
This package contains the library needed to run programs dynamically
linked with OpenAL.

%package -n %{devname}
Summary:	Headers for developing programs that will use OpenAL
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	%{oname}-devel = %{version}-%{release}
%define olddev	%mklibname %{name} 0 -d
%rename		%{olddev}

%description -n	%{devname}
This package contains the headers that programmers will need to develop
applications which will use OpenAL, a free 3D audio library.

%prep
%setup -q -n %{oname}-%{version}

%build
%cmake -DALSOFT_CONFIG=ON
%make

%install
cd build
%makeinstall_std

%files
%{_bindir}/openal-info
%{_bindir}/makehrtf

%files -n %{libname}
%dir %{_sysconfdir}/openal
%config(noreplace) %{_sysconfdir}/openal/alsoft.conf
%{_libdir}/*.so.%{major}*

%files -n %{devname}
%{_includedir}/AL
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/*.so
