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

# 2. Generate Bird's Eye View + Ultra Performance Engine Optimization Config Files
config_dir = os.path.join(desktop_out, "High_iPadView_Config_Files")
os.makedirs(config_dir, exist_ok=True)

# UserCustom.ini (Bird's Eye Camera + Low Draw Distance Performance Scalability)
user_custom_path = os.path.join(config_dir, "UserCustom.ini")
with open(user_custom_path, "w", encoding="utf-8") as f:
    f.write("""[UserCustomConfig]
FieldOfView=120.0
TPPCameraFOV=120.0
FPPCameraFOV=120.0
CameraDistanceScale=2.50
CameraHeightScale=2.00
ThirdPersonFov=120.0
TPPVisionFOV=120.0
AspectRatioScale=1.333333
FrameRateLevel=6
FPSLimit=120
bEnableHighFPS=True

[CameraConfig]
bConstrainAspectRatio=True
AspectRatio=1.333333
AspectRatioAxisConstraint=MaintainXFOV
DefaultFOV=120.0
TPPFov=120.0
FPPFov=120.0
TargetArmLength=650.0
CameraHeightOffset=75.0
SocketOffsetZ=85.0
SocketOffsetY=-15.0

[ScalabilitySettings]
sg.ViewDistanceQuality=0
sg.FoliageQuality=0
sg.ShadowQuality=0
sg.PostProcessQuality=0
sg.EffectsQuality=0
sg.TextureQuality=1
sg.ShadingQuality=0

[PerformanceOptimization]
bEnableDynamicResolution=True
bReduceThermalThrottling=True
bOptimizeDrawCalls=True
""")

# UserOption.ini
user_option_path = os.path.join(config_dir, "UserOption.ini")
with open(user_option_path, "w", encoding="utf-8") as f:
    f.write("""[UserOption]
CameraFOV=120.0
TPPCameraDistance=650.0
CameraHeight=75.0
AspectRatio=1.333333
FPSLimit=120
GraphicLevel=1
FrameRateLevel=6
ViewDistanceLevel=0
""")

# GameUserSettings.ini
game_settings_path = os.path.join(config_dir, "GameUserSettings.ini")
with open(game_settings_path, "w", encoding="utf-8") as f:
    f.write("""[/Script/Engine.GameUserSettings]
bUseVSync=False
ResolutionQuality=85.000000
FrameRateLimit=120.000000
sg.ResolutionQuality=85
sg.ViewDistanceQuality=0
sg.AntiAliasingQuality=0
sg.ShadowQuality=0
sg.PostProcessQuality=0
sg.TextureQuality=1
sg.EffectsQuality=0
sg.FoliageQuality=0

[UserCustomConfig]
FieldOfView=120.0
TPPCameraFOV=120.0
CameraDistanceScale=2.50
CameraHeightScale=2.00
TargetArmLength=650.0
FPSLimit=120
""")

# Copy UserCustom.ini to workspace root for quick access
root_ini = r"c:\Users\lenovo\Desktop\pakunpack\Modders_Core\UserCustom.ini"
shutil.copyfile(user_custom_path, root_ini)

print(f"[OK] Generated Bird's Eye View + Performance Scalability UserCustom.ini at: {user_custom_path}")
print(f"[OK] Generated UserOption.ini at: {user_option_path}")
print(f"[OK] Generated GameUserSettings.ini at: {game_settings_path}")
print(f"[OK] Copied UserCustom.ini to workspace root: {root_ini}")
