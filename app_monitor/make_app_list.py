import os


def get_snap_app_list():
    # Run the 'snap list' command and capture its output
    snap_list_output = os.popen('snap list').read()

    # Check if the command was successful
    if 'error' not in snap_list_output.lower():
        # Split the output into lines to get individual snap packages
        snap_list = snap_list_output.strip().split('\n')[1:]  # Skip the header

        # Parse the snap packages and create a list
        snap_packages = [line.split() for line in snap_list]

        # Get name of packages where Tracking is not 'canonical'
        snap_packages = [package[0] for package in snap_packages if package[4] != 'canonical**']

        return snap_packages
    else:
        print("Error running 'snap list' command.")
        return []



def get_usr_app_list():
    directory = "/usr/share/applications"

    # Check if the directory exists
    if os.path.exists(directory) and os.path.isdir(directory):
        # List the files in the directory
        files = os.listdir(directory)

        # Filter for .desktop files (common for application launchers)
        desktop_files = [file for file in files if file.endswith(".desktop")]

        if len(desktop_files) > 0:
            file_names = [ os.path.splitext(file)[0] for file in desktop_files ]
            return file_names

        else:
            print("No .desktop files found in /usr/share/applications.")
            return []
    else:
        print(f"The directory '{directory}' does not exist.")
        return []



def get_running_app_pids():
    apps = get_snap_app_list()
    app_pids = []

    for app in apps:
        pid = os.popen(f"pgrep -o {app}").read()
        if pid:
            app_pids.append(f"{app} : {int(pid)}")
        
    if len(app_pids) > 0:
        return app_pids
    else:
        print("No running snap applications found.")
        return []



print(get_running_app_pids())
# print(get_snap_app_list())
# print('==============================')
# print(get_usr_app_list())