%global _QTVERSION 5.6.0
%global _APPNAME tdesktop

Summary: Telegram is a new era of messaging
Name: telegram-desktop
Version: 0.10.6
Release: 1%{?dist}

Group: Applications/Internet
License: GPLv3
URL: https://github.com/telegramdesktop
Source0: %{url}/%{_APPNAME}/archive/v%{version}.tar.gz
Source1: https://download.qt.io/official_releases/qt/5.6/5.6.0/submodules/qtbase-opensource-src-5.6.0.tar.xz
Source2: https://download.qt.io/official_releases/qt/5.6/5.6.0/submodules/qtimageformats-opensource-src-5.6.0.tar.xz
Source3: https://chromium.googlesource.com/external/gyp/+archive/master.tar.gz#/gyp.tar.gz
Source4: https://chromium.googlesource.com/breakpad/breakpad/+archive/master.tar.gz#/breakpad.tar.gz
Source5: https://chromium.googlesource.com/linux-syscall-support/+archive/master.tar.gz#/breakpad-lss.tar.gz
Source6: https://cmake.org/files/v3.6/cmake-3.6.2.tar.gz

Source101: telegram.desktop
Source102: telegram-desktop.appdata.xml
Source103: tg.protocol

Patch0: fix_build_under_fedora.patch

Requires: hicolor-icon-theme
BuildRequires: desktop-file-utils
BuildRequires: libappstream-glib
BuildRequires: ffmpeg-devel >= 3.1
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: libwayland-server-devel
BuildRequires: libwayland-cursor-devel
BuildRequires: libproxy-devel
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
BuildRequires: libjpeg-turbo-devel
BuildRequires: openssl-devel
BuildRequires: zlib-devel
BuildRequires: libexif-devel
BuildRequires: opus-devel
BuildRequires: portaudio-devel
BuildRequires: openal-soft-devel
BuildRequires: xcb-util-devel
BuildRequires: xcb-util-wm-devel
BuildRequires: xcb-util-xrm-devel
BuildRequires: xcb-util-image-devel
BuildRequires: xcb-util-cursor-devel
BuildRequires: xcb-util-keysyms-devel
BuildRequires: xcb-util-renderutil-devel
BuildRequires: libva-devel
BuildRequires: libxkbcommon-devel
BuildRequires: libxkbcommon-x11-devel
BuildRequires: harfbuzz-devel
BuildRequires: pcre-devel

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

# Patching Telegram Desktop...
cd "%_builddir/%{_APPNAME}-%{version}"
patch -p1 -i %{PATCH0}

# Unpacking Qt...
cd "$qtdir"
tar -xf %{SOURCE1}
mv -f "qtbase-opensource-src-%{_QTVERSION}" "qtbase"
tar -xf %{SOURCE2}
mv -f "qtimageformats-opensource-src-%{_QTVERSION}" "qtimageformats"

# Applying Qt patch...
cd "$qtdir/qtbase"
patch -p1 -i "$qtpatch"

# Unpacking GYP...
mkdir -p "%_builddir/Libraries/gyp"
cd "%_builddir/Libraries/gyp"
tar -xf %{SOURCE3}

# Applying GYP patch...
patch -p1 -i "%_builddir/%{_APPNAME}-%{version}/Telegram/Patches/gyp.diff"

# Unpacking breakpad with lss support...
mkdir -p "%_builddir/Libraries/breakpad"
cd "%_builddir/Libraries/breakpad"
tar -xf %{SOURCE4}
mkdir -p "%_builddir/Libraries/breakpad/src/third_party/lss"
cd "%_builddir/Libraries/breakpad/src/third_party/lss"
tar -xf %{SOURCE5}

# Unpacking CMake...
cd "%_builddir/Libraries"
tar -xf %{SOURCE6}

%build
# Setting some constants...
qtv=%{_QTVERSION}
qtdir="%_builddir/Libraries/qt${qtv//./_}"

# Building patched Qt...
cd "$qtdir/qtbase"
./configure \
    -prefix "%_builddir/qt" \
    -release \
    -opensource \
    -confirm-license \
    -system-zlib \
    -system-libpng \
    -system-libjpeg \
    -system-freetype \
    -system-harfbuzz \
    -system-pcre \
    -system-xcb \
    -system-xkbcommon-x11 \
    -no-opengl \
    -no-gtkstyle \
    -static \
    -openssl-linked \
    -nomake examples \
    -nomake tests
%make_build
make install

# Exporting new PATH...
export PATH="%_builddir/qt/bin:$PATH"

# Building Qt image plugins...
cd "$qtdir/qtimageformats"
qmake .
%make_build
make install

# Building breakpad...
cd "%_builddir/Libraries/breakpad"
./configure
%make_build

# Building custom cmake...
cd "%_builddir/Libraries/cmake-3.6.2"
./configure
%make_build

# Building Telegram Desktop...
cd "%_builddir/%{_APPNAME}-%{version}/Telegram"
gyp/refresh.sh
cd "%_builddir/%{_APPNAME}-%{version}/out/Release"
%make_build

%install
# Installing executables...
cd "%_builddir/%{_APPNAME}-%{version}/out/Release"
mkdir -p %{buildroot}/%{_bindir}
install -m 755 Telegram %{buildroot}/%{_bindir}/%{name}

# Installing desktop shortcut...
desktop-file-install --dir=%{buildroot}%{_datadir}/applications %{SOURCE101}

# Installing icons...
for size in 16 32 48 64 128 256 512; do
	dir="%{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps"
	install -d "$dir"
	install -m 644 "%_builddir/%{_APPNAME}-%{version}/Telegram/Resources/art/icon${size}.png" "$dir/%{name}.png"
done

# Installing tg protocol handler...
install -d "%{buildroot}%{_datadir}/kde4/services"
install -m 644 %{SOURCE103} "%{buildroot}%{_datadir}/kde4/services/tg.protocol"

# Installing appdata for Gnome Software...
install -d "%{buildroot}%{_datadir}/appdata"
install -m 644 %{SOURCE102} "%{buildroot}%{_datadir}/appdata/%{name}.appdata.xml"

%check
appstream-util validate-relax --nonet %{buildroot}%{_datadir}/appdata/%{name}.appdata.xml

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
/usr/bin/update-desktop-database &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
/usr/bin/update-desktop-database &> /dev/null || :

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files
%{_bindir}/telegram-desktop
%{_datadir}/applications/%{name}.desktop
%{_datadir}/kde4/services/tg.protocol
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_datadir}/appdata/%{name}.appdata.xml

%changelog
* Sat Sep 17 2016 Vitaly Zaitsev <vitaly@easycoding.org> - 0.10.6-1
- Created new SPEC.
