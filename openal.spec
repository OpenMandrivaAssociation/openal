%define	major	1
%define	libname	%mklibname %{name} %{major}
%define	devname	%mklibname %{name} -d
%define	oname	openal-soft

Name:		openal
Summary:	3D Sound Library
Version:	1.13
Release:	1
License:	LGPLv2
Group:		Sound
URL:		http://www.openal.org
Source0:	http://connect.creativelabs.com/openal/Downloads/%{oname}-%{version}.tbz2

Provides:	%{oname} = %{version}-%{release}
Conflicts:	openal1 < 1.7.411-2
BuildRequires:	portaudio-devel
BuildRequires:	libalsa-devel
BuildRequires:	cmake
BuildRequires:	pulseaudio-devel

%description
OpenAL is a free 3D-audio library, with a programming interface similar
to that of OpenGL.

%package -n	%{libname}
Summary:	Main library for OpenAL, a free 3D sound library
Group:		Sound

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

%files -n %{libname}
%dir %{_sysconfdir}/openal
%config(noreplace) %{_sysconfdir}/openal/alsoft.conf
%{_libdir}/*.so.%{major}*

%files -n %{devname}
%{_includedir}/AL
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/*.so


%changelog
* Thu May 05 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 1.13-1
+ Revision: 669487
- fix dependency loop
- clean out legacy stuff
- new version

* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 1.12.854-3
+ Revision: 666947
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 1.12.854-2mdv2011.0
+ Revision: 607012
- rebuild

* Thu May 13 2010 Colin Guthrie <cguthrie@mandriva.org> 1.12.854-1mdv2010.1
+ Revision: 544706
- New version (fixes serious bug relating to alsa initialisation)
- Don't build static library
- Drop legacy openal-config script (pkgconfig support is preferred)
- Drop scripts for older distros

* Mon Feb 15 2010 Emmanuel Andry <eandry@mandriva.org> 1.11.753-1mdv2010.1
+ Revision: 506153
- New version 1.11.753
- rediff p1
- drop p7 (merged upstream)

* Sat Dec 19 2009 Per Øyvind Karlsen <peroyvind@mandriva.org> 1.10.622-2mdv2010.1
+ Revision: 480123
- prefer pulseaudio driver (P7)

* Sat Dec 19 2009 Per Øyvind Karlsen <peroyvind@mandriva.org> 1.10.622-1mdv2010.1
+ Revision: 480067
- new release: 1.10.624

* Tue Oct 06 2009 Thierry Vignaud <tv@mandriva.org> 1.7.411-4mdv2010.0
+ Revision: 455188
- fix conflicts

* Sun Sep 27 2009 Funda Wang <fwang@mandriva.org> 1.7.411-3mdv2010.0
+ Revision: 449677
- add conflicts to ease upgrade

  + Per Øyvind Karlsen <peroyvind@mandriva.org>
    - move non-libraries out of library package to prevent conflicts (fixes #54087)

* Wed May 27 2009 Per Øyvind Karlsen <peroyvind@mandriva.org> 1.7.411-1mdv2010.0
+ Revision: 380211
- clean no longer used buildrequires and add missing ones
- since we already have config files in library package, we might as well carry
  openal-info with it as well..
- update to openal-soft 1.7.411
  * sync with debian patches

* Sat Apr 11 2009 Funda Wang <fwang@mandriva.org> 0.0.8-10mdv2009.1
+ Revision: 365959
- fix str fmt
- rediff pthread patch
- rediff arch patch

* Thu Aug 07 2008 Thierry Vignaud <tv@mandriva.org> 0.0.8-10mdv2009.0
+ Revision: 265206
- rebuild early 2009.0 package (before pixel changes)

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

  + Tomasz Pawel Gajc <tpg@mandriva.org>
    - add -b for patches

* Wed Apr 23 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 0.0.8-9mdv2009.0
+ Revision: 196930
- sync patches with Fedora
- re-order patches

* Mon Feb 11 2008 Frederic Crozat <fcrozat@mandriva.com> 0.0.8-8mdv2008.1
+ Revision: 165400
- Patch3: fix dlopen for audio backends
- Suggests SDL by default and use it by default (better Pulseaudio support)

* Thu Jan 17 2008 Thierry Vignaud <tv@mandriva.org> 0.0.8-7mdv2008.1
+ Revision: 154150
- do not package big changelog
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Tue Oct 23 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 0.0.8-6mdv2008.1
+ Revision: 101529
- new devel library policy
- new license policy
- provide patch 2 (linking with pthread)
- drop arts support
- preffer alsa backend over the native
- remove depreciaded configure options
- spec file clean

* Mon Jul 16 2007 Olivier Blin <oblin@mandriva.com> 0.0.8-5mdv2008.0
+ Revision: 52657
- fix ALCvoid patch

* Mon Jul 16 2007 Olivier Blin <oblin@mandriva.com> 0.0.8-4mdv2008.0
+ Revision: 52619
- fix build with gcc 4.2 and Werror (from Debian #379862)

* Wed Jun 27 2007 Olivier Blin <oblin@mandriva.com> 0.0.8-3mdv2008.0
+ Revision: 45022
- remove invalid pkgconfig requirements (makes pkg-config --exists fail)


* Tue Dec 05 2006 Olivier Blin <oblin@mandriva.com> 0.0.8-2mdv2007.0
+ Revision: 90655
- drop multiarch macro that does not expand anymore in files section
- 0.0.8 final (still one year old)
- Import openal

* Tue Aug 01 2006 Per Øyvind Karlsen <pkarlsen@mandriva.com> 0.0.8-1.20050824.2mdv2007.0
- add config to have openal try several output devices (fixes #23355)
- fix requires for info-install
- fix macro-in-%%changelog

* Thu Aug 25 2005 Per Øyvind Karlsen <pkarlsen@mandriva.com> 0.0.8-1.20050824.1mdk
- new cvs snapshot
- remove some configure options that's no longer used

* Sun Jul 10 2005 Per Øyvind Karlsen <pkarlsen@mandriva.com> 0.0.8-1.20050709.1mdk
- update to latest from cvs
- dlopen arts, alsa and esd (fixes #16713)

* Fri May 06 2005 Per Øyvind Karlsen <pkarlsen@mandriva.com> 0.0.8-1.20050505.1mdk
- update to latest from cvs
- lib64 fix
- %%mkrel
- drop P2 (fixed upstream)

* Sat Mar 12 2005 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 0.0.8-1.20050312.1mdk
- bah, really update to latest from cvs
- multiarch
- let release tag reflect on cvs date

* Sat Feb 19 2005 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 0.0.8-1mdk
- new cvs snapshot (micro version bumpedn to 8
- fix summary-ended-with-dot

* Thu Dec 02 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 0.0.7-3mdk
- new cvs snapshot
- --disable-arch-asm for now

* Sat Oct 16 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 0.0.7-2mdk
- disable jlib

* Thu Jul 29 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 0.0.7-1mdk
- new cvs snapshot (micro version bumped to 7
- fix buildrequires

* Wed Jun 09 2004 Götz Waschk <waschk@linux-mandrake.com> 0.0.6-14mdk
- rebuild

* Tue Feb 10 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 0.0.6-13mdk
- new cvs snapshot
- spec cosmetics
- drop P3, fixed upstream

* Tue Dec 23 2003 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 0.0.6-12mdk
- new cvs snapshot
- alsa 1.0 support (P3, done by me, so probably ugly;)
- s/%%configure2_5x/%%configure/

