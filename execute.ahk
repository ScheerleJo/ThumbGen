#SingleInstance, force
varDate := % A_DDD

if (%varDate% == Fr){
    BlockInput, On
    Run, cmd.exe, C:\Users\schee\Documents\Coding\Thumbnail_Generator,
    Sleep, 200
    SendInput, python thumbGen.py
    Send, {Enter}
    Sleep, 500
    BlockInput, Off
}
ExitApp, 1