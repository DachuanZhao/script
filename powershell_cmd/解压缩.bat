::不显示命令，只显示结果
@echo off 
if exist "C:\Program Files\WinRAR\WinRAR.exe" ( 
	set winrarPath="C:\Program Files\WinRAR"
	echo "C:\Program Files\WinRAR\WinRAR.exe is exit"
)else (::注意空格
	set /p winrarPath=请输入winrar的目录:
)
::pause

echo 即将添加winrar到环境变量
echo winrar所在的路径为：%winrarPath%
set path==%path%;%winrarPath%
::pause

::获取当前文件路径
set batPath=%~dp0
echo 当前路径为：%cd%
echo 脚本路径为：%batPath%
echo 即将切换路径为脚本路径
cd /d %batPath%
echo 即将当前路径为脚本路径
echo 当前路径为：%cd%
pause

set /p myBegin=请输入开始编号:
set /p myEnd=请输入结束编号:
::变量只能是一个字母
for %%i in (*.rar) do (
	::解压缩
	rar x %%i
	copy "%batPath%\sql\*.sql" "C:\"
	for /f %%j in ('dir %batPath% /a:d/s/b') do (rd /q/s "%%j") 	
)

pause
