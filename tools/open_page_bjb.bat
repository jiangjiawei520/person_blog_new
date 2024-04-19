start /min /w mshta vbscript:setTimeout("window.close()",1000)
echo The InputValue is %1
set name=%1
echo %name%
start /d "D:\software_install\Typora"   Typora.exe  "E:\OneDrive - shjd\github\person_blog_new\source\_posts\%name%.md"
pause