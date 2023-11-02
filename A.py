import typing
from PyQt5 import QtCore
from PyQt5.QtWidgets import QLabel,QWidget,QVBoxLayout,QHBoxLayout,QApplication,QFrame,QGridLayout
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
import PyQt5.QtGui
from PyQt5.QtCore import Qt, QTimer,QRect
from PyQt5.QtGui import QPainter, QBrush, QColor, QPen, QPixmap
import math
import sys,os
import json
import datetime

# global variable
month_dict = {
    1:"Jan",
    2:"Feb",
    3:"Mar",
    4:"Apr",
    5:"May",
    6:"Jun",
    7:"Jul",
    8:"Aug",
    9:"Sep",
    10:"Oct",
    11:"Nov",
    12:"Dec"
}


class CircularProgressBar(QWidget): 
    def __init__(self, val=50, hrs=0, mins=0, parent=None):
        super().__init__(parent)
        self.value = val
        self.hrs = hrs
        self.mins = mins
        self.max_value = 100
        self.setMinimumHeight(300)

    def paintEvent(self, event):
        painter = QPainter(self) # painting itself
        painter.setRenderHint(QPainter.Antialiasing) # makes edges curved

        # (C,R)
        center = self.rect().center()
        radius = int(min(self.width(), self.height()) / 2.5 - 10)
        
        start_angle = 90 * 16
        final_angle = int((self.value / self.max_value) * 360 * 16)
        
        # for sketching the track of the filler
        back_pen = QPen()
        back_pen.setColor(QColor(25, 38, 85))
        back_pen.setWidth(15)
        painter.setPen(back_pen)
        painter.drawArc(center.x() - radius, center.y() - radius, 2 * radius, 2 * radius, 90*16, 360*16)

        # for sketching the filler
        pen = QPen()
        pen.setColor(QColor(0, 150, 255))
        pen.setWidth(15)
        painter.setPen(pen)
        painter.drawArc(center.x() - radius, center.y() - radius, 2 * radius, 2 * radius, start_angle, final_angle)

        font = painter.font()
        font.setPointSize(18)
        painter.setFont(font)
        painter.setPen(QColor(0, 0, 0))

        text =  str(self.hrs)+" hrs "+str(self.mins)+" mins"
        text_width = painter.fontMetrics().width(text)

        if text_width + 20 >= 2* radius:
            font.setPointSize(13)
            painter.setFont(font)
            text = str(self.hrs)+" h "+str(self.mins)+" m"
            text_width = painter.fontMetrics().width(text)
        
        text_height = painter.fontMetrics().height()
        textX = (center.x() - text_width / 2)
        textY = (center.y() + text_height / 2) - 10

        painter.drawText(int(textX), int(textY), text)

    # def updateProgressBar(self):


class AppTile(QWidget):
    def __init__(self, name="<Name>",usage="0 hrs 0 mins", visits="0", parent=None):
        super().__init__(parent)
        self.name = name
        self.usage = usage
        self.visits = visits
        self.setFixedHeight(100)
        self.setStyleSheet("background-color : rgb(225,225,240);\n")
        self.make()
        # self.updateTimerObj = QTimer()
        # self.updateTimerObj.startTimer(10)
        # self.updateTimerObj.timeout.connect(self.updateTimer)
    
    # def updateTimer():



    def make(self):
        appTileLayout = QHBoxLayout()

        img_label = QLabel()
        img_label.setText("")
        img_label.setPixmap(QPixmap("../mars.png"))
        img_label.setScaledContents(True)
        img_label.setFixedHeight(60)
        img_label.setFixedWidth(60)
        img_label.setStyleSheet("border-radius: 10px;\n")
        
        appProperties = QWidget()

        appProperties.setStyleSheet("border-radius: 10px;\n")
        appPropertiesLayout = QVBoxLayout()

        appNameLabel = QLabel(self.name)
        appNameLabel.setMinimumHeight(20)

        appUsageLabel = QLabel("Usage Time: "+self.usage)
        appUsageLabel.setMinimumHeight(20)

        appVisitsLabel = QLabel("Visits: "+self.visits)
        appVisitsLabel.setMinimumHeight(20)

        appPropertiesLayout.addWidget(appNameLabel)
        appPropertiesLayout.addWidget(appUsageLabel)
        appPropertiesLayout.addWidget(appVisitsLabel)
        
        appProperties.setLayout(appPropertiesLayout)

        appTileLayout.addWidget(img_label)
        appTileLayout.addWidget(appProperties)

        self.setLayout(appTileLayout)


