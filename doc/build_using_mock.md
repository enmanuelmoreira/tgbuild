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
