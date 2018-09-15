Name: tdlib
Version: 1.3.0
Release: 1%{?dist}
Summary: Cross-platform library for building Telegram clients

License: BSL 1.0
URL: https://github.com/%{name}/td
Source0: %{url}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

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

%description devel
%{summary}.

%description static
%{summary}.

%prep
%autosetup -n td-%{version} -p1
mkdir -p %{_target_platform}

# Adding missing SONAME for shared libraries...
echo "set_property(TARGET tdc PROPERTY SOVERSION ${PROJECT_VERSION})" >> CMakeLists.txt
echo "set_property(TARGET tdcore PROPERTY SOVERSION ${PROJECT_VERSION})" >> CMakeLists.txt
echo "set_property(TARGET tdclient PROPERTY SOVERSION ${PROJECT_VERSION})" >> CMakeLists.txt
echo "set_property(TARGET tdjson PROPERTY SOVERSION ${PROJECT_VERSION})" >> CMakeLists.txt
echo "set_property(TARGET tdjson_static PROPERTY SOVERSION ${PROJECT_VERSION})" >> CMakeLists.txt
echo "set_property(TARGET tg_cli PROPERTY SOVERSION ${PROJECT_VERSION})" >> CMakeLists.txt


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
%{_libdir}/libtd*.so.*

%files devel
%{_includedir}/%{name}
%{_libdir}/libtd*.so
%{_libdir}/cmake/Td

%files static
%{_libdir}/libtd*.a

%changelog