class TimeTile(QWidget):
    def __init__(self, date="01",month="01",year="01",usage="0 hrs 0 mins", unlocks="0", parent=None):
        super().__init__(parent)
        self.date = date
        self.month = month
        self.year = year
        self.usage = usage
        self.unlocks = unlocks
        self.setFixedHeight(100)
        self.setStyleSheet("background-color : rgb(225,225,240);\n")
        self.make()

    def make(self):
        appTileLayout = QHBoxLayout()

        dateFrame = QWidget()
        dateFrame.setStyleSheet("border-radius:10;\n" "background-color:rgb(2,167,196);\n" "color:white;\n")
        dateFrame.setFixedWidth(70)
        dateFrame.setFixedHeight(70)

        dateBox = QLabel(str(self.date),dateFrame)
        dateBox.setGeometry(QRect(15,0,40,40))
        dateBox.setAlignment(Qt.AlignCenter)

        monthBox = QLabel(str(self.month),dateFrame)
        monthBox.setGeometry(QRect(15,30,40,40))
        monthBox.setAlignment(Qt.AlignCenter)
        
        appProperties = QWidget()

        appProperties.setStyleSheet("border-radius: 10px;\n")
        appPropertiesLayout = QVBoxLayout()
        
        appNameLabel = QLabel(str(self.date)+" "+str(self.month)+", "+str(self.year))
        appUsageLabel = QLabel("Usage Time: "+self.usage)
        appVisitsLabel = QLabel("Unlocks: "+self.unlocks)
        appPropertiesLayout.addWidget(appNameLabel)
        appPropertiesLayout.addWidget(appUsageLabel)
        appPropertiesLayout.addWidget(appVisitsLabel)
        
        appProperties.setLayout(appPropertiesLayout)

        appTileLayout.addWidget(dateFrame)
        appTileLayout.addWidget(appProperties)

        self.setLayout(appTileLayout)


class WeeklyTimeTile(QWidget):
    def __init__(self, weekNumber=1,avg_usage="00:00:00", avg_unlocks="0", parent=None):
        super().__init__(parent)
        self.weekNumber = weekNumber
        self.suffix = self.get_week_suffix()
        self.avg_usage = avg_usage
        self.avg_unlocks = avg_unlocks
        self.year = datetime.datetime.now().year

        self.setFixedHeight(100)
        self.setStyleSheet("background-color : rgb(225,225,240);\n")
        self.make()

    def get_week_suffix(self):
        if (self.weekNumber%10==1): return "st"
        elif (self.weekNumber%10==2): return "nd"
        elif (self.weekNumber%10==3): return "rd"
        return "th"

    def make(self):
        appTileLayout = QHBoxLayout()

        weekFrame = QWidget()
        weekFrame.setStyleSheet("border-radius:10;\n" "background-color:rgb(2,167,196);\n" "color:white;\n")
        weekFrame.setFixedWidth(70)
        weekFrame.setFixedHeight(70)

        weekNumberBox = QLabel(str(self.weekNumber)+self.suffix,weekFrame)
        weekNumberBox.setGeometry(QRect(15,0,40,40))
        weekNumberBox.setAlignment(Qt.AlignCenter)

        weekBox = QLabel("week",weekFrame)
        weekBox.setGeometry(QRect(15,30,40,40))
        weekBox.setAlignment(Qt.AlignCenter)
        
        timeProperties = QWidget()

        timeProperties.setStyleSheet("border-radius: 10px;\n")
        timePropertiesLayout = QVBoxLayout()
        
        weekLabel = QLabel("Week "+str(self.weekNumber)+", "+str(self.year))
        avgUsageLabel = QLabel("Average Usage Time: "+self.avg_usage)
        avgVisitsLabel = QLabel("Average Unlocks: "+self.avg_unlocks)
        timePropertiesLayout.addWidget(weekLabel)
        timePropertiesLayout.addWidget(avgUsageLabel)
        timePropertiesLayout.addWidget(avgVisitsLabel)
        
        timeProperties.setLayout(timePropertiesLayout)

        appTileLayout.addWidget(weekFrame)
        appTileLayout.addWidget(timeProperties)

        self.setLayout(appTileLayout)


