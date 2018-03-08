#!/bin/sh
today=`date +%Y%m%d`

basedir="$HOME/github/repositories/strategies/etfshares"
filedir="$HOME/github/repositories/strategies/etfshares/data"
targetdir="$HOME/github/repositories/ASharesData/ETFData"

logfile="$HOME/workspace/log/$today.log"

#cd
cd $basedir
echo "get etf start..."
python $basedir/getszseetf.py >> $logfile
echo "get etf done..."

cd $filedir
checkempty=`ls $filedir`
if [ -z "$checkempty" ]
then
    echo "empty dir!"
    exit 1
fi

mv $filedir/* $targetdir/ >> $logfile
echo "mv done..."
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
