#define MyAppName "Metris Production Dashboard MCMS"
#define MyAppVersion "1.0.2"
#define MyAppPublisher "Metris"
#define MyAppExeName "ProdDashMCMS.exe"
#define MyServiceExeName "ProdDashMCMSService.exe"

[Setup]
AppId={{E38FEE82-44C6-40E9-BF4A-A2AB17153F64}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}

DefaultDirName={autopf}\ANDRITZ\ProdDashMCMS
DisableProgramGroupPage=yes

OutputDir=installer
OutputBaseFilename=ProdDashMCMSSetup

ArchitecturesInstallIn64BitMode=x64
PrivilegesRequired=admin

Compression=lzma
SolidCompression=yes

UninstallDisplayName={#MyAppName}

[Files]
Source: "..\dist\ProdDashMCMS.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\dist\ProdDashMCMSService.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\dist\ProdDashMCMSService.xml"; DestDir: "{app}"; Flags: ignoreversion


[Dirs]
Name: "{commonappdata}\ANDRITZ\ProdDashMCMS\data"

[Run]
Filename: "{app}\ProdDashMCMSService.exe"; Parameters: "install"; Flags: runhidden waituntilterminated
Filename: "{app}\ProdDashMCMSService.exe"; Parameters: "start"; Flags: runhidden waituntilterminated

[UninstallRun]
Filename: "{app}\ProdDashMCMSService.exe"; Parameters: "stop"; Flags: runhidden waituntilterminated
Filename: "{app}\ProdDashMCMSService.exe"; Parameters: "uninstall"; Flags: runhidden waituntilterminated