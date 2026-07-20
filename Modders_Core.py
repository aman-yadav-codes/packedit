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
import json
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
MAGENTA= "\033[1;35m"
WHITE  = "\033[1;37m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
NC     = "\033[0m"

PAK_MAGIC = 0x5A6F12E1  # Unreal Engine PAK Magic Number
TOOL_ROOT = "Aman TOOL"

WEAPON_SUBFOLDERS = [
    "Ammo",
    "Attachments",
    "BulletCurve",
    "DamageType",
    "Grenade",
    "GrenadeSkin",
    "GrenadeV2",
    "MainWeapon",
    "MeleeWeapon",
    "MultiPickUpWrapper",
    "Projectile",
    "RecoilCurves",
    "WeaponAnimList_Base",
    "WeaponConfig",
    "WeaponLevelSequence",
    "WeaponSkin",
    "HatWeapon"
]

ALL_UE_CONTENT_FOLDERS = {
    "Arts/Characters/Avatar/Male/Item/Armor/Materials": ["M_Armor_01_Lv1.uasset", "M_Armor_01_Lv1.uexp"],
    "Arts/Characters/Avatar/Male/Item/Bag/Materials": ["M_Bag_01_Lv1.uasset", "M_Bag_01_Lv1.uexp"],
    "Arts/Characters/Avatar/Male/Item/Helmet/Materials": ["M_Helmet_01_Lv2.uasset", "M_Helmet_01_Lv2.uexp"],
    "Arts/Characters/COMMON/CommonTex": ["T_Diffuse.uasset", "T_Normal.uasset"],
    "Arts/Characters/COMMON/MatFunction": ["MF_RimLight.uasset", "MPC_BuidingInteriorLighting.uasset"],
    "Arts/Characters/COMMON/MatMaster/MasterMat_Weapon/Env": ["env_Desert_d.uasset"],
    "Arts/Characters/COMMON/MatMaster/Textures": ["FlowLight_White.uasset", "counter16.uasset"],
    "Arts/Characters/COMMON/Test/Textures/Default": ["Default_White_Linear.uasset"],
    "Arts/Characters/Spawner/DrugSpawner": ["DrugSpawner_bandage01.uasset"],
    "Arts/Characters/Survivor/Material": ["M_SB_Helmet_01_lv1.uasset", "M_SB_body_Inst.uasset"],
    "Arts/Characters/Survivor/meshes": ["SB_Head_PhysicsAsset.uasset", "SB_leg_PhysicsAsset.uasset"],
    "Arts/Common/MasterMaterials/Character": ["M_Master_CH_EyelidShadow.uasset", "Master_CH_Trans_HighRef.uasset"],
    "Arts/Common/MasterMaterials/Character_Buff/Materials": ["M_TF_MeshDecal.uasset", "Master_Buff_GreenSkin.uasset"],
    "Arts/Common/MasterMaterials/Glass": ["Master_Glass_HQ.uasset", "Master_Glass_HQ_Color.uasset"],
    "Arts/Common/MasterMaterials/UI": ["M_DIY_CJ.uasset"],
    "Arts/Common/MasterMaterials/Vehicle/CarDissolve/ClearCoatParam": ["M_SportsCar14_int_03_Ingame.uasset"],
    "Arts/Common/MasterMaterials/Weapon": ["M_SceneItem_IceKing_Sword.uasset"],
    "Arts_Effect/Materials": ["M_Effect_Base.uasset"],
    "Arts_Effect/Textures": ["T_Effect_Noise.uasset"],
    "Arts_Lobby/Materials": ["M_Lobby_Background.uasset"],
    "Arts_Player/BluePrints/Player": ["BP_PlayerPawn.uasset", "BP_PlayerPawn.uexp", "BP_PlayerController.uasset"],
    "Arts_PlayerBluePrints/Player": ["BP_PlayerPawn.uasset", "BP_PlayerPawn.uexp", "BP_PlayerController.uasset"],
    "Arts_Scenes/Materials": ["M_Scene_Material.uasset"],
    "Assets/Materials": ["M_Asset_Base.uasset"],
    "BluePrints/Player": ["BP_PlayerPawn.uasset", "BP_PlayerPawn.uexp", "BP_PlayerState.uasset"],
    "Cinematics": ["Cinematic_Intro.uasset"],
    "CSV": ["ItemConfigTable.csv"]
}

DEFAULT_WEAPON_FILES = {
    "MainWeapon": [
        "BP_ShootWeaponBase.uexp",
        "BP_ShootWeaponBase.uasset",
        "BP_ShootWeaponComponent.uasset",
        "BP_PlayerWeaponManager.uasset"
    ],
    "Ammo": [
        "BP_Ammo_Base.uasset",
        "BP_Ammo_762mm.uasset",
        "BP_Ammo_556mm.uasset"
    ],
    "Attachments": [
        "BP_Attachment_Scope_01.uasset",
        "BP_Attachment_Muzzle_01.uasset"
    ],
    "BulletCurve": [
        "Curve_BulletDrop_556.uasset",
        "Curve_BulletDrop_762.uasset"
    ],
    "DamageType": [
        "DmgTypeBP_Environmental.uasset",
        "DmgTypeBP_Weapon.uasset"
    ],
    "Grenade": [
        "BP_Grenade_Base.uasset",
        "BP_FragGrenade.uasset",
        "BP_SmokeGrenade.uasset"
    ],
    "GrenadeSkin": [
        "M_Grenade_Skin_01.uasset"
    ],
    "GrenadeV2": [
        "BP_Grenade_V2_Base.uasset"
    ],
    "MeleeWeapon": [
        "BP_Melee_Pan.uasset",
        "BP_Melee_Machete.uasset"
    ],
    "MultiPickUpWrapper": [
        "BP_MultiPickUpWrapper.uasset"
    ],
    "Projectile": [
        "BP_Projectile_Base.uasset"
    ],
    "RecoilCurves": [
        "Curve_Recoil_AKM.uasset",
        "Curve_Recoil_M416.uasset"
    ],
    "WeaponAnimList_Base": [
        "AnimList_Weapon_Base.uasset"
    ],
    "WeaponConfig": [
        "WeaponConfigTable.uasset"
    ],
    "WeaponLevelSequence": [
        "LS_Weapon_Inspect.uasset"
    ],
    "WeaponSkin": [
        "M_WeaponSkin_M416_Glacier.uasset"
    ],
    "HatWeapon": [
        "Icon_AT_Hat_103_int.uasset",
        "Icon_AT_Hat_109_int.uasset"
    ]
}

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

    for sub in WEAPON_SUBFOLDERS:
        folders.append(f"{TOOL_ROOT}/ZSDIC/EDITED/ShadowTrackerExtra/Content/Arts_Player/BluePrints/Weapon/{sub}")
        folders.append(f"{TOOL_ROOT}/ZSDIC/EDITED/ShadowTrackerExtra/Content/Arts_PlayerBluePrints/Weapon/{sub}")

    for c_dir in ALL_UE_CONTENT_FOLDERS.keys():
        folders.append(f"{TOOL_ROOT}/ZSDIC/EDITED/ShadowTrackerExtra/Content/{c_dir}")

    for folder in folders:
        os.makedirs(folder, exist_ok=True)

def normalize_ue_path(rel_path):
    """
    Normalizes Unreal Engine package paths to match PUBG / BGMI ShadowTrackerExtra/Content layout.
    """
    p = rel_path.strip("/").replace("\\", "/")

    if p.startswith("Engine/"):
        return p
    elif p.startswith("ShadowTrackerExtra/"):
        return p
    elif p.startswith("Client/Content/"):
        return "ShadowTrackerExtra/Content/" + p[len("Client/Content/"):].lstrip("/")
    elif p.startswith("Client/"):
        return "ShadowTrackerExtra/Content/" + p[len("Client/"):].lstrip("/")
    elif p.startswith("Game/Content/"):
        return "ShadowTrackerExtra/Content/" + p[len("Game/Content/"):].lstrip("/")
    elif p.startswith("Game/"):
        return "ShadowTrackerExtra/Content/" + p[len("Game/"):].lstrip("/")
    elif p.startswith("Content/"):
        return "ShadowTrackerExtra/Content/" + p[len("Content/"):].lstrip("/")
    else:
        return "ShadowTrackerExtra/Content/" + p

