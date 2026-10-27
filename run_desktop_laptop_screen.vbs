' VRE AC Stock — exact laptop layout preview.
' Uses the laptop's measured 1280x680 CSS-pixel work area. This is the
' reliable value for matching layout; monitor millimeter metadata is not
' reliable enough for physical-size emulation.
Set fso = CreateObject("Scripting.FileSystemObject")
Set sh  = CreateObject("Wscript.Shell")
sh.CurrentDirectory = fso.GetParentFolderName(WScript.ScriptFullName)
sh.Environment("Process")("VRE_PREVIEW_WORKAREA") = "1280x680"
sh.Environment("Process")("VRE_NO_THICKFRAME") = "1"

rc = sh.Run("cmd /c where pythonw >nul 2>nul", 0, True)
If rc = 0 Then
    sh.Run "pythonw desktop_app.py", 0, False
Else
    sh.Run "python desktop_app.py", 0, False
End If
