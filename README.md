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
mkdir -p ~/rpmbuild/{BUILD,BUILDROOT,RPMS,SOURCES,SPECS,SRPMS}
```

# Step 4

Download sources:
```bash
cd tgbuild
spectool --all --get-files --directory ~/rpmbuild/SOURCES/ telegram-desktop.spec
```

# Step 5

Install build-requirements:
```bash
cd tgbuild
sudo dnf builddep telegram-desktop.spec
```

# Step 6

Build RPM package:
```
rpmbuild -ba telegram-desktop.spec
```

# Step 7

Wait and get result in **~/rpmbuild/RPMS/$(uname -m)/** directory. Just install it.
