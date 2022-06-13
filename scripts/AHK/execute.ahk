#SingleInstance, force

if (A_WDay == 6){
    BlockInput, On
    Run, cmd.exe, C:\Users\schee\Documents\Coding\Thumbnail_Generator,
    Sleep, 200
    SendInput, python gui.py
    Send, {Enter}
    BlockInput, Off
}
ExitApp, 1
