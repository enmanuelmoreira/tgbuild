%global _QTVERSION 5.6.0

Summary: Telegram is a new era of messaging
Name: telegram-desktop
Version: 0.10.6
Release: 1%{?dist}

Group: Applications/Internet
License: GPLv3
URL: https://github.com/telegramdesktop
Source0: %{url}/tdesktop/archive/v%{version}.tar.gz

Requires: hicolor-icon-theme
BuildRequires: desktop-file-utils
BuildRequires: libappstream-glib
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: libwayland-server-devel
BuildRequires: libxcb-devel
BuildRequires: libogg-devel
BuildRequires: xz-devel
BuildRequires: libappindicator-devel
BuildRequires: libunity-devel
BuildRequires: libstdc++-devel
BuildRequires: libstdc++-static
BuildRequires: libwebp-devel
BuildRequires: libpng-devel
BuildRequires: xorg-x11-util-macros
BuildRequires: gettext-devel
BuildRequires: cmake
BuildRequires: libICE-devel
BuildRequires: libSM-devel
BuildRequires: libXi-devel
BuildRequires: openjpeg-devel
BuildRequires: openssl-devel
BuildRequires: zlib-devel
BuildRequires: libexif-devel
BuildRequires: opus-devel
BuildRequires: ffmpeg-devel
BuildRequires: portaudio-devel
BuildRequires: openal-soft-devel
BuildRequires: libva-devel
BuildRequires: libxkbcommon-devel

%description
Telegram is a messaging app with a focus on speed and security, it’s super
fast, simple and free. You can use Telegram on all your devices at the same
time — your messages sync seamlessly across any of your phones, tablets or
computers.

With Telegram, you can send messages, photos, videos and files of any type
(doc, zip, mp3, etc), as well as create groups for up to 200 people. You can
write to your phone contacts and find people by their usernames. As a result,
Telegram is like SMS and email combined — and can take care of all your
personal or business messaging needs.

%prep

%build

%install

%files
%{_bindir}/telegram
%{_datadir}/applications/telegram-desktop.desktop
%{_datadir}/pixmaps/telegram.png
%{_datadir}/appdata/%{name}.appdata.xml

%changelog
