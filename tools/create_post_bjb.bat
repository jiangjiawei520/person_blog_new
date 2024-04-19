@echo off
set /p name=input pages name:
echo name:%name%
echo please wait
hexo new %name% && start /min /w mshta vbscript:setTimeout("window.close()",2000) && call open_page_bjb.bat %name%
pause