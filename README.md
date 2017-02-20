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

# Build using rpmbuild
## Step 1

Install spectool and rpmbuild:
```bash
sudo dnf install rpm-build rpmdevtools
```

## Step 2

Create RPM build base directories:
```bash
rpmdev-setuptree
```

## Step 3

Download sources:
```bash
cd tgbuild
spectool -g -R telegram-desktop.spec
```

## Step 4

Copy other files to sources directory:
```bash
cd tgbuild
cp -f {*.patch,telegram*,tg.protocol} $(rpm --eval %{_sourcedir})
```

## Step 5

Install build-requirements:
```bash
cd tgbuild
sudo dnf builddep telegram-desktop.spec
```

## Step 6

Build RPM package:
```bash
rpmbuild -ba telegram-desktop.spec
```

## Step 7

Wait for a while and then install result:
```bash
sudo dnf install ~/rpmbuild/RPMS/$(uname -m)/telegram-desktop*.rpm
```

## Step 8

Now you can remove all files from `~/rpmbuild` directory.

# Build using mock
## Step 1

Install mock, spectool and rpmbuild:
```bash
sudo dnf install rpm-build rpmdevtools mock mock-rpmfusion-free
```

Add yourself to `mock` group (you must run this only for the first time after installing mock):
```bash
sudo usermod -a -G mock $(whoami)
```
You need to relogin to your system after doing this.

## Step 2

Create RPM build base directories:
```bash
rpmdev-setuptree
```

## Step 3

Download Telegram Desktop sources:
```bash
cd tgbuild
spectool -g -R telegram-desktop.spec
```

## Step 4

Copy other files to sources directory:
```bash
cd tgbuild
cp -f {*.patch,telegram*,tg.protocol} $(rpm --eval %{_sourcedir})
```

## Step 5

Generate SRPM package for mock:
```bash
rpmbuild -bs telegram-desktop.spec
```

## Step 6

Start mock build sequence:
```bash
mock -r fedora-$(rpm -E %fedora)-$(uname -m)-rpmfusion_free --rebuild ~/rpmbuild/SRPMS/telegram-desktop*.src.rpm
```

## Step 7

Wait for a while and then install result:
```bash
sudo dnf install /var/lib/mock/*/result/telegram-desktop*.rpm
```

## Step 8

Remove temporary files from `~/rpmbuild`, `/var/cache/mock`, `/var/lib/mock` directories.

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
