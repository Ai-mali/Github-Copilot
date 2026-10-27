' VRE AC Stock — physical-size laptop preview launcher.
' Renders approximately 294mm x 156mm, matching the measured usable
' laptop area (excluding the taskbar), using the current desktop monitor DPI.
Set fso = CreateObject("Scripting.FileSystemObject")
Set sh  = CreateObject("Wscript.Shell")
sh.CurrentDirectory = fso.GetParentFolderName(WScript.ScriptFullName)
sh.Environment("Process")("VRE_PREVIEW_PHYSICAL_MM") = "294x156"
sh.Environment("Process")("VRE_NO_THICKFRAME") = "1"

' Prefer pythonw (no console); fall back to python only if pythonw is missing.
rc = sh.Run("cmd /c where pythonw >nul 2>nul", 0, True)
If rc = 0 Then
    sh.Run "pythonw desktop_app.py", 0, False
Else
    sh.Run "python desktop_app.py", 0, False
End If
