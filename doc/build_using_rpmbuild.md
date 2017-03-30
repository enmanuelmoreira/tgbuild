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
