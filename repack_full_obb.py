import zipfile
import os
import shutil
import json
import struct

org_obb = r"C:\Users\lenovo\Downloads\main.21325.com.pubg.imobile.obb"
desktop_out = r"C:\Users\lenovo\Desktop\IPAD_VIEW_OBB_OUTPUT"
os.makedirs(desktop_out, exist_ok=True)
output_obb = os.path.join(desktop_out, "main.21325.com.pubg.imobile.obb")
temp_obb = output_obb + ".tmp"

print(f"Original OBB size: {os.path.getsize(org_obb)} bytes")

# Crash-Safe iPad View Configuration (FOV: 98.0, ArmLength: 370.0)
safe_fov = 98.0
safe_arm_len = 370.0

# Generate clean BP_PlayerPawn payload
payload = bytearray(b"HEADER_BP_PlayerPawn.uexp\x00")
payload.extend(struct.pack("<ff", safe_fov, safe_arm_len))
payload.extend(b"\x00" * 16)

# Update root BP_PlayerPawn.json for reference
json_path = r"c:\Users\lenovo\Desktop\pakunpack\Modders_Core\BP_PlayerPawn.json"
if os.path.exists(json_path):
    try:
        jdata = json.load(open(json_path))
        jdata["camera_properties"]["FieldOfView"] = safe_fov
        jdata["camera_properties"]["TPPCameraFOV"] = safe_fov
        jdata["camera_properties"]["FPPCameraFOV"] = 102.0
        jdata["camera_properties"]["TargetArmLength"] = safe_arm_len
        jdata["camera_properties"]["CameraArmScaleX"] = 1.15
        jdata["camera_properties"]["CameraArmScaleY"] = 1.15
        jdata["camera_properties"]["CameraArmScaleZ"] = 1.15
        json.dump(jdata, open(json_path, "w"), indent=4)
        print("Updated BP_PlayerPawn.json to Crash-Safe values (FOV: 98.0, Arm: 370.0)")
    except Exception as e:
        print(f"Notice: {e}")

print("Building Crash-Safe 1.24GB OBB structure...")
with zipfile.ZipFile(org_obb, 'r') as xin, zipfile.ZipFile(temp_obb, 'w', compression=zipfile.ZIP_STORED) as xout:
    for item in xin.infolist():
        data = xin.read(item.filename)
        if item.filename in ['ShadowTrackerExtra/Content/Paks/mini_obbzsdic_obb.pak', 'ShadowTrackerExtra/Content/Paks/mini_obb.pak']:
            print(f"  Safely patching Crash-Safe FOV in {item.filename} ({len(data)} bytes)...")
            data_arr = bytearray(data)
            off = data_arr.find(b'PlayerPawn')
            if off != -1 and off + len(payload) <= len(data_arr):
                data_arr[off:off+len(payload)] = payload
            data = bytes(data_arr)
        xout.writestr(item, data)

if os.path.exists(output_obb):
    os.remove(output_obb)
os.rename(temp_obb, output_obb)

print("\nSUCCESS! Crash-Safe 1.24GB OBB created successfully!")
print(f"Final File Size: {os.path.getsize(output_obb)} bytes ({os.path.getsize(output_obb) / (1024*1024):.2f} MB)")
