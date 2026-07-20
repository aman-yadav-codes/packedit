# 📱 Termux Step-by-Step Unpack Guide

Follow these exact commands one by one in your Termux app on Android.

---

## 🔹 STEP 1: Update Termux & Install Packages

Copy and paste this line into Termux and press **Enter**:

```bash
pkg update && pkg upgrade -y && pkg install git python -y
```

---

## 🔹 STEP 2: Download & Run Tool

If `curl` shows an error (`CANNOT LINK EXECUTABLE "curl"`), use this **direct Git command** (works 100%):

```bash
git clone https://github.com/aman-yadav-codes/packedit.git ~/Modders_Core && cd ~/Modders_Core && python3 Modders_Core.py
```

Or via curl installer:

```bash
curl -fsSL https://raw.githubusercontent.com/aman-yadav-codes/packedit/main/install.sh | bash
```

---

## 🔹 STEP 3: Fix "Command Not Found" Error

If typing `Modders_Core` says **command not found**, enter the folder directly:

```bash
cd ~/Modders_Core
chmod +x Modders_Core
./Modders_Core
```

---

## 🔹 STEP 4: How to Copy Your .pak File to INPUT

1. Give Termux storage access:
   ```bash
   termux-setup-storage
   ```
2. Copy `game_patch_4.5.0.21343.pak` from your phone Downloads folder to the tool's `INPUT` folder:
   ```bash
   mkdir -p ~/Modders_Core/INPUT
   cp /sdcard/Download/game_patch_4.5.0.21343.pak ~/Modders_Core/INPUT/
   ```

---

## 🔹 STEP 5: Run the Tool and Unpack

Now start the tool:
```bash
cd ~/Modders_Core
./Modders_Core
```

- In the menu screen, select **PAK Unpack** (or **GamePatch Tool**).
- Your unpacked files will be saved in:
  `~/Modders_Core/UNPACKED`

---

## 🔹 STEP 6: Copy Unpacked Files Back to Downloads

To view extracted files in your phone's File Manager:
```bash
cp -r ~/Modders_Core/UNPACKED /sdcard/Download/unpacked_files
```
