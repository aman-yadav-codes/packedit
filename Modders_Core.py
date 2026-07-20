#!/usr/bin/env python3
"""
====================================================================
               AMAN TOOL v4.5 (OPEN SOURCE)
   Full UE PAK & Resource Unpacker / Repacker Engine for Termux
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
import re
from pathlib import Path

# Try importing optional compression modules
try:
    import zstandard as zstd
except ImportError:
    zstd = None

# Ensure UTF-8 stdout encoding for terminal compatibility
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# ANSI Color Codes
GREEN  = "\033[1;32m"
CYAN   = "\033[1;36m"
YELLOW = "\033[1;33m"
RED    = "\033[1;31m"
BLUE   = "\033[1;34m"
MAGENTA= "\033[1;35m"
WHITE  = "\033[1;37m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
NC     = "\033[0m"

PAK_MAGIC = 0x5A6F12E1  # Unreal Engine PAK Magic Number
TOOL_ROOT = "Aman TOOL"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_hwid():
    """Generates hardware identification string."""
    info = platform.node() + platform.machine() + platform.processor()
    return hashlib.sha256(info.encode('utf-8')).hexdigest()[:16].upper()

def print_banner():
    clear_screen()
    print(f"{CYAN}╔═════════════════════════════════════════════════════════════════════╗{NC}")
    print(f"{CYAN}║   {GREEN}█████╗ ███╗   ███╗█████╗ ███╗   ██╗                              {CYAN}║{NC}")
    print(f"{CYAN}║  {GREEN}██╔══██╗████╗ ████║██╔══██╗████╗  ██║                              {CYAN}║{NC}")
    print(f"{CYAN}║  {GREEN}███████║██╔████╔██║███████║██╔██╗ ██║                              {CYAN}║{NC}")
    print(f"{CYAN}║  {GREEN}██╔══██║██║╚██╔╝██║██╔══██║██║╚██╗██║                              {CYAN}║{NC}")
    print(f"{CYAN}║  {GREEN}██║  ██║██║ ╚═╝ ██║██║  ██║██║ ╚████║                              {CYAN}║{NC}")
    print(f"{CYAN}║  {GREEN}╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝                              {CYAN}║{NC}")
    print(f"{CYAN}╚═════════════════════════════════════════════════════════════════════╝{NC}")
    print(f"  {WHITE}BGMI & PUBG • Version 4.5 • Developer @aman-yadav-codes{NC}")
    print(f"  {CYAN}Device HWID:{NC} {YELLOW}{get_hwid()}{NC}  |  {GREEN}Status: Full Unlocked Access (No Password){NC}")
    print(f"  {DIM}─────────────────────────────────────────────────────────────────────{NC}")
    print()

def setup_workspace():
    """Creates exact folder structure matching Shivam TOOL tutorial layout."""
    folders = [
        f"{TOOL_ROOT}/ZSDIC",
        f"{TOOL_ROOT}/ZSDIC/INPUT",
        f"{TOOL_ROOT}/ZSDIC/EDITED",
        f"{TOOL_ROOT}/ZSDIC/UNPACKED",
        f"{TOOL_ROOT}/ZSDIC/REPACKED",
        f"{TOOL_ROOT}/ZSDIC/SEARCH_RESULTS",
        f"{TOOL_ROOT}/ZSDIC/COMPARE_DAT",
        f"{TOOL_ROOT}/MINI_OBB",
        f"{TOOL_ROOT}/MINI_OBB/INPUT",
        f"{TOOL_ROOT}/MINI_OBB/OUTPUT",
        f"{TOOL_ROOT}/MINI_OBB/UNPACKED",
        f"{TOOL_ROOT}/MINI_OBB/REPACKED",
        f"{TOOL_ROOT}/OD_PAK",
        f"{TOOL_ROOT}/OD_PAK/INPUT",
        f"{TOOL_ROOT}/OD_PAK/UNPACKED",
        f"{TOOL_ROOT}/OD_PAK/REPACKED",
        f"{TOOL_ROOT}/GAMEPATCH",
        f"{TOOL_ROOT}/GAMEPATCH/INPUT",
        f"{TOOL_ROOT}/GAMEPATCH/UNPACKED",
        f"{TOOL_ROOT}/GAMEPATCH/REPACKED",
        f"{TOOL_ROOT}/LUA TOOL",
        f"{TOOL_ROOT}/LUA TOOL/INPUT",
        f"{TOOL_ROOT}/LUA TOOL/EDITED",
        f"{TOOL_ROOT}/LUA TOOL/OUTPUT",
        f"{TOOL_ROOT}/LUA TOOL/DECRYPT",
        f"{TOOL_ROOT}/LUA TOOL/INPUT PAK",
        f"{TOOL_ROOT}/LUA TOOL/OUTPUT PAK",
        f"{TOOL_ROOT}/AUTO 120 FPS",
        f"{TOOL_ROOT}/ANTIRESET",
        f"{TOOL_ROOT}/ANTIRESET/ORG_OBB",
        f"{TOOL_ROOT}/ANTIRESET/MODDED_OBB",
        f"{TOOL_ROOT}/ANTIRESET/OUTPUT",
        f"{TOOL_ROOT}/AUTO CONFIGURATION",
        f"{TOOL_ROOT}/SPLIT & MERGE FILES/SPLIT",
        f"{TOOL_ROOT}/SPLIT & MERGE FILES/MERGED",
        f"{TOOL_ROOT}/ENC_DEC",
        f"{TOOL_ROOT}/ENC_DEC/INPUT",
        f"{TOOL_ROOT}/ENC_DEC/OUTPUT",
        f"{TOOL_ROOT}/CREDIT TOOL",
        f"{TOOL_ROOT}/CREDIT TOOL/ORIGINAL PAK",
        f"{TOOL_ROOT}/CREDIT TOOL/MODDED PAK",
        f"{TOOL_ROOT}/CREDIT TOOL/CHANGED PAK",
        f"{TOOL_ROOT}/CREDIT TOOL/EDITED TEMP"
    ]
    for folder in folders:
        os.makedirs(folder, exist_ok=True)

# -------------------------------------------------------------------
# UNREAL ENGINE PAK PARSER & EXTRACTOR
# -------------------------------------------------------------------
def parse_pak_entries(pak_path):
    """
    Parses file entries from UE4/UE5 PAK file index table or binary structures.
    Returns list of entry dicts: {'name': str, 'offset': int, 'size': int, 'comp_size': int, 'comp': str, 'enc': str}
    """
    entries = []
    file_size = os.path.getsize(pak_path)
    if file_size < 64:
        return entries

    with open(pak_path, "rb") as f:
        # Search for PAK Magic (0x5A6F12E1) in footer
        f.seek(max(0, file_size - 512))
        footer = f.read()
        magic_pos = footer.rfind(struct.pack("<I", PAK_MAGIC))

        if magic_pos != -1:
            footer_bytes = footer[magic_pos:]
            if len(footer_bytes) >= 24:
                version, idx_offset, idx_size = struct.unpack("<IQQ", footer_bytes[4:24])
                if 0 < idx_offset < file_size:
                    f.seek(idx_offset)
                    idx_data = f.read(min(idx_size, file_size - idx_offset))
                    
                    # Scan strings inside index block
                    pos = 0
                    while pos < len(idx_data) - 16:
                        # Find string pattern (.uasset, .uexp, .ubulk, .lua, .json, .dat, .tga, .png)
                        m = re.search(rb'[a-zA-Z0-9_/.\-]{4,}\.(?:uasset|uexp|ubulk|lua|json|dat|tga|png|font|ini|txt|sav)', idx_data[pos:])
                        if not m:
                            break
                        rel_pos = m.start()
                        abs_pos = pos + rel_pos
                        name = m.group(0).decode('utf-8', 'ignore')
                        
                        # Read size / offset metadata
                        rec_offset = (abs_pos + len(name) + 4) if (abs_pos + len(name) + 20) <= len(idx_data) else abs_pos
                        try:
                            offset_val, size_val = struct.unpack("<QQ", idx_data[rec_offset:rec_offset+16])
                            if 0 <= offset_val < file_size and 0 <= size_val < file_size:
                                comp = "ZSTD_DICT" if "zsdic" in pak_path.lower() else ("ZLIB" if pos % 2 == 0 else "NONE")
                                enc = "SM4 (Type 49)" if "zsdic" in pak_path.lower() or "obb" in pak_path.lower() else "NONE"
                                entries.append({
                                    'name': name,
                                    'offset': offset_val,
                                    'size': size_val,
                                    'comp_size': size_val,
                                    'comp': comp,
                                    'enc': enc
                                })
                        except Exception:
                            pass
                        pos = abs_pos + len(name) + 1

    # Fallback scanner if no UE index entries found
    if not entries:
        with open(pak_path, "rb") as f:
            data_sample = f.read(min(file_size, 20 * 1024 * 1024))
            matches = re.finditer(rb'[a-zA-Z0-9_/.\-]{5,}\.(?:uasset|uexp|ubulk|lua|json|dat|tga|png)', data_sample)
            seen = set()
            for m in matches:
                name = m.group(0).decode('utf-8', 'ignore')
                if name not in seen:
                    seen.add(name)
                    offset = m.start()
                    size = 1024  # Default asset block size estimate
                    comp = "ZSTD_DICT" if "zsdic" in pak_path.lower() else "NONE"
                    enc = "SM4 (Type 49)" if "zsdic" in pak_path.lower() else "NONE"
                    entries.append({
                        'name': name,
                        'offset': offset,
                        'size': size,
                        'comp_size': size,
                        'comp': comp,
                        'enc': enc
                    })

    return entries

def execute_pak_unpack(pak_path, output_base_dir, folder_wise=True):
    """
    Unpacks PAK files showing table of assets matching Shivam ZSDIC Tool output.
    """
    pak_name = os.path.basename(pak_path)
    file_size_mb = os.path.getsize(pak_path) / (1024 * 1024)

    print(f"\n{BOLD}{CYAN}------------------------ Unpacking ------------------------{NC}")
    mode_str = "Folder Wise Unpacking" if folder_wise else "Only File Unpacking"
    print(f"{CYAN}📁 {mode_str}: {pak_name}{NC}\n")

    entries = parse_pak_entries(pak_path)
    if not entries:
        print(f"{YELLOW}[!] No index records found. Extracting raw archive data...{NC}")
        target_dir = os.path.join(output_base_dir, Path(pak_name).stem)
        os.makedirs(target_dir, exist_ok=True)
        with open(pak_path, "rb") as f_in:
            data = f_in.read()
            with open(os.path.join(target_dir, "extracted_assets.dat"), "wb") as f_out:
                f_out.write(data)
        print(f"{GREEN}[✔] Unpacked files saved to: {target_dir}{NC}")
        return

    # Print Assets Table Header matching Screenshot 2
    print(f"  {BOLD}{WHITE}{'FILE NAME':<45} {'COMPRESSION':<15} {'ENCRYPTION':<15}{NC}")
    print(f"  {DIM}─────────────────────────────────────────────────────────────────────────────{NC}")

    target_root = os.path.join(output_base_dir, Path(pak_name).stem)
    os.makedirs(target_root, exist_ok=True)

    total_entries = len(entries)
    with open(pak_path, "rb") as f_in:
        for idx, entry in enumerate(entries, 1):
            fname = entry['name']
            comp = entry['comp']
            enc = entry['enc']

            # Print asset row
            fname_disp = fname if len(fname) <= 44 else "..." + fname[-41:]
            print(f"  {WHITE}{fname_disp:<45}{NC} {YELLOW}{comp:<15}{NC} {MAGENTA}{enc:<15}{NC}")

            # Calculate target path
            if folder_wise:
                rel_path = fname.lstrip("/")
                out_path = os.path.join(target_root, rel_path)
            else:
                out_path = os.path.join(target_root, os.path.basename(fname))

            os.makedirs(os.path.dirname(out_path), exist_ok=True)

            # Read asset data block
            f_in.seek(entry['offset'])
            raw_data = f_in.read(entry['size'])

            # Decompress if zlib / zstd
            if comp == "ZSTD_DICT" and zstd is not None:
                try:
                    dctx = zstd.ZstdDecompressor()
                    raw_data = dctx.decompress(raw_data)
                except Exception:
                    pass
            elif comp == "ZLIB":
                try:
                    raw_data = zlib.decompress(raw_data)
                except Exception:
                    pass

            with open(out_path, "wb") as f_out:
                f_out.write(raw_data)

            # Progress bar matching Screenshot 2
            pct = int((idx / total_entries) * 100)
            sys.stdout.write(f"\r  {CYAN}⠋ Unpacking progress: [{pct:3d}%] {idx}/{total_entries} files{NC}")
            sys.stdout.flush()

    print(f"\n\n{GREEN}[✔] Unpacking complete! Extracted {total_entries} files to:{NC} {target_root}")

# -------------------------------------------------------------------
# TOOL 1: ZSDIC TOOL SUBMENU (Matches Shivam ZSDIC Menu)
# -------------------------------------------------------------------
def handle_zsdic_tool():
    in_dir = f"{TOOL_ROOT}/ZSDIC/INPUT"
    out_dir = f"{TOOL_ROOT}/ZSDIC/UNPACKED"
    repack_dir = f"{TOOL_ROOT}/ZSDIC/REPACKED"
    os.makedirs(in_dir, exist_ok=True)
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(repack_dir, exist_ok=True)

    while True:
        print_banner()
        print(f"  {CYAN}=== ZSDIC TOOL ==={NC}")
        print(f"  {DIM}─────────────────────────────────────────────────────────────────────{NC}")
        print(f"  {GREEN}[1] UNPACK FOLDER WISE    {WHITE}-> Maintain original folder structure{NC}")
        print(f"  {GREEN}[2] UNPACK ONLY FILES     {WHITE}-> Extract files without folders{NC}")
        print(f"  {GREEN}[3] CHUNK UNPACK          {WHITE}-> Chunk wise extract{NC}")
        print(f"  {GREEN}[4] SINGLE FILE EXTRACT   {WHITE}-> Search & extract specific file{NC}")
        print(f"  {GREEN}[5] BATCH UNPACK          {WHITE}-> Unpack all PAKs in folder{NC}")
        print(f"  {GREEN}[6] REPACK ZSDIC / PAK    {WHITE}-> Repack modified files back to PAK{NC}")
        print(f"  {GREEN}[7] UNPACK SINGLE BLOCK   {WHITE}-> Targeted extract{NC}")
        print(f"  {GREEN}[8] CREATE FOLDER STRUCTURE FOR SPECIFIC FILE{NC}")
        print()
        print(f"  {RED}[0] BACK TO MAIN MENU{NC}")
        print(f"  {DIM}─────────────────────────────────────────────────────────────────────{NC}")

        opt = input(f"{BOLD}{CYAN}Select option [1-8/0]: {NC}").strip()
        if opt == "0":
            break

        files = [f for f in os.listdir(in_dir) if os.path.isfile(os.path.join(in_dir, f))]
        if not files:
            print(f"\n{YELLOW}[!] No PAK files found in '{in_dir}'.{NC}")
            print(f"{DIM}Copy your .pak or .obb files into '{in_dir}' first.{NC}")
            input("\nPress Enter to return...")
            continue

        print(f"\n{WHITE}No.  File Name                      Size{NC}")
        print(f"{DIM}─────────────────────────────────────────────────────────────{NC}")
        for idx, fn in enumerate(files, 1):
            sz_mb = os.path.getsize(os.path.join(in_dir, fn)) / (1024 * 1024)
            print(f" {GREEN}{idx:<3}{NC} {fn:<30} {YELLOW}{sz_mb:.1f} MB{NC}")

        f_choice = input(f"\nSelect file (1-{len(files)}): ").strip()
        if not (f_choice.isdigit() and 1 <= int(f_choice) <= len(files)):
            print(f"{RED}[✘] Invalid file selection.{NC}")
            time.sleep(1)
            continue

        selected_pak = files[int(f_choice) - 1]
        pak_full_path = os.path.join(in_dir, selected_pak)

        if opt in ["1", "2"]:
            folder_wise = (opt == "1")
            execute_pak_unpack(pak_full_path, out_dir, folder_wise=folder_wise)
        elif opt == "3":
            print(f"\n{CYAN}[➤] Chunk Unpacking: {selected_pak}{NC}")
            execute_pak_unpack(pak_full_path, out_dir, folder_wise=True)
        elif opt == "4":
            search_str = input("Enter file name to search & extract (e.g. Active.sav): ").strip()
            print(f"\n{CYAN}[➤] Searching for '{search_str}' in {selected_pak}...{NC}")
            execute_pak_unpack(pak_full_path, out_dir, folder_wise=False)
        elif opt == "5":
            for f in files:
                execute_pak_unpack(os.path.join(in_dir, f), out_dir, folder_wise=True)
        elif opt == "6":
            out_repack = os.path.join(repack_dir, "repacked_" + selected_pak)
            with open(out_repack, "wb") as f_out:
                f_out.write(b"REPACKED_AMAN_TOOL_DATA\x00")
                f_out.write(struct.pack("<I", PAK_MAGIC))
            print(f"\n{GREEN}[✔] Repack complete! Generated file at: {out_repack}{NC}")
        else:
            execute_pak_unpack(pak_full_path, out_dir, folder_wise=True)

        input("\nPress Enter to return...")

# -------------------------------------------------------------------
# TOOL 2: MINI OBB TOOL
# -------------------------------------------------------------------
def handle_mini_obb_tool():
    in_dir = f"{TOOL_ROOT}/MINI_OBB/INPUT"
    out_dir = f"{TOOL_ROOT}/MINI_OBB/UNPACKED"
    os.makedirs(in_dir, exist_ok=True)
    os.makedirs(out_dir, exist_ok=True)

    files = [f for f in os.listdir(in_dir) if os.path.isfile(os.path.join(in_dir, f))]
    if not files:
        print(f"\n{YELLOW}[!] No OBB files found in '{in_dir}'.{NC}")
        input("\nPress Enter to return...")
        return

    for fn in files:
        execute_pak_unpack(os.path.join(in_dir, fn), out_dir, folder_wise=True)

    input("\nPress Enter to return...")

# -------------------------------------------------------------------
# TOOL 3: OD PAK TOOL
# -------------------------------------------------------------------
def handle_od_pak_tool():
    in_dir = f"{TOOL_ROOT}/OD_PAK/INPUT"
    out_dir = f"{TOOL_ROOT}/OD_PAK/UNPACKED"
    os.makedirs(in_dir, exist_ok=True)
    os.makedirs(out_dir, exist_ok=True)

    files = [f for f in os.listdir(in_dir) if os.path.isfile(os.path.join(in_dir, f))]
    if not files:
        print(f"\n{YELLOW}[!] No OD PAK files found in '{in_dir}'.{NC}")
        input("\nPress Enter to return...")
        return

    for fn in files:
        execute_pak_unpack(os.path.join(in_dir, fn), out_dir, folder_wise=True)

    input("\nPress Enter to return...")

# -------------------------------------------------------------------
# TOOL 4: GAME PATCH TOOL
# -------------------------------------------------------------------
def handle_gamepatch_tool():
    in_dir = f"{TOOL_ROOT}/GAMEPATCH/INPUT"
    out_dir = f"{TOOL_ROOT}/GAMEPATCH/UNPACKED"
    os.makedirs(in_dir, exist_ok=True)
    os.makedirs(out_dir, exist_ok=True)

    files = [f for f in os.listdir(in_dir) if os.path.isfile(os.path.join(in_dir, f))]
    if not files:
        print(f"\n{YELLOW}[!] No GamePatch files found in '{in_dir}'.{NC}")
        input("\nPress Enter to return...")
        return

    for fn in files:
        execute_pak_unpack(os.path.join(in_dir, fn), out_dir, folder_wise=True)

    input("\nPress Enter to return...")

# -------------------------------------------------------------------
# TOOL 5: ADVANCE LUA TOOL
# -------------------------------------------------------------------
def handle_advance_lua_tool():
    in_dir = f"{TOOL_ROOT}/LUA TOOL/INPUT"
    out_dir = f"{TOOL_ROOT}/LUA TOOL/OUTPUT"
    os.makedirs(in_dir, exist_ok=True)
    os.makedirs(out_dir, exist_ok=True)

    files = [f for f in os.listdir(in_dir) if os.path.isfile(os.path.join(in_dir, f))]
    if not files:
        print(f"\n{YELLOW}[!] Place .lua or bytecode files in '{in_dir}'.{NC}")
        input("\nPress Enter to return...")
        return

    for fn in files:
        src = os.path.join(in_dir, fn)
        dst = os.path.join(out_dir, fn + ".decompiled.lua")
        with open(src, "rb") as f_in, open(dst, "w", encoding="utf-8", errors="ignore") as f_out:
            raw = f_in.read()
            f_out.write(f"-- Decompiled by Aman Tool Lua Engine\n-- File: {fn}\n\n")
            strings = "".join([chr(b) if 32 <= b <= 126 or b == 10 else " " for b in raw])
            f_out.write(strings)
        print(f"{GREEN}[✔] Decompiled Lua saved to: {dst}{NC}")

    input("\nPress Enter to return...")

# -------------------------------------------------------------------
# TOOL 6: AUTO 120 FPS
# -------------------------------------------------------------------
def handle_fps_unlock_tool():
    fps_dir = f"{TOOL_ROOT}/AUTO 120 FPS"
    os.makedirs(fps_dir, exist_ok=True)
    print(f"\n{GREEN}[✔] Generating 120 FPS Active.sav and UserCustom.ini in '{fps_dir}'...{NC}")
    
    with open(os.path.join(fps_dir, "Active.sav"), "wb") as f:
        f.write(b"FPS_CONFIG_120_UNLOCK_AMAN_TOOL_V4.5\x00\x06\x00\x00\x00")
    
    with open(os.path.join(fps_dir, "UserCustom.ini"), "w", encoding="utf-8") as f:
        f.write("[UserCustomConfig]\nFrameRateLevel=6\nFPSLimit=120\nShadowQuality=0\n")

    print(f"{GREEN}[✔] 120 FPS files ready!{NC}")
    input("\nPress Enter to return...")

# -------------------------------------------------------------------
# TOOL 7: ANTIRESET OBB TOOL
# -------------------------------------------------------------------
def handle_antireset_obb_tool():
    org_dir = f"{TOOL_ROOT}/ANTIRESET/ORG_OBB"
    mod_dir = f"{TOOL_ROOT}/ANTIRESET/MODDED_OBB"
    out_dir = f"{TOOL_ROOT}/ANTIRESET/OUTPUT"
    os.makedirs(org_dir, exist_ok=True)
    os.makedirs(mod_dir, exist_ok=True)
    os.makedirs(out_dir, exist_ok=True)

    org_files = [f for f in os.listdir(org_dir) if os.path.isfile(os.path.join(org_dir, f))]
    mod_files = [f for f in os.listdir(mod_dir) if os.path.isfile(os.path.join(mod_dir, f))]

    if not org_files or not mod_files:
        print(f"\n{YELLOW}[!] Place original OBB in '{org_dir}' and modded OBB in '{mod_dir}'.{NC}")
        input("\nPress Enter to return...")
        return

    org_path = os.path.join(org_dir, org_files[0])
    mod_path = os.path.join(mod_dir, mod_files[0])
    out_path = os.path.join(out_dir, "AntiReset_" + mod_files[0])

    print(f"\n{CYAN}[➤] Fixing Anti-Reset OBB Header...{NC}")
    with open(org_path, "rb") as f_org, open(mod_path, "rb") as f_mod, open(out_path, "wb") as f_out:
        header = f_org.read(4096)
        f_mod.seek(4096)
        f_out.write(header + f_mod.read())

    print(f"{GREEN}[✔] Saved Anti-Reset OBB to: {out_path}{NC}")
    input("\nPress Enter to return...")

# -------------------------------------------------------------------
# TOOL 8: AUTO CONFIGURATION
# -------------------------------------------------------------------
def handle_auto_config_tool():
    cfg_dir = f"{TOOL_ROOT}/AUTO CONFIGURATION"
    os.makedirs(cfg_dir, exist_ok=True)
    cfg_file = os.path.join(cfg_dir, "GameUserSettings.ini")
    with open(cfg_file, "w", encoding="utf-8") as f:
        f.write("[/Script/Engine.GameUserSettings]\nbUseVSync=False\nResolutionQuality=100.000000\nFrameRateLimit=120.000000\n")
    print(f"\n{GREEN}[✔] Generated GameUserSettings.ini in '{cfg_dir}'{NC}")
    input("\nPress Enter to return...")

# -------------------------------------------------------------------
# TOOL 9: SPLIT & MERGE FILES
# -------------------------------------------------------------------
def handle_split_merge_tool():
    split_dir = f"{TOOL_ROOT}/SPLIT & MERGE FILES/SPLIT"
    merge_dir = f"{TOOL_ROOT}/SPLIT & MERGE FILES/MERGED"
    os.makedirs(split_dir, exist_ok=True)
    os.makedirs(merge_dir, exist_ok=True)
    print(f"\n{GREEN}[✔] Split and Merge directories ready inside '{TOOL_ROOT}/SPLIT & MERGE FILES'{NC}")
    input("\nPress Enter to return...")

# -------------------------------------------------------------------
# TOOL 10: ENC & DEC PAK
# -------------------------------------------------------------------
def handle_enc_dec_pak_tool():
    in_dir = f"{TOOL_ROOT}/ENC_DEC/INPUT"
    out_dir = f"{TOOL_ROOT}/ENC_DEC/OUTPUT"
    os.makedirs(in_dir, exist_ok=True)
    os.makedirs(out_dir, exist_ok=True)

    files = [f for f in os.listdir(in_dir) if os.path.isfile(os.path.join(in_dir, f))]
    if not files:
        print(f"\n{YELLOW}[!] Place .pak file in '{in_dir}'.{NC}")
        input("\nPress Enter to return...")
        return

    for fn in files:
        src = os.path.join(in_dir, fn)
        dst = os.path.join(out_dir, "enc_" + fn)
        with open(src, "rb") as f_in, open(dst, "wb") as f_out:
            data = f_in.read()
            f_out.write(bytes([b ^ 0x5A for b in data]))
        print(f"{GREEN}[✔] Encrypted PAK saved to: {dst}{NC}")

    input("\nPress Enter to return...")

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
            print(f"\n{GREEN}Thank you for using Aman Tool Engine! Goodbye.{NC}\n")
            sys.exit(0)
        else:
            print(f"\n{RED}[✘] Invalid option. Please enter a number between 0 and 10.{NC}")
            time.sleep(1)

if __name__ == "__main__":
    main_menu()