class MonthlyTimeTile(QWidget):
    def __init__(self, monthName="Jan",avg_usage="00:00:00", avg_unlocks="0", parent=None):
        super().__init__(parent)
        self.monthName = monthName
        self.avg_usage = avg_usage
        self.avg_unlocks = avg_unlocks
        self.year = datetime.datetime.now().year

        self.setFixedHeight(100)
        self.setStyleSheet("background-color : rgb(225,225,240);\n")
        self.make()

    def make(self):
        monthTileLayout = QHBoxLayout()

        monthFrame = QWidget()
        monthFrame.setStyleSheet("border-radius:10;\n" "background-color:rgb(2,167,196);\n" "color:white;\n")
        monthFrame.setFixedWidth(70)
        monthFrame.setFixedHeight(70)

        monthNameBox = QLabel(str(self.monthName),monthFrame)
        monthNameBox.setGeometry(QRect(15,15,40,40))
        monthNameBox.setAlignment(Qt.AlignCenter)
        
        timeProperties = QWidget()
        timeProperties.setStyleSheet("border-radius: 10px;\n")
        timePropertiesLayout = QVBoxLayout()
        
        weekLabel = QLabel(str(self.monthName)+" "+str(self.year))
        avgUsageLabel = QLabel("Average Usage Time: "+self.avg_usage)
        avgVisitsLabel = QLabel("Average Unlocks: "+self.avg_unlocks)
        timePropertiesLayout.addWidget(weekLabel)
        timePropertiesLayout.addWidget(avgUsageLabel)
        timePropertiesLayout.addWidget(avgVisitsLabel)
        
        timeProperties.setLayout(timePropertiesLayout)

        monthTileLayout.addWidget(monthFrame)
        monthTileLayout.addWidget(timeProperties)

        self.setLayout(monthTileLayout)


