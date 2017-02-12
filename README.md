# Build Telegram Desktop RPM package from sources
This will build telegram-desktop RPM package from sources. Just follow instructions or just enable repository and install pre-built from this sources and SPECs package.

# Clone this repository
First you need to clone this repository with SPECs and patches to any directory:
```bash
git clone https://github.com/xvitaly/tgbuild.git tgbuild
```

You can also select branch:
 * **master** (default) - SPEC and patches for current stable branch of Telegram Desktop;
 * **dev** - SPEC and patches for latest unstable development (alpha) branch of Telegram Desktop.

```bash
cd tgbuild
git checkout master
```

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
sudo dnf install /var/lib/mock/results/telegram-desktop*.rpm
```

## Step 8

Remove temporary files from `~/rpmbuild`, `/var/cache/mock`, `/var/lib/mock`.
