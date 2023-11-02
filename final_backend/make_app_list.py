import os
import sys
from twisted.internet import task,reactor


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


def get_all_windows():

    listofapps = get_sudo_app_list()
    listofapps.extend(get_snap_app_list())
    # print(listofapps)

    # print()
    # print()


    windows = os.popen("xprop -root | grep '_NET_CLIENT_LIST_STACKING(WINDOW)'").read()
    windows = windows.split(" ")
    windows = [window[:-1] for window in windows if "0x" in window]
    # windows = [window[:-1] for window in windows]
    # print(windows)
    dic = {}
    for window in windows:
        # print(window)
        window_info = os.popen(f"xprop -id {window}").read()
        # print(window_info)

        wm_pid = os.popen(f"xprop -id {window} | grep -e '_NET_WM_PID(CARDINAL)'").readline()[:-1].split("=")[1][1:]
        wm_state = os.popen(f"xprop -id {window} | grep -e '_NET_WM_STATE(ATOM)'").readline()[:-1].split("=")[1][1:]

        is_on_screen = 0 if '_NET_WM_STATE_HIDDEN' in wm_state else 1
            
        process_name = os.popen(f"ps -p {wm_pid} -o comm=").readline()[:-1]

        for app in listofapps:
            # print(app)
            if process_name in app[0] or app[0] in process_name:
                # print(app[1])
                dic[app[1]] = [int(wm_pid), is_on_screen]
                break

    print(dic) 
    print() 
    print()
    # for 

    return dic


if __name__ == "__main__":
    timeout = 2
    trackerObject = task.LoopingCall(get_all_windows)
    trackerObject.start(timeout)
    reactor.run()