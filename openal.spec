%define	major	1
%define	libname	%mklibname %{name} %{major}
%define	devname	%mklibname %{name} -d
%define	oname	openal-soft

Name:		openal
Summary:	3D Sound Library
Version:	1.7.411
Release:	%mkrel 4
License:	LGPLv2
Group:		Sound
URL:		http://www.openal.org
Source0:	http://kcat.strangesoft.net/openal-releases/%{oname}-%{version}.tar.bz2
Patch0:		install-alsoft.conf.patch
Patch1:		install-openal-config.patch
Patch2:		add-openal-config.patch
Patch3:		add-openal-config-manpage.patch
Patch4:		alsoftrc-fix.patch
Patch5:		static_lib.patch
Patch6:		openal-soft-1.7.411-fix-static-library-install-location.patch

Provides:	%{oname} = %{version}-%{release}
Conflicts:	openal1 < 1.7.411-2
BuildRequires:	portaudio-devel
BuildRequires:	libalsa-devel
BuildRequires:	cmake
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
OpenAL is a free 3D-audio library, with a programming interface similar
to that of OpenGL.

%package -n	%{libname}
Summary:	Main library for OpenAL, a free 3D sound library
Group:		Sound
Requires:	%{name} = %{version}-%{release}

%description -n %{libname}
This package contains the library needed to run programs dynamically
linked with OpenAL.

%package -n	%{devname}
Summary:	Headers for developing programs that will use OpenAL
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	%{oname}-devel = %{version}-%{release}
Obsoletes:	%mklibname %{name} 0 -d
Provides:	%mklibname %{name} 0 -d

%description -n	%{devname}
This package contains the headers that programmers will need to develop
applications which will use OpenAL, a free 3D audio library.

%prep
%setup -q -n %{oname}-%{version}
%patch0 -p1 -b .inst_alsoft~
%patch1 -p1 -b .inst_openal_conf~
%patch2 -p1 -b .add_openal_conf~
%patch3 -p1 -b .add_openal_conf_man~
%patch4 -p1 -b .alsoftrc~
%patch5 -p1 -b .static~
%patch6 -p1 -b .static_install~

%build
%cmake		-DBUILD_STATIC=ON \
		-DALSOFT_CONFIG=ON

%make

%install
rm -rf %{buildroot}
cd build
%makeinstall_std
%multiarch_binaries %{buildroot}%{_bindir}/%{name}-config

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%files
%defattr(-,root,root)
%dir %{_sysconfdir}/openal
%config(noreplace) %{_sysconfdir}/openal/alsoft.conf
%{_bindir}/openal-info

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.%{major}*

%files -n %{devname}
%defattr(-,root,root)
%{_includedir}/AL
%{_libdir}/*.a
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/*.so
%{_bindir}/%{name}-config
%{multiarch_bindir}/%{name}-config
%{_mandir}/man1/openal-config.1*
