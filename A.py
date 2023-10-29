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

class CircularProgressBar(QWidget): 
    def __init__(self, val=50, hrs=0, mins=0, parent=None):
        super().__init__(parent)
        self.value = val
        self.hrs = hrs
        self.mins = mins
        self.max_value = 100

    def paintEvent(self, event):
        painter = QPainter(self) # painting itself
        painter.setRenderHint(QPainter.Antialiasing) # makes edges curved

        # (C,R)
        center = self.rect().center()
        radius = int(min(self.width(), self.height()) / 3 - 10)
        
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

class AppTile(QWidget):
    def __init__(self, name="<Name>",usage="0 hrs 0 mins", visits="0", parent=None):
        super().__init__(parent)
        self.name = name
        self.usage = usage
        self.visits = visits
        self.setFixedHeight(100)
        self.setStyleSheet("background-color : rgb(225,225,240);\n")
        self.make()

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
        
        appNameLabel = QLabel(str(self.date)+" "+str(self.month)+" "+str(self.year))
        appUsageLabel = QLabel("Usage Time: "+self.usage)
        appVisitsLabel = QLabel("Unlocks: "+self.unlocks)
        appPropertiesLayout.addWidget(appNameLabel)
        appPropertiesLayout.addWidget(appUsageLabel)
        appPropertiesLayout.addWidget(appVisitsLabel)
        
        appProperties.setLayout(appPropertiesLayout)

        appTileLayout.addWidget(dateFrame)
        appTileLayout.addWidget(appProperties)

        self.setLayout(appTileLayout)

def selectTopFive():

    with open("./apps_info/app_map.json") as file :
        # print(file.read())
        apps = json.loads(file.read())

    app_details = []

    for _ in apps:
        i = apps[_]
        try:
            totalTime = datetime.timedelta(seconds= 0)

            with open("./apps/" + str(i) + "/" + str(datetime.datetime.now().date()) + ".txt") as f:
                lines = f.readlines()

                for line in lines:
                    time = (line.split(' ')[2][:-1].split(':'))
                    totalTime += datetime.timedelta(seconds=int(time[2]))
                    totalTime += datetime.timedelta(minutes=int(time[1]))
                    totalTime += datetime.timedelta(hours=int(time[0]))
            # print( _ , i , str(totalTime) , len(lines))
            app_details.append({
                "Name": _,
                "Usage" : str(totalTime),
                "Visits": str(len(lines))
            })

        except:
            # print(i + " wasn't opened today.")
            continue

    app_details = sorted(app_details , key = time_sort , reverse= True)
    return app_details[:5]
        
def time_sort(t):
    return (t["Usage"] , t["Visits"])

def main():
    app = QApplication([])
    window = QWidget()
    window.showMaximized()
    window.setWindowTitle("My App")
    window.setStyleSheet("background-color: rgb(239,242,249);\n")

    # main row is for containing the whole app's two sides
    rowMain = QHBoxLayout()

    # for containing the left part of the application
    col1 = QVBoxLayout()
    
    # For showing the total time spend in hrs & mins
    hrsSpent, minsSpent = 6, 3

    percentageTimeWidget = CircularProgressBar( math.ceil(((hrsSpent*60 + minsSpent)/1440)*100) ,hrsSpent,minsSpent)

    col1.addWidget(percentageTimeWidget,stretch=3)

    dividingLineHorizontal = QWidget()
    dividingLineHorizontal.setFixedHeight(1)
    dividingLineHorizontal.setStyleSheet("background-color: black;\n")

    col1.addWidget(dividingLineHorizontal)

    topFiveList = selectTopFive()
    
    top5Section = QWidget()
    Grid = QGridLayout()

    for i in range(6):
        if i!=0:
            Grid.addWidget(AppTile(topFiveList[i-1]["Name"],topFiveList[i-1]["Usage"],topFiveList[i-1]["Visits"]))
        else:
            top5Heading = QLabel("Top 5 Used Apps")
            top5Heading.setFont(QFont("Arial",16,500))
            top5Heading.setAlignment(Qt.AlignCenter)
            Grid.addWidget(top5Heading)

        Grid.setRowMinimumHeight(i,100)

    Grid.setSpacing(0)
    Grid.setContentsMargins(0,0,0,0)
    top5Section.setLayout(Grid)

    col1.addWidget(top5Section,stretch=5)


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

    for i in range(20):
        gridDaily.addWidget(TimeTile("25","Oct","2023",topFiveList[i%5]["Usage"],topFiveList[i%5]["Visits"]))
    
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
        gridWeekly.addWidget(TimeTile("25","Oct","2023",topFiveList[i%5]["Usage"],topFiveList[i%5]["Visits"]))
    
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
        gridmonthly.addWidget(TimeTile("25","Oct","2023",topFiveList[i%5]["Usage"],topFiveList[i%5]["Visits"]))
    
    monthlyScrollArea.setWidget(monthlyScrollAreaWidgetContents)
    monthlyLayout.addWidget(monthlyScrollArea)

    monthlyTab.setLayout(monthlyLayout)

    tabs.addTab(monthlyTab, "Monthly")
    # monthly end

    col2.addWidget(tabs)

    rowMain.addLayout(col1,stretch=3)
    rowMain.addWidget(dividingLine)
    rowMain.addLayout(col2,stretch=4)

    window.setLayout(rowMain)

    window.show()
    app.exec_()

if __name__ == '__main__':
    main()