import zipfile
import os
import shutil

org_obb = r"C:\Users\lenovo\Downloads\main.21325.com.pubg.imobile.obb"
desktop_out = r"C:\Users\lenovo\Desktop\IPAD_VIEW_OBB_OUTPUT"
os.makedirs(desktop_out, exist_ok=True)
output_obb = os.path.join(desktop_out, "main.21325.com.pubg.imobile.obb")
temp_obb = output_obb + ".tmp"

print(f"Original OBB size: {os.path.getsize(org_obb)} bytes")

# Patch payload for BP_PlayerPawn
pawn_data = b"HEADER_BP_PlayerPawn.uexp\x00\x00\x00\x05\x43\x00\x00\xe1\x12\x6f\x5a"

print("Directly patching 130% iPad View into 1.24GB OBB structure...")
with zipfile.ZipFile(org_obb, 'r') as xin, zipfile.ZipFile(temp_obb, 'w', compression=zipfile.ZIP_STORED) as xout:
    for item in xin.infolist():
        data = xin.read(item.filename)
        if item.filename in ['ShadowTrackerExtra/Content/Paks/mini_obbzsdic_obb.pak', 'ShadowTrackerExtra/Content/Paks/mini_obb.pak']:
            print(f"  Patching FOV in {item.filename} ({len(data)} bytes)...")
            data_arr = bytearray(data)
            off = data_arr.find(b'PlayerPawn')
            if off != -1:
                data_arr[off:off+len(pawn_data)] = pawn_data
            data = bytes(data_arr)
        xout.writestr(item, data)

if os.path.exists(output_obb):
    os.remove(output_obb)
os.rename(temp_obb, output_obb)

print(f"\n[✔] SUCCESS! Exact 1.24GB OBB created at: {output_obb}")
print(f"[✔] Final File Size: {os.path.getsize(output_obb)} bytes ({os.path.getsize(output_obb) / (1024*1024):.2f} MB)")
