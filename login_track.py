import os
import json
import time
# from twisted.internet import task,reactor
import datetime


# get todays date with month name
def get_date():
    today = datetime.datetime.now()
    return today.strftime("%b %d")


def get_unlocks_today():

    logs = os.popen(f"grep -e 'gdm-password]: pam_unix(gdm-password:session)' -e 'gdm-password]: gkr-pam: unlocked login keyring' /var/log/auth.log").read()
    # logs = os.popen(f"cat /var/log/auth.log").read()
    logs = logs.split("\n")
    # print(len(logs))
    for log in logs:
        print(log)
    # logs = [log[ :15 ] for log in logs]
    
    # date = get_date()

    # logs = [log for log in logs if date in log]
    
    # print(logs)
    print(len(logs))

    return logs



get_unlocks_today()
print(get_date())

# xprop -root | grep '_NET_CLIENT_LIST_STACKING(WINDOW)'
#  xprop -id 0x2400003
#  xprop -id 0x2400003 | grep 'WM_CLASS(STRING)'