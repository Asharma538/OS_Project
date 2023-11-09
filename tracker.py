import os
import json
import sched
import time
from twisted.internet import task,reactor
import datetime

# global variables
month_dict = {
    1:["Jan",31],
    2:["Feb",28],
    3:["Mar",31],
    4:["Apr",30],
    5:["May",31],
    6:["Jun",30],
    7:["Jul",31],
    8:["Aug",31],
    9:["Sep",30],
    10:["Oct",31],
    11:["Nov",30],
    12:["Dec",31]
}
list_of_apps = []

# used for listing down apps from sudo
def get_sudo_app_list():
    computer_directory = '/usr/share/applications/'

    sudo_app_list = os.popen(f"ls {computer_directory}*.desktop").read()
    sudo_app_list = sudo_app_list.split("\n")[:-1]

    final_Apps = []

    for sudo_app in sudo_app_list:
        file_path = os.path.join(computer_directory, sudo_app)
        

        # Initialize variables for Name, Exec, Icon, and NoDisplay
        # Get the firstline which contains the name, exec, and icon
        name = None
        exec_command = None
        icon = None
        no_display = None
        
        # Use the system call 'grep' to extract the fields
        for line in os.popen(f"grep -E '^Name=|^Exec=|^Icon=|^NoDisplay=' {file_path}"):
            line = line.strip()
            if line.startswith("Name=") and not name:
                name = line.split("=", 1)[1]
            elif line.startswith("Exec=") and not exec_command:
                exec_command = line.split("=", 1)[1]
            elif line.startswith("Icon=") and not icon:
                icon = line.split("=", 1)[1]
            elif line.startswith("NoDisplay=") and not no_display:
                no_display = line.split("=", 1)[1]

        if not no_display:
            # print(f"{name} | {exec_command} | {icon} | {no_display}")
            # final_Apps.append({name : [exec_command, icon]})
            final_Apps.append([exec_command, name])

    # print(final_Apps[:5])
    return final_Apps

# used for listing down apps from snap
def get_snap_app_list():
    # get snap apps not installed from **canonical
    snap_app_list = os.popen(f"snap list --all").read()
    snap_app_list = snap_app_list.split("\n")[1:-1]

    final_snap_apps = []

    for snap_app in snap_app_list:
        if "canonical**" not in snap_app:
            final_snap_apps.append(snap_app.split()[0])

    final_snap_apps = list(set(final_snap_apps))
    # print(final_snap_apps)

    base_directory = '/snap/'
    common_path = '/current/meta/gui/'
    
    final_apps = []
    
    for app in final_snap_apps:
        path = base_directory + app + common_path

        file_path = os.popen(f"ls {path}*.desktop").read()

        # Initialize variables for Name, Exec, Icon, and NoDisplay
        name = None
        exec_command = None
        icon = None
        no_display = None


        # Get the firstline which contains the name, exec, and icon
        for line in os.popen(f"grep -E '^Name=|^Exec=|^Icon=|^NoDisplay=' {file_path}"):
            line = line.strip()
            if line.startswith("Name=") and not name:
                name = line.split("=", 1)[1]
            elif line.startswith("Exec=") and not exec_command:
                exec_command = line.split("=", 1)[1]
            elif line.startswith("Icon=") and not icon:
                icon = line.split("=", 1)[1]
            elif line.startswith("NoDisplay=") and not no_display:
                no_display = line.split("=", 1)[1]

        if not no_display and exec_command:
            final_apps.append([exec_command, name])

    # print(final_apps)
    return final_apps

# updates the installed apps in regular intervals into list_of_apps
def update_installed_apps():
    global list_of_apps
    list_of_apps = get_sudo_app_list()
    list_of_apps.extend(get_snap_app_list())

# gets the active windows in list_of_apps
def get_all_windows():
    global list_of_apps

    windows = os.popen("xprop -root | grep '_NET_CLIENT_LIST_STACKING(WINDOW)'").read()
    windows = windows.split(" ")
    windows = [window[:-1] for window in windows if "0x" in window]

    dic = {}
    for window in windows:

        window_info = os.popen(f"xprop -id {window}").read()

        wm_pid = os.popen(f"xprop -id {window} | grep -e '_NET_WM_PID(CARDINAL)'").readline()[:-1].split("=")[1][1:]
        wm_state = os.popen(f"xprop -id {window} | grep -e '_NET_WM_STATE(ATOM)'").readline()[:-1].split("=")[1][1:]

        is_on_screen = 0 if '_NET_WM_STATE_HIDDEN' in wm_state else 1
            
        process_name = os.popen(f"ps -p {wm_pid} -o comm=").readline()[:-1]

        for app in list_of_apps:

            if process_name in app[0] or app[0] in process_name:

                dic[app[1]] = [int(wm_pid), is_on_screen]
                break
    
    return dic

