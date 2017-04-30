# Build using mock
## Step 1

Clone this repository with SPECs and patches to any directory:
```bash
git clone -b master https://github.com/xvitaly/tgbuild.git tgbuild
```

## Step 2

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

## Step 3

Create RPM build base directories:
```bash
rpmdev-setuptree
```

## Step 4

Download Telegram Desktop sources:
```bash
cd tgbuild
spectool -g -R telegram-desktop.spec
```

## Step 5

Copy other files to sources directory:
```bash
cd tgbuild
cp -f {*.patch,telegram*,tg.protocol} $(rpm --eval %{_sourcedir})
```

## Step 6

Generate SRPM package for mock:
```bash
rpmbuild -bs telegram-desktop.spec
```

## Step 7

Start mock build sequence:
```bash
mock -r fedora-$(rpm -E %fedora)-$(uname -m)-rpmfusion_free --rebuild ~/rpmbuild/SRPMS/telegram-desktop*.src.rpm
```

## Step 8

Wait for a while and then install result:
```bash
sudo dnf install /var/lib/mock/*/result/telegram-desktop*.rpm
```

## Step 9

Remove temporary files from `~/rpmbuild`, `/var/cache/mock`, `/var/lib/mock` directories.
