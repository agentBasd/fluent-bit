Name: fluent-bit
Version: 2.1.1
Release: 1%{?dist}
Summary: Fast data collector for Linux
License: ASL 2.0
URL: https://github.com/fluent/fluent-bit
Source0: https://github.com/fluent/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz
# Fix up some install paths in CMake. Not upstream
Patch0: 0001-CMake-fix-up-install-paths.patch
#Patch1: fluent-bit-cmake-c99.patch
# Not sure why these tests never complete -- will debug later
Patch1: hanging-tests.patch

BuildRequires: pkgconfig
BuildRequires: make
BuildRequires: cmake
BuildRequires: systemd-rpm-macros
# systemd-devel BR is needed for systemd input plugin
BuildRequires: systemd-devel
BuildRequires: gcc-c++
BuildRequires: flex
BuildRequires: bison
BuildRequires: doxygen
BuildRequires: graphviz
BuildRequires: libpq-devel
BuildRequires: zlib-devel
BuildRequires: gnutls-devel
BuildRequires: openssl-devel
BuildRequires: cyrus-sasl-devel
BuildRequires: libyaml-devel
%{?systemd_requires}

# Exclude armv7hl temporarily because of failing runtime tests
# https://github.com/fluent/fluent-bit/issues/4395
ExclusiveArch: x86_64 aarch64

%description
Fluent Bit is a high performance and multi-platform log forwarder.

%prep
%autosetup -p1

%build
%cmake\
    -DCMAKE_BUILD_TYPE=RelWithDebInfo\
    -DFLB_EXAMPLES=Off\
    -DFLB_TRACE=On\
    -DFLB_JEMALLOC=On\
    -DFLB_IN_SYSTEMD=On\
    -DFLB_OUT_SLACK=On\
    -DFLB_OUT_TD=On\
    -DFLB_OUT_ES=On\
    -DFLB_OUT_PGSQL=On\
    -DFLB_OUT_KAFKA=On\
    -DFLB_SHARED_LIB=Off\
    -DFLB_TESTS_RUNTIME=Off\
    -DFLB_TESTS_INTERNAL=Off\
    -DFLB_RELEASE=On\
    -DFLB_DEBUG=Off\
    -DFLB_TLS=On\
    -DSYSTEMD_UNITDIR=/usr/lib/systemd/system

%cmake_build

%install
%cmake_install
# We don't ship headers and shared library for plugins (yet)
rm -rvf %{buildroot}%{_includedir}
# Don't ship luajit binary
rm -rvf %{buildroot}%{_bindir}/luajit %{buildroot}%{_libdir}/libluajit.a

%check
%ctest

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%license LICENSE
%doc README.md MAINTAINERS.md CODE_OF_CONDUCT.md CONTRIBUTING.md GOLANG_OUTPUT_PLUGIN.md GOVERNANCE.md
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/*.conf
%{_bindir}/%{name}
%{_unitdir}/%{name}.service

%changelog
* Fri Apr 21 2023 Eduardo Silva <eduardo@calyptia.com> - 2.1.1-1
- Upstream 2.1.1

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jan 18 2023 Florian Weimer <fweimer@redhat.com> - 1.9.9-2
- C99 compatibility fixes for CMake scripts

* Thu Oct 13 2022 Ben Kircher <bkircher@0xadd.de> - 1.9.9-1
- Update to 1.9.9

* Wed Aug 10 2022 Ben Kircher <bkircher@0xadd.de> - 1.9.7-1
- Update to 1.9.7

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jul 13 2022 Ben Kircher <bkircher@0xadd.de> - 1.9.6-1
- Bump to 1.9.6, rebase/drop patches

* Mon Mar 28 2022 Ben Kircher <bkircher@0xadd.de> - 1.8.15-1
- Update to 1.8.15

* Sat Mar 19 2022 Ben Kircher <bkircher@0xadd.de> - 1.8.14-1
- Update to 1.8.14

* Thu Mar 3 2022 Ben Kircher <bkircher@0xadd.de> - 1.8.13-1
- Update to 1.8.13

* Sat Feb 19 2022 Ben Kircher <bkircher@0xadd.de> - 1.8.12-2
- Enable Elasticsearch output plugin

* Fri Jan 28 2022 Ben Kircher <bkircher@0xadd.de> - 1.8.12-1
- Update to 1.8.12, backport small patch from master

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Dec 21 2021 Ben Kircher <bkircher@0xadd.de> - 1.8.11-1
- Update to 1.8.11

* Mon Dec 6 2021 Benjamin Kircher <bkircher@0xadd.de> - 1.8.10-8
- Temp. exclude armv7hl arch because of failing tests

* Sat Dec 4 2021 Benjamin Kircher <bkircher@0xadd.de> - 1.8.10-7
- Fix missing directory ownerships

* Sat Dec 4 2021 Benjamin Kircher <bkircher@0xadd.de> - 1.8.10-6
- Do CMake out-of-source build

* Sat Dec 4 2021 Benjamin Kircher <bkircher@0xadd.de> - 1.8.10-5
- Do not set CMAKE_INSTALL_PREFIX explicitly

* Thu Nov 25 2021 Benjamin Kircher <bkircher@0xadd.de> - 1.8.10-4
- Fix up source URL

* Wed Nov 24 2021 Benjamin Kircher <bkircher@0xadd.de> - 1.8.10-3
- Re-add systemd-devel BR. Remove devel package

* Mon Nov 22 2021 Benjamin Kircher <bkircher@0xadd.de> - 1.8.10-2
- Add systemd scriptlet macros, add patch status comments

* Sat Nov 20 2021 Benjamin Kircher <bkircher@0xadd.de> - 1.8.10-1
- Update to 1.8.10, enable runtime tests

* Mon Nov 1 2021 Benjamin Kircher <bkircher@0xadd.de> - 1.8.9-1
- Update to 1.8.9, remove shared library

* Thu Oct 28 2021 Benjamin Kircher <bkircher@0xadd.de> - 1.8.8-1
- Update to 1.8.8, rebase patches

* Thu Jul 8 2021 Benjamin Kircher <bkircher@0xadd.de> - 1.7.9-1
- Update to 1.7.9

* Wed Jun 9 2021 Benjamin Kircher <bkircher@0xadd.de> - 1.7.8-1
- Update to 1.7.8

* Sun May 23 2021 Benjamin Kircher <bkircher@0xadd.de> - 1.7.6-1
- Update to 1.7.6

* Sat May 15 2021 Benjamin Kircher <bkircher@0xadd.de> - 1.7.5-1
- Update to 1.7.5

* Fri Apr 16 2021 Benjamin Kircher <bkircher@0xadd.de> - 1.7.4-1
- New release; use cmake macros

* Mon Sep 28 2020 Marcin Skarbek <rpm@skarbek.name> - 1.5.7-1
- Initial package
