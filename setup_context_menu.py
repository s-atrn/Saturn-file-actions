import sys
import os
import winreg

def setup_menu():
    script_path = os.path.abspath("saturn_actions.py")
    icon_path = os.path.abspath("saturn.ico")
    python_w_path = sys.executable.replace("python.exe", "pythonw.exe")
    if not os.path.exists(python_w_path):
        python_w_path = sys.executable

    try:
        menu_path = r"*\shell\SaturnFileConverter"
        with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, menu_path) as key:
            winreg.SetValue(key, "", winreg.REG_SZ, "Saturn file converter")
            
            # Automatically links the icon if saturn.ico exists in the folder
            if os.path.exists(icon_path):
                winreg.SetValueEx(key, "Icon", 0, winreg.REG_SZ, icon_path)
            
        with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, f"{menu_path}\\command") as key:
            winreg.SetValue(key, "", winreg.REG_SZ, f'"{python_w_path}" "{script_path}" "%1"')

        print("[SUCCESS] Context menu updated successfully with your icon!")

    except PermissionError:
        print("[ERROR] Administrator privileges required! Right-click your command prompt and select 'Run as administrator'.")
    except Exception as e:
        print(f"[ERROR] {e}")

if __name__ == "__main__":
    setup_menu()