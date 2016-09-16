%global _QTVERSION 5.6.0
%global _APPNAME tdesktop

Summary: Telegram is a new era of messaging
Name: telegram-desktop
Version: 0.10.6
Release: 1%{?dist}

Group: Applications/Internet
License: GPLv3
URL: https://github.com/telegramdesktop
Source0: %{url}/tdesktop/archive/v%{version}.tar.gz
Source1: https://download.qt.io/official_releases/qt/5.6/5.6.0/submodules/qtbase-opensource-src-5.6.0.tar.xz
Source2: https://download.qt.io/official_releases/qt/5.6/5.6.0/submodules/qtimageformats-opensource-src-5.6.0.tar.xz
Source3: https://chromium.googlesource.com/external/gyp/+archive/master.tar.gz#/gyp.tar.gz

Patch0: fix_gyp.patch

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
# Setting some constants...
qtv=%{_QTVERSION}
qtdir="%_builddir/Libraries/qt${qtv//./_}"
qtpatch="%_builddir/%{_APPNAME}-%{version}/Telegram/Patches/qtbase_${qtv//./_}.diff"

# Creating directory for libraries...
mkdir -p "$qtdir"

# Unpacking Telegram Desktop source archive...
tar -xf %{SOURCE0}

# Unpacking Qt...
cd "$qtdir"
tar -xf %{SOURCE1}
mv -f "qtbase-opensource-src-%{_QTVERSION}" "qtbase"
tar -xf %{SOURCE2}
mv -f "qtimageformats-opensource-src-%{_QTVERSION}" "qtimageformats"

# Applying Qt patch...
cd "$qtdir/qtbase"
patch -p1 -i "$qtpatch"

%build

%install

%files
%{_bindir}/telegram
%{_datadir}/applications/telegram-desktop.desktop
%{_datadir}/pixmaps/telegram.png
%{_datadir}/appdata/%{name}.appdata.xml

%changelog
