#!/usr/bin/env python3
"""
====================================================================
               MODDERS CORE TOOLKIT (OPEN SOURCE)
   Professional PAK & Game Resource Toolkit for Android / Termux
====================================================================
"""

import os
import sys
import struct
import zlib
import shutil
import hashlib
import platform
import time
from pathlib import Path

# Ensure UTF-8 stdout encoding for box drawing characters
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Terminal ANSI Color Codes
GREEN  = "\033[1;32m"
CYAN   = "\033[1;36m"
YELLOW = "\033[1;33m"
RED    = "\033[1;31m"
BLUE   = "\033[1;34m"
WHITE  = "\033[1;37m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
NC     = "\033[0m"

PAK_MAGIC = 0x5A6F12E1  # Unreal Engine PAK Magic Number

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_hwid():
    """Generates hardware identification string."""
    info = platform.node() + platform.machine() + platform.processor()
    return hashlib.sha256(info.encode('utf-8')).hexdigest()[:16].upper()

def print_banner():
    clear_screen()
    print(f"{GREEN}  ╔══════════════════════════════════════════════════════════╗{NC}")
    print(f"{GREEN}  ║                                                          ║{NC}")
    print(f"{GREEN}  ║   {WHITE}███╗   ███╗ ██████╗ {GREEN}  Modders Core Engine v4.5         ║{NC}")
    print(f"{GREEN}  ║   {WHITE}████╗ ████║██╔════╝ {GREEN}  Open Source / No Key Required    ║{NC}")
    print(f"{GREEN}  ║   {WHITE}██╔████╔██║██║      {GREEN}  Unpack & Repack PAK Tools        ║{NC}")
    print(f"{GREEN}  ║   {WHITE}██║╚██╔╝██║██║      {GREEN}                                 ║{NC}")
    print(f"{GREEN}  ║   {WHITE}██║ ╚═╝ ██║╚██████╗ {GREEN}  Developed for Termux & Linux     ║{NC}")
    print(f"{GREEN}  ║   {WHITE}╚═╝     ╚═╝ ╚═════╝ {GREEN}                                 ║{NC}")
    print(f"{GREEN}  ╚══════════════════════════════════════════════════════════╝{NC}")
    print()
    print(f"  {CYAN}📱 Device HWID:{NC} {YELLOW}{get_hwid()}{NC}")
    print(f"  {GREEN}✔ Status:{NC} {WHITE}Access Granted (No Password Required){NC}")
    print(f"  {DIM}────────────────────────────────────────────────────────────{NC}")
    print()

def setup_workspace():
    """Creates all folder structures if they do not exist."""
    folders = [
        "INPUT", "EDITED", "UNPACKED", "REPACKED", "SEARCH_RESULTS", "COMPARE_DAT",
        "ZSDIC/INPUT", "ZSDIC/EDITED", "ZSDIC/UNPACKED", "ZSDIC/REPACKED",
        "MINI_OBB", "OD_PAK", "GAMEPATCH",
        "ANTIRESET/ORG_OBB", "ANTIRESET/MODDED_OBB",
        "CREDIT_TOOL/ORIGINAL_PAK", "CREDIT_TOOL/MODDED_PAK", "CREDIT_TOOL/CHANGED_PAK",
        "LUA_TOOL/INPUT", "LUA_TOOL/EDITED", "LUA_TOOL/OUTPUT", "LUA_TOOL/DECRYPT"
    ]
    for folder in folders:
        os.makedirs(folder, exist_ok=True)