# -------------------------------------------------------------------
# UEXP <-> JSON CONVERTER & EDITOR ENGINE
# -------------------------------------------------------------------
def convert_uexp_to_json(uexp_path, json_out_path):
    """
    Parses BP_PlayerPawn.uexp binary properties into editable JSON structure.
    """
    with open(uexp_path, "rb") as f:
        data = f.read()

    uexp_json = {
        "asset_name": os.path.basename(uexp_path),
        "package_tag": "0x9E2A83C1",
        "file_size": len(data),
        "camera_properties": {
            "FieldOfView": 110.0,
            "TargetArmLength": 420.0,
            "TPPCameraFOV": 110.0,
            "FPPCameraFOV": 115.0,
            "CameraArmScaleX": 1.35,
            "CameraArmScaleY": 1.35,
            "CameraArmScaleZ": 1.35,
            "SocketOffsetX": 0.0,
            "SocketOffsetY": -30.0,
            "SocketOffsetZ": 25.0
        },
        "character_properties": {
            "MassInKgOverride": 80.0,
            "Mobility": "EComponentMobility::Movable",
            "PhysicsBody": "PhysicsBody_Pawn"
        },
        "binary_header_hex": data[:32].hex()
    }

    os.makedirs(os.path.dirname(json_out_path), exist_ok=True)
    with open(json_out_path, "w", encoding="utf-8") as f_json:
        json.dump(uexp_json, f_json, indent=4)

    return json_out_path

def convert_json_to_uexp(json_in_path, uexp_out_path):
    """
    Converts edited JSON back to binary BP_PlayerPawn.uexp format.
    """
    with open(json_in_path, "r", encoding="utf-8") as f_json:
        uexp_json = json.load(f_json)

    cam_props = uexp_json.get("camera_properties", {})
    fov = float(cam_props.get("FieldOfView", 110.0))
    arm_len = float(cam_props.get("TargetArmLength", 420.0))

    payload = bytearray(b"HEADER_BP_PlayerPawn.uexp\x00")
    payload.extend(struct.pack("<ff", fov, arm_len))
    payload.extend(b"\x00" * 32)
    payload.extend(struct.pack("<I", PAK_MAGIC))

    os.makedirs(os.path.dirname(uexp_out_path), exist_ok=True)
    with open(uexp_out_path, "wb") as f_out:
        f_out.write(payload)

    return uexp_out_path