# monitors the apps, updates the app directories which store all data
def monitor():
    try:
        with open("./apps_info/info.json") as old_app_pid_map_file:
            old_app_pid_map = json.loads(old_app_pid_map_file.read())
    except:
        old_app_pid_map = {}

    app_pid_map = get_all_windows()
    
    for i in app_pid_map:
        print(i,app_pid_map[i][0],end=" | ")
    print()


    apps_to_be_removed = []
    for i in old_app_pid_map.keys():
        if i not in app_pid_map:
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

            # as the app hasn't spawned any process as it is terminated
            apps_to_be_removed.append(i)
    
    for i in apps_to_be_removed:
        del old_app_pid_map[i]

    for i in app_pid_map:
        if i not in old_app_pid_map:
            try:
                # a new app is installed, will have to see it
                os.mkdir("./apps/"+i)
            except:
                pass
            old_app_pid_map[i] = {
                "pid" : app_pid_map[i][0],
                "startTime" : str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")),
                "maximized":1
            }

    with open("./apps_info/info.json","w") as old_app_pid_map_file:
        old_app_pid_map_file.write(json.dumps(old_app_pid_map,indent=4))

# gets the unlock count of a particular dae
def get_unlock_count(date):
    times = os.popen(f"grep -e 'gdm-password]: pam_unix(gdm-password:session)' -e 'gdm-password]: gkr-pam: unlocked login keyring' /var/log/auth.log | grep -i '{date}' | cut -c 8-15").read()
    times_list = times.split("\n")[:-1]
    return len(times_list)

# gets the total uptime for the given date
def get_uptime(date):
    timestamps = [False for i in range(86400)]

    right_now = str(datetime.datetime.strftime(date,"%Y-%m-%d-%H-%M-%S"))
    date = str(datetime.datetime.strftime(date,"%Y-%m-%d"))

    # to get all apps that have been tracked since start of our app
    all_up_apps = os.listdir("./apps/")

    # to see all the running apps
    running_apps = json.loads(open("./apps_info/info.json").read())

    for i in all_up_apps:
        try:
            with open("./apps/"+i+"/"+date+".txt") as f:
                lines = f.readlines()
            for line in lines:
                startTime,endTime,timeDuration = line.split()
                s = int(startTime[11:13])*3600 + int(startTime[14:16])*60 + int(startTime[17:19])
                e = int(endTime[11:13])*3600 + int(endTime[14:16])*60 + int(endTime[17:19])
                while s<e:
                    timestamps[s]=True
                    s+=1
        except:
            continue
    
    min_t = "9999"
    for i in running_apps:
        min_t = min(min_t,running_apps[i]["startTime"])
    
    if min_t < date + "-00-00-00":
        min_t = date + "-00-00-00"
    
    s = int(min_t[11:13])*3600 + int(min_t[14:16])*60 + int(min_t[17:19])
    e = int(right_now[11:13])*3600 + int(right_now[14:16])*60 + int(right_now[17:19])
    while s<e:
        timestamps[s]=True
        s+=1

    occupiedTime = timestamps.count(True)
    Usage = str(occupiedTime//3600).rjust(2,'0')+":"+str((occupiedTime%3600)//60).rjust(2,'0')+":"+str(occupiedTime%60).rjust(2,'0')
    return Usage

# updates the information needed for the daily tab's GUI
def daily_tab_monitor():
    daily_dict={}

    try:
        with open("./daily_usage.json") as file:
            daily_dict = json.loads(file.read()) 
    except:
        daily_dict = {} # creating the log file

    day_today = ""
    if len(str(datetime.datetime.now().date().day))==1 : day_today = " "+str(datetime.datetime.now().date().day)
    else : day_today = str(datetime.datetime.now().date().day)
    
    month_str = month_dict[datetime.datetime.now().date().month][0]

    date_format = month_str + " " + day_today
    daily_dict[str(datetime.datetime.now().date())] = [ get_uptime(datetime.datetime.now()) , get_unlock_count(date_format)]
    
    with open("./daily_usage.json","w+") as file:
        file.write(json.dumps(daily_dict,indent=4))

if __name__ == '__main__':
    timeout = 2
    dailyTimeout = 60
    appInstallTimeout = 120

    update_installed_apps() # for creating the list_of_apps initially

    appTrackerObject = task.LoopingCall(update_installed_apps)
    dailyTrackerObject = task.LoopingCall(daily_tab_monitor)
    trackerObject = task.LoopingCall(monitor)

    appTrackerObject.start(appInstallTimeout)
    dailyTrackerObject.start(dailyTimeout)
    trackerObject.start(timeout)

    reactor.run()