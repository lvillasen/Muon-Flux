# ...28/Dec/24
# ...Author: LV
# ...make the bash scripts executable with
# chmod a+x start.sh
# chmod a+x stop.sh
# ...Check  crontab is installed with
# systemctl status cron
# ...Enter 
# crontab -l
# ...Check this line shows up
# */5 * * * * /usr/bin/python3 /root/Muon-Flux/muonFluxCrontab.py > /var/log/cronMF.log 2>&1
# ...If it does not insert it with 
# crontab -e
# ...To see the log file enter
# grep CRON /var/log/syslog
# ...or
# cat /var/log/cron.log
# ...or
# journalctl -u cron
# ...Si no hay log file install it with
# sudo apt update
# sudo apt install rsyslog
# systemctl restart rsyslog

rm /root/Muon-Flux/Rates.json
systemctl start cron
echo "Muon Flux DAQ started ....."
date
