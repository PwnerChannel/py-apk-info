import os
import zipfile
from pyaxmlparser import APK

API_MAPPING = {
    1: "Android 1.0",
    2: "Android 1.1",
    3: "Android 1.5 (Cupcake)",
    4: "Android 1.6 (Donut)",
    5: "Android 2.0 (Eclair)",
    6: "Android 2.0.1 (Eclair)",
    7: "Android 2.1 (Eclair)",
    8: "Android 2.2 (Froyo)",
    9: "Android 2.3 (Gingerbread)",
    10: "Android 2.3.3 (Gingerbread)",
    11: "Android 3.0 (Honeycomb)",
    12: "Android 3.1 (Honeycomb)",
    13: "Android 3.2 (Honeycomb)",
    14: "Android 4.0 (Ice Cream Sandwich)",
    15: "Android 4.0.3 (Ice Cream Sandwich)",
    16: "Android 4.1 (Jelly Bean)",
    17: "Android 4.2 (Jelly Bean)",
    18: "Android 4.3 (Jelly Bean)",
    19: "Android 4.4 (KitKat)",
    20: "Android 4.4W (KitKat Watch)",
    21: "Android 5.0 (Lollipop)",
    22: "Android 5.1 (Lollipop)",
    23: "Android 6.0 (Marshmallow)",
    24: "Android 7.0 (Nougat)",
    25: "Android 7.1 (Nougat)",
    26: "Android 8.0 (Oreo)",
    27: "Android 8.1 (Oreo)",
    28: "Android 9 (Pie)",
    29: "Android 10",
    30: "Android 11",
    31: "Android 12",
    32: "Android 12L",
    33: "Android 13",
    34: "Android 14",
    35: "Android 15",
    36: "Android 16",
    37: "Android 17"
}

ABI_MAPPING = {
    "armeabi-v7a": "ARMv7 (32-bit)",
    "arm64-v8a": "ARM64 (64-bit)",
    "x86": "x86 (32-bit)",
    "x86_64": "x86_64 (64-bit)"
}

def get_android_version(sdk_level):
    if sdk_level is None:
        return "Unknown"
    try:
        level = int(sdk_level)
        return API_MAPPING.get(level, f"API {level}")
    except ValueError:
        return str(sdk_level)

def get_file_size(file_path):
    size_bytes = os.path.getsize(file_path)
    size_mb = size_bytes / (1024 * 1024)
    return f"{size_mb:.2f} MB"

def get_architectures(file_path):
    architectures = set()
    try:
        with zipfile.ZipFile(file_path, 'r') as zf:
            for filename in zf.namelist():
                if filename.startswith('lib/'):
                    parts = filename.split('/')
                    if len(parts) > 1 and parts[1]:
                        abi = parts[1]
                        readable_abi = ABI_MAPPING.get(abi, abi)
                        architectures.add(readable_abi)
    except Exception:
        pass
    return list(architectures) if architectures else ["Java Only / Independent"]

def analyze_apk(file_path):
    print("=" * 60)
    print(f"File:           {os.path.basename(file_path)}")
    print(f"File Size:      {get_file_size(file_path)}")
    print("=" * 60)
    
    try:
        apk = APK(file_path)
        
        min_sdk = apk.get_min_sdk_version()
        target_sdk = apk.get_target_sdk_version()
        icon_path = apk.get_app_icon()
        architectures = get_architectures(file_path)
        
        print(f"App Label:      {apk.get_app_name()}")
        print(f"Package Name:   {apk.package}")
        print(f"Version Name:   {apk.version_name}")
        print(f"Version Code:   {apk.version_code}")
        print(f"Min SDK:        {min_sdk} ({get_android_version(min_sdk)})")
        print(f"Target SDK:     {target_sdk} ({get_android_version(target_sdk)})")
        print(f"Main Activity:  {apk.get_main_activity()}")
        print(f"Architectures:  {', '.join(architectures)}")
        print(f"Icon Path:      {icon_path if icon_path else 'Not found'}")
        print(f"Permissions:    {len(apk.get_permissions())}")
        
    except Exception as e:
        print(f"Error: {e}")

def main():
    current_dir = os.getcwd()
    print(f"Scanning directory: {current_dir}\n")
    
    apk_files = [f for f in os.listdir(current_dir) if f.lower().endswith('.apk')]
    
    if not apk_files:
        print("No .apk files found in the current directory.")
        return
    
    print(f"Found {len(apk_files)} APK file(s).\n")
    
    for apk_file in apk_files:
        full_path = os.path.join(current_dir, apk_file)
        analyze_apk(full_path)
        print()

if __name__ == "__main__":
    main()