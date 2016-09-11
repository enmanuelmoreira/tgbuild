# Build Telegram Desktop from sources
This script will download sources of Telegram Desktop and all required libraries.

*DO NOT RUN THIS SCRIPT OUTSIDE VIRTUAL MACHINE!*

Step 1
========
Install clean Fedora from official ISO's into VirtualBox or other VM.

Step 2
========
Launch installed VM. Install guest additions if needed.

Step 3
========
Download Git repository with build scripts:
```bash
git clone https://github.com/xvitaly/tgbuild.git tgbuild
```

Step 4
========
Change current directory and execute build script:
```bash
cd tgbuild
./build_tg.sh
```

Step 5
========
Wait and enter sudo password when prompted.

Step 6
========
Extract result binary *tdesktop/Linux/Release/Telegram* from virtual machine.
