@echo off
title [ FP ] Building...
echo Building...

rd dist /s/q
copy main.py falsepositive.py

pyinstaller --noconfirm --onefile --windowed  "D:/FalsePositive/falsepositive.py"

rd build /s/q
del falsepositive.py /s/q
del falsepositive.spec /s/q
cls
title [ FP ] Builded
echo Builded.
pause