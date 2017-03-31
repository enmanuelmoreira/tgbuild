# Build Telegram Desktop RPM package from sources
This will build telegram-desktop RPM package from sources. Just follow instructions or just enable repository and install package pre-built from this sources.

# Clone this repository
First you need to clone this repository with SPECs and patches to any directory:
```bash
git clone -b master https://github.com/xvitaly/tgbuild.git tgbuild
```

You can also select branch:
 * **master** (default) - SPEC and patches for current stable branch of Telegram Desktop;
 * **unstable** - SPEC and patches for latest unstable development (alpha) branch of Telegram Desktop.

# Build package from sources manually
Select one of these ways:
 * [build using mock](doc/build_using_mock.md) (recommended);
 * [build using rpmbuild](doc/build_using_rpmbuild.md).

# Install pre-built from this sources packages
You can also install pre-built from this sources package from russianfedora-free repository (maybe it will be added to RPMFusion later; package is still waiting for [package review](https://bugzilla.rpmfusion.org/show_bug.cgi?id=4285)).

Add RPMFusion repository:
```bash
sudo dnf install --nogpgcheck https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm https://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm
```

Add RussianFedora repository:
```bash
sudo dnf install --nogpgcheck https://mirror.yandex.ru/fedora/russianfedora/russianfedora/free/fedora/russianfedora-free-release-stable.noarch.rpm https://mirror.yandex.ru/fedora/russianfedora/russianfedora/nonfree/fedora/russianfedora-nonfree-release-stable.noarch.rpm
```

Now install Telegram Desktop:
```bash
sudo dnf install telegram-desktop
```
