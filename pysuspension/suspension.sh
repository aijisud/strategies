#!/bin/sh
today=`date +%Y%m%d`
basedir="$HOME/github/repositories/pydisclosure/pysuspension"
targetdir="$HOME/github/repositories/SuspensionWeekly"
csvdir="$HOME/github/repositories/pydisclosure/pysuspension/data"

logfile="$HOME/workspace/stock/log/$today.log"

#save csv
python $basedir/suspension.py >> $logfile

cd $csvdir
csvfile=`ls *.csv`

if $? -ne 0
then
    exit 1

echo csvfile >> $logfile

#mv csv
cp $csvdir/$csvfile $csvdir/latest.csv >> $logfile
mv $csvdir/*.csv $targetdir/ >> $logfile


#github push
cd $tragetdir
git add $csvfile
git add latest.csv
git commit -m "$csvdir"
git push origin

echo "done" >> $logfile
echo "done"
exit(0)
#end
