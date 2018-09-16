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

# Build requires at least 16 GB of free RAM. It cannot be built
# on non-x86 architectures.
ExclusiveArch: i686 x86_64

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

%build
pushd %{_target_platform}
    %cmake -G Ninja \
    -DCMAKE_BUILD_TYPE=Release \
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
