import os
import shutil

org_obb = r"C:\Users\lenovo\Downloads\main.21325.com.pubg.imobile.obb"
desktop_out = r"C:\Users\lenovo\Desktop\IPAD_VIEW_OBB_OUTPUT"
os.makedirs(desktop_out, exist_ok=True)
target_obb = os.path.join(desktop_out, "main.21325.com.pubg.imobile.obb")

# 1. Ensure uncorrupted OBB is copied to Desktop
if not os.path.exists(target_obb) or os.path.getsize(target_obb) != os.path.getsize(org_obb):
    shutil.copyfile(org_obb, target_obb)
    print(f"[OK] Restored uncorrupted OBB file at: {target_obb}")

# 2. Generate 140% Max-FOV Extended iPad View Config Files
config_dir = os.path.join(desktop_out, "High_iPadView_Config_Files")
os.makedirs(config_dir, exist_ok=True)

# UserCustom.ini (140% Max FOV & Camera Boom)
user_custom_path = os.path.join(config_dir, "UserCustom.ini")
with open(user_custom_path, "w", encoding="utf-8") as f:
    f.write("""[UserCustomConfig]
FieldOfView=140.0
TPPCameraFOV=140.0
FPPCameraFOV=140.0
CameraDistanceScale=1.75
CameraHeightScale=1.50
ThirdPersonFov=140.0
TPPVisionFOV=140.0
AspectRatioScale=1.33
FrameRateLevel=6
FPSLimit=120
bEnableHighFPS=True

[CameraConfig]
DefaultFOV=140.0
TPPFov=140.0
FPPFov=140.0
TargetArmLength=520.0
CameraHeightOffset=65.0
""")

# UserOption.ini
user_option_path = os.path.join(config_dir, "UserOption.ini")
with open(user_option_path, "w", encoding="utf-8") as f:
    f.write("""[UserOption]
CameraFOV=140.0
TPPCameraDistance=520.0
CameraHeight=65.0
AspectRatio=1.33
FPSLimit=120
""")

# GameUserSettings.ini
game_settings_path = os.path.join(config_dir, "GameUserSettings.ini")
with open(game_settings_path, "w", encoding="utf-8") as f:
    f.write("""[/Script/Engine.GameUserSettings]
bUseVSync=False
ResolutionQuality=100.000000
FrameRateLimit=120.000000

[UserCustomConfig]
FieldOfView=140.0
TPPCameraFOV=140.0
CameraDistanceScale=1.75
""")

# Copy UserCustom.ini to workspace root for quick access
root_ini = r"c:\Users\lenovo\Desktop\pakunpack\Modders_Core\UserCustom.ini"
shutil.copyfile(user_custom_path, root_ini)

print(f"[OK] Generated 140% iPad View UserCustom.ini at: {user_custom_path}")
print(f"[OK] Generated UserOption.ini at: {user_option_path}")
print(f"[OK] Generated GameUserSettings.ini at: {game_settings_path}")
print(f"[OK] Copied 140% UserCustom.ini to workspace root: {root_ini}")
