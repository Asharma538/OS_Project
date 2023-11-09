# /* # # import sys
# # # from PyQt5.QtWidgets import QWidget,QPushButton,QApplication,QListWidget,QGridLayout,QLabel
# # # from PyQt5.QtCore import QTimer,QDateTime

# # # class WinForm(QWidget):
# # #     def __init__(self,parent=None):
# # #         super(WinForm, self).__init__(parent)
# # #         self.setWindowTitle('QTimer demonstration')

# # #         self.listFile=QListWidget()
# # #         self.label=QLabel('Label')
# # #         self.startBtn=QPushButton('Start')
# # #         self.endBtn=QPushButton('Stop')

# # #         layout=QGridLayout()

# # #         self.timer=QTimer()
# # #         self.timer.timeout.connect(self.showTime)

# # #         layout.addWidget(self.label,0,0,1,2)
# # #         layout.addWidget(self.startBtn,1,0)
# # #         layout.addWidget(self.endBtn,1,1)

# # #         self.startBtn.clicked.connect(self.startTimer)
# # #         self.endBtn.clicked.connect(self.endTimer)

# # #         self.setLayout(layout)

# # #     def showTime(self):
# # #         current_time=QDateTime.currentDateTime()
# # #         formatted_time=current_time.toString('yyyy-MM-dd hh:mm:ss dddd')
# # #         self.label.setText(formatted_time)

# # #     def startTimer(self):
# # #         self.timer.start(1000)
# # #         self.startBtn.setEnabled(False)
# # #         self.endBtn.setEnabled(True)

# # #     def endTimer(self):
# # #         self.timer.stop()
# # #         self.startBtn.setEnabled(True)
# # #         self.endBtn.setEnabled(False)

# # # if __name__ == '__main__':
# # #     app=QApplication(sys.argv)
# # #     form=WinForm()
# # #     form.show()
# # # --commands

# # # ls /usr/share/applications | awk -F '.desktop' ' { print $1}' -
# # # grep -i "Name=" /usr/share/applications/*.desktop # main 

# # # -----------------------------------------------------------
# # # idle time getter function

# # # def get_idle_time():
# # #     app_map = get_app_map()
    
# # #     # clocks = datetime.datetime.now()
    
# # #     # False -> idle , True -> Some app was running

# # #     timeStamps = [False for i in range(86400)]
    
# # #     for i in app_map.values():
# # #         try:
# # #             with open("./apps/"+i+"/"+str(datetime.datetime.now().date())+".txt") as f:
# # #                 lines = f.readlines()
# # #             for line in lines:
# # #                 startTime,endTime,timeDuration = line.split()
                
# # #                 s = int(startTime[11:13])*3600 + int(startTime[14:16])*60 + int(startTime[17:19])
# # #                 e = int(endTime[11:13])*3600 + int(endTime[14:16])*60 + int(endTime[17:19])
# # #                 while s<e:
# # #                     timeStamps[s]=True
# # #                     s+=1
# # #         except:
# # #             continue
# # #     occupiedTime = timeStamps.count(True)
# # #     Usage = str(occupiedTime//3600)+":"+str((occupiedTime%3600)//60)+":"+str(occupiedTime%60)
# # #     return Usage

# # def get_sudo_app_list():
# #     computer_directory = '/usr/share/applications/'

# #     sudo_app_list = os.popen(f"ls {computer_directory}*.desktop").read()
# #     sudo_app_list = sudo_app_list.split("\n")[:-1]

# #     final_Apps = []

# #     for sudo_app in sudo_app_list:
# #         file_path = os.path.join(computer_directory, sudo_app)
        

# #         # Initialize variables for Name, Exec, Icon, and NoDisplay
# #         # Get the firstline which contains the name, exec, and icon
# #         name = None
# #         exec_command = None
# #         icon = None
# #         no_display = None
        
# #         # Use the system call 'grep' to extract the fields
# #         for line in os.popen(f"grep -E '^Name=|^Exec=|^Icon=|^NoDisplay=' {file_path}"):
# #             line = line.strip()
# #             if line.startswith("Name=") and not name:
# #                 name = line.split("=", 1)[1]
# #             elif line.startswith("Exec=") and not exec_command:
# #                 exec_command = line.split("=", 1)[1]
# #             elif line.startswith("Icon=") and not icon:
# #                 icon = line.split("=", 1)[1]
# #             elif line.startswith("NoDisplay=") and not no_display:
# #                 no_display = line.split("=", 1)[1]

# #         if not no_display:
# #             # print(f"{name} | {exec_command} | {icon} | {no_display}")
# #             # final_Apps.append({name : [exec_command, icon]})
# #             final_Apps.append([exec_command, name])

# #     # print(final_Apps[:5])
# #     return final_Apps

# # import os
# # import datetime

# # def get_snap_app_list():
# #     # get snap apps not installed from **canonical
# #     snap_app_list = os.popen(f"snap list --all").read()
# #     snap_app_list = snap_app_list.split("\n")[1:-1]

# #     final_snap_apps = []

# #     for snap_app in snap_app_list:
# #         if "canonical**" not in snap_app:
# #             final_snap_apps.append(snap_app.split()[0])

# #     final_snap_apps = list(set(final_snap_apps))
# #     # print(final_snap_apps)


# #     base_directory = '/snap/'
# #     common_path = '/current/meta/gui/'
    
# #     final_apps = []
    
# #     for app in final_snap_apps:
# #         path = base_directory + app + common_path

# #         file_path = os.popen(f"ls {path}*.desktop").read()

# #         # Initialize variables for Name, Exec, Icon, and NoDisplay
# #         name = None
# #         exec_command = None
# #         icon = None
# #         no_display = None


# #         # Get the firstline which contains the name, exec, and icon
# #         for line in os.popen(f"grep -E '^Name=|^Exec=|^Icon=|^NoDisplay=' {file_path}"):
# #             line = line.strip()
# #             if line.startswith("Name=") and not name:
# #                 name = line.split("=", 1)[1]
# #             elif line.startswith("Exec=") and not exec_command:
# #                 exec_command = line.split("=", 1)[1]
# #             elif line.startswith("Icon=") and not icon:
# #                 icon = line.split("=", 1)[1]
# #             elif line.startswith("NoDisplay=") and not no_display:
# #                 no_display = line.split("=", 1)[1]

# #         if not no_display and exec_command:
# #             final_apps.append([exec_command, name])

# #     # print(final_apps)
# #     return final_apps

# # if __name__ == '__main__':
# #     s = datetime.datetime.now()
# #     l = get_snap_app_list()
# #     l.extend(get_sudo_app_list())
# #     print(datetime.datetime.now() - s)
# #     print(l,'\n')
#  */
# div{
#     background-image: url(images/bg.png);
# }
from datetime import date
print(date(2023,11,9).isocalendar()[1])