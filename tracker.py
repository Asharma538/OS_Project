import os
import json
import sched
import time
from twisted.internet import task,reactor
import datetime


def get_app_map():
    app_map = {}
    with open("./apps/app_map.json") as app_map_file:
        app_map = json.loads(app_map_file.read())

    return app_map

def get_running_app_pid_map(apps):
    app_pid_map = {}
    for app in apps:
        pid = os.popen(f"pgrep -o {app}").read()
        if pid:
            app_pid_map[app] = int(pid)
        else:
            app_pid_map[app] = -1
        
    return app_pid_map

def monitor():
    app_map = get_app_map()
    app_pid_map = get_running_app_pid_map(app_map.values())
    with open("./apps/info.json") as old_app_pid_map_file:
        old_app_pid_map = json.loads(old_app_pid_map_file.read())
    
    print(old_app_pid_map)

    for i in app_pid_map:
        if i not in old_app_pid_map:
            # a new app is install, will have to see it
            pass
        else:
            # this app is already being monitored
            new_pid = app_pid_map[i]
            old_pid = old_app_pid_map[i]['pid']
            
            if new_pid!=old_pid:
                if new_pid==-1:
                    # new pid is -1
                    # app is terminated

                    if str(datetime.datetime.now().date())[8:10] == old_app_pid_map[i]['startTime'][8:10]:
                        time_elapsed = datetime.datetime.now() - datetime.datetime.strptime(old_app_pid_map[i]['startTime'], "%Y-%m-%d-%H-%M-%S")

                        # -------------------
                        # update file , tbd : file heirarchy
                        # -------------------
                        old_app_pid_map[i]['startTime']=""

                    else:

                        # -------------------
                        # update file , tbd : file heirarchy
                        # -------------------

                        old_app_pid_map[i]['startTime']= str(datetime.datetime.now().date())+"-00:00:00"

                    old_app_pid_map[i]['pid']=-1
                else:
                    # old pid is -1
                    # app is started
                    old_app_pid_map[i]['pid'] = new_pid
                    old_app_pid_map[i]['startTime'] = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    with open("./apps/info.json","w") as old_app_pid_map_file:
        old_app_pid_map_file.write(json.dumps(old_app_pid_map,indent=4))
    

if __name__ == '__main__':
    timeout = 10

    # monitor()
    l = task.LoopingCall(monitor)
    l.start(timeout)
    reactor.run()