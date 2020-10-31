%undefine __cmake_in_source_build
%global debug_package %{nil}

%global commit0 1d4f7d74ff1a627db6e45682efd0e3b85738e426
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global date 20201030

Name: tg_owt
Version: 0
Release: 1.%{date}git%{shortcommit0}%{?dist}

# Main project - BSD
# abseil-cpp - ASL 2.0
# libsrtp - BSD
# libwebm - BSD
# libyuv - BSD
# openh264 - BSD
# pffft - BSD
# rnnoise - BSD
# usrsctp - BSD
License: BSD and ASL 2.0
Summary: WebRTC library for the Telegram messenger
URL: https://github.com/desktop-app/%{name}
Source0: %{url}/archive/%{commit0}/%{name}-%{shortcommit0}.tar.gz

BuildRequires: pulseaudio-libs-devel
BuildRequires: libjpeg-turbo-devel
BuildRequires: alsa-lib-devel
BuildRequires: openssl-devel
BuildRequires: ffmpeg-devel
BuildRequires: ninja-build
BuildRequires: opus-devel
BuildRequires: gcc-c++
BuildRequires: cmake
BuildRequires: yasm
BuildRequires: gcc

%description
Special fork of the OpenWebRTC library for the Telegram messenger.

%package devel
Summary: Development files for %{name}

%description devel
%{summary}.

%package static
Summary: Static libraries for %{name}
Requires: %{name}-devel%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides: bundled(openh264) = 0~git
Provides: bundled(abseil-cpp) = 0~git
Provides: bundled(libsrtp) = 0~git
Provides: bundled(libvpx) = 0~git
Provides: bundled(libyuv) = 0~git
Provides: bundled(pffft) = 0~git
Provides: bundled(rnnoise) = 0~git
Provides: bundled(usrsctp) = 0~git
Provides: bundled(libwebm) = 0~git

%description static
%{summary}.

%prep
%autosetup -n %{name}-%{commit0} -p1

%build
%cmake -G Ninja \
    -DCMAKE_BUILD_TYPE=Release \
    -DTG_OWT_PACKAGED_BUILD:BOOL=ON
%cmake_build

%install
%cmake_install

%files devel
%{_includedir}/%{name}
%{_libdir}/cmake/%{name}

%files static
%doc src/AUTHORS src/OWNERS
%license LICENSE src/PATENTS
%{_libdir}/lib%{name}.a

%changelog
* Sat Oct 31 2020 Vitaly Zaitsev <vitaly@easycoding.org> - 0-1.20201030git1d4f7d7
- Initial SPEC release.
