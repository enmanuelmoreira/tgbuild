# Build Telegram Desktop from sources
This will build telegram-desktop RPM package from sources. Just follow instructions.

# Step 1

Install Git, spectool and rpmbuild:
```bash
sudo dnf install git rpm-build rpmdevtools
```

# Step 2

Download this Git repository:
```bash
git clone https://github.com/xvitaly/tgbuild.git tgbuild
```

# Step 3

Create RPM build base directories:
```bash
rpmdev-setuptree
```

# Step 4

Download sources:
```bash
cd tgbuild
spectool -g -R telegram-desktop.spec
```

# Step 5

Copy other files to sources directory:
```bash
cd tgbuild
cp -f {*.patch,telegram*,tg.protocol} $(rpm --eval %{_sourcedir})
```

# Step 6

Install build-requirements:
```bash
cd tgbuild
sudo dnf builddep telegram-desktop.spec
```

# Step 7

Build RPM package:
```bash
rpmbuild -ba telegram-desktop.spec
```

# Step 8

Wait for a while and then install result:
```bash
sudo dnf install ~/rpmbuild/RPMS/$(uname -m)/telegram-desktop*.rpm
```
