#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.
$Esc::
constant = 1 
Sleep 1000
Loop
{
	FileReadLine, line, tasks.txt, %A_Index%
	if ErrorLevel
        break
	Send, %line%{Enter}
	Sleep 1000    ;
}
return

^Esc::ExitApp    ; <- Ctrl+Esc to kill the script