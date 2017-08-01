%global commit0 01f27014b268b280c40cdbaf57c18bfa0d596770
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global date 20170727

Summary: VoIP library for Telegram clients
Name: libtgvoip
Version: 1.0
Release: 1.%{date}git%{shortcommit0}%{?dist}

License: Public Domain
URL: https://github.com/grishka/%{name}

Source0: %{url}/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz
Patch0: fix_libtgvoip.patch

BuildRequires: gcc-c++
BuildRequires: cmake
BuildRequires: gcc
BuildRequires: gyp
BuildRequires: pulseaudio-libs-devel
BuildRequires: alsa-lib-devel
BuildRequires: opus-devel

%if 0%{?fedora} && 0%{?fedora} >= 26
BuildRequires: compat-openssl10-devel
%else
BuildRequires: openssl-devel
%endif

%description
Provides VoIP library for Telegram clients.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description devel
%{summary}.

%prep
%autosetup -n %{name}-%{commit0}

%build
export VOIPVER="%{version}"
gyp --format=cmake --depth=. --generator-output=. -Goutput_dir=out -Gconfig=Release %{name}.gyp

pushd out/Release
    %cmake .
    %make_build
popd

%install
# Installing shared library...
mkdir -p "%{buildroot}%{_libdir}"
install -m 0755 -p out/Release/lib.target/%{name}.so.%{version} "%{buildroot}%{_libdir}/%{name}.so.%{version}"
ln -s %{name}.so.%{version} "%{buildroot}%{_libdir}/%{name}.so.1"
ln -s %{name}.so.%{version} "%{buildroot}%{_libdir}/%{name}.so"

# Installing additional development files...
mkdir -p "%{buildroot}%{_includedir}/%{name}/audio"
find . -maxdepth 1 -type f -name "*.h" -exec install -m 0644 -p '{}' %{buildroot}%{_includedir}/%{name} \;
find audio -maxdepth 1 -type f -name "*.h" -exec install -m 0644 -p '{}' %{buildroot}%{_includedir}/%{name}/audio \;

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license UNLICENSE
%{_libdir}/%{name}.so.*

%files devel
%{_includedir}/%{name}
%{_libdir}/%{name}.so

%changelog
* Tue Aug 01 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.0-1.20170727git01f2701
- Initial release.
