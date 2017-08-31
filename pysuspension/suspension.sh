#!/bin/sh
today=`date +%Y%m%d`
basedir="$HOME/github/pydisclosure/pysuspension"
targetdir="$HOME/github/SuspensionWeekly"
logdir="$HOME/workspace/stock/log"
csvdir="$HOME/github/pydisclosure/pysuspension/data"

logfile="$HOME/workspace/stock/log/$today.log"

#save csv
python $basedir/suspension.py >> $logfile

cd $csvdir
csvfile=`ls *.csv`

#mv csv
cp $csvdir/$csvfile $csvdir/latest.csv
mv $csvdir/*.csv $targetdir/

#github push
cd $tragetdir
git add $csvfile
git add latest.csv
git commit -m "$csvdir"
git push origin

echo "done" >> $logfile

#end
