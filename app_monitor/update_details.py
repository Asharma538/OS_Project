import os
from make_app_list import get_running_app_pids
from datetime import datetime

def get_pid_info( pid : int ):
    # os.system(f"ps -f -p {pid} > /home/enigmachine/Desktop/app_monitor/apps/{pid}/info.txt")
    apps = get_running_app_pids()
    for i in apps.keys():
        app_details = []
        new_start = -1
        new_pid = -1
        duration = 0
        with open(f"Desktop/app_monitor/{i}") as f:
            for l in f:
                x = l.split(':')
                app_details.append(x[1])
        if i['pid'] != app_details[2]:
            now = datetime.now()
            new_start = now.time()
            new_pid = apps[i]
            duration = new_start - app_details[3]
            with open(f"app_monitor/{i}") as f:
                l = f.readlines()
                init = l[0].split(':')[1]
                updated = int(init) + duration
                replace = l[0][1].replace(l[0][1], str(updated))
                l = replace
        
        elif apps[i] == '':
                                    
            duration = new_start - app_details[3]
            with open(f"app_monitor/{i}") as f:
                l = f.readlines()
                init = l[0].split(':')[1]
                updated = int(init) + duration
                replace = l[0][1].replace(l[0][1], str(updated))
                l = replace

        elif apps[i] == app_details[2]:
