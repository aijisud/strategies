@echo off
@title bat交互执行git命令

echo\&echo
cd /d D:\Workspace\GitHub\DisclosureDaily

echo this is a new file for test > auto_push.bat.test

git add -v .
git commit -m "auto test"
git push origin


echo\&echo done...

REM END
