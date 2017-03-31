# Build using rpmbuild
## Step 1

Clone this repository with SPECs and patches to any directory:
```bash
git clone -b master https://github.com/xvitaly/tgbuild.git tgbuild
```

You can also select branch:
 * **master** (default) - SPEC and patches for current stable branch of Telegram Desktop;
 * **unstable** - SPEC and patches for latest unstable development (alpha) branch of Telegram Desktop.

## Step 2

Install spectool and rpmbuild:
```bash
sudo dnf install rpm-build rpmdevtools
```

## Step 3

Create RPM build base directories:
```bash
rpmdev-setuptree
```

## Step 4

Download sources:
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

Install build-requirements:
```bash
cd tgbuild
sudo dnf builddep telegram-desktop.spec
```

## Step 7

Build RPM package:
```bash
rpmbuild -ba telegram-desktop.spec
```

## Step 8

Wait for a while and then install result:
```bash
sudo dnf install ~/rpmbuild/RPMS/$(uname -m)/telegram-desktop*.rpm
```

## Step 9

Now you can remove all files from `~/rpmbuild` directory.
