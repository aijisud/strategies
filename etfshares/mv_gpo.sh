#!/bin/sh
today=`date +%Y%m%d`

basedir="$HOME/github/repositories/strategies/etfshares"
filedir="$HOME/github/repositories/strategies/etfshares/data"
targetdir="$HOME/github/repositories/ASharesData/ETFData"

logfile="$HOME/workspace/log/$today.log"

mailnotice_dir = "$HOME/workspace/mailnotice"

#cd
echo "get etf start..."
echo "get etf start..." >> $logfile

cd $basedir
python $basedir/getszseetf.py >> $logfile

if [ $? -ne 0 ]
then
    echo "error in py"
    echo "error in py" >> $logfile
    python $mail_dir/get_etf_error_notice.py
    exit 1
fi
echo "get etf done..."
echo "get etf done..." >> $logfile

cd $filedir
checkempty=`ls $filedir`
if [ -z "$checkempty" ]
then
    echo "empty dir!"
    echo "empty dir!" >> $logfile
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