class Top5Apps(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.timer = QTimer(self)
        self.make()
        self.timer.timeout.connect(self.make)
        self.timer.start(1000)
    
    def make(self):
        self.topFiveList = selectTopFive()
        Grid = QGridLayout()
        for i in range(1+len(self.topFiveList)):
            if i!=0:
                Grid.addWidget(AppTile(self.topFiveList[i-1]["Name"],self.topFiveList[i-1]["Usage"],self.topFiveList[i-1]["Visits"]))
            else:
                top5Heading = QLabel("No Apps used today")
                if len(self.topFiveList)!=0:
                    top5Heading = QLabel(f"Top Apps with the Highest Uptime Today")
                top5Heading.setFont(QFont("Arial",16,500))
                top5Heading.setAlignment(Qt.AlignCenter)
                Grid.addWidget(top5Heading)

            Grid.setRowMinimumHeight(i,100)

        Grid.setSpacing(0)
        Grid.setContentsMargins(0,0,0,0)
        self.grid = Grid
        if self.layout() is not None:
            self.layout().deleteLater()
        self.setLayout(self.grid)


def get_unlock_count(date):
    times = os.popen(f"grep -e 'gdm-password]: pam_unix(gdm-password:session)' -e 'gdm-password]: gkr-pam: unlocked login keyring' /var/log/auth.log | grep -i '{date}' | cut -c 8-15").read()
    times_list = times.split("\n")[:-1]
    return len(times_list)


def selectTopFive():

    app_details = []

    with open("./apps_info/info.json") as f:
        app_info = json.loads(f.read())
    print(app_info)

    app_names = os.listdir('./apps/')
    for _ in app_names:
        try:
            totalTime = datetime.timedelta(seconds= 0)

            with open("./apps/" + str(_) + "/" + str(datetime.datetime.now().date()) + ".txt") as f:
                lines = f.readlines()

                for line in lines:
                    time = (line.split(' ')[2][:-1].split(':'))
                    totalTime += datetime.timedelta(seconds=int(time[2]))
                    totalTime += datetime.timedelta(minutes=int(time[1]))
                    totalTime += datetime.timedelta(hours=int(time[0]))

            visits = len(lines)

            if _ in app_info:
                totalTime += datetime.datetime.strptime(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"),"%Y-%m-%d-%H-%M-%S") - datetime.datetime.strptime(app_info[_]["startTime"] , "%Y-%m-%d-%H-%M-%S")
                visits += 1
            app_details.append({
                "Name": _,
                "Usage" : str(totalTime),
                "Visits": str(visits)
            })

        except Exception as e:
            if _ in app_info:
                app_details.append({
                    "Name": _,
                    "Usage" : str(datetime.datetime.strptime(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"),"%Y-%m-%d-%H-%M-%S") - datetime.datetime.strptime(app_info[_]["startTime"] , "%Y-%m-%d-%H-%M-%S")),
                    "Visits": "1"
                })

    print(app_details)
    app_details = sorted(app_details , key = timeSort , reverse= True)
    return app_details[:5]


def timeSort(t):
    hrs,mins,secs = t["Usage"].split(":")
    return ( int(hrs)*3600 + int(mins)*60 + int(secs) , int(t["Visits"]))


def main():
    app = QApplication([])
    window = QWidget()
    window.showMaximized()
    window.setWindowTitle("App UpTime Tracker")
    window.setStyleSheet("background-color: rgb(239,242,249);\n")

    # main row is for containing the whole app's two sides
    rowMain = QHBoxLayout()

    # for containing the left part of the application
    col1 = QVBoxLayout()
    

    hrsSpent, minsSpent,secsSpent = 5 , 10 , 0
    percentageTimeWidget = CircularProgressBar( math.ceil(((hrsSpent*60 + minsSpent)/1440)*100) ,hrsSpent,minsSpent)

    col1.addWidget(percentageTimeWidget)

    dividingLineHorizontal = QWidget()
    dividingLineHorizontal.setFixedHeight(1)
    dividingLineHorizontal.setStyleSheet("background-color: black;\n")

    col1.addWidget(dividingLineHorizontal)

    top5widget = Top5Apps()
    col1.addWidget(top5widget)

    # for containing the right part of the application
    dividingLine = QWidget()
    dividingLine.setFixedWidth(1)
    dividingLine.setStyleSheet("background-color: black;\n")


    col2 =  QVBoxLayout()
    
    tabs = QTabWidget()
    
    #daily begin
    dailyTab = QWidget()

    dailyLayout = QVBoxLayout()
    dailyScrollArea = QScrollArea()
    dailyScrollArea.setWidgetResizable(True)
    dailyScrollAreaWidgetContents = QWidget()
    gridDaily = QGridLayout(dailyScrollAreaWidgetContents)

    with open("./daily_usage.json") as file :
        dailyUsageDetails = json.loads(file.read())

    # print(dailyUsageDetails)

    for i in (dailyUsageDetails):
        dailyYear , dailyMonth , dailyDate = list(map(str , i.split('-')))
        
        print(dailyUsageDetails[i][0] , dailyUsageDetails[i][1])
        gridDaily.addWidget(TimeTile(dailyDate, month_dict[int(dailyMonth)] ,dailyYear, dailyUsageDetails[i][0] , str(dailyUsageDetails[i][1])))
    
    gridDaily.setAlignment(Qt.AlignmentFlag.AlignTop)
    dailyScrollArea.setWidget(dailyScrollAreaWidgetContents)
    dailyLayout.addWidget(dailyScrollArea)

    dailyTab.setLayout(dailyLayout)

    tabs.addTab(dailyTab, "Daily")
    #daily end

    #weekly begin
    weeklyTab = QWidget()
    
    weeklyLayout = QVBoxLayout()
    weeklyScrollArea = QScrollArea()
    weeklyScrollArea.setWidgetResizable(True)
    weeklyScrollAreaWidgetContents = QWidget()
    gridWeekly = QGridLayout(weeklyScrollAreaWidgetContents)

    for i in range(20):
        gridWeekly.addWidget(WeeklyTimeTile(2 ,"00:00:00","0"))
    
    gridWeekly.setAlignment(Qt.AlignmentFlag.AlignTop)

    weeklyScrollArea.setWidget(weeklyScrollAreaWidgetContents)
    weeklyLayout.addWidget(weeklyScrollArea)

    weeklyTab.setLayout(weeklyLayout)

    tabs.addTab(weeklyTab, "Weekly")
    #weekly end

    # monthly begin
    monthlyTab = QWidget()

    monthlyLayout = QVBoxLayout()
    monthlyScrollArea = QScrollArea()
    monthlyScrollArea.setWidgetResizable(True)
    monthlyScrollAreaWidgetContents = QWidget()
    gridmonthly = QGridLayout(monthlyScrollAreaWidgetContents)

    for i in range(20):
        gridmonthly.addWidget(MonthlyTimeTile("Oct","00:00:00","0"))
    
    gridmonthly.setAlignment(Qt.AlignmentFlag.AlignTop)

    monthlyScrollArea.setWidget(monthlyScrollAreaWidgetContents)
    monthlyLayout.addWidget(monthlyScrollArea)

    monthlyTab.setLayout(monthlyLayout)

    tabs.addTab(monthlyTab, "Monthly")
    # monthly end

    col2.addWidget(tabs)

    col3 = QVBoxLayout()
    col3.addWidget(QLabel("Third section"))

    rowMain.addLayout(col1,stretch=1)
    rowMain.addWidget(dividingLine)
    rowMain.addLayout(col2,stretch=1)

    window.setLayout(rowMain)

    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
    # selectTopFive()