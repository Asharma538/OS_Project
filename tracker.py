import os
import json
import sched
import time
from twisted.internet import task,reactor
import datetime


def get_app_map():
    app_map = {}
    with open("./apps_info/app_map.json") as app_map_file:
        app_map = json.loads(app_map_file.read())

    return app_map

def get_running_apps_pids(apps):
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
    app_pid_map = get_running_apps_pids(app_map.values())
    with open("./apps_info/info.json") as old_app_pid_map_file:
        old_app_pid_map = json.loads(old_app_pid_map_file.read())
    
    # print("Status right now:",end=" ")
    # print(app_pid_map)
    # print()

    app_list = os.listdir("./apps/")

    for i in app_pid_map:
        if i not in old_app_pid_map:
            # a new app is install, will have to see it
            print(app_pid_map)
            pass
        else:
            # this app is already being monitored
            new_pid = app_pid_map[i]
            old_pid = old_app_pid_map[i]['pid']
            
            if new_pid!=old_pid:
                if new_pid==-1:
                    # new pid is -1
                    # app is terminated

                    if str(datetime.datetime.now().date())[:10] == old_app_pid_map[i]['startTime'][:10]:
                        # app is terminated on the same day it was started
                        
                        right_now_timestamp = datetime.datetime.now() # time right now
                        time_elapsed = right_now_timestamp - datetime.datetime.strptime(old_app_pid_map[i]['startTime'], "%Y-%m-%d-%H-%M-%S") # up time of app today

                        with open("./apps/"+i+"/" + str(datetime.datetime.now().date()) + ".txt","a+") as app_timing_file:
                            # making entry in the app's directory
                            app_timing_file.write(old_app_pid_map[i]['startTime']+" "+str(right_now_timestamp.strftime("%Y-%m-%d-%H-%M-%S"))+" "+str(time_elapsed)[:7]+'\n')

                    else:
                        # app is terminated on a different day

                        date_today = datetime.datetime.now().date()
                        
                        start_time_old = datetime.datetime.strptime(old_app_pid_map[i]['startTime'], "%Y-%m-%d-%H-%M-%S")
                        date_old = start_time_old.date()
                        midnight_day_old = str(date_old)+"-23-59-59"

                        time_elapsed = str(datetime.datetime.strptime(midnight_day_old,"%Y-%m-%d-%H-%M-%S") - start_time_old)
                        
                        # till we make all old days entries
                        while ( date_today !=  date_old ):

                            with open("./apps/"+i+"/"+str(date_old)+".txt","a+") as app_timing_file:
                                # making entry in the app's directory for day_old
                                app_timing_file.write(old_app_pid_map[i]['startTime'] +" "+midnight_day_old+" "+time_elapsed+'\n')

                            date_old = (datetime.datetime.strptime(str(date_old),"%Y-%m-%d") + datetime.timedelta(days=1)).date()
                            midnight_day_old = str(date_old)+"-23-59-59"
                            time_elapsed = "24:00:00"
                            old_app_pid_map[i]['startTime'] = str(date_old)+"-00-00-00"


                        right_now_timestamp = datetime.datetime.now() # time right now
                        time_elapsed = right_now_timestamp - datetime.datetime.strptime(old_app_pid_map[i]['startTime'], "%Y-%m-%d-%H-%M-%S") # up time of app today

                        with open("./apps/"+i+"/" + str(date_today) + ".txt","a+") as app_timing_file:
                            app_timing_file.write(old_app_pid_map[i]['startTime']+" "+str(right_now_timestamp.strftime("%Y-%m-%d-%H-%M-%S"))+" "+str(time_elapsed)[:7]+'\n')

                    # as the app hasn't spawned any process as it is terminated we keep the pid as -1 and startTime empty
                    old_app_pid_map[i]['pid']=-1
                    old_app_pid_map['startTime']=""

                else:
                    # old pid is -1
                    # app is started
                    old_app_pid_map[i]['pid'] = new_pid
                    old_app_pid_map[i]['startTime'] = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    with open("./apps_info/info.json","w") as old_app_pid_map_file:
        old_app_pid_map_file.write(json.dumps(old_app_pid_map,indent=4))
    

if __name__ == '__main__':
    timeout = 2

    # monitor()
    l = task.LoopingCall(monitor)
    l.start(timeout)
    reactor.run()