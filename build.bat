@echo off
title [ FalsePositive ] building...
echo Building launcher...
copy main.py falsepositive.py
rd dist /s/q

pyinstaller --noconfirm --onefile --windowed  "falsepositive.py"

del falsepositive.py /s/q
del falsepositive.spec /s/q
rd build /s/q
cls
title [ FalsePositive ] builded
echo Builded successfuly.
pause