@echo off

::获取当前文件路径
set batPath=%~dp0
echo 当前路径为：%cd%
echo 脚本路径为：%batPath%
echo 即将当前路径为脚本路径
cd /d %batPath%
echo 当前路径为：%cd%
pause

start python update_hs.py
exit  