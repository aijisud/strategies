@echo off
@title bat交互执行git命令

echo\&echo
cd /d D:\Workspace\GitHub\DisclosureDaily

echo new file +1 > auto_push.bat.test


git add -v .
git commit -m "auto"
git push origin


echo\&echo done...

REM END
