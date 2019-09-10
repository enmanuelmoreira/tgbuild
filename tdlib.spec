# Use clang on Fedora 30+...
%if 0%{?fedora} && 0%{?fedora} >= 30
%bcond_without clang
%else
%bcond_with clang
%endif

# Applying workaround to RHBZ#1559007...
%if %{with clang}
%global optflags %(echo %{optflags} | sed -e 's/-mcet//g' -e 's/-fcf-protection//g' -e 's/-fstack-clash-protection//g' -e 's/$/-Qunused-arguments -Wno-unknown-warning-option/')
%endif

Name: tdlib
Version: 1.5.0
Release: 1%{?dist}
Summary: Cross-platform library for building Telegram clients

License: Boost
URL: https://github.com/%{name}/td
Source0: %{url}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch0: %{name}-system-crypto.patch

BuildRequires: gperftools-devel
BuildRequires: openssl-devel
BuildRequires: ninja-build
BuildRequires: zlib-devel
BuildRequires: gcc-c++
BuildRequires: gperf
BuildRequires: cmake
BuildRequires: gcc

%if %{with clang}
BuildRequires: compiler-rt
BuildRequires: clang
BuildRequires: llvm
%endif

# Building with default settings require at least 16 GB of free RAM.
# Builds on ARM and other low-memory architectures are failing.
ExclusiveArch: x86_64

%description
TDLib (Telegram Database library) is a cross-platform library for
building Telegram clients. It can be easily used from almost any
programming language.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%package static
Summary: Static libraries for %{name}
Requires: %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires: %{name}-devel%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description devel
%{summary}.

%description static
%{summary}.

%prep
%autosetup -n td-%{version} -p1
mkdir -p %{_target_platform}

# Patching LIBDIR path...
sed -e 's@DESTINATION lib@DESTINATION %{_lib}@g' -e 's@lib/@%{_lib}/@g' -i CMakeLists.txt
sed -i 's@DESTINATION lib@DESTINATION %{_lib}@g' {sqlite,tdactor,tddb,tdnet,tdutils}/CMakeLists.txt

%build
pushd %{_target_platform}
    %cmake -G Ninja \
%if %{with clang}
    -DCMAKE_C_COMPILER=clang \
    -DCMAKE_CXX_COMPILER=clang++ \
    -DCMAKE_AR=%{_bindir}/llvm-ar \
    -DCMAKE_RANLIB=%{_bindir}/llvm-ranlib \
    -DCMAKE_LINKER=%{_bindir}/llvm-ld \
    -DCMAKE_OBJDUMP=%{_bindir}/llvm-objdump \
    -DCMAKE_NM=%{_bindir}/llvm-nm \
%else
    -DCMAKE_AR=%{_bindir}/gcc-ar \
    -DCMAKE_RANLIB=%{_bindir}/gcc-ranlib \
    -DCMAKE_NM=%{_bindir}/gcc-nm \
%endif
    -DCMAKE_BUILD_TYPE=Release \
    ..
popd
%ninja_build -C %{_target_platform}

%install
%ninja_install -C %{_target_platform}

%files
%license LICENSE_1_0.txt
%doc README.md CHANGELOG.md
%{_libdir}/libtd*.so.%{version}

%files devel
%{_includedir}/td
%{_libdir}/libtd*.so
%{_libdir}/cmake/Td

%files static
%{_libdir}/libtd*.a

%changelog
* Tue Sep 10 2019 Vitaly Zaitsev <vitaly@easycoding.org> - 1.5.0-1
- Updated to version 1.5.0.

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 02 2019 Vitaly Zaitsev <vitaly@easycoding.org> - 1.4.0-1
- Updated to version 1.4.0.

* Mon Feb 04 2019 Vitaly Zaitsev <vitaly@easycoding.org> - 1.3.0-4
- Switched to clang on Fedora 30+.

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Sep 16 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 1.3.0-2
- Fixed issue with crypto policies.

* Sat Sep 15 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 1.3.0-1
- Initial SPEC release.
