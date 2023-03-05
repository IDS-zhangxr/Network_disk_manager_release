Set ws = CreateObject("Wscript.Shell")
strRootPath = ws.ExpandEnvironmentStrings("%ALIST_RCLONE_ROOT%")
ws.run (strRootPath + "\alist_component\alist.exe server"),vbhide