#!/bin/sh
today=`date +%Y%m%d`
basedir="$HOME/github/repositories/pydisclosure/pysuspension"
csvdir="$HOME/github/repositories/pydisclosure/pysuspension/data"

targetdir="$HOME/github/repositories/SuspensionWeekly"

logfile="$HOME/workspace/log/$today.log"

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
if $? -ne 0
then
    exit 1

mv $csvdir/*.csv $targetdir/ >> $logfile
if $? -ne 0
then
    exit 1


#github push
cd $tragetdir
git add $csvfile
if $? -ne 0
then
    exit 1


git add latest.csv
if $? -ne 0
then
    exit 1

git commit -m "$csvdir"
git push origin


echo "done" >> $logfile
echo "done"
exit(0)
#end
