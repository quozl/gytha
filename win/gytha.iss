; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

; then did a few changes to make maintenance, move to other folder easier
;
; define the path to your work folder
#define BaseFolder "C:\Users\Administrator\Desktop\python\sandbox\netrek-client-pygame-0.6\dist"

; get version information from the exe
#define ExeName BaseFolder+"\dist\start.exe"
#define AppVersionNo GetFileVersion(ExeName)
#define AppMajorVersionIdx Pos(".", AppVersionNo)
#define AppMinorVersionTemp Copy(AppVersionNo, AppMajorVersionIdx +1)
#define AppMajorVersionNo Copy(AppVersionNo, 1, AppMajorVersionIdx -1)
#define AppMinorVersionNo Copy(AppMinorVersionTemp, 1, Pos(".", AppMinorVersionTemp)-1)

; define some more stuff, mainly to just keep it all at the beginning
#define MyAppName "gytha"
#define MyAppPublisher "James Cameron"
#define MyAppURL "http://quozl.us.netrek.org/gytha/"
#define MyAppSupportURL "http://quozl.us.netrek.org/gytha/"
#define MyAppUpdatesURL "http://quozl.us.netrek.org/gytha/"

#define MyAppExeName "start.exe"

#define OutputFileName "setup-gytha"



[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{7EF7CADC-886C-4813-BC7D-D0C18F6826C3}
AppName={#MyAppName}
AppVersion={#AppVersionNo}
AppVerName={#MyAppName} version {#AppMajorVersionNo}.{#AppMinorVersionNo}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppSupportURL}
AppUpdatesURL={#MyAppUpdatesURL}
; following should probably be something like "{pf}\yourappname" for a real application
DefaultDirName=c:\gytha
DefaultGroupName=gytha
AllowNoIcons=yes

OutputBaseFilename={#OutputFileName}_{#AppVersionNo}

; bzip/9 is better by about 400KB over zip/9 and lzma is even better
Compression=lzma/ultra
; following would reduce size a bit more
;SolidCompression=yes

[Languages]
Name: english; MessagesFile: compiler:Default.isl

[Tasks]
Name: desktopicon; Description: {cm:CreateDesktopIcon}; GroupDescription: {cm:AdditionalIcons}; Flags: unchecked
Name: quicklaunchicon; Description: {cm:CreateQuickLaunchIcon}; GroupDescription: {cm:AdditionalIcons}; Flags: unchecked

[Files]

;Source: \dist\Microsoft.VC90.CRT\*; DestDir: {app}\Microsoft.VC90.CRT; Flags: ignoreversion recursesubdirs createallsubdirs
Source: ..\dist\bz2.pyd; DestDir: {app}; Flags: ignoreversion
Source: ..\dist\images\*; DestDir: {app}\images; Flags: ignoreversion recursesubdirs createallsubdirs
Source: ..\dist\library.zip; DestDir: {app}; Flags: ignoreversion
Source: ..\dist\pyexpat.pyd; DestDir: {app}; Flags: ignoreversion
Source: ..\dist\pygame.base.pyd; DestDir: {app}; Flags: ignoreversion
Source: ..\dist\pygame.bufferproxy.pyd; DestDir: {app}; Flags: ignoreversion
Source: ..\dist\pygame.cdrom.pyd; DestDir: {app}; Flags: ignoreversion
Source: ..\dist\pygame.color.pyd; DestDir: {app}; Flags: ignoreversion
Source: ..\dist\pygame.constants.pyd; DestDir: {app}; Flags: ignoreversion
Source: ..\dist\pygame.display.pyd; DestDir: {app}; Flags: ignoreversion
Source: ..\dist\pygame.draw.pyd; DestDir: {app}; Flags: ignoreversion
Source: ..\dist\pygame.event.pyd; DestDir: {app}; Flags: ignoreversion
Source: ..\dist\pygame.fastevent.pyd; DestDir: {app}; Flags: ignoreversion
Source: ..\dist\pygame.font.pyd; DestDir: {app}; Flags: ignoreversion
Source: ..\dist\pygame.image.pyd; DestDir: {app}; Flags: ignoreversion
Source: ..\dist\pygame.imageext.pyd; DestDir: {app}; Flags: ignoreversion
Source: ..\dist\pygame.joystick.pyd; DestDir: {app}; Flags: ignoreversion
Source: ..\dist\pygame.key.pyd; DestDir: {app}; Flags: ignoreversion
Source: ..\dist\pygame.mask.pyd; DestDir: {app}; Flags: ignoreversion
Source: ..\dist\pygame.math.pyd; DestDir: {app}; Flags: ignoreversion
Source: ..\dist\pygame.mixer.pyd; DestDir: {app}; Flags: ignoreversion
Source: ..\dist\pygame.mixer_music.pyd; DestDir: {app}; Flags: ignoreversion
Source: ..\dist\pygame.mouse.pyd; DestDir: {app}; Flags: ignoreversion
Source: ..\dist\pygame.movie.pyd; DestDir: {app}; Flags: ignoreversion
Source: ..\dist\pygame.overlay.pyd; DestDir: {app}; Flags: ignoreversion
Source: ..\dist\pygame.pixelarray.pyd; DestDir: {app}; Flags: ignoreversion
Source: ..\dist\pygame.rect.pyd; DestDir: {app}; Flags: ignoreversion
Source: ..\dist\pygame.rwobject.pyd; DestDir: {app}; Flags: ignoreversion
Source: ..\dist\pygame.scrap.pyd; DestDir: {app}; Flags: ignoreversion
Source: ..\dist\pygame.surface.pyd; DestDir: {app}; Flags: ignoreversion
Source: ..\dist\pygame.surflock.pyd; DestDir: {app}; Flags: ignoreversion
Source: ..\dist\pygame.time.pyd; DestDir: {app}; Flags: ignoreversion
Source: ..\dist\pygame.transform.pyd; DestDir: {app}; Flags: ignoreversion
Source: ..\dist\pygame._arraysurfarray.pyd; DestDir: {app}; Flags: ignoreversion
Source: ..\dist\pygame._numericsndarray.pyd; DestDir: {app}; Flags: ignoreversion
Source: ..\dist\pygame._numericsurfarray.pyd; DestDir: {app}; Flags: ignoreversion
Source: ..\dist\python26.dll; DestDir: {app}; Flags: ignoreversion
Source: ..\dist\SDL.dll; DestDir: {app}; Flags: ignoreversion
Source: ..\dist\SDL_image.dll; DestDir: {app}; Flags: ignoreversion
Source: ..\dist\SDL_mixer.dll; DestDir: {app}; Flags: ignoreversion
Source: ..\dist\SDL_ttf.dll; DestDir: {app}; Flags: ignoreversion
Source: ..\dist\select.pyd; DestDir: {app}; Flags: ignoreversion
Source: ..\dist\smpeg.dll; DestDir: {app}; Flags: ignoreversion
Source: ..\dist\start.exe; DestDir: {app}; Flags: ignoreversion
Source: ..\dist\unicodedata.pyd; DestDir: {app}; Flags: ignoreversion
Source: ..\dist\_ctypes.pyd; DestDir: {app}; Flags: ignoreversion
Source: ..\dist\_hashlib.pyd; DestDir: {app}; Flags: ignoreversion
Source: ..\dist\_multiprocessing.pyd; DestDir: {app}; Flags: ignoreversion
Source: ..\dist\_socket.pyd; DestDir: {app}; Flags: ignoreversion
Source: ..\dist\_ssl.pyd; DestDir: {app}; Flags: ignoreversion
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: {group}\{#MyAppName}; Filename: {app}\{#MyAppExeName}
Name: {commondesktop}\{#MyAppName}; Filename: {app}\{#MyAppExeName}; Tasks: desktopicon
Name: {userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName}; Filename: {app}\{#MyAppExeName}; Tasks: quicklaunchicon

[Run]
Filename: {app}\{#MyAppExeName}; Description: {cm:LaunchProgram,{#MyAppName}}; Flags: nowait postinstall skipifsilent