' VRE AC Stock — silent laptop preview launcher.
' Uses the same launcher behavior as run_desktop.vbs with a 1280x680
' CSS work-area preview for validating a 150% scaled customer laptop.
Set fso = CreateObject("Scripting.FileSystemObject")
Set sh  = CreateObject("Wscript.Shell")
sh.CurrentDirectory = fso.GetParentFolderName(WScript.ScriptFullName)
sh.Environment("Process")("VRE_PREVIEW_WORKAREA") = "1280x680"
sh.Environment("Process")("VRE_NO_THICKFRAME") = "1"

' Prefer pythonw (no console); fall back to python only if pythonw is missing.
rc = sh.Run("cmd /c where pythonw >nul 2>nul", 0, True)
If rc = 0 Then
    sh.Run "pythonw desktop_app.py", 0, False
Else
    sh.Run "python desktop_app.py", 0, False
End If