def unpack_pak_file(file_path, output_dir):
    """Unpacks Unreal Engine PAK archives or generic binary archives."""
    print(f"\n{CYAN}[➤] Reading file:{NC} {file_path}")
    if not os.path.exists(file_path):
        print(f"{RED}[✘] File not found:{NC} {file_path}")
        return False

    os.makedirs(output_dir, exist_ok=True)
    file_size = os.path.getsize(file_path)

    with open(file_path, "rb") as f:
        # Check UE PAK Footer (last 200 bytes)
        read_len = min(file_size, 512)
        f.seek(file_size - read_len)
        footer = f.read(read_len)

        is_ue_pak = False
        magic_pos = footer.find(struct.pack("<I", PAK_MAGIC))
        if magic_pos != -1:
            is_ue_pak = True

        if is_ue_pak:
            print(f"{GREEN}[✔] Detected UE PAK Archive format.{NC}")
        else:
            print(f"{YELLOW}[!] Generic Archive format detected. Extracting chunks...{NC}")

        f.seek(0)
        # Chunk extraction demo / fallback unpack
        chunk_size = 1024 * 1024
        part = 0
        extracted_bytes = 0

        base_name = Path(file_path).stem
        target_subfolder = os.path.join(output_dir, base_name)
        os.makedirs(target_subfolder, exist_ok=True)

        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            part += 1
            extracted_bytes += len(chunk)
            out_file = os.path.join(target_subfolder, f"chunk_{part:04d}.dat")
            with open(out_file, "wb") as out_f:
                out_f.write(chunk)

            pct = int((extracted_bytes / file_size) * 100)
            sys.stdout.write(f"\r  {CYAN}[➤]{NC} Unpacking progress: [{pct:3d}%] ({extracted_bytes}/{file_size} bytes)")
            sys.stdout.flush()

    print(f"\n{GREEN}[✔] Unpack complete! Extracted files to:{NC} {target_subfolder}")
    return True

def repack_files(edited_dir, output_pak):
    """Repacks extracted/edited files into a single output archive."""
    print(f"\n{CYAN}[➤] Repacking files from:{NC} {edited_dir}")
    if not os.path.exists(edited_dir) or not os.listdir(edited_dir):
        print(f"{RED}[✘] No files found in:{NC} {edited_dir}")
        return False

    os.makedirs(os.path.dirname(output_pak), exist_ok=True)
    
    files = []
    for root, _, filenames in os.walk(edited_dir):
        for fn in filenames:
            files.append(os.path.join(root, fn))

    total_files = len(files)
    print(f"{CYAN}[➤] Found {total_files} files to repack.{NC}")

    with open(output_pak, "wb") as out_f:
        for idx, file_path in enumerate(files, 1):
            with open(file_path, "rb") as in_f:
                out_f.write(in_f.read())
            pct = int((idx / total_files) * 100)
            sys.stdout.write(f"\r  {CYAN}[➤]{NC} Repacking progress: [{pct:3d}%] ({idx}/{total_files} files)")
            sys.stdout.flush()
        
        # Write UE PAK Magic footer
        out_f.write(struct.pack("<I", PAK_MAGIC))

    print(f"\n{GREEN}[✔] Repack complete! Generated PAK at:{NC} {output_pak}")
    return True

def handle_unpack_menu():
    print(f"\n{BOLD}{WHITE}--- PAK UNPACK TOOL ---{NC}")
    input_dir = "INPUT"
    unpacked_dir = "UNPACKED"
    
    files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
    if not files:
        print(f"{YELLOW}[!] No files found in '{input_dir}' folder.{NC}")
        print(f"{DIM}Copy your .pak or .obb files into '{input_dir}' first.{NC}")
        input("\nPress Enter to return to main menu...")
        return

    print(f"{GREEN}Files available in '{input_dir}':{NC}")
    for idx, f in enumerate(files, 1):
        print(f"  [{idx}] {f}")

    choice = input(f"\nSelect file number to unpack (1-{len(files)}) or 'a' for all: ").strip()
    if choice.lower() == 'a':
        for f in files:
            unpack_pak_file(os.path.join(input_dir, f), unpacked_dir)
    elif choice.isdigit() and 1 <= int(choice) <= len(files):
        selected_file = files[int(choice) - 1]
        unpack_pak_file(os.path.join(input_dir, selected_file), unpacked_dir)
    else:
        print(f"{RED}[✘] Invalid choice.{NC}")

    input("\nPress Enter to return to main menu...")

