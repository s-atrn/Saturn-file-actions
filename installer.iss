[Setup]
AppName=Saturn File Actions
AppVersion=1.0
DefaultDirName={pf}\SaturnFileActions
DefaultGroupName=Saturn File Actions
OutputBaseFilename=SaturnFileActionsSetup
Compression=lzma
SolidCompression=yes
PrivilegesRequired=admin

[Files]
; Copy the entire compiled folder and all its contents recursively
Source: "dist\saturn_actions\*"; DestDir: "{app}\saturn_actions"; Flags: ignoreversion recursesubdirs createallsubdirs
; Copy your custom icon to the installation directory
Source: "saturn.ico"; DestDir: "{app}"; Flags: ignoreversion

[Registry]
; 1. Create the main right-click menu entry
Root: HKCR; Subkey: "*\shell\SaturnFileActions"; ValueType: string; ValueData: "Saturn file actions"; Flags: uninsdeletekey
; 2. Link your custom Saturn icon to the menu entry
Root: HKCR; Subkey: "*\shell\SaturnFileActions"; ValueType: string; ValueName: "Icon"; ValueData: "{app}\saturn.ico"; Flags: uninsdeletekey
; 3. Configure the command to launch the executable inside the folder with the target file argument
Root: HKCR; Subkey: "*\shell\SaturnFileActions\command"; ValueType: string; ValueData: """{app}\saturn_actions\saturn_actions.exe"" ""%1"""; Flags: uninsdeletekey