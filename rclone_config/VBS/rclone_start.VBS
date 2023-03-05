Set ws = CreateObject("Wscript.Shell")
strRootPath = ws.ExpandEnvironmentStrings("%ALIST_RCLONE_ROOT%")
ws.run (strRootPath + "\rclone_component\rclone mount alist_webdav:/ X: --network-mode --cache-dir " + strRootPath + "\TempCache --vfs-cache-mode writes"),vbhide