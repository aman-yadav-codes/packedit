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

# 2. Generate 120° iPad View + 120 FPS Smooth Gameplay Config Files
config_dir = os.path.join(desktop_out, "High_iPadView_Config_Files")
os.makedirs(config_dir, exist_ok=True)

# UserCustom.ini (120° FOV + Extreme 120 FPS Boost + Anti-Heat Performance Optimization)
user_custom_path = os.path.join(config_dir, "UserCustom.ini")
with open(user_custom_path, "w", encoding="utf-8") as f:
    f.write("""[UserCustomConfig]
FieldOfView=120.0
TPPCameraFOV=120.0
FPPCameraFOV=120.0
CameraDistanceScale=1.50
CameraHeightScale=1.35
ThirdPersonFov=120.0
TPPVisionFOV=120.0
AspectRatioScale=1.33
FrameRateLevel=6
FPSLimit=120
bEnableHighFPS=True

[PerformanceOptimization]
ShadowQuality=0
AntiAliasingQuality=0
PostProcessQuality=0
EffectsQuality=0
TextureQuality=1
FoliageQuality=0
ShadingQuality=0
bEnableDynamicResolution=True
bReduceThermalThrottling=True

[CameraConfig]
DefaultFOV=120.0
TPPFov=120.0
FPPFov=120.0
TargetArmLength=450.0
CameraHeightOffset=50.0
""")

# UserOption.ini
user_option_path = os.path.join(config_dir, "UserOption.ini")
with open(user_option_path, "w", encoding="utf-8") as f:
    f.write("""[UserOption]
CameraFOV=120.0
TPPCameraDistance=450.0
CameraHeight=50.0
AspectRatio=1.33
FPSLimit=120
GraphicLevel=1
FrameRateLevel=6
""")

# GameUserSettings.ini
game_settings_path = os.path.join(config_dir, "GameUserSettings.ini")
with open(game_settings_path, "w", encoding="utf-8") as f:
    f.write("""[/Script/Engine.GameUserSettings]
bUseVSync=False
ResolutionQuality=90.000000
FrameRateLimit=120.000000
sg.ResolutionQuality=90
sg.ViewDistanceQuality=1
sg.AntiAliasingQuality=0
sg.ShadowQuality=0
sg.PostProcessQuality=0
sg.TextureQuality=1
sg.EffectsQuality=0
sg.FoliageQuality=0

[UserCustomConfig]
FieldOfView=120.0
TPPCameraFOV=120.0
CameraDistanceScale=1.50
FPSLimit=120
""")

# Copy UserCustom.ini to workspace root for quick access
root_ini = r"c:\Users\lenovo\Desktop\pakunpack\Modders_Core\UserCustom.ini"
shutil.copyfile(user_custom_path, root_ini)

print(f"[OK] Generated 120 deg + 120 FPS Optimized UserCustom.ini at: {user_custom_path}")
print(f"[OK] Generated UserOption.ini at: {user_option_path}")
print(f"[OK] Generated GameUserSettings.ini at: {game_settings_path}")
print(f"[OK] Copied 120 deg UserCustom.ini to workspace root: {root_ini}")
