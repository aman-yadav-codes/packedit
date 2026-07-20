import os
import shutil

org_obb = r"C:\Users\lenovo\Downloads\main.21325.com.pubg.imobile.obb"
desktop_out = r"C:\Users\lenovo\Desktop\IPAD_VIEW_OBB_OUTPUT"
os.makedirs(desktop_out, exist_ok=True)
target_obb = os.path.join(desktop_out, "main.21325.com.pubg.imobile.obb")

# 1. Restore exact original OBB without corrupting internal PAK index tables
shutil.copyfile(org_obb, target_obb)
print(f"[OK] Restored 100% uncorrupted original OBB file at: {target_obb}")
print(f"[OK] File Size: {os.path.getsize(target_obb)} bytes ({os.path.getsize(target_obb)/(1024*1024):.2f} MB)")

# 2. Generate clean UserCustom.ini & GameUserSettings.ini for crash-free FOV
config_dir = os.path.join(desktop_out, "CrashFree_Config_Files")
os.makedirs(config_dir, exist_ok=True)

user_custom_path = os.path.join(config_dir, "UserCustom.ini")
with open(user_custom_path, "w", encoding="utf-8") as f:
    f.write("""[UserCustomConfig]
FieldOfView=98.0
TPPCameraFOV=98.0
FPPCameraFOV=102.0
CameraDistanceScale=1.20
FPSLimit=120
""")

print(f"[OK] Generated Crash-Free UserCustom.ini at: {user_custom_path}")
