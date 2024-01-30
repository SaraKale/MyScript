rem 批量解压多个rar压缩包并将解压出来的文件夹和文件以该压缩包的名称重命名
rem 推荐这个脚本，能成功解压，适用于素材中国下载的rar包

@echo off
mode con lines=5000
set #=Any question&set @=WX
title %#% +%$%%$%/%@% %z%
cd /d "%~dp0"
set "exefile=C:\Program Files\WinRAR\WinRAR.exe"

if not exist "%exefile%" (echo;"%exefile%" 未找到&pause&exit)

rem 循环处理当前目录下所有.rar文件
for %%a in (*.rar) do (
    echo;"%%a"
    rem 使用WinRAR解压当前.rar文件到以其名称为名称的子目录中
    "%exefile%" e -y "%%a" ".\%%~na\"
    
    rem 检查是否成功解压，如果子目录存在
    if exist ".\%%~na\" (
        rem 进入子目录
        pushd ".\%%~na"
        
        rem 循环处理子目录中的所有文件和文件夹
        for %%c in (*) do (
            rem 移除文件和文件夹的只读属性，以便可以重命名或删除
            attrib -R "%%c" >nul
            
            rem 检查文件的扩展名是否为.url或.txt
            if not "%%~xc"==".url" (
                if not "%%~xc"==".txt" (
                    rem 如果不是.url或.txt文件，则重命名为.rar文件名
                    ren "%%c" "%%~na%%~xc"
                ) else (
                    rem 如果是.txt文件，则直接删除
                    del "%%c"
                )
            ) else (
                rem 如果是.url文件，则直接删除
                del "%%c"
            )
        )
        
        rem 回到上一级目录
        popd
    )
)

echo;%#% +%$%%$%/%@% %z%

pause
exit