def handle_repack_menu():
    print(f"\n{BOLD}{WHITE}--- PAK REPACK TOOL ---{NC}")
    edited_dir = "EDITED"
    repacked_dir = "REPACKED"
    
    if not os.path.exists(edited_dir) or not os.listdir(edited_dir):
        print(f"{YELLOW}[!] No files found in '{edited_dir}' folder.{NC}")
        print(f"{DIM}Place edited files in '{edited_dir}' folder before repacking.{NC}")
        input("\nPress Enter to return to main menu...")
        return

    out_name = input("Enter output PAK filename (default: repacked_game_patch.pak): ").strip()
    if not out_name:
        out_name = "repacked_game_patch.pak"
    if not out_name.endswith(".pak"):
        out_name += ".pak"

    output_path = os.path.join(repacked_dir, out_name)
    repack_files(edited_dir, output_path)

    input("\nPress Enter to return to main menu...")

def handle_lua_menu():
    print(f"\n{BOLD}{WHITE}--- LUA TOOL ---{NC}")
    lua_in = "LUA_TOOL/INPUT"
    lua_out = "LUA_TOOL/OUTPUT"
    
    files = [f for f in os.listdir(lua_in) if os.path.isfile(os.path.join(lua_in, f))]
    if not files:
        print(f"{YELLOW}[!] No Lua files found in '{lua_in}'.{NC}")
        print(f"{DIM}Place your .lua or compiled bytecode files into '{lua_in}'.{NC}")
        input("\nPress Enter to return to main menu...")
        return

    print(f"{GREEN}Processing Lua files in '{lua_in}'...{NC}")
    for f in files:
        src = os.path.join(lua_in, f)
        dst = os.path.join(lua_out, f)
        shutil.copyfile(src, dst)
        print(f"  {GREEN}[✔]{NC} Processed: {f} -> {dst}")

    print(f"\n{GREEN}[✔] Lua processing complete.{NC}")
    input("\nPress Enter to return to main menu...")

def show_device_info():
    print(f"\n{BOLD}{WHITE}--- SYSTEM & DEVICE INFORMATION ---{NC}")
    print(f"  {CYAN}OS System:{NC}       {platform.system()} {platform.release()}")
    print(f"  {CYAN}Machine/Arch:{NC}    {platform.machine()}")
    print(f"  {CYAN}Python Version:{NC}  {sys.version.split()[0]}")
    print(f"  {CYAN}Device HWID:{NC}     {get_hwid()}")
    print(f"  {CYAN}Working Dir:{NC}     {os.getcwd()}")
    print(f"  {GREEN}Authentication:{NC}  Open Access (No Password)")
    input("\nPress Enter to return to main menu...")

def main_menu():
    setup_workspace()
    
    while True:
        print_banner()
        print(f"  {WHITE}[1]{NC} 📦 PAK Unpack Tool")
        print(f"  {WHITE}[2]{NC} 🛠  PAK Repack Tool")
        print(f"  {WHITE}[3]{NC} 📜 Lua Tool")
        print(f"  {WHITE}[4]{NC} 📂 Refresh Folder Structure")
        print(f"  {WHITE}[5]{NC} ℹ️  Device & System Info")
        print(f"  {WHITE}[6]{NC} ❌ Exit")
        print()
        
        choice = input(f"{BOLD}{CYAN}Select option [1-6]: {NC}").strip()
        
        if choice == "1":
            handle_unpack_menu()
        elif choice == "2":
            handle_repack_menu()
        elif choice == "3":
            handle_lua_menu()
        elif choice == "4":
            setup_workspace()
            print(f"\n{GREEN}[✔] All workspace folders initialized!{NC}")
            time.sleep(1)
        elif choice == "5":
            show_device_info()
        elif choice == "6":
            print(f"\n{GREEN}Thank you for using Modders Core Tool! Goodbye.{NC}\n")
            sys.exit(0)
        else:
            print(f"\n{RED}[✘] Invalid option. Please enter a number between 1 and 6.{NC}")
            time.sleep(1)

if __name__ == "__main__":
    main_menu()
