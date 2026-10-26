#define AppName "Mastermind"
#define AppVersion "1.0.0"
#define SourceDir AddBackslash(SourcePath) + "dist\Mastermind"

[Setup]
AppId={{2A73D2BD-5156-4B06-86A2-67D15E2C0B1A}
AppName={#AppName}
AppVersion={#AppVersion}
DefaultDirName={localappdata}\Programs\{#AppName}
DefaultGroupName={#AppName}
PrivilegesRequired=lowest
OutputDir={#SourcePath}\dist
OutputBaseFilename=Setup-Mastermind
UninstallDisplayIcon={app}\Mastermind.exe
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64

[Tasks]
Name: "desktopicon"; Description: "Créer une icône sur le bureau"; Flags: unchecked

[Files]
Source: "{#SourceDir}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autoprograms}\{#AppName}"; Filename: "{app}\Mastermind.exe"
Name: "{autodesktop}\{#AppName}"; Filename: "{app}\Mastermind.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\Mastermind.exe"; Description: "Lancer Mastermind"; Flags: nowait postinstall skipifsilent