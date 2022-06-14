#SingleInstance, force
SetTitleMatchMode, 2

if (A_WDay > 5 || A_WDay == 1){

    FormatTime, WDay,, WDay
    if (WDay != 1) {
        value := 8 - WDay
        EnvAdd, date, value, days
    } else {
        EnvAdd, date, 0, days
    }
    FormatTime, formatOut, %date%, dd.MM.yyyy
    path := "./Thumbnail " formatOut ".png"

    if (FileExist(path))
    BlockInput, On
    Run, cmd.exe, C:\Users\schee\Documents\Coding\Thumbnail_Generator,
    Sleep, 200
    SendInput, python ./scripts/gui.py
    Send, {Enter}
    WinWait, python
    WinHide
    BlockInput, Off
}
ExitApp, 1



