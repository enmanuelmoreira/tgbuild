#!/bin/sh
set -e

# Version variables. Edit it if you want.
_QTVERSION="5.6.0"
_TGVERSION="0.10.6"

# Setting additional variables...
SRCDIR=$(pwd)
ARGS="-j$(nproc --all)"
QT_PATCH="$SRCDIR/tdesktop/Telegram/Patches/qtbase_${_QTVERSION//./_}.diff"
QTDIR="$SRCDIR/Libraries/qt${_QTVERSION//./_}"

# Exporting some paths required for build...
export PKG_CONFIG_PATH="/usr/local/lib/pkgconfig:/usr/local/tdesktop/Qt-${_QTVERSION}/lib/pkgconfig:/usr/lib64/pkgconfig"
export PATH="/usr/local/tdesktop/Qt-${_QTVERSION}/bin:$PATH"

# Checking for root rights...
SUDO=''
if [ "$EUID" -ne 0 ]; then
    SUDO='sudo'
fi

# Installing compilers and prerequirements...
$SUDO dnf -y install git gcc gcc-c++ automake autoconf libtool freetype-devel libwayland-server-devel libjpeg-devel libxcb-devel yasm openal-devel libogg-devel opus-devel openssl-devel lzma-devel xz-devel libappindicator-devel libunity-devel libstdc++-devel libstdc++-static libwebp-devel libpng-devel xorg-x11-util-macros gettext-devel bison doxygen portaudio-devel

# Downloading Telegram Desktop sources...
git clone --recursive https://github.com/telegramdesktop/tdesktop.git "$SRCDIR/tdesktop"

# Extracting required version of Telegram Desktop...
cd "$SRCDIR/tdesktop"
git checkout v$_TGVERSION

# Creating dir for shared 3rd-party libraries...
mkdir -p "$SRCDIR/Libraries"

# Downloading and installing libva...
git clone git://anongit.freedesktop.org/git/libva "$SRCDIR/Libraries/libva"
cd "$SRCDIR/Libraries/libva"
./autogen.sh --enable-static
make $ARGS
$SUDO make install

# Downloading and installing latest ffmpeg...
git clone https://github.com/FFmpeg/FFmpeg.git "$SRCDIR/Libraries/ffmpeg"
cd "$SRCDIR/Libraries/ffmpeg"
git checkout release/3.1
./configure --prefix=/usr/local --disable-programs --disable-doc --disable-everything --enable-protocol=file --enable-libopus --enable-decoder=aac --enable-decoder=aac_latm --enable-decoder=aasc --enable-decoder=flac --enable-decoder=gif --enable-decoder=h264 --enable-decoder=h264_vdpau --enable-decoder=mp1 --enable-decoder=mp1float --enable-decoder=mp2 --enable-decoder=mp2float --enable-decoder=mp3 --enable-decoder=mp3adu --enable-decoder=mp3adufloat --enable-decoder=mp3float --enable-decoder=mp3on4 --enable-decoder=mp3on4float --enable-decoder=mpeg4 --enable-decoder=mpeg4_vdpau --enable-decoder=msmpeg4v2 --enable-decoder=msmpeg4v3 --enable-decoder=opus --enable-decoder=vorbis --enable-decoder=wavpack --enable-decoder=wmalossless --enable-decoder=wmapro --enable-decoder=wmav1 --enable-decoder=wmav2 --enable-decoder=wmavoice --enable-encoder=libopus --enable-hwaccel=h264_vaapi --enable-hwaccel=h264_vdpau --enable-hwaccel=mpeg4_vaapi --enable-hwaccel=mpeg4_vdpau --enable-parser=aac --enable-parser=aac_latm --enable-parser=flac --enable-parser=h264 --enable-parser=mpeg4video --enable-parser=mpegaudio --enable-parser=opus --enable-parser=vorbis --enable-demuxer=aac --enable-demuxer=flac --enable-demuxer=gif --enable-demuxer=h264 --enable-demuxer=mov --enable-demuxer=mp3 --enable-demuxer=ogg --enable-demuxer=wav --enable-muxer=ogg --enable-muxer=opus
make $ARGS
$SUDO make install

# Downloading and installing libxkbcommon...
git clone https://github.com/xkbcommon/libxkbcommon.git "$SRCDIR/Libraries/libxkbcommon"
cd "$SRCDIR/Libraries/libxkbcommon"
./autogen.sh --prefix=/usr/local --disable-x11
make $ARGS
$SUDO make install

# Downloading and installing breakpad...
git clone https://chromium.googlesource.com/breakpad/breakpad "$SRCDIR/Libraries/breakpad"
git clone https://chromium.googlesource.com/linux-syscall-support "$SRCDIR/Libraries/breakpad/src/third_party/lss"
cd "$SRCDIR/Libraries/breakpad"
./configure
make $ARGS
$SUDO make install

# Downloading Qt sources and applying Telegram patches onto it...
if [ "$QT_PATCH" -nt "$QTDIR" ]; then
  rm -rf "$QTDIR"
  git clone git://code.qt.io/qt/qt5.git "$QTDIR"
  cd "$QTDIR"
  git checkout 5.6
  perl init-repository --module-subset=qtbase,qtimageformats
  git checkout v$_QTVERSION
  cd qtimageformats
  git checkout v$_QTVERSION
  cd ../qtbase
  git checkout v$_QTVERSION
  git apply "$QT_PATCH"
fi

# Downloading GYP...
mkdir -p "$SRCDIR/Libraries/gyp"
git clone https://chromium.googlesource.com/external/gyp "$SRCDIR/Libraries/gyp"
cd "$SRCDIR/Libraries/gyp"
git apply "$SRCDIR/tdesktop/Telegram/Patches/gyp.diff"

# Downloading cmake...
cd "$SRCDIR/Libraries"
wget https://cmake.org/files/v3.6/cmake-3.6.2.tar.gz
tar -xf cmake-3.6.2.tar.gz
cd "$SRCDIR/Libraries/cmake-3.6.2"
./configure
make $ARGS

# Building and installing patched Qt...
cd "$QTDIR"
./configure -prefix "/usr/local/tdesktop/Qt-${_QTVERSION}" -release -opensource -confirm-license -system-zlib -system-libpng -system-libjpeg -system-freetype -system-harfbuzz -system-pcre -qt-xcb -qt-xkbcommon-x11 -no-opengl -no-gtkstyle -static -nomake examples -nomake tests
make $ARGS
$SUDO make install

# Building and installing qtimageformat plugins for Qt...
cd "$QTDIR/qtimageformats"
qmake .
make $ARGS
$SUDO make install

# Building Telegram Desktop...
cd "$SRCDIR/tdesktop/Telegram"
gyp/refresh.sh
cd "$SRCDIR/tdesktop/out/Release"
make $ARGS
