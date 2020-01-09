%global commit0 88b47b6f808f2573d4eaf37e1463ecd59c43deda
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global date 20191230

Name: libtgvoip
Version: 2.4.4
Release: 3.%{date}git%{shortcommit0}%{?dist}

# Libtgvoip shared library - Public Domain.
# Bundled webrtc library - BSD with patented echo cancellation algorithms.
License: Public Domain and BSD
URL: https://github.com/telegramdesktop/%{name}
Summary: VoIP library for Telegram clients

Source0: %{url}/archive/%{commit0}/%{name}-%{shortcommit0}.tar.gz
Patch0: %{name}-build-fixes.patch

# https://github.com/telegramdesktop/libtgvoip/pull/6
Patch100: %{name}-pr6.patch

Provides: bundled(webrtc-audio-processing) = 0.3

BuildRequires: pulseaudio-libs-devel
BuildRequires: alsa-lib-devel
BuildRequires: openssl-devel
BuildRequires: json11-devel
BuildRequires: opus-devel
BuildRequires: automake
BuildRequires: autoconf
BuildRequires: gcc-c++
BuildRequires: libtool
BuildRequires: gcc

%description
Provides VoIP library for Telegram clients.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description devel
%{summary}.

%prep
%autosetup -n %{name}-%{commit0} -p1
rm -f json11.*

%build
autoreconf --force --install
%configure --disable-static
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/*.la

%files
%license UNLICENSE
%{_libdir}/%{name}.so.*

%files devel
%{_includedir}/tgvoip/
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/tgvoip.pc

%changelog
* Thu Jan 09 2020 Vitaly Zaitsev <vitaly@easycoding.org> - 2.4.4-3.20191230git88b47b6
- Switched to supported fork.

* Fri Aug 09 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Mar 12 2019 Vitaly Zaitsev <vitaly@easycoding.org> - 2.4.4-1
- Updated to 2.4.4 (regular release).
