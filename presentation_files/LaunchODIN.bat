@echo off

cls

title ODIN - HR Chatbot
color 09

cd assets
cd nfo

"%SystemRoot%\System32\cscript.exe" //nologo "INFO.vbs"

echo ================================================
cd ..
cd text
type "ODIN.txt"
echo ================================================

cd ..
cd ..
cd src
python "ODIN_FINAL_QT.py"

pause