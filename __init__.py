# -*- coding: utf-8 -*-

from PySide import  QtGui

from .gui import Ui_MainWindow

def main():
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
