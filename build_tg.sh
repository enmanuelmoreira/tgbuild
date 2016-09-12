#!/bin/sh
set -e

# Version variables. Edit it if you want.
_QTVERSION="5.6.0"
_TGVERSION="0.10.1"

# Setting additional variables...
SRCDIR=$(pwd)
ARGS="-j$(nproc --all)"
QT_PATCH="$SRCDIR/tdesktop/Telegram/Patches/qtbase_${_QTVERSION//./_}.diff"
QTDIR="$SRCDIR/Libraries/qt${_QTVERSION//./_}"

# Exporting some paths required for build...
export PKG_CONFIG_PATH="/usr/local/lib/pkgconfig:/usr/local/Qt-${_QTVERSION}/lib/pkgconfig:/usr/lib64/pkgconfig"
export PATH="/usr/local/Qt-${_QTVERSION}/bin:$PATH"

# Checking for root rights...
SUDO=''
if [ "$EUID" -ne 0 ]; then
    SUDO='sudo'
fi

# Installing compilers and prerequirements...
$SUDO dnf -y install git gcc gcc-c++ automake autoconf libtool freetype-devel libwayland-server-devel libjpeg-devel libxcb-devel yasm openal-devel libogg-devel opus-devel openssl-devel lzma-devel xz-devel libappindicator-devel libunity-devel libstdc++-devel libstdc++-static libwebp-devel libpng-devel xorg-x11-util-macros gettext-devel bison doxygen

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
./autogen.sh --prefix=/usr/local
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

# Downloading breakpad sources...
git clone --recursive https://chromium.googlesource.com/chromium/tools/depot_tools.git "$SRCDIR/Libraries/depot_tools"
mkdir -p "$SRCDIR/Libraries/breakpad"
cd "$SRCDIR/Libraries/breakpad"
"$SRCDIR/Libraries/depot_tools/fetch" breakpad
mv -f src src1
mv -f src1/* "$SRCDIR/Libraries/breakpad/"

# Patching .PRO file...
sed -i 's/CUSTOM_API_ID//g' "$SRCDIR/tdesktop/Telegram/Telegram.pro"

# Setting additional build options...
(
  echo "LIBS += /usr/local/lib/libxkbcommon-x11.a"
  echo "DEFINES += TDESKTOP_DISABLE_AUTOUPDATE"
  echo "DEFINES += TDESKTOP_DISABLE_REGISTER_CUSTOM_SCHEME"
  echo "DEFINES += TDESKTOP_DISABLE_DESKTOP_FILE_GENERATION"
  echo "DEFINES += TDESKTOP_DISABLE_CRASH_REPORTS"
) >> "$SRCDIR/tdesktop/Telegram/Telegram.pro"

# Building and installing patched Qt...
cd "$QTDIR"
./configure -release -opensource -confirm-license -system-zlib -system-libpng -system-libjpeg -system-freetype -system-harfbuzz -system-pcre -qt-xcb -qt-xkbcommon-x11 -no-opengl -no-gtkstyle -static -nomake examples -nomake tests
make $ARGS
$SUDO make install

# Building and installing qtimageformat plugins for Qt...
cd "$QTDIR/qtimageformats"
qmake .
make $ARGS
$SUDO make install

# Building breakpad...
cd "$SRCDIR/Libraries/breakpad"
./configure
make $ARGS

# Building codegen_style...
mkdir -p "$SRCDIR/tdesktop/Linux/obj/codegen_style/Release"
cd "$SRCDIR/tdesktop/Linux/obj/codegen_style/Release"
qmake CONFIG+=release ../../../../Telegram/build/qmake/codegen_style/codegen_style.pro
make $ARGS

# Building codegen_numbers...
mkdir -p "$SRCDIR/tdesktop/Linux/obj/codegen_numbers/Release"
cd "$SRCDIR/tdesktop/Linux/obj/codegen_numbers/Release"
qmake CONFIG+=release ../../../../Telegram/build/qmake/codegen_numbers/codegen_numbers.pro
make $ARGS

# Building MetaLang...
mkdir -p "$SRCDIR/tdesktop/Linux/ReleaseIntermediateLang"
cd "$SRCDIR/tdesktop/Linux/ReleaseIntermediateLang"
qmake CONFIG+=release "../../Telegram/MetaLang.pro"
make $ARGS

# Building Telegram Desktop...
mkdir -p "$SRCDIR/tdesktop/Linux/ReleaseIntermediate"
cd "$SRCDIR/tdesktop/Linux/ReleaseIntermediate"
./../codegen/Release/codegen_style "-I./../../Telegram/Resources" "-I./../../Telegram/SourceFiles" "-o./GeneratedFiles/styles" all_files.style --rebuild
./../codegen/Release/codegen_numbers "-o./GeneratedFiles" "./../../Telegram/Resources/numbers.txt"
./../ReleaseLang/MetaLang -lang_in ./../../Telegram/Resources/langs/lang.strings -lang_out ./GeneratedFiles/lang_auto
qmake CONFIG+=release QT_TDESKTOP_PATH="/usr/local/Qt-${_QTVERSION}" QT_TDESKTOP_VERSION=$_QTVERSION "../../Telegram/Telegram.pro"
make $ARGS 
