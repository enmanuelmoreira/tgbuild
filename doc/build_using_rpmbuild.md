# Build using rpmbuild
## Prepare build environment
## Step 1

Clone this repository with SPECs and patches to any directory:
```bash
git clone -b master https://github.com/xvitaly/tgbuild.git tgbuild
```

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

## Building required VoIP library
### Step 4

Download sources:
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

Install build-requirements:
```bash
cd tgbuild
sudo dnf builddep libtgvoip.spec
```

### Step 7

Build RPM package:
```bash
rpmbuild -ba libtgvoip.spec
```

### Step 8

Wait for a while and then install result without debug subpackages:
```bash
sudo dnf install ~/rpmbuild/RPMS/$(uname -m)/libtgvoip*.rpm --exclude="*debug*"
```

## Building Telegram Desktop package
### Step 9

Download sources:
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

Install build-requirements:
```bash
cd tgbuild
sudo dnf builddep telegram-desktop.spec
```

### Step 12

Build RPM package:
```bash
rpmbuild -ba telegram-desktop.spec
```

### Step 13

Wait for a while and then install result without debug subpackages:
```bash
sudo dnf install ~/rpmbuild/RPMS/$(uname -m)/telegram-desktop*.rpm  --exclude="*debug*"
```

### Step 14

Now you can remove all files from `~/rpmbuild` directory.
