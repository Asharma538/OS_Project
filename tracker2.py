import os
import json
import sched
import time
from twisted.internet import task,reactor
import datetime


def get_all_windows():
    windows = os.popen("xprop -root | grep '_NET_CLIENT_LIST_STACKING(WINDOW)'").read()
    windows = windows.split(" ")
    windows = [window[:-1] for window in windows if "0x" in window]
    # windows = [window[:-1] for window in windows]
    print(windows)
    dic = {}
    for window in windows:
        # print(window)
        window_info = os.popen(f"xprop -id {window}").read()
        # print(window_info)

        # print(os.popen(f"xprop -id {window}").read().split("\n"))

        # print(os.popen(f"xprop -id {window} | grep -e 'WM_NAME(UTF8_STRING)'").readline()[:-1])
        # print(wm_name)
        
        # print(os.popen(f"xprop -id {window} | grep -e '_NET_WM_PID(CARDINAL)'").readline()[:-1])
        # print(wm_pid)

        wm_name = os.popen(f"xprop -id {window} | grep -e 'WM_NAME(UTF8_STRING)'").readline()[:-1].split("=")[1][1:].split('-')[-1][1:-1]
        wm_pid = os.popen(f"xprop -id {window} | grep -e '_NET_WM_PID(CARDINAL)'").readline()[:-1].split("=")[1][1:]
        wm_state = os.popen(f"xprop -id {window} | grep -e '_NET_WM_STATE(ATOM)'").readline()[:-1].split("=")[1][1:]
        wm_class = os.popen(f"xprop -id {window} | grep -e 'WM_CLASS(STRING)'").readline()[:-1]

        is_on_screen = 0 if '_NET_WM_STATE_HIDDEN' in wm_state else 1
        
        if wm_class:
            if 'Gnome-' in wm_class:
                dic[wm_name] = [wm_pid, is_on_screen]

            else:
                wm_class = wm_class.split(',')[1].strip()[1:-1]
                dic[wm_class] = [wm_pid, is_on_screen]

            
        else:
            is_on_screen = 0 if '_NET_WM_STATE_HIDDEN' in wm_state else 1
            dic[wm_name] = [wm_pid, is_on_screen]


        # print(f"{wm_name} | {wm_pid} | {wm_class} | {window} | {wm_state}")

    # print()
    # print("\n")
    # print(dic)  
    return dic

def monitor():
    # app_map = get_app_map()
    # app_pid_map = get_running_apps_pids(app_map.values())
    app_pid_map = get_all_windows()
    print(app_pid_map)
    with open("./apps_info/info.json") as old_app_pid_map_file:
        old_app_pid_map = json.loads(old_app_pid_map_file.read())
    
    for i in app_pid_map:
        print(i,app_pid_map[i],end=" | ")
    print()
    
    for i in app_pid_map:
        if i not in old_app_pid_map:
            # a new app is installed, will have to see it
            os.mkdir("./apps/"+i)
            old_app_pid_map[i] = {
                "pid" : app_pid_map[i],
                "startTime" : str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
            }
        else:
            # this app is already being monitored
            new_pid = app_pid_map[i]
            old_pid = old_app_pid_map[i]['pid']
            
            # if the app was closed and still closed -1 == -1
            # if the app was running and still running with same PID go on....
            # else : run -> closed,closed -> run

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
                    old_app_pid_map[i]['startTime']=""

                else:
                    # old pid is -1
                    # app is started
                    old_app_pid_map[i]['pid'] = new_pid
                    old_app_pid_map[i]['startTime'] = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    with open("./apps_info/info.json","w") as old_app_pid_map_file:
        old_app_pid_map_file.write(json.dumps(old_app_pid_map,indent=4))

    
    
# def get_idle_time():
#     app_map = get_app_map()
    
#     # clocks = datetime.datetime.now()
    
#     # False -> idle , True -> Some app was running

#     timeStamps = [False for i in range(86400)]
    
#     for i in app_map.values():
#         try:
#             with open("./apps/"+i+"/"+str(datetime.datetime.now().date())+".txt") as f:
#                 lines = f.readlines()
#             for line in lines:
#                 startTime,endTime,timeDuration = line.split()
                
#                 s = int(startTime[11:13])*3600 + int(startTime[14:16])*60 + int(startTime[17:19])
#                 e = int(endTime[11:13])*3600 + int(endTime[14:16])*60 + int(endTime[17:19])
#                 while s<e:
#                     timeStamps[s]=True
#                     s+=1
#         except:
#             continue
#     occupiedTime = timeStamps.count(True)
#     Usage = str(occupiedTime//3600)+":"+str((occupiedTime%3600)//60)+":"+str(occupiedTime%60)
#     return Usage

# def daily_update():
#     with open("./log/"+str(datetime.datetime.now().date())+".txt","w") as log_file:
#         log_file.write(get_idle_time())

if __name__ == '__main__':
    timeout = 10
    dailyTimeout = 60

    trackerObject = task.LoopingCall(monitor)
    trackerObject.start(timeout)

    # dailyUpdaterObject = task.LoopingCall(daily_update)
    # dailyUpdaterObject.start(dailyTimeout)

    # trackerObject = task.LoopingCall(get_all_windows)
    # trackerObject.start(timeout)
    reactor.run()
    # get_all_windows()



# WM_NAME(UTF8_STRING)
# WM_CLASS(STRING)
# _NET_WM_PID(CARDINAL)
# WM_CLASS(STRING) = "evince