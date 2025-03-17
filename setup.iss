[Setup]
AppName=Temp Indicator
AppVersion=1.0
DefaultDirName={pf}\TempIndicator
DefaultGroupName=TempIndicator

[Files]
Source: "dist\main.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Github\temp-indicator\OpenHardwareMonitor\OpenHardwareMonitor.exe"; DestDir: "{app}\OpenHardwareMonitor"; Flags: ignoreversion

[Icons]
Name: "{group}\TempIndicator"; Filename: "{app}\main.exe"
