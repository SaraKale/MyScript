@echo off
:: 设置变量
setlocal enabledelayedexpansion

:: 切换到Git仓库路径，自行修改路径
cd /d "C:\blog"

:: 执行git add
git add .

:: 获取当前日期
for /f "delims=" %%a in ('wmic OS Get localdatetime ^| find "."') do set datetime=%%a
set year=!datetime:~0,4!
set month=!datetime:~4,2!
set day=!datetime:~6,2!

:: 执行git commit
git commit -m "%year%-%month%-%day%"

:: 执行git push
git push

:: 结束脚本
endlocal
