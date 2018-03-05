#!/bin/sh
today=`date +%Y%m%d`

basedir="$HOME/github/repositories/strategies/etfshares"
filedir="$HOME/github/repositories/strategies/etfshares/data"
targetdir="$HOME/github/repositories/ASharesData/ETFData"

logfile="$HOME/workspace/log/$today.log"

python $basedir/getszseetf.py >> $logfile

mv $filedir/* $targetdir/ >> $logfile
if [ $? -ne 0 ]
then
    exit 1
fi

#github push
cd $targetdir
echo $targetdir
echo $targetdir >> $logfile

git add -A
if [ $? -ne 0 ]
then
    exit 1
fi
echo "git added ALL" >> $logfile
echo "git added ALL"

git commit -m "$today"
if [ $? -ne 0 ]
then
    exit 1
fi
echo "git commited" >> $logfile
echo "git commited"

git push origin
if [ $? -ne 0 ]
then
    exit 1
fi
echo "git pushed" >> $logfile
echo "git pushed"


echo "done" >> $logfile
echo "done"
exit 0
#end
