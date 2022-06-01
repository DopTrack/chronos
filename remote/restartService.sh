
echo "kill all processes for remote python service"
ps -ef | grep 'DoptrackControlService.py\|DoptrackMonitorService.py\|ReceiverService.py' | grep -v grep | awk '{print $2}' | xargs -r kill

echo "start Control"
nohup python /home/rvandenberg/data/DoptrackControlService.py &

#echo "start Monitor"
#nohup python /home/rvandenberg/data/DoptrackMonitorService.py &

echo "start Receiver"
nohup python /home/rvandenberg/data/ReceiverService.py &

echo "show log"
tail -8f /home/rvandenberg/data/DoptrackService.log 
