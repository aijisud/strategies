#!/bin/sh
today=`date +%Y%m%d`
basedir="$HOME/github/repositories/pydisclosure/pysuspension"
csvdir="$HOME/github/repositories/pydisclosure/pysuspension/data"

targetdir="$HOME/github/repositories/SuspensionWeekly"

logfile="$HOME/workspace/log/$today.log"

#save csv
cd $basedir
python $basedir/suspension.py >> $logfile

cd $csvdir
csvfile=`ls *.csv`

if [ $? -ne 0 ]
then
    exit 1
fi

echo $csvfile >> $logfile

#mv csv
cp $csvfile latest.csv >> $logfile
if [ $? -ne 0 ]
then
    exit 1
fi

mv $csvdir/*.csv $targetdir/ >> $logfile
if [ $? -ne 0 ]
then
    exit 1
fi

#github push
cd $targetdir
echo $targetdir
git add $csvfile
if [ $? -ne 0 ]
then
    exit 1
fi
echo "git added csv"

git add latest.csv
if [ $? -ne 0 ]
then
    exit 1
fi
echo "git added latest.csv"

git commit -m "$today"
if [ $? -ne 0 ]
then
    exit 1
fi
echo "git commited"

git push origin
if [ $? -ne 0 ]
then
    exit 1
fi
echo "git pushed"


echo "done" >> $logfile
echo "done"
exit 0
#end
