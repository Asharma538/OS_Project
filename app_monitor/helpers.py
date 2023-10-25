import os


# def get_application_name(pid: int):

#     cmdline_file_path = f"/proc/{pid}/cmdline"
#     if not os.path.exists(cmdline_file_path):
#         return "Process not found"

#     try:
#         with open(cmdline_file_path, "rb") as cmdline_file:
#             cmdline = cmdline_file.read().decode("utf-8").split("\0")
#             application_name = cmdline[0]

#             return application_name
#     except (IOError, PermissionError):
#         return "Permission denied"

# # def get_process_application_process( p : int ):
# #     parent_id = os.system(f"ps -f -p {p} | awk '{{print $3}}' | tail -1")
# #     while()

# # print(get_application_name(4059))
# tree = os.system("pstree -p 2657")
# print(tree)
















def make_app_folder( name : str ):
    path = f"/home/enigmachine/Desktop/app_monitor/apps/"

    if os.path.exists(f"{path}{name}"):
        print("App folder already exists.")
        return 0
    
    else:
        os.mkdir(f"{path}{name}")
        return 1
    


def make_info_file( name : str ):
    path = f"/home/enigmachine/Desktop/app_monitor/apps/{name}/"
    os.system(f"touch {path}info.txt")
    
    os.system(f"echo 'Name: {name}' > {path}info.txt")
    os.system(f"echo 'Status: ' >> {path}info.txt")
    
    os.system(f"echo 'Current PID: ' >> {path}info.txt")

    os.system(f"echo 'Start Time: ' >> {path}info.txt")
    
    # os.system(f"echo 'CPU: ' >> {path}info.txt")
    # os.system(f"echo 'Memory: ' >> {path}info.txt")
    # os.system(f"echo 'Disk: ' >> {path}info.txt")
    # os.system(f"echo 'Network: ' >> {path}info.txt")
    # os.system(f"echo 'User: ' >> {path}info.txt")


make_app_folder("test")
make_info_file("test")