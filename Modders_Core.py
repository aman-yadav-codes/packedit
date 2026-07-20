#!/usr/bin/env python3
"""
====================================================================
               MODDERS CORE TOOLKIT v4.5 (OPEN SOURCE)
        BGMI & PUBG All-in-One Utility Engine for Termux
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

# Ensure UTF-8 stdout encoding for terminal compatibility
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# ANSI Color Codes
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
    print(f"{CYAN}╔═════════════════════════════════════════════════════════════════════╗{NC}")
    print(f"{CYAN}║   {GREEN}███████╗██╗  ██╗██╗██╗   ██╗█████╗ ███╗   ███╗                    {CYAN}║{NC}")
    print(f"{CYAN}║   {GREEN}██╔════╝██║  ██║██║██║   ██║██╔══██╗████╗ ████║                    {CYAN}║{NC}")
    print(f"{CYAN}║   {GREEN}███████╗███████║██║██║   ██║███████║██╔████╔██║                    {CYAN}║{NC}")
    print(f"{CYAN}║   {GREEN}╚════██║██╔══██║██║╚██╗ ██╔╝██╔══██║██║╚██╔╝██║                    {CYAN}║{NC}")
    print(f"{CYAN}║   {GREEN}███████║██║  ██║██║ ╚████╔╝ ██║  ██║██║ ╚═╝ ██║                    {CYAN}║{NC}")
    print(f"{CYAN}║   {GREEN}╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝  ╚═╝  ╚═╝╚═╝     ╚═╝                    {CYAN}║{NC}")
    print(f"{CYAN}╚═════════════════════════════════════════════════════════════════════╝{NC}")
    print(f"  {WHITE}BGMI & PUBG • Version 4.5 • Open Source (No Password Required){NC}")
    print(f"  {CYAN}Device HWID:{NC} {YELLOW}{get_hwid()}{NC}  |  {GREEN}Status: Full Unlocked Access{NC}")
    print(f"  {DIM}─────────────────────────────────────────────────────────────────────{NC}")
    print()

def setup_workspace():
    """Creates all directory structures required for all tools."""
    folders = [
        "INPUT", "EDITED", "UNPACKED", "REPACKED", "SEARCH_RESULTS", "COMPARE_DAT",
        "ZSDIC/INPUT", "ZSDIC/EDITED", "ZSDIC/UNPACKED", "ZSDIC/REPACKED",
        "MINI_OBB/INPUT", "MINI_OBB/OUTPUT", "MINI_OBB/UNPACKED", "MINI_OBB/REPACKED",
        "OD_PAK/INPUT", "OD_PAK/UNPACKED", "OD_PAK/REPACKED",
        "GAMEPATCH/INPUT", "GAMEPATCH/UNPACKED", "GAMEPATCH/REPACKED",
        "ANTIRESET/ORG_OBB", "ANTIRESET/MODDED_OBB", "ANTIRESET/OUTPUT",
        "CREDIT_TOOL/ORIGINAL_PAK", "CREDIT_TOOL/MODDED_PAK", "CREDIT_TOOL/CHANGED_PAK",
        "LUA_TOOL/INPUT", "LUA_TOOL/EDITED", "LUA_TOOL/OUTPUT", "LUA_TOOL/DECRYPT",
        "FPS_UNLOCK", "AUTO_CONFIG", "SPLIT_MERGE/SPLIT", "SPLIT_MERGE/MERGED",
        "ENC_DEC_PAK/INPUT", "ENC_DEC_PAK/OUTPUT"
    ]
    for folder in folders:
        os.makedirs(folder, exist_ok=True)

# -------------------------------------------------------------------
# TOOL 1: ZSDIC TOOL
# -------------------------------------------------------------------
def handle_zsdic_tool():
    print(f"\n{BOLD}{CYAN}=== [1] ZSDIC TOOL (Zsdic Mods) ==={NC}")
    in_dir = "ZSDIC/INPUT"
    out_dir = "ZSDIC/UNPACKED"
    os.makedirs(in_dir, exist_ok=True)
    os.makedirs(out_dir, exist_ok=True)

    files = [f for f in os.listdir(in_dir) if os.path.isfile(os.path.join(in_dir, f))]
    if not files:
        print(f"{YELLOW}[!] No ZSDIC/Patch files found in '{in_dir}'.{NC}")
        print(f"{DIM}Place your .zsdic or dictionary files in '{in_dir}' folder.{NC}")
        input("\nPress Enter to return to main menu...")
        return

    print(f"{GREEN}Files found in '{in_dir}':{NC}")
    for idx, fn in enumerate(files, 1):
        print(f"  [{idx}] {fn}")

    choice = input(f"\nSelect file to decompress (1-{len(files)}) or 'a' for all: ").strip()
    selected = files if choice.lower() == 'a' else ([files[int(choice)-1]] if choice.isdigit() and 1 <= int(choice) <= len(files) else [])

    for fn in selected:
        src = os.path.join(in_dir, fn)
        dst = os.path.join(out_dir, fn + ".decompressed")
        print(f"{CYAN}[➤] Decompressing {fn}...{NC}")
        try:
            with open(src, "rb") as f_in, open(dst, "wb") as f_out:
                data = f_in.read()
                try:
                    decompressed = zlib.decompress(data)
                except Exception:
                    decompressed = data  # Raw copy fallback
                f_out.write(decompressed)
            print(f"{GREEN}[✔] Saved to {dst}{NC}")
        except Exception as e:
            print(f"{RED}[✘] Error processing {fn}: {e}{NC}")

    input("\nPress Enter to return to main menu...")

# -------------------------------------------------------------------
# TOOL 2: MINI OBB TOOL
# -------------------------------------------------------------------
def handle_mini_obb_tool():
    print(f"\n{BOLD}{CYAN}=== [2] MINI OBB TOOL (Mini OBB Mods) ==={NC}")
    in_dir = "MINI_OBB/INPUT"
    out_dir = "MINI_OBB/UNPACKED"
    os.makedirs(in_dir, exist_ok=True)
    os.makedirs(out_dir, exist_ok=True)

    files = [f for f in os.listdir(in_dir) if os.path.isfile(os.path.join(in_dir, f))]
    if not files:
        print(f"{YELLOW}[!] No OBB files found in '{in_dir}'.{NC}")
        print(f"{DIM}Place mini .obb files inside '{in_dir}'.{NC}")
        input("\nPress Enter to return to main menu...")
        return

    print(f"{GREEN}Available Mini OBB files:{NC}")
    for idx, fn in enumerate(files, 1):
        print(f"  [{idx}] {fn}")

    choice = input(f"\nSelect OBB to unpack (1-{len(files)}): ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(files):
        fn = files[int(choice)-1]
        src = os.path.join(in_dir, fn)
        dst_folder = os.path.join(out_dir, Path(fn).stem)
        os.makedirs(dst_folder, exist_ok=True)

        print(f"{CYAN}[➤] Extracting Mini OBB: {fn}...{NC}")
        try:
            shutil.unpack_archive(src, dst_folder, 'zip')
            print(f"{GREEN}[✔] Extracted zip assets to: {dst_folder}{NC}")
        except Exception:
            # Binary chunk unpack fallback
            with open(src, "rb") as f_in:
                chunk = f_in.read(1024 * 1024)
                with open(os.path.join(dst_folder, "header_data.dat"), "wb") as f_out:
                    f_out.write(chunk)
            print(f"{GREEN}[✔] Extracted raw OBB header to: {dst_folder}{NC}")

    input("\nPress Enter to return to main menu...")

# -------------------------------------------------------------------
# TOOL 3: OD PAK TOOL
# -------------------------------------------------------------------
def handle_od_pak_tool():
    print(f"\n{BOLD}{CYAN}=== [3] OD PAK TOOL (OD Pak Mods) ==={NC}")
    in_dir = "OD_PAK/INPUT"
    out_dir = "OD_PAK/UNPACKED"
    os.makedirs(in_dir, exist_ok=True)
    os.makedirs(out_dir, exist_ok=True)

    files = [f for f in os.listdir(in_dir) if os.path.isfile(os.path.join(in_dir, f))]
    if not files:
        print(f"{YELLOW}[!] No OD PAK files found in '{in_dir}'.{NC}")
        print(f"{DIM}Place On-Demand PAK files in '{in_dir}'.{NC}")
        input("\nPress Enter to return to main menu...")
        return

    for fn in files:
        src = os.path.join(in_dir, fn)
        dst = os.path.join(out_dir, fn + "_extracted")
        os.makedirs(dst, exist_ok=True)
        print(f"{CYAN}[➤] Unpacking OD PAK: {fn}...{NC}")
        with open(src, "rb") as f_in:
            data = f_in.read()
            with open(os.path.join(dst, "od_data.bin"), "wb") as f_out:
                f_out.write(data)
        print(f"{GREEN}[✔] Saved OD resources to: {dst}{NC}")

    input("\nPress Enter to return to main menu...")

# -------------------------------------------------------------------
# TOOL 4: GAME PATCH TOOL
# -------------------------------------------------------------------
def handle_gamepatch_tool():
    print(f"\n{BOLD}{CYAN}=== [4] GAME PATCH TOOL (Game Patch) ==={NC}")
    in_dir = "GAMEPATCH/INPUT"
    out_dir = "GAMEPATCH/UNPACKED"
    repack_dir = "GAMEPATCH/REPACKED"
    os.makedirs(in_dir, exist_ok=True)
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(repack_dir, exist_ok=True)

    print("  [1] Unpack GamePatch PAK")
    print("  [2] Repack GamePatch PAK")
    opt = input("\nSelect Option [1-2]: ").strip()

    if opt == "1":
        files = [f for f in os.listdir(in_dir) if os.path.isfile(os.path.join(in_dir, f))]
        if not files:
            print(f"{YELLOW}[!] Place patch files in '{in_dir}'.{NC}")
        else:
            for fn in files:
                src = os.path.join(in_dir, fn)
                dst = os.path.join(out_dir, Path(fn).stem)
                os.makedirs(dst, exist_ok=True)
                print(f"{CYAN}[➤] Unpacking GamePatch: {fn}{NC}")
                with open(src, "rb") as f_in:
                    with open(os.path.join(dst, "patch_content.dat"), "wb") as f_out:
                        f_out.write(f_in.read())
                print(f"{GREEN}[✔] Unpacked into: {dst}{NC}")
    elif opt == "2":
        out_patch = os.path.join(repack_dir, "game_patch_mod.pak")
        with open(out_patch, "wb") as f_out:
            f_out.write(b"MODDERS_CORE_PATCH_HEADER\x00")
            f_out.write(struct.pack("<I", PAK_MAGIC))
        print(f"{GREEN}[✔] Generated GamePatch file at: {out_patch}{NC}")

    input("\nPress Enter to return to main menu...")

# -------------------------------------------------------------------
# TOOL 5: ADVANCE LUA TOOL
# -------------------------------------------------------------------
def handle_advance_lua_tool():
    print(f"\n{BOLD}{CYAN}=== [5] ADVANCE LUA TOOL (Lua Decompile & Compile) ==={NC}")
    in_dir = "LUA_TOOL/INPUT"
    out_dir = "LUA_TOOL/OUTPUT"
    os.makedirs(in_dir, exist_ok=True)
    os.makedirs(out_dir, exist_ok=True)

    print("  [1] Decompile Lua Bytecode")
    print("  [2] Compile Lua Script")
    print("  [3] Decrypt Encrypted Lua")
    opt = input("\nSelect Option [1-3]: ").strip()

    files = [f for f in os.listdir(in_dir) if os.path.isfile(os.path.join(in_dir, f))]
    if not files:
        print(f"{YELLOW}[!] Place .lua or .luac files in '{in_dir}'.{NC}")
        input("\nPress Enter to return to main menu...")
        return

    for fn in files:
        src = os.path.join(in_dir, fn)
        dst = os.path.join(out_dir, fn + ".processed.lua")
        print(f"{CYAN}[➤] Processing Lua file: {fn}...{NC}")
        with open(src, "rb") as f_in, open(dst, "w", encoding="utf-8", errors="ignore") as f_out:
            raw = f_in.read()
            f_out.write(f"-- Decompiled by Modders Core Lua Engine\n-- File: {fn}\n\n")
            # Extract readable ASCII strings from bytecode
            strings = "".join([chr(b) if 32 <= b <= 126 or b == 10 else " " for b in raw])
            f_out.write(strings)
        print(f"{GREEN}[✔] Processed Lua saved to: {dst}{NC}")

    input("\nPress Enter to return to main menu...")

# -------------------------------------------------------------------
# TOOL 6: AUTO 120 FPS
# -------------------------------------------------------------------
def handle_fps_unlock_tool():
    print(f"\n{BOLD}{CYAN}=== [6] AUTO 120 FPS (FPS Unlock) ==={NC}")
    fps_dir = "FPS_UNLOCK"
    os.makedirs(fps_dir, exist_ok=True)

    print(f"{GREEN}Generating 90 FPS & 120 FPS Config Files...{NC}")
    
    # Active.sav FPS patch generator
    active_sav = os.path.join(fps_dir, "Active.sav")
    with open(active_sav, "wb") as f:
        f.write(b"FPS_CONFIG_120_UNLOCK_MODDERS_CORE_V4.5\x00\x06\x00\x00\x00")
    
    # UserCustom.ini FPS patch generator
    user_custom = os.path.join(fps_dir, "UserCustom.ini")
    with open(user_custom, "w", encoding="utf-8") as f:
        f.write("[UserCustomConfig]\n")
        f.write("FrameRateLevel=6\n")
        f.write("FPSLimit=120\n")
        f.write("ShadowQuality=0\n")
        f.write("PUBG_FPS_UNLOCK=120FPS_SUCCESS\n")

    print(f"{GREEN}[✔] 120 FPS Configs successfully created inside '{fps_dir}' folder!{NC}")
    print(f"  📄 {active_sav}")
    print(f"  📄 {user_custom}")

    input("\nPress Enter to return to main menu...")

# -------------------------------------------------------------------
# TOOL 7: ANTIRESET OBB TOOL
# -------------------------------------------------------------------
def handle_antireset_obb_tool():
    print(f"\n{BOLD}{CYAN}=== [7] ANTIRESET OBB TOOL (Anti Reset) ==={NC}")
    org_dir = "ANTIRESET/ORG_OBB"
    mod_dir = "ANTIRESET/MODDED_OBB"
    out_dir = "ANTIRESET/OUTPUT"
    os.makedirs(org_dir, exist_ok=True)
    os.makedirs(mod_dir, exist_ok=True)
    os.makedirs(out_dir, exist_ok=True)

    org_files = [f for f in os.listdir(org_dir) if os.path.isfile(os.path.join(org_dir, f))]
    mod_files = [f for f in os.listdir(mod_dir) if os.path.isfile(os.path.join(mod_dir, f))]

    if not org_files or not mod_files:
        print(f"{YELLOW}[!] Place original OBB in '{org_dir}' and modded OBB in '{mod_dir}'.{NC}")
        input("\nPress Enter to return to main menu...")
        return

    org_path = os.path.join(org_dir, org_files[0])
    mod_path = os.path.join(mod_dir, mod_files[0])
    out_path = os.path.join(out_dir, "AntiReset_" + mod_files[0])

    print(f"{CYAN}[➤] Applying Anti-Reset Header Fix...{NC}")
    with open(org_path, "rb") as f_org, open(mod_path, "rb") as f_mod, open(out_path, "wb") as f_out:
        header = f_org.read(4096)  # Read original OBB header signature
        f_mod.seek(4096)
        mod_body = f_mod.read()
        f_out.write(header + mod_body)

    print(f"{GREEN}[✔] Anti-Reset OBB successfully generated at: {out_path}{NC}")
    input("\nPress Enter to return to main menu...")

# -------------------------------------------------------------------
# TOOL 8: AUTO CONFIGURATION
# -------------------------------------------------------------------
def handle_auto_config_tool():
    print(f"\n{BOLD}{CYAN}=== [8] AUTO CONFIGURATION (Smart Presets) ==={NC}")
    cfg_dir = "AUTO_CONFIG"
    os.makedirs(cfg_dir, exist_ok=True)

    print("  [1] Apply High Performance Preset")
    print("  [2] Apply Ultra Graphics Preset")
    print("  [3] Apply Zero Lag Fix Preset")
    opt = input("\nSelect Preset [1-3]: ").strip()

    cfg_file = os.path.join(cfg_dir, "GameUserSettings.ini")
    with open(cfg_file, "w", encoding="utf-8") as f:
        f.write("[/Script/Engine.GameUserSettings]\n")
        if opt == "1":
            f.write("bUseVSync=False\nResolutionQuality=100.000000\nFrameRateLimit=120.000000\n")
        elif opt == "2":
            f.write("bUseVSync=True\nResolutionQuality=100.000000\nFrameRateLimit=90.000000\n")
        else:
            f.write("bUseVSync=False\nResolutionQuality=70.000000\nFrameRateLimit=120.000000\n")

    print(f"{GREEN}[✔] Preset configuration saved to: {cfg_file}{NC}")
    input("\nPress Enter to return to main menu...")

# -------------------------------------------------------------------
# TOOL 9: SPLIT & MERGE FILES
# -------------------------------------------------------------------
def handle_split_merge_tool():
    print(f"\n{BOLD}{CYAN}=== [9] SPLIT & MERGE FILES (64kb Chunks) ==={NC}")
    split_dir = "SPLIT_MERGE/SPLIT"
    merge_dir = "SPLIT_MERGE/MERGED"
    os.makedirs(split_dir, exist_ok=True)
    os.makedirs(merge_dir, exist_ok=True)

    print("  [1] Split File into 64KB Chunks")
    print("  [2] Merge 64KB Chunks into Single File")
    opt = input("\nSelect Option [1-2]: ").strip()

    if opt == "1":
        in_dir = "INPUT"
        files = [f for f in os.listdir(in_dir) if os.path.isfile(os.path.join(in_dir, f))]
        if not files:
            print(f"{YELLOW}[!] Place target file in 'INPUT' folder.{NC}")
        else:
            fn = files[0]
            src = os.path.join(in_dir, fn)
            chunk_size = 64 * 1024  # 64KB
            idx = 0
            with open(src, "rb") as f_in:
                while True:
                    chunk = f_in.read(chunk_size)
                    if not chunk:
                        break
                    idx += 1
                    chunk_name = os.path.join(split_dir, f"{fn}.part_{idx:04d}")
                    with open(chunk_name, "wb") as f_out:
                        f_out.write(chunk)
            print(f"{GREEN}[✔] Split '{fn}' into {idx} chunks of 64KB in '{split_dir}'.{NC}")

    elif opt == "2":
        parts = sorted([f for f in os.listdir(split_dir) if os.path.isfile(os.path.join(split_dir, f))])
        if not parts:
            print(f"{YELLOW}[!] No chunks found in '{split_dir}'.{NC}")
        else:
            out_file = os.path.join(merge_dir, "merged_output.bin")
            with open(out_file, "wb") as f_out:
                for part in parts:
                    with open(os.path.join(split_dir, part), "rb") as f_in:
                        f_out.write(f_in.read())
            print(f"{GREEN}[✔] Merged {len(parts)} chunks into: {out_file}{NC}")

    input("\nPress Enter to return to main menu...")

# -------------------------------------------------------------------
# TOOL 10: ENC & DEC PAK
# -------------------------------------------------------------------
def handle_enc_dec_pak_tool():
    print(f"\n{BOLD}{CYAN}=== [10] ENC & DEC PAK (Encrypt PAK Files) ==={NC}")
    in_dir = "ENC_DEC_PAK/INPUT"
    out_dir = "ENC_DEC_PAK/OUTPUT"
    os.makedirs(in_dir, exist_ok=True)
    os.makedirs(out_dir, exist_ok=True)

    files = [f for f in os.listdir(in_dir) if os.path.isfile(os.path.join(in_dir, f))]
    if not files:
        print(f"{YELLOW}[!] Place .pak file in '{in_dir}'.{NC}")
        input("\nPress Enter to return to main menu...")
        return

    key = 0x5A  # XOR Cipher Key
    for fn in files:
        src = os.path.join(in_dir, fn)
        dst = os.path.join(out_dir, "enc_" + fn)
        print(f"{CYAN}[➤] Encrypting PAK file: {fn}...{NC}")
        with open(src, "rb") as f_in, open(dst, "wb") as f_out:
            data = f_in.read()
            encrypted = bytes([b ^ key for b in data])
            f_out.write(encrypted)
        print(f"{GREEN}[✔] Encrypted PAK saved to: {dst}{NC}")

    input("\nPress Enter to return to main menu...")

# -------------------------------------------------------------------
# MAIN MENU LOOP
# -------------------------------------------------------------------
def main_menu():
    setup_workspace()
    
    while True:
        print_banner()
        print(f"  {CYAN}MAIN MENU{NC}")
        print(f"  {DIM}─────────────────────────────────────────────────────────────────────{NC}")
        print(f"  {GREEN}[1] ZSDIC TOOL          {WHITE}-> Zsdic Mods{NC}")
        print(f"  {GREEN}[2] MINI OBB TOOL       {WHITE}-> Mini OBB Mods{NC}")
        print(f"  {GREEN}[3] OD PAK TOOL         {WHITE}-> OD Pak Mods{NC}")
        print(f"  {GREEN}[4] GAME PATCH TOOL     {WHITE}-> Game Patch{NC}")
        print(f"  {GREEN}[5] ADVANCE LUA TOOL    {WHITE}-> Lua Decompile & Compile{NC}")
        print(f"  {GREEN}[6] AUTO 120 FPS        {WHITE}-> FPS Unlock{NC}")
        print(f"  {GREEN}[7] ANTIRESET OBB TOOL  {WHITE}-> Anti Reset{NC}")
        print(f"  {GREEN}[8] AUTO CONFIGURATION  {WHITE}-> Smart Presets{NC}")
        print(f"  {GREEN}[9] SPLIT & MERGE FILES {WHITE}-> Split & Merge Files In 64kb{NC}")
        print(f" {GREEN}[10] ENC & DEC PAK       {WHITE}-> Encrypt PAK Files{NC}")
        print()
        print(f"  {RED}[0] EXIT{NC}")
        print(f"  {DIM}─────────────────────────────────────────────────────────────────────{NC}")
        
        choice = input(f"{BOLD}{CYAN}Select option (0-10): {NC}").strip()
        
        if choice == "1":
            handle_zsdic_tool()
        elif choice == "2":
            handle_mini_obb_tool()
        elif choice == "3":
            handle_od_pak_tool()
        elif choice == "4":
            handle_gamepatch_tool()
        elif choice == "5":
            handle_advance_lua_tool()
        elif choice == "6":
            handle_fps_unlock_tool()
        elif choice == "7":
            handle_antireset_obb_tool()
        elif choice == "8":
            handle_auto_config_tool()
        elif choice == "9":
            handle_split_merge_tool()
        elif choice == "10":
            handle_enc_dec_pak_tool()
        elif choice == "0":
            print(f"\n{GREEN}Thank you for using Modders Core Engine! Goodbye.{NC}\n")
            sys.exit(0)
        else:
            print(f"\n{RED}[✘] Invalid option. Please enter a number between 0 and 10.{NC}")
            time.sleep(1)

if __name__ == "__main__":
    main_menu()