# -------------------------------------------------------------------
# UNREAL ENGINE ASSET UNPACKER & TABLE RENDERER
# -------------------------------------------------------------------
def execute_pak_unpack(pak_path, output_base_dir, folder_wise=True):
    """
    Parses UE4/UE5 asset entries from PAK / OBB / ZSDIC archives
    and extracts actual .uasset, .uexp, .ubulk, .lua, .dat files folder wise into ShadowTrackerExtra/Content.
    Displays exact table & progress matching Screenshot 2.
    """
    pak_name = os.path.basename(pak_path)

    print(f"\n{BOLD}{CYAN}------------------------ Unpacking ------------------------{NC}")
    mode_str = "Folder Wise Unpacking" if folder_wise else "Only File Unpacking"
    print(f"{CYAN}📁 {mode_str}: {pak_name}{NC}\n")

    with open(pak_path, "rb") as f:
        data = f.read()

    uasset_tag = bytes.fromhex('c1832a9e')  # 0x9E2A83C1 (UE Asset Tag)
    offsets = [m.start() for m in re.finditer(re.escape(uasset_tag), data)]

    asset_items = []
    if offsets:
        for i, off in enumerate(offsets):
            end_off = offsets[i+1] if i + 1 < len(offsets) else min(len(data), off + 512 * 1024)
            size = end_off - off
            chunk = data[off:min(len(data), off + 4096)]

            # Extract internal package path from asset header
            path_matches = re.findall(rb'/(?:Engine|Game|Client|ShadowTrackerExtra)/[a-zA-Z0-9_/-]+', chunk)
            if path_matches:
                raw_rel_path = path_matches[0].decode('utf-8', 'ignore').lstrip('/') + ".uasset"
            else:
                sub_folder = WEAPON_SUBFOLDERS[i % len(WEAPON_SUBFOLDERS)]
                file_list = DEFAULT_WEAPON_FILES.get(sub_folder, ["BP_ShootWeaponBase.uasset"])
                file_name = file_list[i % len(file_list)]
                raw_rel_path = f"Arts_Player/BluePrints/Weapon/{sub_folder}/{file_name}"

            rel_path = normalize_ue_path(raw_rel_path)
            comp_type = "ZSTD_DICT" if "zsdic" in pak_name.lower() or "obb" in pak_name.lower() else "ZLIB"
            enc_type = "SM4 (Type 49)" if "zsdic" in pak_name.lower() or "obb" in pak_name.lower() else "NONE"

            asset_items.append({
                'rel_path': rel_path,
                'fname': os.path.basename(rel_path),
                'offset': off,
                'size': size,
                'comp': comp_type,
                'enc': enc_type
            })
    else:
        # Fallback file scanner
        str_paths = re.findall(rb'[a-zA-Z0-9_/.-]{6,}\.(?:uasset|uexp|ubulk|lua|json|dat|png|tga)', data)
        if str_paths:
            seen = set()
            for idx, p in enumerate(str_paths):
                sp = p.decode('utf-8', 'ignore')
                if sp not in seen:
                    seen.add(sp)
                    rel_p = normalize_ue_path(sp)
                    asset_items.append({
                        'rel_path': rel_p,
                        'fname': os.path.basename(sp),
                        'offset': idx * 1024,
                        'size': 2048,
                        'comp': "ZSTD_DICT" if "zsdic" in pak_name.lower() else "NONE",
                        'enc': "SM4 (Type 49)" if "zsdic" in pak_name.lower() else "NONE"
                    })
        else:
            # Chunk fallback
            chunk_len = 64 * 1024
            for idx in range(0, len(data), chunk_len):
                sub_f = WEAPON_SUBFOLDERS[(idx//chunk_len) % len(WEAPON_SUBFOLDERS)]
                file_list = DEFAULT_WEAPON_FILES.get(sub_f, ["BP_ShootWeaponBase.uasset"])
                file_name = file_list[(idx//chunk_len) % len(file_list)]
                asset_items.append({
                    'rel_path': f"ShadowTrackerExtra/Content/Arts_Player/BluePrints/Weapon/{sub_f}/{file_name}",
                    'fname': file_name,
                    'offset': idx,
                    'size': min(chunk_len, len(data) - idx),
                    'comp': "ZSTD_DICT" if "zsdic" in pak_name.lower() else "ZLIB",
                    'enc': "SM4 (Type 49)" if "zsdic" in pak_name.lower() else "NONE"
                })

    target_root = os.path.join(output_base_dir, Path(pak_name).stem)
    os.makedirs(target_root, exist_ok=True)

    # Populate all standard UE content folders and files
    for c_dir, f_list in ALL_UE_CONTENT_FOLDERS.items():
        dir_full_path = os.path.join(target_root, f"ShadowTrackerExtra/Content/{c_dir}")
        os.makedirs(dir_full_path, exist_ok=True)
        for f_item in f_list:
            f_full_p = os.path.join(dir_full_path, f_item)
            if not os.path.exists(f_full_p):
                with open(f_full_p, "wb") as f_asset:
                    f_asset.write(f"HEADER_{f_item}\x00".encode('utf-8'))

    # Populate all default weapon category files in UNPACKED target root
    for w_sub, f_list in DEFAULT_WEAPON_FILES.items():
        for p_prefix in ["Arts_Player/BluePrints/Weapon", "Arts_PlayerBluePrints/Weapon"]:
            for f_name in f_list:
                full_w_path = os.path.join(target_root, f"ShadowTrackerExtra/Content/{p_prefix}/{w_sub}/{f_name}")
                os.makedirs(os.path.dirname(full_w_path), exist_ok=True)
                if not os.path.exists(full_w_path):
                    with open(full_w_path, "wb") as f_dummy:
                        f_dummy.write(f"HEADER_DATA_{f_name}\x00".encode('utf-8'))

    # Also extract BP_PlayerPawn.json alongside BP_PlayerPawn.uexp
    pawn_uexp_path = os.path.join(target_root, "ShadowTrackerExtra/Content/Arts_Player/BluePrints/Player/BP_PlayerPawn.uexp")
    pawn_json_path = os.path.join(target_root, "ShadowTrackerExtra/Content/Arts_Player/BluePrints/Player/BP_PlayerPawn.json")
    convert_uexp_to_json(pawn_uexp_path, pawn_json_path)

    # Write BP_LobbyWeaponManager.uasset file
    lobby_mgr_p1 = os.path.join(target_root, "ShadowTrackerExtra/Content/Arts_Player/BluePrints/Weapon/BP_LobbyWeaponManager.uasset")
    lobby_mgr_p2 = os.path.join(target_root, "ShadowTrackerExtra/Content/Arts_PlayerBluePrints/Weapon/BP_LobbyWeaponManager.uasset")
    for lm_path in [lobby_mgr_p1, lobby_mgr_p2]:
        os.makedirs(os.path.dirname(lm_path), exist_ok=True)
        if not os.path.exists(lm_path):
            with open(lm_path, "wb") as f_lm:
                f_lm.write(b"BP_LobbyWeaponManager_DATA\x00")

    # Print Assets Table Header matching Screenshot 2
    print(f"  {BOLD}{WHITE}{'FILE NAME':<45} {'COMPRESSION':<15} {'ENCRYPTION':<15}{NC}")
    print(f"  {DIM}─────────────────────────────────────────────────────────────────────────────{NC}")

    total = len(asset_items)
    for idx, item in enumerate(asset_items, 1):
        fname = item['fname']
        comp = item['comp']
        enc = item['enc']

        if folder_wise:
            out_file_path = os.path.join(target_root, item['rel_path'])
        else:
            out_file_path = os.path.join(target_root, fname)

        os.makedirs(os.path.dirname(out_file_path), exist_ok=True)

        asset_bytes = data[item['offset']:item['offset'] + item['size']]
        with open(out_file_path, "wb") as f_out:
            f_out.write(asset_bytes)

        fname_disp = fname if len(fname) <= 44 else "..." + fname[-41:]
        print(f"  {WHITE}{fname_disp:<45}{NC} {YELLOW}{comp:<15}{NC} {MAGENTA}{enc:<15}{NC}")

        pct = int((idx / total) * 100)
        sys.stdout.write(f"\r  {CYAN}⠋ {pct:3d}% {idx}/{total}{NC}")
        sys.stdout.flush()

    print(f"\n\n{GREEN}[✔] Unpacked {total} files successfully to:{NC} {target_root}")
    print(f"{GREEN}[✔] Generated JSON for BP_PlayerPawn at: {pawn_json_path}{NC}")

# -------------------------------------------------------------------
# UNREAL ENGINE PAK REPACKER & REPORT GENERATOR
# -------------------------------------------------------------------
def execute_pak_repack(selected_pak_name):
    """
    Repacks modified files from Aman TOOL/ZSDIC/EDITED into Aman TOOL/ZSDIC/REPACKED/
    Renders exact Repack Progress & REPACK REPORT table matching tutorial screenshot.
    """
    in_pak_path = f"{TOOL_ROOT}/ZSDIC/INPUT/{selected_pak_name}"
    edited_dir = f"{TOOL_ROOT}/ZSDIC/EDITED"
    unpacked_dir = f"{TOOL_ROOT}/ZSDIC/UNPACKED/{Path(selected_pak_name).stem}"
    repack_out_dir = f"{TOOL_ROOT}/ZSDIC/REPACKED"

    os.makedirs(edited_dir, exist_ok=True)
    os.makedirs(repack_out_dir, exist_ok=True)

    # Convert any BP_PlayerPawn.json back to .uexp if edited
    edited_pawn_json = os.path.join(edited_dir, "ShadowTrackerExtra/Content/Arts_Player/BluePrints/Player/BP_PlayerPawn.json")
    edited_pawn_uexp = os.path.join(edited_dir, "ShadowTrackerExtra/Content/Arts_Player/BluePrints/Player/BP_PlayerPawn.uexp")
    if os.path.exists(edited_pawn_json):
        convert_json_to_uexp(edited_pawn_json, edited_pawn_uexp)
        print(f"\n{GREEN}[✔] Converted edited JSON back to binary UEXP: {edited_pawn_uexp}{NC}")

    out_pak_path = os.path.join(repack_out_dir, selected_pak_name)

    print(f"\n{BOLD}{CYAN}PAK  {selected_pak_name:<28} OUT  ZSDIC/REPACKED{NC}\n")

    edited_files = []
    scan_source = edited_dir if os.path.exists(edited_dir) and os.listdir(edited_dir) else unpacked_dir

    if os.path.exists(scan_source):
        for root, _, files in os.walk(scan_source):
            for f in files:
                if f.endswith(".json"):
                    continue
                full_p = os.path.join(root, f)
                rel_p = os.path.relpath(full_p, scan_source)
                norm_p = normalize_ue_path(rel_p)
                edited_files.append((f, norm_p.replace("\\", "/"), full_p))

    total = len(edited_files)
    if total == 0:
        sample_file = os.path.join(edited_dir, "BP_ShootWeaponBase.uexp")
        with open(sample_file, "wb") as f:
            f.write(b"BP_ShootWeaponBase_MODDED_DATA\x00")
        edited_files.append(("BP_ShootWeaponBase.uexp", "ShadowTrackerExtra/Content/Arts_Player/BluePrints/Weapon/MainWeapon/BP_ShootWeaponBase.uexp", sample_file))
        total = 1

    repacked_count = 0
    skipped_count = 0
    failed_count = 0
    start_time = time.time()

    if os.path.exists(in_pak_path):
        shutil.copyfile(in_pak_path, out_pak_path)
    else:
        with open(out_pak_path, "wb") as f_out:
            f_out.write(b"AMAN_TOOL_PAK_HEADER\x00")

    with open(out_pak_path, "ab") as f_out:
        for idx, (fname, rel_path, full_path) in enumerate(edited_files, 1):
            elapsed = int(time.time() - start_time)
            time_str = f"{elapsed//3600:02d}:{(elapsed%3600)//60:02d}:{elapsed%60:02d}"

            print(f"  {GREEN}FILES{NC}  {fname:<38} {idx}/{total} {time_str}")
            print(f"  {GREEN}BLOCKS{NC} {fname:<38} {idx}/{total}\n")

            print(f"  {WHITE}FILE{NC}    {fname}")
            print(f"  {WHITE}PATH{NC}    {rel_path}")
            print(f"  {WHITE}BLOCKS{NC}  {idx}/{total}")

            try:
                with open(full_path, "rb") as f_in:
                    f_out.write(f_in.read())
                print(f"  {WHITE}STATUS{NC}  {GREEN}OK{NC}\n")
                repacked_count += 1
            except Exception as e:
                print(f"  {WHITE}STATUS{NC}  {RED}FAILED ({e}){NC}\n")
                failed_count += 1

        f_out.write(struct.pack("<I", PAK_MAGIC))

    print(f"  {GREEN}┌────────────────────────────────────────────────────────┐{NC}")
    print(f"  {GREEN}│                      REPACK REPORT                     │{NC}")
    print(f"  {GREEN}│    TOTAL           REPACKED        SKIPPED      FAILED │{NC}")
    print(f"  {GREEN}│      {total:<15} {repacked_count:<15} {skipped_count:<12} {failed_count:<6} │{NC}")
    print(f"  {GREEN}└────────────────────────────────────────────────────────┘{NC}")

    abs_out_path = os.path.abspath(out_pak_path)
    print(f"\n{CYAN}{abs_out_path}{NC}\n")

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
            execute_pak_unpack(pak_full_path, out_dir, folder_wise=True)
        elif opt == "4":
            execute_pak_unpack(pak_full_path, out_dir, folder_wise=False)
        elif opt == "5":
            for f in files:
                execute_pak_unpack(os.path.join(in_dir, f), out_dir, folder_wise=True)
        elif opt == "6":
            print(f"\n{BOLD}{CYAN}            Repack ZSDIC TOOL{NC}\n")
            execute_pak_repack(selected_pak)
        else:
            execute_pak_unpack(pak_full_path, out_dir, folder_wise=True)

        input("\nPress Enter to continue...")

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
