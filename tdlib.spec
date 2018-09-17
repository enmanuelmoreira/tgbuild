# Building with default settings require at least 16 GB of free RAM.
# We will make some tweaks for secondary arches.
%ifnarch %{ix86} x86_64
%global lowmem 1
%endif

# Decrease debuginfo verbosity to reduce memory consumption...
%if 0%{?lowmem}
%global optflags %(echo %{optflags} | sed 's/-g /-g1 /')
%endif

Name: tdlib
Version: 1.3.0
Release: 2%{?dist}
Summary: Cross-platform library for building Telegram clients

License: Boost
URL: https://github.com/%{name}/td
Source0: %{url}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch0: %{name}-system-crypto.patch

BuildRequires: gperftools-devel
BuildRequires: openssl-devel
BuildRequires: ninja-build
BuildRequires: gcc-c++
BuildRequires: gperf
BuildRequires: cmake
BuildRequires: gcc

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

# Adding missing SOVERSION for shared libraries...
echo "set_property(TARGET tdclient PROPERTY SOVERSION 1)" >> CMakeLists.txt
echo "set_property(TARGET tdjson PROPERTY SOVERSION 1)" >> CMakeLists.txt

# Patching LIBDIR path...
sed -e 's@DESTINATION lib@DESTINATION %{_lib}@g' -e 's@lib/@%{_lib}/@g' -i CMakeLists.txt
sed -i 's@DESTINATION lib@DESTINATION %{_lib}@g' {sqlite,tdactor,tddb,tdnet,tdutils}/CMakeLists.txt

# Disable FLTO on lowend build configurations...
%if 0%{?lowmem}
sed -e '/-flto/d' -i CMakeLists.txt
%endif

%build
pushd %{_target_platform}
    %cmake -G Ninja \
    -DCMAKE_BUILD_TYPE=Release \
%if 0%{?lowmem}
    -DTD_ENABLE_LTO=OFF \
    -j1 \
%endif
    ..
popd
%ninja_build -C %{_target_platform}

%install
%ninja_install -C %{_target_platform}

%files
%license LICENSE_1_0.txt
%doc README.md CHANGELOG.md
%{_libdir}/libtd*.so.1*

%files devel
%{_includedir}/td
%{_libdir}/libtd*.so
%{_libdir}/cmake/Td

%files static
%{_libdir}/libtd*.a

%changelog
* Sun Sep 16 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 1.3.0-2
- Fixed issue with crypto policies.

* Sat Sep 15 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 1.3.0-1
- Initial SPEC release.
