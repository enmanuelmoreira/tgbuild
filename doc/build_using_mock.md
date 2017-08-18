# Build using mock
## Prepare build environment
### Step 1

Clone this repository with SPECs and patches to any directory:
```bash
git clone -b master https://github.com/xvitaly/tgbuild.git tgbuild
```

### Step 2

Install mock, spectool and rpmbuild:
```bash
sudo dnf install rpm-build rpmdevtools mock mock-rpmfusion-free
```

Add yourself to `mock` group (you must run this only for the first time after installing mock):
```bash
sudo usermod -a -G mock $(whoami)
```
You need to relogin to your system after doing this or run:
```bash
newgrp mock
```

### Step 3

Create RPM build base directories:
```bash
rpmdev-setuptree
```

## Building required VoIP library
### Step 4

Download libtgvoip sources:
```bash
cd tgbuild
spectool -g -R libtgvoip.spec
```

### Step 5

Copy patches to sources directory:
```bash
cd tgbuild
cp -f *.patch $(rpm --eval %{_sourcedir})
```

### Step 6

Generate SRPM package for mock:
```bash
rpmbuild -bs libtgvoip.spec
```

### Step 7

Start mock build sequence:
```bash
mock -r fedora-$(rpm -E %fedora)-$(uname -m)-rpmfusion_free --rebuild ~/rpmbuild/SRPMS/libtgvoip*.src.rpm
```

### Step 8

Wait for a while and then install result into chroot:
```bash
mock -r fedora-$(rpm -E %fedora)-$(uname -m)-rpmfusion_free --install /var/lib/mock/*/result/libtgvoip*.$(uname -m).rpm
```

## Building Telegram Desktop package
### Step 9

Download Telegram Desktop sources:
```bash
cd tgbuild
spectool -g -R telegram-desktop.spec
```

### Step 10

Copy patches and other files to sources directory:
```bash
cd tgbuild
cp -f *.patch $(rpm --eval %{_sourcedir})
```

### Step 11

Generate SRPM package for mock:
```bash
rpmbuild -bs telegram-desktop.spec
```

### Step 12

Start mock build sequence without chroot cleanup:
```bash
mock -r fedora-$(rpm -E %fedora)-$(uname -m)-rpmfusion_free --rebuild --no-clean ~/rpmbuild/SRPMS/telegram-desktop*.src.rpm
```

### Step 13

Wait for a while and then install result without debug subpackages:
```bash
sudo dnf install /var/lib/mock/*/result/*.$(uname -m).rpm --exclude="*debug*"
```

### Step 14

Remove temporary files from `~/rpmbuild`, `/var/cache/mock`, `/var/lib/mock` directories.
