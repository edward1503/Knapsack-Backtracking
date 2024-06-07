import sys
import threading
from copy import deepcopy
from random import randint

import plotly.express as px
import plotly.graph_objs as go
from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import (QApplication, QMainWindow, QTableWidgetItem,
                             QTreeWidget, QTreeWidgetItem, QVBoxLayout,
                             QWidget)

from ui1_ui import Ui_MainWindow
from vs1 import draw
from knapsack_backtrack import backtracking


class KnapsackApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Knapsack Problem Solver')

        self.time = 0

        self.add.clicked.connect(self.add_var)
        self.random.clicked.connect(self.rand_var)
        self.solve.clicked.connect(self.solveproblem)

        self.treeWidget.setColumnCount(1)
        self.treeWidget.setHeaderLabels(["Options"])
        self.type = 1

        self.worker = Worker(self)
        layout = QVBoxLayout(self.tab3)
        #layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)

        self.view = QWebEngineView()
        layout.addWidget(self.view)
        self.worker.htmlChanged.connect(self.view.setHtml)

        self.type1.setChecked(True)
        self.type1.toggled.connect(lambda:self.btnstate(self.type1))
        self.type3.toggled.connect(lambda:self.btnstate(self.type3))

        self.restart.clicked.connect(self.remove)
    #remove data and result to restart
    def remove(self):
        num = self.table.rowCount()
        for j in range(num, -1, -1):
            self.table.removeRow(j)
        self.textBrowser.setText('')
    #Knapsack Type
    def btnstate (self, b):
        if b.text() == '0/1 Knapsack':
            self.type = 1
            for j in range(self.table.rowCount()):
                self.table.setItem(j, 2, QTableWidgetItem(str(1)))

        if b.text() == 'Unbounded Knapsack':
            self.type = 3
            try:
                max_weight = int(self.max.text())
                for j in range(self.table.rowCount()):
                    wght = int(self.table.item(j, 0).text())
                    #the max quatity of item j
                    self.table.setItem(j, 2, QTableWidgetItem(str(max_weight // wght)))
            except ValueError:
                self.textBrowser.setText("Invalid Data")
    #insert a new row 
    def new_row(self, weight, value, quantity):
        currentRowCount = self.table.rowCount()
        self.table.insertRow(currentRowCount)
        self.table.setItem(currentRowCount, 0, QTableWidgetItem(str(weight)))
        self.table.setItem(currentRowCount, 1, QTableWidgetItem(str(value)))
        self.table.setItem(currentRowCount, 2, QTableWidgetItem(str(quantity)))
    #Add items manually:
    def add_var(self):
        weight = self.w.text()
        value = self.v.text()
        quantity = self.q.text()
        try:
            if weight and value:
                tem1 = int(weight)
                tem2 = int(value)
                if quantity:
                    tem3 = int(quantity)
                else:
                    tem3 = 1
                self.new_row(tem1, tem2, tem3)

        except ValueError or TypeError:
            self.textBrowser.setText("Invalid Data")
        
        self.w.setText("")
        self.v.setText("")
        self.q.setText("")
    #Randomly Generate Items
    def rand_var(self):
        soluong = self.num.text()
        try:
            if soluong:
                for i in range(int(soluong)):
                    if self.type == 1:
                        self.new_row(randint(1, 10), randint(1, 10), 1)
                   
                    if self.type == 3:
                        max_weight = self.max.text()
                        if max_weight:
                            wght = randint(1, 10)
                            self.new_row(wght, randint(1, 10), int(max_weight) // wght)
                        else:
                            self.textBrowser.setText("Input Knapsack’s Capacity:")
            self.num.setText("")
        except ValueError:
             self.textBrowser.setText("Invalid Data")

    def solveproblem(self):        
        weights = []
        values = []
        domains = []

        #fill quantity based on Knapsack Type
        for i in range(self.table.rowCount()):
            weights.append(int(self.table.item(i,0).text()))
            values.append(int(self.table.item(i,1).text()))
            d = []
            for j in range(int(self.table.item(i,2).text()) + 1):
                d.append(j)
            domains.append(d)
        max_weight = self.max.text()

        #Solve problem
        if max_weight and self.table.rowCount() > 0:

            self.time += 1
            item_0 = QTreeWidgetItem(self.treeWidget)
            item_0.setText(0, f'Result {self.time}')
            
            max_weight = int(max_weight)
            self.results = backtracking(values, weights, max_weight, domains, item_0)
            text = f'Giá trị lớn nhất là {self.results[0]} \nCó khối lượng: {self.results[2]} \n'
            choosen = [f'   Vật {i + 1} số lượng: {self.results[1][i]}' 
					for i in range(len(self.results[1])) if self.results[1][i] > 0]
            #show result in tab 'result'
            text += '\n'.join(choosen)
            self.textBrowser.setText(text)
            self.show_pic()
        else:
            self.textBrowser.setText("Invalid Data")
    #draw graph in tab 'graph'
    def show_pic(self):        
        fig = draw(self.results)
        self.view.setHtml(fig.to_html(include_plotlyjs='cdn'))

#signal used for changing KnapSack Type
class Worker(QObject):
    htmlChanged = pyqtSignal(str)

    def execute(self, html):
        threading.Thread(target=self.task, daemon=True, args=([html])).start()

    def task(self, html):
        self.htmlChanged.emit(html)

def main():
    app = QApplication(sys.argv)
    window = KnapsackApp()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()