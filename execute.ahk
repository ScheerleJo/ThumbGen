#SingleInstance, force


^+!1::
    BlockInput, On
    Run, cmd.exe, C:\Users\schee\Documents\Coding\Thumbnail_Generator,
    Sleep, 200
    SendInput, python thumbGen.py
    Send, {Enter}
    Sleep, 500
    Process, Close, cmd.exe
    BlockInput, Off
    Return