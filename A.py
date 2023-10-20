import sys
import random
from PyQt6.QtWidgets import *
import pyqtgraph as pg
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QColor

class DynamicGraphWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground(QColor(240,240,240))

        layout.addWidget(self.plot_widget)

        # Create a PlotDataItem for the curve
        self.curve = self.plot_widget.plot()

        # Timer to update the graph
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_graph)
        self.timer.start(100)  # Update every 100 milliseconds

        self.x_data = []
        self.y_data = []

    def update_graph(self):

        x = len(self.x_data)
        y = random.uniform(0, 100)

        # if (len(self.x_data)>20):
        #     self.x_data = self.x_data[1:]
        #     self.y_data = self.y_data[1:]
        
        self.x_data.append(x)
        self.y_data.append(y)
        self.curve.setData(self.x_data, self.y_data)


app = QApplication([])

window = QMainWindow()
window.setWindowTitle("Resouce Utilisation")

body = QWidget()
window.setCentralWidget(body)

layout = QVBoxLayout()

cpu_text = QLabel("<div>CPU Utilisation</div>")
cpu_box = DynamicGraphWindow()

mem_text = QLabel("<div>Memory and Swap Area Utilisation</div>")
mem_box = DynamicGraphWindow()


layout.addWidget(cpu_text)
layout.addWidget(cpu_box)
layout.addWidget(mem_text)
layout.addWidget(mem_box)

body.setStyleSheet("background-color: #ffffff;")
body.setLayout(layout)

window.showMaximized()
sys.exit(app.exec())