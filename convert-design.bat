@echo off
title Converting...
echo Converting in file design.py...
python -m PyQt5.uic.pyuic -x fpositive-design.ui -o design.py
title Converted
echo Converted successfuly!
pause