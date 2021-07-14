import Part
import FreeCAD as App
from FreeCAD import Base
import FreeCADGui as Gui
import math
from math import pi
import PySide
from PySide import QtCore, QtGui
import os
import time
import csv
import shutil

#Create new document
App.newDocument("Assembly")
App.setActiveDocument("Assembly")
App.ActiveDocument=App.getDocument("Assembly")
Gui.ActiveDocument=Gui.getDocument("Assembly")

global switch ; switch = 0

csv_filename = '/Users/Steffen/AppData/Roaming/FreeCAD/Macro/testdatei_write.csv'
csv_filename = '/Users/usf/Morphoa/Steffen/testdatei_write.csv'

source_path = r'C:\Users\usf\Morphoa\Steffen' + '\\' 

doe_halter_filename = 'DOE-Halter_01_D25___V05'
deckel_filename = 'Deckel___V03'
 
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s
 
try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)
 
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.window = MainWindow
        global switch
 
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(600, 800)
        MainWindow.setMinimumSize(QtCore.QSize(600, 300))
        MainWindow.setMaximumSize(QtCore.QSize(600, 900))
        self.widget = QtGui.QWidget(MainWindow)
        self.widget.setObjectName(_fromUtf8("widget"))

        #Font
        font = QtGui.QFont()          # see http://doc.qt.io/qt-4.8/qfont.html              # label text displayed and colored in red
        font.setFamily("Times New Roman")                                                   # font used (Windows)
        font.setPointSize(10)                                                               # font PointSize
        font.setWeight(10)                                                                  # font Weight
        font.setBold(True)                                                                  # Bolt True or False 


#        section groupBox for the four radioButton
        self.groupBox = QtGui.QGroupBox(self.widget)                                        # this is the group for associate the four radioButton
        self.groupBox.setGeometry(QtCore.QRect(10, 5, 580, 250))                          # coordinates position
        self.groupBox.setObjectName(_fromUtf8("groupBox"))                                  # name of window groupBox

#        section groupBox for the four radioButton
        self.groupBox2 = QtGui.QGroupBox(self.widget)                                        # this is the group for associate the four radioButton
        self.groupBox2.setGeometry(QtCore.QRect(10, 270, 580, 485))                          # coordinates position
        self.groupBox2.setObjectName(_fromUtf8("groupBox"))   

        # Labeling 
        self.label_1 = QtGui.QLabel(self.widget)                                            # labels displayed on widget
        self.label_1.setGeometry(QtCore.QRect(25, 372, 190, 45))                           # label coordinates 
        self.label_1.setObjectName(_fromUtf8("label_1"))                                    # label name                                   # Color text
        self.label_1.setText(_translate("MainWindow", "DOE Hole Width [mm]", None))                 # same resultt with "<b>Hello world</b>"
 
        self.label_2 = QtGui.QLabel(self.widget)                                            # labels displayed on widget
        self.label_2.setGeometry(QtCore.QRect(25, 618, 150, 25))                           # label coordinates 
        self.label_2.setObjectName(_fromUtf8("label_2"))                                    # label name                                   # Color text
        self.label_2.setText(_translate("MainWindow", "comp. Location", None))                 # same resultt with "<b>Hello world</b>"
        
        self.label_3 = QtGui.QLabel(self.widget)                                            # labels displayed on widget
        self.label_3.setGeometry(QtCore.QRect(205, 640, 400, 25))                           # label coordinates 
        self.label_3.setObjectName(_fromUtf8("label_3"))                                    # label name                                   # Color text
        self.label_3.setFont(font)
        self.label_3.setText(_translate("MainWindow", "e.g.: C:/Users/ITO/Desktop/Testdatei", None))                 # same resultt with "<b>Hello world</b>"

        self.label_4 = QtGui.QLabel(self.widget)                                            # labels displayed on widget
        self.label_4.setGeometry(QtCore.QRect(465, 640, 120, 25))                           # label coordinates 
        self.label_4.setObjectName(_fromUtf8("label_4"))                                    # label name                                   # Color text
        self.label_4.setFont(font)
        self.label_4.setText(_translate("MainWindow", "file format", None))                 # same resultt with "<b>Hello world</b>"
 
        self.label_5 = QtGui.QLabel(self.widget)                                            # labels displayed on widget
        self.label_5.setGeometry(QtCore.QRect(25, 522, 160, 50))                           # label coordinates 
        self.label_5.setObjectName(_fromUtf8("label_5"))                                    # label name                                   # Color text
        self.label_5.setText(_translate("MainWindow", "integrated Lens", None))                 # same resultt with "<b>Hello world</b>"

        self.label_6 = QtGui.QLabel(self.widget)                                            # labels displayed on widget
        self.label_6.setGeometry(QtCore.QRect(25, 398, 190, 45))                           # label coordinates 
        self.label_6.setObjectName(_fromUtf8("label_6"))                                    # label name                                   # Color text
        self.label_6.setText(_translate("MainWindow", "DOE Hole Height [mm]", None))                 # same resultt with "<b>Hello world</b>"

        self.label_7 = QtGui.QLabel(self.widget)                                            # labels displayed on widget
        self.label_7.setGeometry(QtCore.QRect(25, 322, 190, 45))                           # label coordinates 
        self.label_7.setObjectName(_fromUtf8("label_7"))                                    # label name                                   # Color text
        self.label_7.setText(_translate("MainWindow", "Lens Diameter [mm]", None))                 # same resultt with "<b>Hello world</b>"

        self.label_8 = QtGui.QLabel(self.widget)                                            # labels displayed on widget
        self.label_8.setGeometry(QtCore.QRect(25, 347, 190, 45))                           # label coordinates 
        self.label_8.setObjectName(_fromUtf8("label_8"))                                    # label name                                   # Color text
        self.label_8.setText(_translate("MainWindow", "Lens Holder Depth [mm]", None))                 # same resultt with "<b>Hello world</b>"

        self.label_9 = QtGui.QLabel(self.widget)                                            # labels displayed on widget
        self.label_9.setGeometry(QtCore.QRect(25, 273, 190, 45))                           # label coordinates 
        self.label_9.setObjectName(_fromUtf8("label_9"))                                    # label name                                   # Color text
        self.label_9.setText(_translate("MainWindow", "Laser Diameter [mm]", None))                 # same resultt with "<b>Hello world</b>"

        self.label_10 = QtGui.QLabel(self.widget)                                            # labels displayed on widget
        self.label_10.setGeometry(QtCore.QRect(25, 548, 190, 45))                           # label coordinates 
        self.label_10.setObjectName(_fromUtf8("label_10"))                                    # label name                                   # Color text
        self.label_10.setText(_translate("MainWindow", "Rod Length [mm]", None))                 # same resultt with "<b>Hello world</b>"

        self.label_11 = QtGui.QLabel(self.widget)                                            # labels displayed on widget
        self.label_11.setGeometry(QtCore.QRect(25, 297, 190, 45))                           # label coordinates 
        self.label_11.setObjectName(_fromUtf8("label_11"))                                    # label name                                   # Color text
        self.label_11.setText(_translate("MainWindow", "Laser Length [mm]", None))                 # same resultt with "<b>Hello world</b>"

        self.label_12 = QtGui.QLabel(self.widget)                                            # labels displayed on widget
        self.label_12.setGeometry(QtCore.QRect(25, 423, 190, 45))                           # label coordinates 
        self.label_12.setObjectName(_fromUtf8("label_12"))                                    # label name                                   # Color text
        self.label_12.setText(_translate("MainWindow", "Dist. Laser-Lens [mm]", None))                 # same resultt with "<b>Hello world</b>"

        self.label_13 = QtGui.QLabel(self.widget)                                            # labels displayed on widget
        self.label_13.setGeometry(QtCore.QRect(25, 3, 190, 45))                           # label coordinates 
        self.label_13.setObjectName(_fromUtf8("label_13"))                                    # label name                                   # Color text
        self.label_13.setText(_translate("MainWindow", "Desired Wavelength [nm]", None))                 # same resultt with "<b>Hello world</b>"

        self.label_14 = QtGui.QLabel(self.widget)                                            # labels displayed on widget
        self.label_14.setGeometry(QtCore.QRect(25, 28, 190, 45))                           # label coordinates 
        self.label_14.setObjectName(_fromUtf8("label_14"))                                    # label name                                   # Color text
        self.label_14.setText(_translate("MainWindow", "Desired Laser Power [mW]", None))                 # same resultt with "<b>Hello world</b>"

        self.label_15 = QtGui.QLabel(self.widget)                                            # labels displayed on widget
        self.label_15.setGeometry(QtCore.QRect(25, 573, 190, 45))                           # label coordinates 
        self.label_15.setObjectName(_fromUtf8("label_15"))                                    # label name                                   # Color text
        self.label_15.setText(_translate("MainWindow", "Mounting element", None))                 # same resultt with "<b>Hello world</b>"

        self.label_16 = QtGui.QLabel(self.widget)                                            # labels displayed on widget
        self.label_16.setGeometry(QtCore.QRect(25, 448, 190, 45))                           # label coordinates 
        self.label_16.setObjectName(_fromUtf8("label_16"))                                    # label name                                   # Color text
        self.label_16.setText(_translate("MainWindow", "Projection Height/Width [mm]", None))                 # same resultt with "<b>Hello world</b>"

        self.label_17 = QtGui.QLabel(self.widget)                                            # labels displayed on widget
        self.label_17.setGeometry(QtCore.QRect(25, 473, 190, 45))                           # label coordinates 
        self.label_17.setObjectName(_fromUtf8("label_17"))                                    # label name                                   # Color text
        self.label_17.setText(_translate("MainWindow", "Projection Depth [mm]", None))                 # same resultt with "<b>Hello world</b>"

        self.label_18 = QtGui.QLabel(self.widget)                                            # labels displayed on widget
        self.label_18.setGeometry(QtCore.QRect(25, 498, 190, 45))                           # label coordinates 
        self.label_18.setObjectName(_fromUtf8("label_18"))                                    # label name                                   # Color text
        self.label_18.setText(_translate("MainWindow", "Working Distance [cm]", None))                 # same resultt with "<b>Hello world</b>"

        #        section horizontalSlider 
        self.horizontalSlider1 = QtGui.QSlider(self.widget)                                  # create horizontalSlider
        self.horizontalSlider1.setRange(10, 130)                                                 #value*10 to get to get one decimal digit
        self.horizontalSlider1.setGeometry(QtCore.QRect(205, 388, 230, 18))                     # coordinates position
        self.horizontalSlider1.setOrientation(QtCore.Qt.Horizontal)                          # orientation Horizontal
        self.horizontalSlider1.setInvertedAppearance(False)                                  # displacement rigth to left or left to rigth value "True" or "False"
        self.horizontalSlider1.setObjectName(_fromUtf8("horizontalSlider1"))                  # object Name
        self.horizontalSlider1.valueChanged.connect(self.on_horizontal_slider1)               # connect on "def on_horizontal_slider:" for execute action

        #        section horizontalSlider 
        self.horizontalSlider2 = QtGui.QSlider(self.widget)                                  # create horizontalSlider
        self.horizontalSlider2.setRange(10, 130)                                                 #value*10 to get to get one decimal digit
        self.horizontalSlider2.setGeometry(QtCore.QRect(205, 413, 230, 18))                     # coordinates position
        self.horizontalSlider2.setOrientation(QtCore.Qt.Horizontal)                          # orientation Horizontal
        self.horizontalSlider2.setInvertedAppearance(False)                                  # displacement rigth to left or left to rigth value "True" or "False"
        self.horizontalSlider2.setObjectName(_fromUtf8("horizontalSlider2"))                  # object Name
        self.horizontalSlider2.valueChanged.connect(self.on_horizontal_slider2)               # connect on "def on_horizontal_slider:" for execute action

        #        section horizontalSlider 
        self.horizontalSlider3 = QtGui.QSlider(self.widget)                                  # create horizontalSlider
        self.horizontalSlider3.setRange(100, 260)                                                 #value*10 to get to get one decimal digit
        self.horizontalSlider3.setGeometry(QtCore.QRect(205, 338, 230, 18))                     # coordinates position
        self.horizontalSlider3.setOrientation(QtCore.Qt.Horizontal)                          # orientation Horizontal
        self.horizontalSlider3.setInvertedAppearance(False)                                  # displacement rigth to left or left to rigth value "True" or "False"
        self.horizontalSlider3.setObjectName(_fromUtf8("horizontalSlider3"))                  # object Name
        self.horizontalSlider3.valueChanged.connect(self.on_horizontal_slider3)               # connect on "def on_horizontal_slider:" for execute action

        #        section horizontalSlider 
        self.horizontalSlider4 = QtGui.QSlider(self.widget)                                  # create horizontalSlider
        self.horizontalSlider4.setRange(30, 300)                                                 #value*10 to get to get one decimal digit
        self.horizontalSlider4.setGeometry(QtCore.QRect(205, 363, 230, 18))                     # coordinates position
        self.horizontalSlider4.setOrientation(QtCore.Qt.Horizontal)                          # orientation Horizontal
        self.horizontalSlider4.setInvertedAppearance(False)                                  # displacement rigth to left or left to rigth value "True" or "False"
        self.horizontalSlider4.setObjectName(_fromUtf8("horizontalSlider4"))                  # object Name
        self.horizontalSlider4.valueChanged.connect(self.on_horizontal_slider4)               # connect on "def on_horizontal_slider:" for execute action

        #        section horizontalSlider 
        self.horizontalSlider5 = QtGui.QSlider(self.widget)                                  # create horizontalSlider
        self.horizontalSlider5.setRange(100, 260)                                                 #value*10 to get to get one decimal digit
        self.horizontalSlider5.setGeometry(QtCore.QRect(205, 288, 230, 18))                     # coordinates position
        self.horizontalSlider5.setOrientation(QtCore.Qt.Horizontal)                          # orientation Horizontal
        self.horizontalSlider5.setInvertedAppearance(False)                                  # displacement rigth to left or left to rigth value "True" or "False"
        self.horizontalSlider5.setObjectName(_fromUtf8("horizontalSlider5"))                  # object Name
        self.horizontalSlider5.valueChanged.connect(self.on_horizontal_slider5)               # connect on "def on_horizontal_slider:" for execute action

        #        section horizontalSlider 
        self.horizontalSlider6 = QtGui.QSlider(self.widget)                                  # create horizontalSlider
        self.horizontalSlider6.setRange(220, 1200)                                                 #value*10 to get to get one decimal digit
        self.horizontalSlider6.setGeometry(QtCore.QRect(205, 313, 230, 18))                     # coordinates position
        self.horizontalSlider6.setOrientation(QtCore.Qt.Horizontal)                          # orientation Horizontal
        self.horizontalSlider6.setInvertedAppearance(False)                                  # displacement rigth to left or left to rigth value "True" or "False"
        self.horizontalSlider6.setObjectName(_fromUtf8("horizontalSlider6"))                  # object Name
        self.horizontalSlider6.valueChanged.connect(self.on_horizontal_slider6)               # connect on "def on_horizontal_slider:" for execute action

        #        section horizontalSlider 
        self.horizontalSlider7 = QtGui.QSlider(self.widget)                                  # create horizontalSlider
        self.horizontalSlider7.setRange(500, 1000)                                                 #value*10 to get to get one decimal digit
        self.horizontalSlider7.setGeometry(QtCore.QRect(205, 438, 230, 18))                     # coordinates position
        self.horizontalSlider7.setOrientation(QtCore.Qt.Horizontal)                          # orientation Horizontal
        self.horizontalSlider7.setInvertedAppearance(False)                                  # displacement rigth to left or left to rigth value "True" or "False"
        self.horizontalSlider7.setObjectName(_fromUtf8("horizontalSlider7"))                  # object Name
        self.horizontalSlider7.valueChanged.connect(self.on_horizontal_slider7)               # connect on "def on_horizontal_slider:" for execute action

        #        section horizontalSlider 
        self.horizontalSlider8 = QtGui.QSlider(self.widget)                                  # create horizontalSlider
        self.horizontalSlider8.setRange(4000, 10000)                                                 #value*10 to get to get one decimal digit
        self.horizontalSlider8.setGeometry(QtCore.QRect(205, 18, 230, 18))                     # coordinates position
        self.horizontalSlider8.setOrientation(QtCore.Qt.Horizontal)                          # orientation Horizontal
        self.horizontalSlider8.setInvertedAppearance(False)                                  # displacement rigth to left or left to rigth value "True" or "False"
        self.horizontalSlider8.setObjectName(_fromUtf8("horizontalSlider8"))                  # object Name
        self.horizontalSlider8.valueChanged.connect(self.on_horizontal_slider8)               # connect on "def on_horizontal_slider:" for execute action

        #        section horizontalSlider 
        self.horizontalSlider9 = QtGui.QSlider(self.widget)                                  # create horizontalSlider
        self.horizontalSlider9.setRange(4, 2000)                                                 #value*10 to get to get one decimal digit
        self.horizontalSlider9.setGeometry(QtCore.QRect(205, 44, 230, 18))                     # coordinates position
        self.horizontalSlider9.setOrientation(QtCore.Qt.Horizontal)                          # orientation Horizontal
        self.horizontalSlider9.setInvertedAppearance(False)                                  # displacement rigth to left or left to rigth value "True" or "False"
        self.horizontalSlider9.setObjectName(_fromUtf8("horizontalSlider9"))                  # object Name
        self.horizontalSlider9.valueChanged.connect(self.on_horizontal_slider9)               # connect on "def on_horizontal_slider:" for execute action

        #        section horizontalSlider 
        self.horizontalSlider10 = QtGui.QSlider(self.widget)                                  # create horizontalSlider
        self.horizontalSlider10.setRange(100, 20000)                                                 #value*10 to get to get one decimal digit
        self.horizontalSlider10.setGeometry(QtCore.QRect(205,463, 230, 18))                     # coordinates position
        self.horizontalSlider10.setOrientation(QtCore.Qt.Horizontal)                          # orientation Horizontal
        self.horizontalSlider10.setInvertedAppearance(False)                                  # displacement rigth to left or left to rigth value "True" or "False"
        self.horizontalSlider10.setObjectName(_fromUtf8("horizontalSlider10"))                  # object Name
        self.horizontalSlider10.valueChanged.connect(self.on_horizontal_slider10)               # connect on "def on_horizontal_slider:" for execute action

        #        section horizontalSlider 
        self.horizontalSlider11 = QtGui.QSlider(self.widget)                                  # create horizontalSlider
        self.horizontalSlider11.setRange(10, 20000)                                                 #value*10 to get to get one decimal digit
        self.horizontalSlider11.setGeometry(QtCore.QRect(205, 488, 230, 18))                     # coordinates position
        self.horizontalSlider11.setOrientation(QtCore.Qt.Horizontal)                          # orientation Horizontal
        self.horizontalSlider11.setInvertedAppearance(False)                                  # displacement rigth to left or left to rigth value "True" or "False"
        self.horizontalSlider11.setObjectName(_fromUtf8("horizontalSlider11"))                  # object Name
        self.horizontalSlider11.valueChanged.connect(self.on_horizontal_slider11)               # connect on "def on_horizontal_slider:" for execute action

        #        section horizontalSlider 
        self.horizontalSlider12 = QtGui.QSlider(self.widget)                                  # create horizontalSlider
        self.horizontalSlider12.setRange(100, 10000)                                                 #value*10 to get to get one decimal digit
        self.horizontalSlider12.setGeometry(QtCore.QRect(205, 513, 230, 18))                     # coordinates position
        self.horizontalSlider12.setOrientation(QtCore.Qt.Horizontal)                          # orientation Horizontal
        self.horizontalSlider12.setInvertedAppearance(False)                                  # displacement rigth to left or left to rigth value "True" or "False"
        self.horizontalSlider12.setObjectName(_fromUtf8("horizontalSlider12"))                  # object Name
        self.horizontalSlider12.valueChanged.connect(self.on_horizontal_slider12)               # connect on "def on_horizontal_slider:" for execute action

#        section pushButton 1
        self.pushButton_1 = QtGui.QPushButton(self.widget)                                  # create object PushButton_1
        self.pushButton_1.setGeometry(QtCore.QRect(240, 720, 75, 30))                        # coordinates position
        self.pushButton_1.setObjectName(_fromUtf8("pushButton_1"))                          # name of object
        self.pushButton_1.clicked.connect(self.on_pushButton_1_clicked)                     # connect on def "on_pushButton_1_clicked"
 
#        section pushButton 2
        self.pushButton_2 = QtGui.QPushButton(self.widget)                                  # create object pushButton_2
        self.pushButton_2.setGeometry(QtCore.QRect(330, 720, 75, 30))                       # coordinates position
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))                          # name of object
        self.pushButton_2.clicked.connect(self.on_pushButton_2_clicked)                     # connect on def "on_pushButton_2_clicked"

#        section pushButton 3
        self.pushButton_3 = QtGui.QPushButton(self.widget)                                  # create object pushButton_2
        self.pushButton_3.setGeometry(QtCore.QRect(510, 720, 75, 30))                       # coordinates position
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))                          # name of object
        self.pushButton_3.clicked.connect(self.on_pushButton_3_clicked)                     # connect on def "on_pushButton_2_clicked"

#        section pushButton 4
        self.pushButton_4 = QtGui.QPushButton(self.widget)                                  # create object pushButton_2
        self.pushButton_4.setGeometry(QtCore.QRect(420, 720, 75, 30))                       # coordinates position
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))                          # name of object
        self.pushButton_4.clicked.connect(self.on_pushButton_4_clicked)                     # connect on def "on_pushButton_2_clicked"

#        section pushButton 5
        self.pushButton_5 = QtGui.QPushButton(self.widget)                                  # create object pushButton_2
        self.pushButton_5.setGeometry(QtCore.QRect(464, 225, 122, 25))                       # coordinates position
        self.pushButton_5.setObjectName(_fromUtf8("pushButton_5"))                          # name of object
        self.pushButton_5.clicked.connect(self.on_pushButton_5_clicked)                     # connect on def "on_pushButton_2_clicked"

#        section comboBox1
        self.cb1 = QtGui.QComboBox(self.widget)
        self.cb1.setGeometry(QtCore.QRect(465, 536, 120, 25))
        self.cb1.addItem("yes")
        self.cb1.addItem("no")
        self.cb1.currentIndexChanged.connect(self.selectionchange1)

#        section comboBox2
        self.cb2 = QtGui.QComboBox(self.widget)
        self.cb2.setGeometry(QtCore.QRect(465, 619, 120, 23))
        self.cb2.addItem(".stl")
        self.cb2.addItem(".step")
        self.cb2.addItems([".FreeCAD"])
        self.cb2.currentIndexChanged.connect(self.selectionchange2)

#        section comboBox3
        self.cb3 = QtGui.QComboBox(self.widget)
        self.cb3.setGeometry(QtCore.QRect(465, 564, 120, 23))
        self.cb3.addItem("200")
        self.cb3.addItem("125")
        self.cb3.addItems(["150","170","235"])
        self.cb3.currentIndexChanged.connect(self.selectionchange3)

#        section comboBox4
        self.cb4 = QtGui.QComboBox(self.widget)
        self.cb4.setGeometry(QtCore.QRect(465, 590, 120, 23))
        self.cb4.addItem("2x, 180°")
        self.cb4.addItem("1x")
        self.cb4.addItems(["2x, 90°","3x","4x"])
        self.cb4.currentIndexChanged.connect(self.selectionchange4)



        #        section lineEdit 1
        self.lineEdit_1 = QtGui.QLineEdit(self.widget)                                      # create object lineEdit_1
        self.lineEdit_1.setGeometry(QtCore.QRect(465, 386, 120, 22))                          # coordinates position
        self.lineEdit_1.setObjectName(_fromUtf8("lineEdit_1"))                              # name of object
        self.lineEdit_1.setText("1.0")                                                        # text by default
        self.lineEdit_1.returnPressed.connect(self.on_lineEdit_1_Pressed)                  # connect on def "on_lineEdit_1_Pressed" for execute actionn   # for validate the data with press on return touch
        #self.lineEdit_1.textChanged.connect(self.on_lineEdit_1_Pressed)                     # connect on def "on_lineEdit_1_Pressed" for execute actionn   # with tips key char by char
                                                                                            # a tooltip can be set to all objects

#        section lineEdit 2
        self.lineEdit_2 = QtGui.QLineEdit(self.widget)                                      # create object lineEdit_2
        self.lineEdit_2.setGeometry(QtCore.QRect(205, 620, 250, 22))                          # coordinates position
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))                              # name of object
        self.lineEdit_2.setText("")                                                        # text by default
        self.lineEdit_2.returnPressed.connect(self.on_lineEdit_2_Pressed)                  # connect on def "on_lineEdit_2_Pressed" for execute actionn   # for validate the data with press on return touch
        #self.lineEdit_2.textChanged.connect(self.on_lineEdit_2_Pressed)                     # connect on def "on_lineEdit_2_Pressed" for execute actionn   # with tips key char by char
                                                                                            # a tooltip can be set to all objects

        #        section lineEdit 3
        self.lineEdit_3 = QtGui.QLineEdit(self.widget)                                      # create object lineEdit_3
        self.lineEdit_3.setGeometry(QtCore.QRect(465, 411, 120, 22))                          # coordinates position
        self.lineEdit_3.setObjectName(_fromUtf8("lineEdit_3"))                              # name of object
        self.lineEdit_3.setText("1.0")                                                        # text by default
        self.lineEdit_3.returnPressed.connect(self.on_lineEdit_3_Pressed)                  # connect on def "on_lineEdit_3_Pressed" for execute actionn   # for validate the data with press on return touch
        #self.lineEdit_3.textChanged.connect(self.on_lineEdit_3_Pressed)                     # connect on def "on_lineEdit_3_Pressed" for execute actionn   # with tips key char by char
                                                                                            # a tooltip can be set to all objects

#        section lineEdit 4
        self.lineEdit_4 = QtGui.QLineEdit(self.widget)                                      # create object lineEdit_2
        self.lineEdit_4.setGeometry(QtCore.QRect(465, 336, 120, 22))                          # coordinates position
        self.lineEdit_4.setObjectName(_fromUtf8("lineEdit_4"))                              # name of object
        self.lineEdit_4.setText("10.0")                                                        # text by default
        self.lineEdit_4.returnPressed.connect(self.on_lineEdit_4_Pressed)                  # connect on def "on_lineEdit_2_Pressed" for execute actionn   # for validate the data with press on return touch
        #self.lineEdit_4.textChanged.connect(self.on_lineEdit_4_Pressed)                     # connect on def "on_lineEdit_2_Pressed" for execute actionn   # with tips key char by char
                                                                                            # a tooltip can be set to all objects

#        section lineEdit 5
        self.lineEdit_5 = QtGui.QLineEdit(self.widget)                                      # create object lineEdit_2
        self.lineEdit_5.setGeometry(QtCore.QRect(465, 361, 120, 22))                          # coordinates position
        self.lineEdit_5.setObjectName(_fromUtf8("lineEdit_5"))                              # name of object
        self.lineEdit_5.setText("3.0")                                                        # text by default
        self.lineEdit_5.returnPressed.connect(self.on_lineEdit_5_Pressed)                  # connect on def "on_lineEdit_2_Pressed" for execute actionn   # for validate the data with press on return touch
        #self.lineEdit_5.textChanged.connect(self.on_lineEdit_5_Pressed)                     # connect on def "on_lineEdit_2_Pressed" for execute actionn   # with tips key char by char
                                                                                            # a tooltip can be set to all objects

#        section lineEdit 6
        self.lineEdit_6 = QtGui.QLineEdit(self.widget)                                      # create object lineEdit_2
        self.lineEdit_6.setGeometry(QtCore.QRect(465,286, 120, 22))                          # coordinates position
        self.lineEdit_6.setObjectName(_fromUtf8("lineEdit_6"))                              # name of object
        self.lineEdit_6.setText("10.0")                                                        # text by default
        self.lineEdit_6.returnPressed.connect(self.on_lineEdit_6_Pressed)                  # connect on def "on_lineEdit_2_Pressed" for execute actionn   # for validate the data with press on return touch
        #self.lineEdit_6.textChanged.connect(self.on_lineEdit_6_Pressed)                     # connect on def "on_lineEdit_2_Pressed" for execute actionn   # with tips key char by char
                                                                                            # a tooltip can be set to all objects

#        section lineEdit 7
        self.lineEdit_7 = QtGui.QLineEdit(self.widget)                                      # create object lineEdit_2
        self.lineEdit_7.setGeometry(QtCore.QRect(465, 311, 120, 22))                          # coordinates position
        self.lineEdit_7.setObjectName(_fromUtf8("lineEdit_7"))                              # name of object
        self.lineEdit_7.setText("22.0")                                                        # text by default
        self.lineEdit_7.returnPressed.connect(self.on_lineEdit_7_Pressed)                  # connect on def "on_lineEdit_2_Pressed" for execute actionn   # for validate the data with press on return touch
        #self.lineEdit_6.textChanged.connect(self.on_lineEdit_7_Pressed)                     # connect on def "on_lineEdit_2_Pressed" for execute actionn   # with tips key char by char
                                                                                            # a tooltip can be set to all objects

#        section lineEdit 8
        self.lineEdit_8 = QtGui.QLineEdit(self.widget)                                      # create object lineEdit_2
        self.lineEdit_8.setGeometry(QtCore.QRect(465, 436, 120, 22))                          # coordinates position
        self.lineEdit_8.setObjectName(_fromUtf8("lineEdit_8"))                              # name of object
        self.lineEdit_8.setText("50.0")                                                        # text by default
        self.lineEdit_8.returnPressed.connect(self.on_lineEdit_8_Pressed)                  # connect on def "on_lineEdit_2_Pressed" for execute actionn   # for validate the data with press on return touch
        #self.lineEdit_6.textChanged.connect(self.on_lineEdit_8_Pressed)                     # connect on def "on_lineEdit_2_Pressed" for execute actionn   # with tips key char by char
                                                                                            # a tooltip can be set to all objects

#        section lineEdit 9
        self.lineEdit_9 = QtGui.QLineEdit(self.widget)                                      # create object lineEdit_2
        self.lineEdit_9.setGeometry(QtCore.QRect(465, 18, 120, 22))                          # coordinates position
        self.lineEdit_9.setObjectName(_fromUtf8("lineEdit_9"))                              # name of object
        self.lineEdit_9.setText("400.0")                                                        # text by default
        self.lineEdit_9.returnPressed.connect(self.on_lineEdit_9_Pressed)                  # connect on def "on_lineEdit_2_Pressed" for execute actionn   # for validate the data with press on return touch
        #self.lineEdit_9.textChanged.connect(self.on_lineEdit_9_Pressed)                     # connect on def "on_lineEdit_2_Pressed" for execute actionn   # with tips key char by char
                                                                                            # a tooltip can be set to all objects

#        section lineEdit 10
        self.lineEdit_10 = QtGui.QLineEdit(self.widget)                                      # create object lineEdit_2
        self.lineEdit_10.setGeometry(QtCore.QRect(465, 43, 120, 22))                          # coordinates position
        self.lineEdit_10.setObjectName(_fromUtf8("lineEdit_10"))                              # name of object
        self.lineEdit_10.setText("0.4")                                                        # text by default
        self.lineEdit_10.returnPressed.connect(self.on_lineEdit_10_Pressed)                  # connect on def "on_lineEdit_2_Pressed" for execute actionn   # for validate the data with press on return touch
        #self.lineEdit_10.textChanged.connect(self.on_lineEdit_10_Pressed)                     # connect on def "on_lineEdit_2_Pressed" for execute actionn   # with tips key char by char
                                                                                            # a tooltip can be set to all objects

#        section lineEdit 11
        self.lineEdit_11 = QtGui.QLineEdit(self.widget)                                      # create object lineEdit_2
        self.lineEdit_11.setGeometry(QtCore.QRect(465, 461, 120, 22))                          # coordinates position
        self.lineEdit_11.setObjectName(_fromUtf8("lineEdit_11"))                              # name of object
        self.lineEdit_11.setText("10.0")                                                        # text by default
        self.lineEdit_11.returnPressed.connect(self.on_lineEdit_11_Pressed)                  # connect on def "on_lineEdit_2_Pressed" for execute actionn   # for validate the data with press on return touch
        #self.lineEdit_11.textChanged.connect(self.on_lineEdit_10_Pressed)                     # connect on def "on_lineEdit_2_Pressed" for execute actionn   # with tips key char by char
                                                                                            # a tooltip can be set to all objects

#        section lineEdit 12
        self.lineEdit_12 = QtGui.QLineEdit(self.widget)                                      # create object lineEdit_2
        self.lineEdit_12.setGeometry(QtCore.QRect(465, 486, 120, 22))                          # coordinates position
        self.lineEdit_12.setObjectName(_fromUtf8("lineEdit_12"))                              # name of object
        self.lineEdit_12.setText("1.0")                                                        # text by default
        self.lineEdit_12.returnPressed.connect(self.on_lineEdit_12_Pressed)                  # connect on def "on_lineEdit_2_Pressed" for execute actionn   # for validate the data with press on return touch
        #self.lineEdit_12.textChanged.connect(self.on_lineEdit_12_Pressed)                     # connect on def "on_lineEdit_2_Pressed" for execute actionn   # with tips key char by char
                                                                                            # a tooltip can be set to all objects

#        section lineEdit 13
        self.lineEdit_13 = QtGui.QLineEdit(self.widget)                                      # create object lineEdit_2
        self.lineEdit_13.setGeometry(QtCore.QRect(465, 511, 120, 22))                          # coordinates position
        self.lineEdit_13.setObjectName(_fromUtf8("lineEdit_13"))                              # name of object
        self.lineEdit_13.setText("10.0")                                                        # text by default
        self.lineEdit_13.returnPressed.connect(self.on_lineEdit_13_Pressed)                  # connect on def "on_lineEdit_2_Pressed" for execute actionn   # for validate the data with press on return touch
        #self.lineEdit_13.textChanged.connect(self.on_lineEdit_13_Pressed)                     # connect on def "on_lineEdit_2_Pressed" for execute actionn   # with tips key char by char
                                                                                            # a tooltip can be set to all objects









############################################################################



        font = QtGui.QFont()          # see http://doc.qt.io/qt-4.8/qfont.html              # label text displayed and colored in red
        font.setFamily("Calibri")                                                   # font used (Windows)
        font.setPointSize(10)                                                               # font PointSize
        font.setWeight(10)                                                                  # font Weight
        font.setBold(False)                                                                  # Bolt True or False 
        #self.label_00.setFont(font)                                                          # associate label_00 and font  
        #self.label_00.setObjectName("label_00")                                               # name of object
        #self.label_00.setStyleSheet("color : #0017ff")                                       # Color text
        #self.label_00.setText(_translate("MainWindow", "", None))                 # same resultt with "<b>Hello world</b>"  
        self.label_1.setFont(font)   
        self.label_2.setFont(font)   
        self.label_3.setFont(font)   
        self.label_4.setFont(font)   
        self.label_5.setFont(font)   
        self.label_6.setFont(font)   
        self.label_7.setFont(font)   
        self.label_8.setFont(font)   
        self.label_9.setFont(font)   
        self.label_10.setFont(font)   
        self.label_11.setFont(font)   
        self.label_12.setFont(font)
        self.label_13.setFont(font)   
        self.label_14.setFont(font)
        self.label_15.setFont(font)
        self.label_16.setFont(font)
        self.label_17.setFont(font)
        self.label_18.setFont(font)
        self.cb1.setFont(font)    
        self.cb2.setFont(font)  
        self.cb3.setFont(font)  
        self.cb4.setFont(font) 

        font2 = QtGui.QFont()          # see http://doc.qt.io/qt-4.8/qfont.html              # label text displayed and colored in red
        font2.setFamily("Calibri")                                                   # font used (Windows)
        font2.setPointSize(13)                                                               # font PointSize
        font2.setWeight(10)                                                                  # font Weight
        font2.setBold(True)  
        self.label_00 = QtGui.QLabel(self.widget)
        self.label_00.setGeometry(QtCore.QRect(25, 88, 300, 110))
        self.label_00.setObjectName(_fromUtf8("label_00"))
        self.label_00.setObjectName("label_00")                                               # name of object
        self.label_00.setStyleSheet("color : #0017ff")                                       # Color text
        self.label_00.setText(_translate("MainWindow", "", None))                 # same resultt with "<b>Hello world</b>"
        self.label_00.setFont(font2)

        font3 = QtGui.QFont()          # see http://doc.qt.io/qt-4.8/qfont.html              # label text displayed and colored in red
        font3.setFamily("Calibri")                                                   # font used (Windows)
        font3.setPointSize(12)                                                               # font PointSize
        font3.setWeight(10)                                                                  # font Weight
        font3.setBold(True)  
        self.pushButton_1.setFont(font3)
        self.pushButton_2.setFont(font3)
        self.pushButton_3.setFont(font3)
        self.pushButton_4.setFont(font3)
        self.pushButton_5.setFont(font3)


        font4 = QtGui.QFont()          # see http://doc.qt.io/qt-4.8/qfont.html              # label text displayed and colored in red
        font4.setFamily("Calibri")                                                   # font used (Windows)
        font4.setPointSize(8)                                                               # font PointSize
        font4.setWeight(10)                                                                  # font Weight
        font4.setBold(False)
        self.lineEdit_1.setFont(font4)   
        self.lineEdit_2.setFont(font4)   
        self.lineEdit_3.setFont(font4)   
        self.lineEdit_4.setFont(font4)   
        self.lineEdit_5.setFont(font4)   
        self.lineEdit_6.setFont(font4)   
        self.lineEdit_7.setFont(font4)   
        self.lineEdit_8.setFont(font4)   
        self.lineEdit_9.setFont(font4)   
        self.lineEdit_10.setFont(font4)
        self.lineEdit_11.setFont(font4)
        self.lineEdit_12.setFont(font4)
        self.lineEdit_13.setFont(font4) 





############################################################################









        ### ---graphicsView---
        MainWindow.setCentralWidget(self.widget)
        self.menuBar = QtGui.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 500, 26))
        self.menuBar.setObjectName(_fromUtf8("menuBar"))
        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QtGui.QToolBar(MainWindow)
        self.mainToolBar.setObjectName(_fromUtf8("mainToolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtGui.QStatusBar(MainWindow)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        MainWindow.setStatusBar(self.statusBar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
 
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)





    def retranslateUi(self, MainWindow):
        MainWindow.setWindowFlags(PySide.QtCore.Qt.WindowStaysOnTopHint)                   # this function turns the front window (stay to hint)
        MainWindow.setWindowTitle(_translate("MainWindow", "P-CAN Software", None))            # title main window
        #MainWindow.setWindowIcon(QtGui.QIcon(path+'MEPlan.png'))                           # change the icon of the main window
         
     
        #self.lineEdit_1.setToolTip(_translate("MainWindow", "LineEdit 1", None))
        #self.label_1.setText(_translate("MainWindow", "LineEdit 1", None))
        self.pushButton_1.setToolTip(_translate("MainWindow", "pushButton_1", None))
        self.pushButton_1.setText(_translate("MainWindow", "Reset", None))
        self.pushButton_2.setToolTip(_translate("MainWindow", "pushButton_2", None))
        self.pushButton_2.setText(_translate("MainWindow", "Quit", None))
        self.pushButton_3.setToolTip(_translate("MainWindow", "pushButton_3", None))
        self.pushButton_3.setText(_translate("MainWindow", "Save", None))            
        self.pushButton_4.setToolTip(_translate("MainWindow", "pushButton_4", None))
        self.pushButton_4.setText(_translate("MainWindow", "Apply", None))            
        self.pushButton_5.setToolTip(_translate("MainWindow", "pushButton_4", None))
        self.pushButton_5.setText(_translate("MainWindow", "Search Laser", None)) 









    def affectation_X (self,val_X0):                                                        # connection affectation_X
        val_X = float(val_X0)                                                              # extract the value and transform it in float
        #
        #here your code
        #
        print( val_X0)
        return (float(val_X))
        #

    def affectation_Y (self,val_Y0):                                                        # connection affectation_X
        val_Y = float(val_Y0)                                                              # extract the value and transform it in float
        #
        #here your code
        #
        print( val_Y0)
        return (float(val_Y))
        #

    def affectation_LensDiameter (self,val_LensDiameter0):                                                        # connection affectation_X
        val_LensDiameter = float(val_LensDiameter0)                                                              # extract the value and transform it in float
        #
        #here your code
        #
        print( val_LensDiameter0)
        return (float(val_LensDiameter))
        #


    def affectation_HolderDepth (self,val_HolderDepth0):                                                        # connection affectation_X
        val_HolderDepth = float(val_HolderDepth0)                                                              # extract the value and transform it in float
        #
        #here your code
        #
        print( val_HolderDepth0)
        return (float(val_HolderDepth))
        #

    def affectation_LaserDiameter (self,val_LaserDiameter0):                                                        # connection affectation_X
        val_LaserDiameter = float(val_LaserDiameter0)                                                              # extract the value and transform it in float
        #
        #here your code
        #
        print( val_LaserDiameter0)
        return (float(val_LaserDiameter))
        #

    def affectation_LaserLength (self,val_LaserLength0):                                                        # connection affectation_X
        val_LaserLength = float(val_LaserLength0)                                                              # extract the value and transform it in float
        #
        #here your code
        #
        print( val_LaserLength0)
        return (float(val_LaserLength))
        #

    def affectation_DisLaserLens (self,val_DisLaserLens0):                                                        # connection affectation_X
        val_DisLaserLens = float(val_DisLaserLens0)                                                              # extract the value and transform it in float
        #
        #here your code
        #
        print( val_DisLaserLens0)
        return (float(val_DisLaserLens))
        #

    def affectation_Wavelength (self,val_Wavelength0):                                                        # connection affectation_X
        val_Wavelength = float(val_Wavelength0)                                                              # extract the value and transform it in float
        #
        #here your code
        #
        print( val_Wavelength0)
        return (float(val_Wavelength))
        #

    def affectation_Power (self,val_Power0):                                                        # connection affectation_X
        val_Power = float(val_Power0)                                                              # extract the value and transform it in float
        #
        #here your code
        #
        print( val_Power0)
        return (float(val_Power))
        #

    def affectation_ProjHeightWidth (self,val_ProjHeightWidth0):                                                        # connection affectation_X
        val_ProjHeightWidth = float(val_ProjHeightWidth0)                                                              # extract the value and transform it in float
        #
        #here your code
        #
        print( val_ProjHeightWidth0)
        return (float(val_ProjHeightWidth))
        #

    def affectation_ProjDepth (self,val_ProjDepth0):                                                        # connection affectation_X
        val_ProjDepth = float(val_ProjDepth0)                                                              # extract the value and transform it in float
        #
        #here your code
        #
        print( val_ProjDepth0)
        return (float(val_ProjDepth))
        #

    def affectation_WorkingDistance (self,val_WorkingDistance0):                                                        # connection affectation_X
        val_WorkingDistance = float(val_WorkingDistance0)                                                              # extract the value and transform it in float
        #
        #here your code
        #
        print( val_WorkingDistance0)
        return (float(val_WorkingDistance))
        #

    def selectionchange1 (self):
        e=10						#Random Value to give function the needed arguments
        #self.Darstellung(e)

    def selectionchange2 (self):
        e=10						#Random Value to give function the needed arguments
        #self.Darstellung(e)

    def selectionchange3 (self):
        e=10						#Random Value to give function the needed arguments
        #self.Darstellung(e)

    def selectionchange4 (self):
        e=10						#Random Value to give function the needed arguments
        #self.Darstellung(e)

########################################################################
    def Darstellung(self, val_X):						#Plot Part
        #Definition of Values
        csvdatei = open(csv_filename,"r",encoding="latin-1")
        csv_reader = csv.reader(csvdatei, delimiter=';')
        zeilennummer = 0
        for row in csv_reader:
            if zeilennummer == 0:
                print(f'Spaltennamen sind: {", ".join(row)}')
            else:
                Width=float(row[0])
                Height=float(row[1])
                DL=float(row[2])
                Thickness=float(row[3])
                LHD=float(row[4])
                RodLength=int(row[5])
                LensBin= int(row[6])
                LL=float(row[7])
                DLL= float(row[8])
                Mount = int(row[11])


            zeilennummer += 1
        
        csvdatei.close()

        clearAll()
        ###Part-Code###############################################################
        ###DOE-Holder1###############################################################
        ##BasePart
        #make sketch
        x1=15
        y1=-30
        x2=15
        y2=30
        x3=18
        y3=30
        x4=18
        y4=21
        x5=23
        y5=16
        x6=23
        y6=6.5
        x7=20
        y7=6.5
        x8=20
        y8=15.25
        x9=17
        y9=15.25
        x10=17
        y10=-15.25
        x11=20
        y11=-15.25
        x12=20
        y12=-6.5
        x13=23
        y13=-6.5
        x14=23
        y14=-16
        x15=18
        y15=-21
        x16=18
        y16=-30
        x17=15
        y17=-30

        #Extrude
        lshape_wire = Part.makePolygon([Base.Vector(x1, y1, 0), Base.Vector(x2, y2, 0), Base.Vector(x3, y3, 0), Base.Vector(x4, y4, 0), Base.Vector(x5, y5, 0), Base.Vector(x6, y6, 0), Base.Vector(x7, y7, 0), Base.Vector(x8, y8, 0), Base.Vector(x9, y9, 0), Base.Vector(x10, y10, 0), Base.Vector(x11, y11, 0), Base.Vector(x12, y12, 0), Base.Vector(x13, y13, 0), Base.Vector(x14, y14, 0), Base.Vector(x15, y15, 0), Base.Vector(x16, y16, 0), Base.Vector(x17, y17, 0)])
        L=Part.Face(lshape_wire)
        BasePart=  L.extrude(Base.Vector(0, 0, 60))

        #Part.show(BasePart)


        #SquareHole
        SquareHole=Part.makeBox(15,15,2)
        SquareHole.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 1, 0), 90)
        TranslationSquareHole=(15,-15/2,30+15/2)
        SquareHole.translate(TranslationSquareHole)
        #Part.show(SquareHole)


        fused1=BasePart.cut(SquareHole)
        #Part.show(fused1)

        #Cylinders for threads
        Cylinder=Part.makeCylinder(8/2,3)
        Cylinder.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 1, 0), 90)
        TranslationCylinder=(23,11,30)
        Cylinder.translate(TranslationCylinder)
        fused2=fused1.fuse(Cylinder)
        #Part.show(Cylinder)


        TranslationCylinder=(0,-2*11,0)
        Cylinder.translate(TranslationCylinder)
        fused3=fused2.fuse(Cylinder)
        #Part.show(Cylinder)


        #Part.show(fused3)

        #Drilling
        Drilling=Part.makeCylinder(3.9/2,6)
        Drilling.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 1, 0), 90)
        DrillingTranslation=(20,11,30)
        Drilling.translate(DrillingTranslation)
        fused4=fused3.cut(Drilling)
        TranslationDrilling=(0,-2*11,0)
        Drilling.translate(TranslationDrilling)
        fused5=fused4.cut(Drilling)

        #Part.show(fused5)

        #threads
        #Screw
        x1=0
        y1=0
        x2=0.1
        y2=0
        x3=0.1
        y3=0.05
        x4=1.0392/2+0.1
        y4=0.35
        x5=0.1
        y5=0.65
        x6=0.1
        y6=0.7
        x7=0
        y7=0.7
        x8=0
        y8=0
        
        shape1=Part.makeHelix(0.8,8,4.134/2)
        shape2= Part.makePolygon([Base.Vector(x1, y1, 0), Base.Vector(x2, y2, 0), Base.Vector(x3, y3, 0), Base.Vector(x4, y4, 0), Base.Vector(x5, y5, 0), Base.Vector(x6, y6, 0), Base.Vector(x7, y7, 0), Base.Vector(x8, y8, 0)])
        shape2.rotate(Base.Vector(0, 0, 0),Base.Vector(1, 0, 0), 90)
        TranslationShape2=(4.134/2-0.1,0,0)
        shape2.translate(TranslationShape2)

        traj = Part.Wire([shape1])
        section = Part.Wire([shape2])

        makeSolid = True #1
        isFrenet = True #1

        # create a 3D shape and assigh it to the current document
        Sweep = Part.Wire(traj).makePipeShell([section],makeSolid,isFrenet)
        inner=Part.makeCylinder(4.132/2,10)
        
        Thread=inner.fuse(Sweep)
        Thread.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 1, 0), 90)

        TranslationThread=(18.5,11,30)
        Thread.translate(TranslationThread)

        fused6=fused5.cut(Thread)

        TranslationThread=(0,-2*11,0)
        Thread.translate(TranslationThread)
        BasePart=fused6.cut(Thread)

        #Part.show(fused7)

        ################################################################
        ##LaserHolder Part
        #Definition
        HoleTolerance=0
        RectangleTolerance=0
        ToleranceNubble=0


	        
        #OuterRing
        BossExtrude1=Part.makeCylinder(40/2,15)
        CutExtrude1=Part.makeCylinder(33/2,15)
        PartBossExtrude1=BossExtrude1.cut(CutExtrude1)
	        

        #OuterRingSquares
        Square=Part.makeBox(5.13,15,15)
        TranslationSquare=(17.37,-15/2,0)
        Square.translate(TranslationSquare)
        #Part.show(Square)

	
        #CutoutsOuterRingSquares1
        Hole=Part.makeCylinder(2.2+HoleTolerance,15)
        TranslationHole=(20.3,0,0)
        Hole.translate(TranslationHole)
        PartCutout=Square.cut(Hole)
        fused6=PartBossExtrude1.cut(Hole)

        Rectangle=Part.makeBox(0.69+0.5,3.2+RectangleTolerance,15)
        TranslationRectangle=(21.81-0.25,-3.2/2-RectangleTolerance/2,0)
        Rectangle.translate(TranslationRectangle)
        PartCut=PartCutout.cut(Rectangle)
        fused7= fused6.fuse(PartCut)

        #CutoutsOuterRingSquares2
        PartCut.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 90)
        Hole.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 90)
        fused8=fused7.fuse(PartCut)
        fused9=fused8.cut(Hole)

	
        #CutoutsOuterRingSquares3
        PartCut.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 180)
        Hole.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 180)
        fused10=fused9.fuse(PartCut)
        fused11=fused10.cut(Hole)
        
	
        #CutoutsOuterRingSquares4
        PartCut.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 270)
        Hole.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 270)
        fused12=fused11.fuse(PartCut)
        fused13=fused12.cut(Hole)
        #Part.show(fused13)

	
	

        #Outer Polygon
        x1=18+2.75/(math.tan((30)*2*pi/360))
        y1=-4.25
        x2=18+2.75/(math.tan((30)*2*pi/360))
        y2=4.25
        x3=18
        y3=4.25
        x4=18
        y4=-4.25
        x5=18+2.75/(math.tan((30)*2*pi/360))
        y5=-4.25


        lshape_wire = Part.makePolygon([Base.Vector(x1, y1, 0), Base.Vector(x2, y2, 0), Base.Vector(x3, y3, 0), Base.Vector(x4, y4, 0), Base.Vector(x5, y5, 0)])
        L=Part.Face(lshape_wire)
        K1 = L.extrude(Base.Vector(0, 0, 15))
        K2 = L.extrude(Base.Vector(0, 0, 15))
        K3 = L.extrude(Base.Vector(0, 0, 15))
        K4 = L.extrude(Base.Vector(0, 0, 15))
        K1.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), -45)
        K2.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 45)
        K3.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 225)
        K4.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 135)

        fused14=fused13.fuse(K1)
        fused15=fused14.fuse(K2)
        fused16=fused15.fuse(K3)
        fused17=fused16.fuse(K4)
       
        fused17.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 1, 0), 90)	
        TranslationHolder4=(0,0,30)
        fused17.translate(TranslationHolder4)

        fused18=fused17.fuse(BasePart)
        #Part.show(fused18)

        #clampings
        #make sketch
        x1=0
        y1=0
        x2=0
        y2=3.25
        x3=2
        y3=3.25
        x4=15
        y4=0.25
        x5=15
        y5=0
        x6=0
        y6=0
        
        #Extrude
        lshape_wire = Part.makePolygon([Base.Vector(x1, y1, 0), Base.Vector(x2, y2, 0), Base.Vector(x3, y3, 0), Base.Vector(x4, y4, 0), Base.Vector(x5, y5, 0), Base.Vector(x6, y6, 0)])
        L=Part.Face(lshape_wire)
        Clamping=  L.extrude(Base.Vector(0, 0, 1.5))
        Clamping.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 1, 0), 180)
        Clamping.rotate(Base.Vector(0, 0, 0),Base.Vector(1, 0, 0), -90)
        TranslationClamping=(15,-4.25,7.75)
        Clamping.translate(TranslationClamping)
        #Part.show(Clamping)
        fused19=fused18.fuse(Clamping)
        Clamping.rotate(Base.Vector(0, 0, 30),Base.Vector(1, 0, 0), -90)
        #Part.show(Clamping)
        fused20=fused19.fuse(Clamping)
        Clamping.rotate(Base.Vector(0, 0, 30),Base.Vector(1, 0, 0), -90)
        #Part.show(Clamping)
        fused21=fused20.fuse(Clamping)
        Clamping.rotate(Base.Vector(0, 0, 30),Base.Vector(1, 0, 0), -90)
        #Part.show(Clamping)
        fused22=fused21.fuse(Clamping)
        
        TranslationClamping=(0,0,10)
        Clamping.translate(TranslationClamping)
        #Part.show(Clamping)
        fused23=fused22.fuse(Clamping)
        Clamping.rotate(Base.Vector(0, 0, 30),Base.Vector(1, 0, 0), -90)
        #Part.show(Clamping)
        fused24=fused23.fuse(Clamping)
        Clamping.rotate(Base.Vector(0, 0, 30),Base.Vector(1, 0, 0), -90)
        #Part.show(Clamping)
        fused25=fused24.fuse(Clamping)
        Clamping.rotate(Base.Vector(0, 0, 30),Base.Vector(1, 0, 0), -90)
        #Part.show(Clamping)
        fused26=fused25.fuse(Clamping)
        fused26.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 1, 0), 90)
        AssemblyTranslation=(-30,0,0)
        fused26.translate(AssemblyTranslation)
        
        #chamferinnerring
        Holder4=FreeCAD.ActiveDocument.addObject("Part::Feature", "myHolder4")
        Holder4.Shape=fused26
        Holder4.Shape=Holder4.Shape.removeSplitter()
        
        chmfr = FreeCAD.ActiveDocument.addObject("Part::Chamfer", "DOE_Holder1")
        chmfr.Base = FreeCAD.ActiveDocument.myHolder4
        myEdges = []
        

        myEdges.append((2, 1.74, 1.74))# (edge number, chamfer start length, chamfer end length)
        myEdges.append((144, 1.74, 1.74))
        myEdges.append((170, 1.74, 1.74))
        myEdges.append((184, 1.74, 1.74))
        myEdges.append((209, 1.74, 1.74))
        myEdges.append((223, 1.74, 1.74))
        myEdges.append((248, 1.74, 1.74))
        myEdges.append((270, 1.74, 1.74))
        

        myEdges.append((21, 1.5, 1.5))
        myEdges.append((156, 1.5, 1.5))
        myEdges.append((158, 1.5, 1.5))
        myEdges.append((195, 1.5, 1.5))
        myEdges.append((197, 1.5, 1.5))
        myEdges.append((234, 1.5, 1.5))
        myEdges.append((236, 1.5, 1.5))
        myEdges.append((258, 1.5, 1.5))
        myEdges.append((394, 1.5, 1.5))
        myEdges.append((395, 1.5, 1.5))
        myEdges.append((396, 1.5, 1.5))
        myEdges.append((397, 1.5, 1.5))
        myEdges.append((398, 1.5, 1.5))
        myEdges.append((399, 1.5, 1.5))
        myEdges.append((400, 1.5, 1.5))
        myEdges.append((401, 1.5, 1.5))
        myEdges.append((402, 1.5, 1.5))
        myEdges.append((403, 1.5, 1.5))
        myEdges.append((404, 1.5, 1.5))
        myEdges.append((405, 1.5, 1.5))
        myEdges.append((112, 7.0, 7.0))
        myEdges.append((113, 7.0, 7.0))
        myEdges.append((114, 7.0, 7.0))
        myEdges.append((128, 7.0, 7.0))


        chmfr.Edges = myEdges

        FreeCADGui.ActiveDocument.myHolder4.Visibility = False


        FreeCAD.ActiveDocument.recompute()
   
        chmfr.ViewObject.ShapeColor = (103/204,125/204,0.0)
        ###DOE-Holder1_End############################################################
        ###DOE-Holder3##############################################################
        #Base
        BossExtrude1=Part.makeBox(40,30,2.5)

        #Square Hole
        CutExtrude1=Part.makeBox(Height,Width,2.5)
        TranslationCutExtrude1=(20-Height/2,15-Width/2,0)
        #TranslationCutExtrude1=(17,12,0)
        CutExtrude1.translate(TranslationCutExtrude1)
        PartCutExtrude1=BossExtrude1.cut(CutExtrude1)
        DOEHolder3Translation=(-20,-15,-19.5)
        PartCutExtrude1.translate(DOEHolder3Translation)

        #chamfer
        DOE_Holder_3=FreeCAD.ActiveDocument.addObject("Part::Feature", "DOE_Holder_3")
        DOE_Holder_3.Shape=PartCutExtrude1
        DOE_Holder_3.Shape=DOE_Holder_3.Shape.removeSplitter()

        chmfr = FreeCAD.ActiveDocument.addObject("Part::Chamfer", "DOE_Holder3")
        chmfr.Base = FreeCAD.ActiveDocument.DOE_Holder_3
        myEdges = []

        myEdges.append((1, 2.0, 2.0))# (edge number, chamfer start length, chamfer end length)
        myEdges.append((3, 2.0, 2.0))
        myEdges.append((6, 2.0, 2.0))
        myEdges.append((15, 2.0, 2.0))


        chmfr.Edges = myEdges
        FreeCADGui.ActiveDocument.DOE_Holder_3.Visibility = False

        FreeCAD.ActiveDocument.recompute()
        
        chmfr.ViewObject.ShapeColor = (232/255,113/225,8/225)
        ###DOE-Holder3_End###########################################################
        ###Rod1##################################################################
        #BossExtrude1
        BossExtrude1=Part.makeCylinder(4/2,RodLength)
        #Part.show(BossExtrude1)
        TranslationRod1=(20.5,0,-15)
        BossExtrude1.translate(TranslationRod1)
        
        #Fillets
        Rod1=FreeCAD.ActiveDocument.addObject("Part::Feature", "Rod1")
        Rod1.Shape=BossExtrude1



        FreeCAD.ActiveDocument.addObject("Part::Fillet","MetalRod1")
        FreeCAD.ActiveDocument.MetalRod1.Base = FreeCAD.ActiveDocument.Rod1
        __fillets__ = []
        __fillets__.append((1,0.50,0.50))
        __fillets__.append((3,0.50,0.50))
        FreeCAD.ActiveDocument.MetalRod1.Edges = __fillets__
        del __fillets__

        Rod1.ViewObject.ShapeColor = (0.3,0.3,0.3)
        FreeCADGui.ActiveDocument.Rod1.Visibility = False
        FreeCAD.ActiveDocument.recompute()
        ###Rod1_End###############################################################
        ###Rod2##################################################################
        #BossExtrude1
        BossExtrude1=Part.makeCylinder(4/2,RodLength)
        #Part.show(BossExtrude1)
        TranslationRod2=(-20.5,0,-15)
        BossExtrude1.translate(TranslationRod2)

        #Fillets
        Rod2=FreeCAD.ActiveDocument.addObject("Part::Feature", "Rod2")
        Rod2.Shape=BossExtrude1



        FreeCAD.ActiveDocument.addObject("Part::Fillet","MetalRod2")
        FreeCAD.ActiveDocument.MetalRod2.Base = FreeCAD.ActiveDocument.Rod2
        __fillets__ = []
        __fillets__.append((1,0.50,0.50))
        __fillets__.append((3,0.50,0.50))
        FreeCAD.ActiveDocument.MetalRod2.Edges = __fillets__
        del __fillets__

        Rod2.ViewObject.ShapeColor = (0.3,0.3,0.3)
        FreeCADGui.ActiveDocument.Rod2.Visibility = False
        FreeCAD.ActiveDocument.recompute()
        ###Rod2_End###############################################################
        ###Rod3##################################################################
        #BossExtrude1
        BossExtrude1=Part.makeCylinder(4/2,RodLength)
        #Part.show(BossExtrude1)
        TranslationRod3=(0,20.5,-15)
        BossExtrude1.translate(TranslationRod3)

        #Fillets
        Rod3=FreeCAD.ActiveDocument.addObject("Part::Feature", "Rod3")
        Rod3.Shape=BossExtrude1

        

        FreeCAD.ActiveDocument.addObject("Part::Fillet","MetalRod3")
        FreeCAD.ActiveDocument.MetalRod3.Base = FreeCAD.ActiveDocument.Rod3
        __fillets__ = []
        __fillets__.append((1,0.50,0.50))
        __fillets__.append((3,0.50,0.50))
        FreeCAD.ActiveDocument.MetalRod3.Edges = __fillets__
        del __fillets__

        Rod3.ViewObject.ShapeColor = (0.3,0.3,0.3)
        FreeCADGui.ActiveDocument.Rod3.Visibility = False
        FreeCAD.ActiveDocument.recompute()
        ###Rod3_End###############################################################
        ###Rod4##################################################################
        #BossExtrude1
        BossExtrude1=Part.makeCylinder(4/2,RodLength)
        #Part.show(BossExtrude1)
        TranslationRod4=(0,-20.5,-15)
        BossExtrude1.translate(TranslationRod4)

        #Fillets
        Rod4=FreeCAD.ActiveDocument.addObject("Part::Feature", "Rod4")
        Rod4.Shape=BossExtrude1



        FreeCAD.ActiveDocument.addObject("Part::Fillet","MetalRod4")
        FreeCAD.ActiveDocument.MetalRod4.Base = FreeCAD.ActiveDocument.Rod4
        __fillets__ = []
        __fillets__.append((1,0.50,0.50))
        __fillets__.append((3,0.50,0.50))
        FreeCAD.ActiveDocument.MetalRod4.Edges = __fillets__
        del __fillets__

        Rod4.ViewObject.ShapeColor = (0.3,0.3,0.3)
        FreeCADGui.ActiveDocument.Rod4.Visibility = False
        FreeCAD.ActiveDocument.recompute()
        ###Rod4_End###############################################################
        ###Lens-Holder#############################################################
        if LensBin==1:
            #Definition
            #DL=16.2
            ##DL=8.9*2
            #DSA=106/15*DL-431/5
            #DSA=106/15*LHD-431/5+1+14+4+(LHD-16.2)*2
            #DSA=106/15*LHD-431/5
            #DSA=47.28+(LHD-16.2)*8
            DSA=6.1*DL-58.6
            DSI=DSA-5
            #MM=4*DL-42
            #MM=4*LHD-42+7+2+(LHD-16.2)/2*2
            #MM=4*LHD-42
            #MM=31.8+(LHD-16.2)*4.25
            MM=3.5*DL-27.8
            ##Thickness=8
            #HoleTolerance=0
            #RectangleTolerance=0
            #ToleranceNubble=0


	        
            #OuterRing
            BossExtrude1=Part.makeCylinder(40/2,Thickness)
            CutExtrude1=Part.makeCylinder(33/2,Thickness)
            PartBossExtrude1=BossExtrude1.cut(CutExtrude1)
	        
	        
            #InnerRing
            #BossExtrude2=Part.makeCylinder((DL+5)/2,Thickness)
            #CutExtrude2=Part.makeCylinder(DL/2,Thickness)
            #PartBossExtrude2=BossExtrude2.cut(CutExtrude2)

            #InnerRing
            if DL>=14:
                BossExtrude2=Part.makeCylinder((DL+5)/2,Thickness)
                CutExtrude2=Part.makeCylinder(DL/2,Thickness)
                PartBossExtrude2=BossExtrude2.cut(CutExtrude2)
            elif DL<14:
                BossExtrude2=Part.makeCylinder((DL+5+14-DL)/2,Thickness)
                CutExtrude2=Part.makeCylinder(DL/2,Thickness)
                PartBossExtrude2=BossExtrude2.cut(CutExtrude2)
        	        
        	
            #CutsInnerRing
            x1=0
            y1=0
            x2=(DL+4)*math.sin((20)*2*pi/360)
            y2=DL+4
            x3=-(DL+4)*math.sin((20)*2*pi/360)
            y3=DL+4
            x4=0
            y4=0
    	        
	        
            #lshape_wire = Part.makePolygon([Base.Vector(x1, y1, 0), Base.Vector(x2, y2, 0), Base.Vector(x3, y3, 0), Base.Vector(x4, y4, 0), Base.Vector(x5, y5, 0), Base.Vector(x6, y6, 0)])
            lshape_wire = Part.makePolygon([Base.Vector(x1, y1, 0), Base.Vector(x2, y2, 0), Base.Vector(x3, y3, 0), Base.Vector(x4, y4, 0)])
            L=Part.Face(lshape_wire)
            K1 = L.extrude(Base.Vector(0, 0, Thickness))
            K2 = L.extrude(Base.Vector(0, 0, Thickness))
            K3 = L.extrude(Base.Vector(0, 0, Thickness))
            K4 = L.extrude(Base.Vector(0, 0, Thickness))
            K1.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), -45)
            K2.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 45)
            K3.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 225)
            K4.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 135)
            C1=PartBossExtrude2.cut(K1)
            C2=C1.cut(K2)
            C3=C2.cut(K3)
            C4=C3.cut(K4)
        	        
	
            #SpringElements
            #BossExtrude3=Part.makeCylinder(DSA/2,Thickness)
            #CutExtrude3=Part.makeCylinder(DSI/2,Thickness)
            #PartBossExtrude3=BossExtrude3.cut(CutExtrude3)
            #TranslationPartBossExtrude3=(MM,0,0)
            #PartBossExtrude3.translate(TranslationPartBossExtrude3)
            #BossExtrude4=Part.makeCylinder(DSA*2,Thickness)
            #CutExtrude4=Part.makeCylinder(36/2,Thickness)
            #PartBossExtrude4=BossExtrude4.cut(CutExtrude4)




            if DL>=14:
                #SpringElements
                BossExtrude3=Part.makeCylinder(DSA/2,Thickness)
                CutExtrude3=Part.makeCylinder(DSI/2,Thickness)
                PartBossExtrude3=BossExtrude3.cut(CutExtrude3)
                TranslationPartBossExtrude3=(MM,0,0)
                PartBossExtrude3.translate(TranslationPartBossExtrude3)
                BossExtrude4=Part.makeCylinder(DSA*2,Thickness)
                CutExtrude4=Part.makeCylinder(36/2,Thickness)
                PartBossExtrude4=BossExtrude4.cut(CutExtrude4)

            elif DL<14:
                #SpringElements
                BossExtrude3=Part.makeCylinder(26.8/2,Thickness)
                CutExtrude3=Part.makeCylinder(21.8/2,Thickness)
                PartBossExtrude3=BossExtrude3.cut(CutExtrude3)
                TranslationPartBossExtrude3=(21.2,0,0)
                PartBossExtrude3.translate(TranslationPartBossExtrude3)
                BossExtrude4=Part.makeCylinder(26.8*2,Thickness)
                CutExtrude4=Part.makeCylinder(36/2,Thickness)
                PartBossExtrude4=BossExtrude4.cut(CutExtrude4)




	        
	
            #UnionParts
            fused1 = PartBossExtrude1.fuse(C4)
            

            PartBossExtrude5=PartBossExtrude3.cut(PartBossExtrude4)
            #Part.show(PartBossExtrude5)
            fused2= fused1.fuse(PartBossExtrude5)
            PartBossExtrude5.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 90)
            #Part.show(PartBossExtrude5)
            fused3= fused2.fuse(PartBossExtrude5)
            PartBossExtrude5.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 180)
            #Part.show(PartBossExtrude5)
            fused4= fused3.fuse(PartBossExtrude5)
            PartBossExtrude5.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 270)
            #Part.show(PartBossExtrude5)
            fused5= fused4.fuse(PartBossExtrude5)
        

            #OuterRingSquares
            Square=Part.makeBox(5.13,15,Thickness)
            TranslationSquare=(17.37,-15/2,0)
            Square.translate(TranslationSquare)
            #Part.show(Square)
            
        	
            #CutoutsOuterRingSquares1
            Hole=Part.makeCylinder(2.1,Thickness)
            TranslationHole=(20.5,0,0)
            Hole.translate(TranslationHole)
            PartCutout=Square.cut(Hole)
            fused6=fused5.cut(Hole)
    
            Rectangle=Part.makeBox(0.69+0.5,3.2,Thickness)
            TranslationRectangle=(21.81-0.25,-3.2/2,0)
            Rectangle.translate(TranslationRectangle)
            PartCut=PartCutout.cut(Rectangle)
            fused7= fused6.fuse(PartCut)
            
            #CutoutsOuterRingSquares2
            PartCut.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 90)
            Hole.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 90)
            fused8=fused7.fuse(PartCut)
            fused9=fused8.cut(Hole)
    
        	
            #CutoutsOuterRingSquares3
            PartCut.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 180)
            Hole.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 180)
            fused10=fused9.fuse(PartCut)
            fused11=fused10.cut(Hole)
            
	
            #CutoutsOuterRingSquares4
            PartCut.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 270)
            Hole.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 270)
            fused12=fused11.fuse(PartCut)
            fused13=fused12.cut(Hole)
            #Part.show(fused13)

	
	

            #Outer Polygon
            #x1=18+2.75/(math.tan((30)*2*pi/360))
            x1=22.7
            y1=-5
            #x2=18+2.75/(math.tan((30)*2*pi/360))
            x2=22.7
            y2=5
            x3=18
            y3=5
            x4=18
            y4=-5
            #x5=18+2.75/(math.tan((30)*2*pi/360))
            x5=22.7
            y5=-5


            lshape_wire = Part.makePolygon([Base.Vector(x1, y1, 0), Base.Vector(x2, y2, 0), Base.Vector(x3, y3, 0), Base.Vector(x4, y4, 0), Base.Vector(x5, y5, 0)])
            L=Part.Face(lshape_wire)
            K1 = L.extrude(Base.Vector(0, 0, Thickness))
            K2 = L.extrude(Base.Vector(0, 0, Thickness))
            K3 = L.extrude(Base.Vector(0, 0, Thickness))
            K4 = L.extrude(Base.Vector(0, 0, Thickness))
            K1.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), -45)
            K2.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 45)
            K3.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 225)
            K4.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 135)
    
            fused14=fused13.fuse(K1)
            fused15=fused14.fuse(K2)
            fused16=fused15.fuse(K3)
            fused17=fused16.fuse(K4)
            #Part.show(fused17)
       
            #TranslationLensHolder=(0,0,69	
            TranslationLensHolder=(0,0,83-DLL)
            fused17.translate(TranslationLensHolder)
            #Part.show(fused17)
    


      
            #chamferinnerring
            Holder1=FreeCAD.ActiveDocument.addObject("Part::Feature", "myHolder1")
            Holder1.Shape=fused17
            Holder1.Shape=Holder1.Shape.removeSplitter()
          

            FreeCAD.ActiveDocument.addObject("Part::Fillet","LensHolder1")
            FreeCAD.ActiveDocument.LensHolder1.Base = FreeCAD.ActiveDocument.myHolder1
            __fillets__ = []
            __fillets__.append((184,0.50,0.50))
            __fillets__.append((185,0.50,0.50))
            __fillets__.append((197,0.50,0.50))
            __fillets__.append((198,0.50,0.50))
            __fillets__.append((221,0.50,0.50))
            __fillets__.append((222,0.50,0.50))
            __fillets__.append((209,0.50,0.50))
            __fillets__.append((210,0.50,0.50))
            FreeCAD.ActiveDocument.LensHolder1.Edges = __fillets__
            del __fillets__
            FreeCADGui.ActiveDocument.myHolder1.Visibility = False



            chmfr = FreeCAD.ActiveDocument.addObject("Part::Chamfer", "LensHolder")
            #chmfr.Base = FreeCAD.ActiveDocument.myHolder4
            chmfr.Base = FreeCAD.ActiveDocument.LensHolder1
            myEdges = []


            myEdges.append((9, 1.0, 1.0))# (edge number, chamfer start length, chamfer end length)
            myEdges.append((10, 1.0, 1.0))
            myEdges.append((25, 1.0, 1.0))
            myEdges.append((26, 1.0, 1.0))
            myEdges.append((115, 1.0, 1.0))
            myEdges.append((116, 1.0, 1.0))
            myEdges.append((118, 1.0, 1.0))
            myEdges.append((147, 1.0, 1.0))
            myEdges.append((150, 1.0, 1.0))
            myEdges.append((38, 1.0, 1.0))
            myEdges.append((39, 1.0, 1.0))
            myEdges.append((40, 1.0, 1.0))
            myEdges.append((41, 1.0, 1.0))
            myEdges.append((42, 1.0, 1.0))
            myEdges.append((52, 1.0, 1.0))
            myEdges.append((53, 1.0, 1.0))
            myEdges.append((54, 1.0, 1.0))
            myEdges.append((55, 1.0, 1.0))
            myEdges.append((56, 1.0, 1.0))
            myEdges.append((66, 1.0, 1.0))
            myEdges.append((67, 1.0, 1.0))
            myEdges.append((68, 1.0, 1.0))
            myEdges.append((69, 1.0, 1.0))
            myEdges.append((70, 1.0, 1.0))
            myEdges.append((80, 1.0, 1.0))
            myEdges.append((81, 1.0, 1.0))
            myEdges.append((82, 1.0, 1.0))
            myEdges.append((83, 1.0, 1.0))
            myEdges.append((84, 1.0, 1.0))
            myEdges.append((173, 1.0, 1.0))
            myEdges.append((176, 1.0, 1.0))
            myEdges.append((177, 1.0, 1.0))
            myEdges.append((178, 1.0, 1.0))
            myEdges.append((180, 1.0, 1.0))
            myEdges.append((199, 1.0, 1.0))
            myEdges.append((202, 1.0, 1.0))
            myEdges.append((203, 1.0, 1.0))
            myEdges.append((204, 1.0, 1.0))
            myEdges.append((206, 1.0, 1.0))
            myEdges.append((225, 1.0, 1.0))
            myEdges.append((228, 1.0, 1.0))
            myEdges.append((229, 1.0, 1.0))
            myEdges.append((230, 1.0, 1.0))
            myEdges.append((232, 1.0, 1.0))
            myEdges.append((251, 1.0, 1.0))
            myEdges.append((254, 1.0, 1.0))
            myEdges.append((255, 1.0, 1.0))
            myEdges.append((256, 1.0, 1.0))
            myEdges.append((258, 1.0, 1.0))
            myEdges.append((169, 2.0, 2.0))
            myEdges.append((182, 2.0, 2.0))
            myEdges.append((195, 2.0, 2.0))
            myEdges.append((208, 2.0, 2.0))
            myEdges.append((221, 2.0, 2.0))
            myEdges.append((234, 2.0, 2.0))
            myEdges.append((247, 2.0, 2.0))
            myEdges.append((260, 2.0, 2.0))

            chmfr.Edges = myEdges
        
            FreeCADGui.ActiveDocument.LensHolder1.Visibility = False
        
        
            FreeCAD.ActiveDocument.recompute()
                
            #Holder4.ViewObject.ShapeColor = (103/204,125/204,204/204)
            chmfr.ViewObject.ShapeColor = (103/204,125/204,0.0)
        
        else:
            print("no Lens")
        ###Lens-Holder_End##########################################################
        ###Lens#################################################################
        if LensBin==1:
            #init
            #d=2*8.0
            R=2*DL/2
        
            sphere = Part.makeSphere(R)
            cube = Part.makeBox(2*R,2*R,2*R)
            x=math.cos(math.asin((DL/2)/(R)))*R
            translation = (-x,-R,-R)
            cube.translate(translation)
            PartCutExtrude1=sphere.cut(cube)
            #Part.show(PartCutExtrude1)

            Cylinder=Part.makeCylinder(DL/2,DL/10)
            Cylinder.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 1, 0), 90)
            translationCylinder = (-x,0,0)
            Cylinder.translate(translationCylinder)
            #Part.show(Cylinder)


            sphere2 = Part.makeSphere(R)
            cube2 = Part.makeBox(2*R,2*R,2*R)
            x2=math.cos(math.asin((DL/2)/(R)))*R
            translation2 = (-2*R+x2,-R,-R)
            cube2.translate(translation2)
            PartCutExtrude2=sphere2.cut(cube2)
            translation3=(-2*x+DL/10,0,0)
            PartCutExtrude2.translate(translation3)
            #Part.show(PartCutExtrude2)

            fused1=PartCutExtrude1.fuse(Cylinder)
            fused2=fused1.fuse(PartCutExtrude2)
            #Part.show(fused2)
            fused2.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 1, 0), -90)
            #TranslationLens=(0,0,84.75+DL-16)
            #TranslationLens=(0,0,84.75+DL-2-DLL)
            TranslationLens=(0,0,84.75+DL-1-0.1*DL-DLL)
            fused2.translate(TranslationLens)

            #Display
            Lens = FreeCAD.ActiveDocument.addObject("Part::Feature", "Lens")
            Lens.Shape=fused2
            Lens.Shape=Lens.Shape.removeSplitter()
            Lens.ViewObject.ShapeColor = (152/255,245/255,255/255)
            Lens.ViewObject.Transparency=50

        else:
            print("no Lens")
        ###Lens_End##############################################################
        ###Laser-Holder1############################################################
        #Definition
        #DL=16.2
        ##LHD=7.9*2
        #DSA=106/15*DL-431/5
        #DSA=106/15*LHD-431/5+1+14+4+(LHD-16.2)*2
        #DSA=106/15*LHD-431/5
        #DSA=47.28+(LHD-16.2)*8
        DSA=6.1*LHD-58.6
        DSI=DSA-5
        #MM=4*DL-42
        #MM=4*LHD-42+7+2+(LHD-16.2)/2*2
        #MM=4*LHD-42
        #MM=31.8+(LHD-16.2)*4.25
        MM=3.5*LHD-27.8
        #HoleTolerance=0
        #RectangleTolerance=0
        #ToleranceNubble=0
        

	        
        #OuterRing
        BossExtrude1=Part.makeCylinder(40/2,15)
        CutExtrude1=Part.makeCylinder(33/2,15)
        PartBossExtrude1=BossExtrude1.cut(CutExtrude1)
	        
	        
        #InnerRing

        if LHD >=14:
            BossExtrude2=Part.makeCylinder((LHD+5)/2,15)
            CutExtrude2=Part.makeCylinder(LHD/2,15)
            PartBossExtrude2=BossExtrude2.cut(CutExtrude2)
        elif LHD<14:
            BossExtrude2=Part.makeCylinder((LHD+5+14-LHD)/2,15)
            CutExtrude2=Part.makeCylinder(LHD/2,15)
            PartBossExtrude2=BossExtrude2.cut(CutExtrude2)
	        
	
        #CutsInnerRing
        x1=0
        y1=0
        x2=(LHD+4)*math.sin((20)*2*pi/360)
        y2=LHD+4
        x3=-(LHD+4)*math.sin((20)*2*pi/360)
        y3=LHD+4
        x4=0
        y4=0
	        
	        
        #lshape_wire = Part.makePolygon([Base.Vector(x1, y1, 0), Base.Vector(x2, y2, 0), Base.Vector(x3, y3, 0), Base.Vector(x4, y4, 0), Base.Vector(x5, y5, 0), Base.Vector(x6, y6, 0)])
        lshape_wire = Part.makePolygon([Base.Vector(x1, y1, 0), Base.Vector(x2, y2, 0), Base.Vector(x3, y3, 0), Base.Vector(x4, y4, 0)])
        L=Part.Face(lshape_wire)
        K1 = L.extrude(Base.Vector(0, 0, 15))
        K2 = L.extrude(Base.Vector(0, 0, 15))
        K3 = L.extrude(Base.Vector(0, 0, 15))
        K4 = L.extrude(Base.Vector(0, 0, 15))
        K1.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), -45)
        K2.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 45)
        K3.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 225)
        K4.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 135)
        C1=PartBossExtrude2.cut(K1)
        C2=C1.cut(K2)
        C3=C2.cut(K3)
        C4=C3.cut(K4)
	        
	
        if LHD>=14:
            #SpringElements
            BossExtrude3=Part.makeCylinder(DSA/2,15)
            CutExtrude3=Part.makeCylinder(DSI/2,15)
            PartBossExtrude3=BossExtrude3.cut(CutExtrude3)
            TranslationPartBossExtrude3=(MM,0,0)
            PartBossExtrude3.translate(TranslationPartBossExtrude3)
            BossExtrude4=Part.makeCylinder(DSA*2,15)
            CutExtrude4=Part.makeCylinder(36/2,15)
            PartBossExtrude4=BossExtrude4.cut(CutExtrude4)

        elif LHD<14:
            #SpringElements
            BossExtrude3=Part.makeCylinder(26.8/2,15)
            CutExtrude3=Part.makeCylinder(21.8/2,15)
            PartBossExtrude3=BossExtrude3.cut(CutExtrude3)
            TranslationPartBossExtrude3=(21.2,0,0)
            PartBossExtrude3.translate(TranslationPartBossExtrude3)
            BossExtrude4=Part.makeCylinder(26.8*2,15)
            CutExtrude4=Part.makeCylinder(36/2,15)
            PartBossExtrude4=BossExtrude4.cut(CutExtrude4)
	        
	
        #UnionParts
        fused1 = PartBossExtrude1.fuse(C4)
        

        PartBossExtrude5=PartBossExtrude3.cut(PartBossExtrude4)
        #Part.show(PartBossExtrude5)
        fused2= fused1.fuse(PartBossExtrude5)
        PartBossExtrude5.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 90)
        #Part.show(PartBossExtrude5)
        fused3= fused2.fuse(PartBossExtrude5)
        PartBossExtrude5.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 180)
        #Part.show(PartBossExtrude5)
        fused4= fused3.fuse(PartBossExtrude5)
        PartBossExtrude5.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 270)
        #Part.show(PartBossExtrude5)
        fused5= fused4.fuse(PartBossExtrude5)


        #OuterRingSquares
        Square=Part.makeBox(5.13,15,15)
        TranslationSquare=(17.37,-15/2,0)
        Square.translate(TranslationSquare)
        #Part.show(Square)

	
        #CutoutsOuterRingSquares1
        Hole=Part.makeCylinder(2.1,15)
        TranslationHole=(20.5,0,0)
        Hole.translate(TranslationHole)
        PartCutout=Square.cut(Hole)
        fused6=fused5.cut(Hole)

        Rectangle=Part.makeBox(0.69+0.5,3.2,15)
        TranslationRectangle=(21.81-0.25,-3.2/2,0)
        Rectangle.translate(TranslationRectangle)
        PartCut=PartCutout.cut(Rectangle)
        fused7= fused6.fuse(PartCut)

        #CutoutsOuterRingSquares2
        PartCut.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 90)
        Hole.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 90)
        fused8=fused7.fuse(PartCut)
        fused9=fused8.cut(Hole)

        	
        #CutoutsOuterRingSquares3
        PartCut.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 180)
        Hole.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 180)
        fused10=fused9.fuse(PartCut)
        fused11=fused10.cut(Hole)
        
	
        #CutoutsOuterRingSquares4
        PartCut.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 270)
        Hole.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 270)
        fused12=fused11.fuse(PartCut)
        fused13=fused12.cut(Hole)
        #Part.show(fused13)

	
	

        #Outer Polygon
        #x1=18+2.75/(math.tan((30)*2*pi/360))
        x1=22.7
        y1=-5
        #x2=18+2.75/(math.tan((30)*2*pi/360))
        x2=22.7
        y2=5
        x3=18
        y3=5
        x4=18
        y4=-5
        #x5=18+2.75/(math.tan((30)*2*pi/360))
        x5=22.7
        y5=-5


        lshape_wire = Part.makePolygon([Base.Vector(x1, y1, 0), Base.Vector(x2, y2, 0), Base.Vector(x3, y3, 0), Base.Vector(x4, y4, 0), Base.Vector(x5, y5, 0)])
        L=Part.Face(lshape_wire)
        K1 = L.extrude(Base.Vector(0, 0, 15))
        K2 = L.extrude(Base.Vector(0, 0, 15))
        K3 = L.extrude(Base.Vector(0, 0, 15))
        K4 = L.extrude(Base.Vector(0, 0, 15))
        K1.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), -45)
        K2.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 45)
        K3.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 225)
        K4.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 135)

        fused14=fused13.fuse(K1)
        fused15=fused14.fuse(K2)
        fused16=fused15.fuse(K3)
        fused17=fused16.fuse(K4)
        #Part.show(fused17)
       
	
        #TranslationHolder2=(0,0,102.5)
        #TranslationHolder2=(0,0,192.5-LL)
        #TranslationHolder2=(0,0,RodLength-7.5-LL)
        TranslationHolder2=(0,0,RodLength-31-LL)
        fused17.translate(TranslationHolder2)
        #Part.show(fused17)



      
        #chamferinnerring
        Holder2=FreeCAD.ActiveDocument.addObject("Part::Feature", "myHolder2")
        Holder2.Shape=fused17
        Holder2.Shape=Holder2.Shape.removeSplitter()
      

        FreeCAD.ActiveDocument.addObject("Part::Fillet","LaserHolder_1")
        FreeCAD.ActiveDocument.LaserHolder_1.Base = FreeCAD.ActiveDocument.myHolder2
        __fillets__ = []
        __fillets__.append((184,0.50,0.50))
        __fillets__.append((185,0.50,0.50))
        __fillets__.append((197,0.50,0.50))
        __fillets__.append((198,0.50,0.50))
        __fillets__.append((221,0.50,0.50))
        __fillets__.append((222,0.50,0.50))
        __fillets__.append((209,0.50,0.50))
        __fillets__.append((210,0.50,0.50))
        FreeCAD.ActiveDocument.LaserHolder_1.Edges = __fillets__
        del __fillets__
        FreeCADGui.ActiveDocument.myHolder2.Visibility = False


        
        chmfr = FreeCAD.ActiveDocument.addObject("Part::Chamfer", "LaserHolder1")
        #chmfr.Base = FreeCAD.ActiveDocument.myHolder4
        chmfr.Base = FreeCAD.ActiveDocument.LaserHolder_1
        myEdges = []
        

        myEdges.append((9, 1.0, 1.0))# (edge number, chamfer start length, chamfer end length)
        myEdges.append((10, 1.0, 1.0))
        myEdges.append((25, 1.0, 1.0))
        myEdges.append((26, 1.0, 1.0))
        myEdges.append((115, 1.0, 1.0))
        myEdges.append((116, 1.0, 1.0))
        myEdges.append((118, 1.0, 1.0))
        myEdges.append((147, 1.0, 1.0))
        myEdges.append((150, 1.0, 1.0))
        myEdges.append((38, 1.0, 1.0))
        myEdges.append((39, 1.0, 1.0))
        myEdges.append((40, 1.0, 1.0))
        myEdges.append((41, 1.0, 1.0))
        myEdges.append((42, 1.0, 1.0))
        myEdges.append((52, 1.0, 1.0))
        myEdges.append((53, 1.0, 1.0))
        myEdges.append((54, 1.0, 1.0))
        myEdges.append((55, 1.0, 1.0))
        myEdges.append((56, 1.0, 1.0))
        myEdges.append((66, 1.0, 1.0))
        myEdges.append((67, 1.0, 1.0))
        myEdges.append((68, 1.0, 1.0))
        myEdges.append((69, 1.0, 1.0))
        myEdges.append((70, 1.0, 1.0))
        myEdges.append((80, 1.0, 1.0))
        myEdges.append((81, 1.0, 1.0))
        myEdges.append((82, 1.0, 1.0))
        myEdges.append((83, 1.0, 1.0))
        myEdges.append((84, 1.0, 1.0))
        myEdges.append((173, 1.0, 1.0))
        myEdges.append((176, 1.0, 1.0))
        myEdges.append((177, 1.0, 1.0))
        myEdges.append((178, 1.0, 1.0))
        myEdges.append((180, 1.0, 1.0))
        myEdges.append((199, 1.0, 1.0))
        myEdges.append((202, 1.0, 1.0))
        myEdges.append((203, 1.0, 1.0))
        myEdges.append((204, 1.0, 1.0))
        myEdges.append((206, 1.0, 1.0))
        myEdges.append((225, 1.0, 1.0))
        myEdges.append((228, 1.0, 1.0))
        myEdges.append((229, 1.0, 1.0))
        myEdges.append((230, 1.0, 1.0))
        myEdges.append((232, 1.0, 1.0))
        myEdges.append((251, 1.0, 1.0))
        myEdges.append((254, 1.0, 1.0))
        myEdges.append((255, 1.0, 1.0))
        myEdges.append((256, 1.0, 1.0))
        myEdges.append((258, 1.0, 1.0))
        myEdges.append((169, 2.0, 2.0))
        myEdges.append((182, 2.0, 2.0))
        myEdges.append((195, 2.0, 2.0))
        myEdges.append((208, 2.0, 2.0))
        myEdges.append((221, 2.0, 2.0))
        myEdges.append((234, 2.0, 2.0))
        myEdges.append((247, 2.0, 2.0))
        myEdges.append((260, 2.0, 2.0))

        chmfr.Edges = myEdges

        FreeCADGui.ActiveDocument.LaserHolder_1.Visibility = False


        FreeCAD.ActiveDocument.recompute()
        
        #Holder4.ViewObject.ShapeColor = (103/204,125/204,204/204)
        chmfr.ViewObject.ShapeColor = (103/204,125/204,0.0)

        ###Laser-Holder1_End#########################################################
        
        ###Laser-Holder2############################################################
        #Definition
        #DL=16.2
        ##LHD=7.9*2
        #DSA=106/15*DL-431/5
        #DSA=106/15*LHD-431/5+1+14+4+(LHD-16.2)*2
        #DSA=106/15*LHD-431/5
        #DSA=47.28+(LHD-16.2)*8
        DSA=6.1*LHD-58.6
        DSI=DSA-5
        #MM=4*DL-42
        #MM=4*LHD-42+7+2+(LHD-16.2)/2*2
        #MM=4*LHD-42
        #MM=31.8+(LHD-16.2)*4.25
        MM=3.5*LHD-27.8
        #HoleTolerance=0
        #RectangleTolerance=0
        #ToleranceNubble=0


	        
        #OuterRing
        BossExtrude1=Part.makeCylinder(40/2,15)
        CutExtrude1=Part.makeCylinder(33/2,15)
        PartBossExtrude1=BossExtrude1.cut(CutExtrude1)
	        
	        

        #InnerRing
        if LHD >=14:
            BossExtrude2=Part.makeCylinder((LHD+5)/2,15)
            CutExtrude2=Part.makeCylinder(LHD/2,15)
            PartBossExtrude2=BossExtrude2.cut(CutExtrude2)
        elif LHD<14:
            BossExtrude2=Part.makeCylinder((LHD+5+14-LHD)/2,15)
            CutExtrude2=Part.makeCylinder(LHD/2,15)
            PartBossExtrude2=BossExtrude2.cut(CutExtrude2)
	        
	
        #CutsInnerRing
        x1=0
        y1=0
        x2=(LHD+4)*math.sin((20)*2*pi/360)
        y2=LHD+4
        x3=-(LHD+4)*math.sin((20)*2*pi/360)
        y3=LHD+4
        x4=0
        y4=0
	        
	        
        #lshape_wire = Part.makePolygon([Base.Vector(x1, y1, 0), Base.Vector(x2, y2, 0), Base.Vector(x3, y3, 0), Base.Vector(x4, y4, 0), Base.Vector(x5, y5, 0), Base.Vector(x6, y6, 0)])
        lshape_wire = Part.makePolygon([Base.Vector(x1, y1, 0), Base.Vector(x2, y2, 0), Base.Vector(x3, y3, 0), Base.Vector(x4, y4, 0)])
        L=Part.Face(lshape_wire)
        K1 = L.extrude(Base.Vector(0, 0, 15))
        K2 = L.extrude(Base.Vector(0, 0, 15))
        K3 = L.extrude(Base.Vector(0, 0, 15))
        K4 = L.extrude(Base.Vector(0, 0, 15))
        K1.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), -45)
        K2.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 45)
        K3.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 225)
        K4.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 135)
        C1=PartBossExtrude2.cut(K1)
        C2=C1.cut(K2)
        C3=C2.cut(K3)
        C4=C3.cut(K4)
	        

        if LHD>=14:
            #SpringElements
            BossExtrude3=Part.makeCylinder(DSA/2,15)
            CutExtrude3=Part.makeCylinder(DSI/2,15)
            PartBossExtrude3=BossExtrude3.cut(CutExtrude3)
            TranslationPartBossExtrude3=(MM,0,0)
            PartBossExtrude3.translate(TranslationPartBossExtrude3)
            BossExtrude4=Part.makeCylinder(DSA*2,15)
            CutExtrude4=Part.makeCylinder(36/2,15)
            PartBossExtrude4=BossExtrude4.cut(CutExtrude4)

        elif LHD<14:
            #SpringElements
            BossExtrude3=Part.makeCylinder(26.8/2,15)
            CutExtrude3=Part.makeCylinder(21.8/2,15)
            PartBossExtrude3=BossExtrude3.cut(CutExtrude3)
            TranslationPartBossExtrude3=(21.2,0,0)
            PartBossExtrude3.translate(TranslationPartBossExtrude3)
            BossExtrude4=Part.makeCylinder(26.8*2,15)
            CutExtrude4=Part.makeCylinder(36/2,15)
            PartBossExtrude4=BossExtrude4.cut(CutExtrude4)
	
	
        #UnionParts
        fused1 = PartBossExtrude1.fuse(C4)
                

        PartBossExtrude5=PartBossExtrude3.cut(PartBossExtrude4)
        #Part.show(PartBossExtrude5)
        fused2= fused1.fuse(PartBossExtrude5)
        PartBossExtrude5.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 90)
        #Part.show(PartBossExtrude5)
        fused3= fused2.fuse(PartBossExtrude5)
        PartBossExtrude5.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 180)
        #Part.show(PartBossExtrude5)
        fused4= fused3.fuse(PartBossExtrude5)
        PartBossExtrude5.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 270)
        #Part.show(PartBossExtrude5)
        fused5= fused4.fuse(PartBossExtrude5)


        #OuterRingSquares
        Square=Part.makeBox(5.13,15,15)
        TranslationSquare=(17.37,-15/2,0)
        Square.translate(TranslationSquare)
        #Part.show(Square)

	
        #CutoutsOuterRingSquares1
        Hole=Part.makeCylinder(2.1,15)
        TranslationHole=(20.5,0,0)
        Hole.translate(TranslationHole)
        PartCutout=Square.cut(Hole)
        fused6=fused5.cut(Hole)

        Rectangle=Part.makeBox(0.69+0.5,3.2,15)
        TranslationRectangle=(21.81-0.25,-3.2/2,0)
        Rectangle.translate(TranslationRectangle)
        PartCut=PartCutout.cut(Rectangle)
        fused7= fused6.fuse(PartCut)

        #CutoutsOuterRingSquares2
        PartCut.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 90)
        Hole.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 90)
        fused8=fused7.fuse(PartCut)
        fused9=fused8.cut(Hole)

	
        #CutoutsOuterRingSquares3
        PartCut.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 180)
        Hole.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 180)
        fused10=fused9.fuse(PartCut)
        fused11=fused10.cut(Hole)
        
	
        #CutoutsOuterRingSquares4
        PartCut.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 270)
        Hole.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 270)
        fused12=fused11.fuse(PartCut)
        fused13=fused12.cut(Hole)
        #Part.show(fused13)

	
	

        #Outer Polygon
        #x1=18+2.75/(math.tan((30)*2*pi/360))
        x1=22.7
        y1=-5
        #x2=18+2.75/(math.tan((30)*2*pi/360))
        x2=22.7
        y2=5
        x3=18
        y3=5
        x4=18
        y4=-5
        x5=22.7
        #x5=18+2.75/(math.tan((30)*2*pi/360))
        y5=-5


        lshape_wire = Part.makePolygon([Base.Vector(x1, y1, 0), Base.Vector(x2, y2, 0), Base.Vector(x3, y3, 0), Base.Vector(x4, y4, 0), Base.Vector(x5, y5, 0)])
        L=Part.Face(lshape_wire)
        K1 = L.extrude(Base.Vector(0, 0, 15))
        K2 = L.extrude(Base.Vector(0, 0, 15))
        K3 = L.extrude(Base.Vector(0, 0, 15))
        K4 = L.extrude(Base.Vector(0, 0, 15))
        K1.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), -45)
        K2.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 45)
        K3.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 225)
        K4.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 135)

        fused14=fused13.fuse(K1)
        fused15=fused14.fuse(K2)
        fused16=fused15.fuse(K3)
        fused17=fused16.fuse(K4)
        #Part.show(fused17)
       
	
        TranslationHolder3=(0,0,RodLength-37.5)
        fused17.translate(TranslationHolder3)
        #Part.show(fused17)
        


      
        #chamferinnerring
        Holder3=FreeCAD.ActiveDocument.addObject("Part::Feature", "myHolder3")
        Holder3.Shape=fused17
        Holder3.Shape=Holder3.Shape.removeSplitter()
      

        FreeCAD.ActiveDocument.addObject("Part::Fillet","LaserHolder_2")
        FreeCAD.ActiveDocument.LaserHolder_2.Base = FreeCAD.ActiveDocument.myHolder3
        __fillets__ = []
        __fillets__.append((184,0.50,0.50))
        __fillets__.append((185,0.50,0.50))
        __fillets__.append((197,0.50,0.50))
        __fillets__.append((198,0.50,0.50))
        __fillets__.append((221,0.50,0.50))
        __fillets__.append((222,0.50,0.50))
        __fillets__.append((209,0.50,0.50))
        __fillets__.append((210,0.50,0.50))
        FreeCAD.ActiveDocument.LaserHolder_2.Edges = __fillets__
        del __fillets__
        FreeCADGui.ActiveDocument.myHolder3.Visibility = False



        chmfr = FreeCAD.ActiveDocument.addObject("Part::Chamfer", "LaserHolder2")
        #chmfr.Base = FreeCAD.ActiveDocument.myHolder4
        chmfr.Base = FreeCAD.ActiveDocument.LaserHolder_2
        myEdges = []


        myEdges.append((9, 1.0, 1.0))# (edge number, chamfer start length, chamfer end length)
        myEdges.append((10, 1.0, 1.0))
        myEdges.append((25, 1.0, 1.0))
        myEdges.append((26, 1.0, 1.0))
        myEdges.append((115, 1.0, 1.0))
        myEdges.append((116, 1.0, 1.0))
        myEdges.append((118, 1.0, 1.0))
        myEdges.append((147, 1.0, 1.0))
        myEdges.append((150, 1.0, 1.0))
        myEdges.append((38, 1.0, 1.0))
        myEdges.append((39, 1.0, 1.0))
        myEdges.append((40, 1.0, 1.0))
        myEdges.append((41, 1.0, 1.0))
        myEdges.append((42, 1.0, 1.0))
        myEdges.append((52, 1.0, 1.0))
        myEdges.append((53, 1.0, 1.0))
        myEdges.append((54, 1.0, 1.0))
        myEdges.append((55, 1.0, 1.0))
        myEdges.append((56, 1.0, 1.0))
        myEdges.append((66, 1.0, 1.0))
        myEdges.append((67, 1.0, 1.0))
        myEdges.append((68, 1.0, 1.0))
        myEdges.append((69, 1.0, 1.0))
        myEdges.append((70, 1.0, 1.0))
        myEdges.append((80, 1.0, 1.0))
        myEdges.append((81, 1.0, 1.0))
        myEdges.append((82, 1.0, 1.0))
        myEdges.append((83, 1.0, 1.0))
        myEdges.append((84, 1.0, 1.0))
        myEdges.append((173, 1.0, 1.0))
        myEdges.append((176, 1.0, 1.0))
        myEdges.append((177, 1.0, 1.0))
        myEdges.append((178, 1.0, 1.0))
        myEdges.append((180, 1.0, 1.0))
        myEdges.append((199, 1.0, 1.0))
        myEdges.append((202, 1.0, 1.0))
        myEdges.append((203, 1.0, 1.0))
        myEdges.append((204, 1.0, 1.0))
        myEdges.append((206, 1.0, 1.0))
        myEdges.append((225, 1.0, 1.0))
        myEdges.append((228, 1.0, 1.0))
        myEdges.append((229, 1.0, 1.0))
        myEdges.append((230, 1.0, 1.0))
        myEdges.append((232, 1.0, 1.0))
        myEdges.append((251, 1.0, 1.0))
        myEdges.append((254, 1.0, 1.0))
        myEdges.append((255, 1.0, 1.0))
        myEdges.append((256, 1.0, 1.0))
        myEdges.append((258, 1.0, 1.0))
        myEdges.append((169, 2.0, 2.0))
        myEdges.append((182, 2.0, 2.0))
        myEdges.append((195, 2.0, 2.0))
        myEdges.append((208, 2.0, 2.0))
        myEdges.append((221, 2.0, 2.0))
        myEdges.append((234, 2.0, 2.0))
        myEdges.append((247, 2.0, 2.0))
        myEdges.append((260, 2.0, 2.0))
        
        chmfr.Edges = myEdges

        FreeCADGui.ActiveDocument.LaserHolder_2.Visibility = False


        FreeCAD.ActiveDocument.recompute()
        
        #Holder4.ViewObject.ShapeColor = (103/204,125/204,204/204)
        chmfr.ViewObject.ShapeColor = (103/204,125/204,0.0)
        ###Laser-Holder2_End##########################################################
        
        ###Laser##################################################################
        #Cylinder
        BossExtrude1=Part.makeCylinder(LHD/2,LL)


        #Cutouts
        BossExtrude2=Part.makeCylinder((LHD+1)/2,1.84)
        CutExtrude1=Part.makeCylinder((LHD-2)/2,1.84)
        PartBossExtrude1=BossExtrude2.cut(CutExtrude1)
        TranslationPartBossExtrude1=(0,0,LL-14.7)
        PartBossExtrude1.translate(TranslationPartBossExtrude1)
        BossExtrude2=BossExtrude1.cut(PartBossExtrude1)

        TranslationPartBossExtrude2=(0,0,1.84*2)
        PartBossExtrude1.translate(TranslationPartBossExtrude2)
        BossExtrude3=BossExtrude2.cut(PartBossExtrude1)

        PartBossExtrude1.translate(TranslationPartBossExtrude2)
        BossExtrude4=BossExtrude3.cut(PartBossExtrude1)

        PartBossExtrude1.translate(TranslationPartBossExtrude2)
        BossExtrude5=BossExtrude4.cut(PartBossExtrude1)

        #Part.show(BossExtrude5)

        #Drillings
        Drilling1=Part.makeCylinder(3/2,3)
        TranslationDrilling1=(0,0,LL-3)
        Drilling1.translate(TranslationDrilling1)
        #Part.show(Drilling1)
        BossExtrude6=BossExtrude5.cut(Drilling1)

        Drilling2=Part.makeCylinder(1.6/2,5)
        TranslationDrilling2=(1.6,0,0)
        Drilling2.translate(TranslationDrilling2)
        #Part.show(Drilling2)
        BossExtrude7=BossExtrude6.cut(Drilling2)

        TranslationDrilling2=(-3.2,0,0)
        Drilling2.translate(TranslationDrilling2)
        #Part.show(Drilling2)
        BossExtrude8=BossExtrude7.cut(Drilling2)

        BossExtrude8.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 1, 0), 180)
        TranslationLaser=(0,0,RodLength-22.5)
        BossExtrude8.translate(TranslationLaser)



        #chamfer
        laser=FreeCAD.ActiveDocument.addObject("Part::Feature", "laser")
        laser.Shape=BossExtrude8
        laser.Shape=laser.Shape.removeSplitter()

        chmfr = FreeCAD.ActiveDocument.addObject("Part::Chamfer", "Laser")
        chmfr.Base = FreeCAD.ActiveDocument.laser
        myEdges = []
        
        myEdges.append((13, 0.5, 0.5))# (edge number, chamfer start length, chamfer end length)
        myEdges.append((33, 0.5, 0.5))


        chmfr.Edges = myEdges
        FreeCADGui.ActiveDocument.laser.Visibility = False

        FreeCAD.ActiveDocument.recompute()
        
        chmfr.ViewObject.ShapeColor = (0.3,0.3,0.3)
        ###Laser_End###############################################################
        ###Cap###################################################################

        #make sketch
        x1=-23
        y1=-30
        x2=23
        y2=-30
        x3=30
        y3=-23
        x4=30
        y4=23
        x5=23
        y5=30
        x6=-23
        y6=30
        x7=-30
        y7=23
        x8=-30
        y8=-23
        x9=-23
        y9=-30

        #Extrude
        lshape_wire = Part.makePolygon([Base.Vector(x1, y1, 0), Base.Vector(x2, y2, 0), Base.Vector(x3, y3, 0), Base.Vector(x4, y4, 0), Base.Vector(x5, y5, 0), Base.Vector(x6, y6, 0), Base.Vector(x7, y7, 0), Base.Vector(x8, y8, 0), Base.Vector(x9, y9, 0)])
        L=Part.Face(lshape_wire)
        BasePart=  L.extrude(Base.Vector(0, 0, 3))

        #Part.show(BasePart)
        
        #Drillings
        CentralDrilling = Part.makeCylinder(16/2,3)
        BossExtrude=BasePart.cut(CentralDrilling)

        SmallDrilling = Part.makeCylinder(5/2,3)
        TranslationSmallDrilling1 = (0,-20.5,0)
        SmallDrilling.translate(TranslationSmallDrilling1)
        BossExtrude1=BossExtrude.cut(SmallDrilling)

        TranslationSmallDrilling2 = (0,20.5*2,0)
        SmallDrilling.translate(TranslationSmallDrilling2)
        BossExtrude2=BossExtrude1.cut(SmallDrilling)

        TranslationSmallDrilling3 = (-20.5,-20.5,0)
        SmallDrilling.translate(TranslationSmallDrilling3)
        BossExtrude3=BossExtrude2.cut(SmallDrilling)

        TranslationSmallDrilling4 = (20.5*2,0,0)
        SmallDrilling.translate(TranslationSmallDrilling4)
        BossExtrude4=BossExtrude3.cut(SmallDrilling)

        #Plug
        Basepart1=Part.makeCone(4.18,2.3,7)
        TranslationBasepart1=(0,0,3)
        Basepart1.translate(TranslationBasepart1)
        #Part.show(Basepart1)
        Basepart2=Part.makeCylinder(4.18,3)
        #Part.show(Basepart2)

        fused=Basepart1.fuse(Basepart2)
        #Part.show(fused)


        #make sketch
        x1=0
        y1=0
        x2=-1
        y2=5
        x3=1
        y3=5
        x4=0
        y4=0
        
        lshape_wire = Part.makePolygon([Base.Vector(x1, y1, 0), Base.Vector(x2, y2, 0), Base.Vector(x3, y3, 0), Base.Vector(x4, y4, 0)])
        L=Part.Face(lshape_wire)
        CutPart=  L.extrude(Base.Vector(0, 0, 10))
        #Part.show(CutPart)
        Extrude1=fused.cut(CutPart)

        CutPart.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 45)
        #Part.show(CutPart)
        Extrude2=Extrude1.cut(CutPart)

        CutPart.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 45)
        #Part.show(CutPart)
        Extrude3=Extrude2.cut(CutPart)

        CutPart.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 45)
        #Part.show(CutPart)
        Extrude4=Extrude3.cut(CutPart)

        CutPart.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 45)
        #Part.show(CutPart)
        Extrude5=Extrude4.cut(CutPart)

        CutPart.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 45)
        #Part.show(CutPart)
        Extrude6=Extrude5.cut(CutPart)

        CutPart.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 45)
        #Part.show(CutPart)
        Extrude7=Extrude6.cut(CutPart)

        CutPart.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 45)
        #Part.show(CutPart)
        Extrude8=Extrude7.cut(CutPart)
        #Part.show(Extrude8)


        Central=Part.makeCylinder(2.3,10)
        fused1=Central.fuse(Extrude8)
        #Part.show(fused1)

        Translationfused1=(21.12,21.12,3)
        fused1.translate(Translationfused1)
        fused2=BossExtrude4.fuse(fused1)

        Translationfused2=(-21.12*2,0,0)
        fused1.translate(Translationfused2)
        fused3=fused2.fuse(fused1)
        Translationfused3=(0,-21.12*2,0)
        fused1.translate(Translationfused3)
        fused4=fused3.fuse(fused1)
        Translationfused4=(21.12*2,0,0)
        fused1.translate(Translationfused4)
        fused5=fused4.fuse(fused1)
        
        fused5.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 1, 0), 180)
        Translationcap=(0,0,RodLength-19.5)
        fused5.translate(Translationcap)

        
        #Display
        cap = FreeCAD.ActiveDocument.addObject("Part::Feature", "cap")
        cap.Shape=fused5
        cap.Shape=cap.Shape.removeSplitter()
        cap.ViewObject.ShapeColor = (1.0,1.0,192/255)

        ###Cap_End################################################################
        ###Clamping_Holder1##########################################################
        if LensBin==1:
            #Cylinder
            BossExtrude1=Part.makeCylinder(8/2,5)
            CutExtrude1=Part.makeCylinder(4/2,5)
            PartBossExtrude1=BossExtrude1.cut(CutExtrude1)
            #Part.show(PartBossExtrude1)
        
        
            #Cutouts
            CutExtrude2=Part.makeBox(3,1,1)
            CutExtrude3=Part.makeBox(1,0.5,5)
            CutExtrude4=Part.makeBox(3.4,3,5)
            TranslationCutExtrude2=(1,-0.5,4)
            TranslationCutExtrude3=(1.5,-0.25,0)
            TranslationCutExtrude4=(-4,-1.7,0)
            CutExtrude2.translate(TranslationCutExtrude2)
            CutExtrude3.translate(TranslationCutExtrude3)
            CutExtrude4.translate(TranslationCutExtrude4)
            #Part.show(CutExtrude2)
            #Part.show(CutExtrude3)
            PartBossExtrude2=PartBossExtrude1.cut(CutExtrude2)
            PartBossExtrude3=PartBossExtrude2.cut(CutExtrude3)
            PartBossExtrude4=PartBossExtrude3.cut(CutExtrude4)
            #Part.show(PartBossExtrude3)
            #clampingholderTranslation=(20.5,0,64)
            clampingholderTranslation=(20.5,0,78-DLL)
            PartBossExtrude4.translate(clampingholderTranslation)


            #chamfer
            clamping_holder1=FreeCAD.ActiveDocument.addObject("Part::Feature", "clamping_holder1")
            clamping_holder1.Shape=PartBossExtrude4
            clamping_holder1.Shape=clamping_holder1.Shape.removeSplitter()
    
            chmfr = FreeCAD.ActiveDocument.addObject("Part::Chamfer", "clamping_Holder1")
            chmfr.Base = FreeCAD.ActiveDocument.clamping_holder1
            myEdges = []
        
            myEdges.append((15, 0.5, 0.5))# (edge number, chamfer start length, chamfer end length)
            myEdges.append((18, 0.5, 0.5))
            myEdges.append((19, 0.5, 0.5))
            myEdges.append((26, 0.5, 0.5))
            myEdges.append((30, 0.5, 0.5))
            myEdges.append((37, 0.5, 0.5))
            
            chmfr.Edges = myEdges
            FreeCADGui.ActiveDocument.clamping_holder1.Visibility = False
    
            FreeCAD.ActiveDocument.recompute()
            
            chmfr.ViewObject.ShapeColor = (1.0,0.0,0.0)
        else:
            print("no Lens")
        ###Clamping_Holder1_End#######################################################
        ###Clamping_Holder2##########################################################
        if LensBin==1:
            #Cylinder
            BossExtrude1=Part.makeCylinder(8/2,5)
            CutExtrude1=Part.makeCylinder(4/2,5)
            PartBossExtrude1=BossExtrude1.cut(CutExtrude1)
            #Part.show(PartBossExtrude1)
    
    
            #Cutouts
            CutExtrude2=Part.makeBox(3,1,1)
            CutExtrude3=Part.makeBox(1,0.5,5)
            CutExtrude4=Part.makeBox(3.4,3,5)
            TranslationCutExtrude2=(1,-0.5,4)
            TranslationCutExtrude3=(1.5,-0.25,0)
            TranslationCutExtrude4=(-4,-1.7,0)
            CutExtrude2.translate(TranslationCutExtrude2)
            CutExtrude3.translate(TranslationCutExtrude3)
            CutExtrude4.translate(TranslationCutExtrude4)
            #Part.show(CutExtrude2)
            #Part.show(CutExtrude3)
            PartBossExtrude2=PartBossExtrude1.cut(CutExtrude2)
            PartBossExtrude3=PartBossExtrude2.cut(CutExtrude3)
            PartBossExtrude4=PartBossExtrude3.cut(CutExtrude4)
            #Part.show(PartBossExtrude3)
            clampingholderTranslation=(-20.5,0,78-DLL)
            PartBossExtrude4.translate(clampingholderTranslation)
            
        
            #chamfer
            clamping_holder2=FreeCAD.ActiveDocument.addObject("Part::Feature", "clamping_holder2")
            clamping_holder2.Shape=PartBossExtrude4
            clamping_holder2.Shape=clamping_holder2.Shape.removeSplitter()
            
            chmfr = FreeCAD.ActiveDocument.addObject("Part::Chamfer", "clamping_Holder2")
            chmfr.Base = FreeCAD.ActiveDocument.clamping_holder2
            myEdges = []

            myEdges.append((15, 0.5, 0.5))# (edge number, chamfer start length, chamfer end length)
            myEdges.append((18, 0.5, 0.5))
            myEdges.append((19, 0.5, 0.5))
            myEdges.append((26, 0.5, 0.5))
            myEdges.append((30, 0.5, 0.5))
            myEdges.append((37, 0.5, 0.5))
            
            chmfr.Edges = myEdges
            FreeCADGui.ActiveDocument.clamping_holder2.Visibility = False

            FreeCAD.ActiveDocument.recompute()
        
            chmfr.ViewObject.ShapeColor = (1.0,0.0,0.0)
        
        else:
            print("no Lens")
        ###Clamping_Holder2_End#######################################################
        ###Clamping_Holder3##########################################################
        if LensBin==1:
            #Cylinder
            BossExtrude1=Part.makeCylinder(8/2,5)
            CutExtrude1=Part.makeCylinder(4/2,5)
            PartBossExtrude1=BossExtrude1.cut(CutExtrude1)
            #Part.show(PartBossExtrude1)
        

            #Cutouts
            CutExtrude2=Part.makeBox(3,1,1)
            CutExtrude3=Part.makeBox(1,0.5,5)
            CutExtrude4=Part.makeBox(3.4,3,5)
            TranslationCutExtrude2=(1,-0.5,4)
            TranslationCutExtrude3=(1.5,-0.25,0)
            TranslationCutExtrude4=(-4,-1.7,0)
            CutExtrude2.translate(TranslationCutExtrude2)
            CutExtrude3.translate(TranslationCutExtrude3)
            CutExtrude4.translate(TranslationCutExtrude4)
            #Part.show(CutExtrude2)
            #Part.show(CutExtrude3)
            PartBossExtrude2=PartBossExtrude1.cut(CutExtrude2)
            PartBossExtrude3=PartBossExtrude2.cut(CutExtrude3)
            PartBossExtrude4=PartBossExtrude3.cut(CutExtrude4)
            #Part.show(PartBossExtrude3)
            clampingholderTranslation=(0,20.5,78-DLL)
            PartBossExtrude4.translate(clampingholderTranslation)
            
    
            #chamfer
            clamping_holder3=FreeCAD.ActiveDocument.addObject("Part::Feature", "clamping_holder3")
            clamping_holder3.Shape=PartBossExtrude4
            clamping_holder3.Shape=clamping_holder3.Shape.removeSplitter()
    
            chmfr = FreeCAD.ActiveDocument.addObject("Part::Chamfer", "clamping_Holder3")
            chmfr.Base = FreeCAD.ActiveDocument.clamping_holder3
            myEdges = []
    
            myEdges.append((15, 0.5, 0.5))# (edge number, chamfer start length, chamfer end length)
            myEdges.append((18, 0.5, 0.5))
            myEdges.append((19, 0.5, 0.5))
            myEdges.append((26, 0.5, 0.5))
            myEdges.append((30, 0.5, 0.5))
            myEdges.append((37, 0.5, 0.5))
            
            chmfr.Edges = myEdges
            FreeCADGui.ActiveDocument.clamping_holder3.Visibility = False

            FreeCAD.ActiveDocument.recompute()
        
            chmfr.ViewObject.ShapeColor = (1.0,0.0,0.0)
        else:
            print("no Lens")
        ###Clamping_Holder3_End#######################################################
        ###Clamping_Holder4##########################################################
        if LensBin==1:
            #Cylinder
            BossExtrude1=Part.makeCylinder(8/2,5)
            CutExtrude1=Part.makeCylinder(4/2,5)
            PartBossExtrude1=BossExtrude1.cut(CutExtrude1)
            #Part.show(PartBossExtrude1)
        
        
            #Cutouts
            CutExtrude2=Part.makeBox(3,1,1)
            CutExtrude3=Part.makeBox(1,0.5,5)
            CutExtrude4=Part.makeBox(3.4,3,5)
            TranslationCutExtrude2=(1,-0.5,4)
            TranslationCutExtrude3=(1.5,-0.25,0)
            TranslationCutExtrude4=(-4,-1.7,0)
            CutExtrude2.translate(TranslationCutExtrude2)
            CutExtrude3.translate(TranslationCutExtrude3)
            CutExtrude4.translate(TranslationCutExtrude4)
            #Part.show(CutExtrude2)
            #Part.show(CutExtrude3)
            PartBossExtrude2=PartBossExtrude1.cut(CutExtrude2)
            PartBossExtrude3=PartBossExtrude2.cut(CutExtrude3)
            PartBossExtrude4=PartBossExtrude3.cut(CutExtrude4)
            #Part.show(PartBossExtrude3)
            clampingholderTranslation=(0,-20.5,78-DLL)
            PartBossExtrude4.translate(clampingholderTranslation)
        
        
            #chamfer
            clamping_holder4=FreeCAD.ActiveDocument.addObject("Part::Feature", "clamping_holder4")
            clamping_holder4.Shape=PartBossExtrude4
            clamping_holder4.Shape=clamping_holder4.Shape.removeSplitter()
            
            chmfr = FreeCAD.ActiveDocument.addObject("Part::Chamfer", "clamping_Holder4")
            chmfr.Base = FreeCAD.ActiveDocument.clamping_holder4
            myEdges = []
            
            myEdges.append((15, 0.5, 0.5))# (edge number, chamfer start length, chamfer end length)
            myEdges.append((18, 0.5, 0.5))
            myEdges.append((19, 0.5, 0.5))
            myEdges.append((26, 0.5, 0.5))
            myEdges.append((30, 0.5, 0.5))
            myEdges.append((37, 0.5, 0.5))
    
            chmfr.Edges = myEdges
            FreeCADGui.ActiveDocument.clamping_holder4.Visibility = False

            FreeCAD.ActiveDocument.recompute()
                
            chmfr.ViewObject.ShapeColor = (1.0,0.0,0.0)
        else:
            print("no Lens")
        ###Clamping_Holder4_End#######################################################
        ###Clamping_Holder5##########################################################
        #Cylinder
        BossExtrude1=Part.makeCylinder(8/2,5)
        CutExtrude1=Part.makeCylinder(4/2,5)
        PartBossExtrude1=BossExtrude1.cut(CutExtrude1)
        #Part.show(PartBossExtrude1)
        
        
        #Cutouts
        CutExtrude2=Part.makeBox(3,1,1)
        CutExtrude3=Part.makeBox(1,0.5,5)
        CutExtrude4=Part.makeBox(3.4,3,5)
        TranslationCutExtrude2=(1,-0.5,4)
        TranslationCutExtrude3=(1.5,-0.25,0)
        TranslationCutExtrude4=(-4,-1.7,0)
        CutExtrude2.translate(TranslationCutExtrude2)
        CutExtrude3.translate(TranslationCutExtrude3)
        CutExtrude4.translate(TranslationCutExtrude4)
        #Part.show(CutExtrude2)
        #Part.show(CutExtrude3)
        PartBossExtrude2=PartBossExtrude1.cut(CutExtrude2)
        PartBossExtrude3=PartBossExtrude2.cut(CutExtrude3)
        PartBossExtrude4=PartBossExtrude3.cut(CutExtrude4)
        #Part.show(PartBossExtrude3)
        clampingholderTranslation=(20.5,0,RodLength-19.5)
        PartBossExtrude4.translate(clampingholderTranslation)


        #chamfer
        clamping_holder5=FreeCAD.ActiveDocument.addObject("Part::Feature", "clamping_holder5")
        clamping_holder5.Shape=PartBossExtrude4
        clamping_holder5.Shape=clamping_holder5.Shape.removeSplitter()
        
        chmfr = FreeCAD.ActiveDocument.addObject("Part::Chamfer", "clamping_Holder5")
        chmfr.Base = FreeCAD.ActiveDocument.clamping_holder5
        myEdges = []

        myEdges.append((15, 0.5, 0.5))# (edge number, chamfer start length, chamfer end length)
        myEdges.append((18, 0.5, 0.5))
        myEdges.append((19, 0.5, 0.5))
        myEdges.append((26, 0.5, 0.5))
        myEdges.append((30, 0.5, 0.5))
        myEdges.append((37, 0.5, 0.5))

        chmfr.Edges = myEdges
        FreeCADGui.ActiveDocument.clamping_holder5.Visibility = False

        FreeCAD.ActiveDocument.recompute()
        
        chmfr.ViewObject.ShapeColor = (1.0,0.0,0.0)
        ###Clamping_Holder5_End#######################################################
        ###Clamping_Holder6##########################################################
        #Cylinder
        BossExtrude1=Part.makeCylinder(8/2,5)
        CutExtrude1=Part.makeCylinder(4/2,5)
        PartBossExtrude1=BossExtrude1.cut(CutExtrude1)
        #Part.show(PartBossExtrude1)


        #Cutouts
        CutExtrude2=Part.makeBox(3,1,1)
        CutExtrude3=Part.makeBox(1,0.5,5)
        CutExtrude4=Part.makeBox(3.4,3,5)
        TranslationCutExtrude2=(1,-0.5,4)
        TranslationCutExtrude3=(1.5,-0.25,0)
        TranslationCutExtrude4=(-4,-1.7,0)
        CutExtrude2.translate(TranslationCutExtrude2)
        CutExtrude3.translate(TranslationCutExtrude3)
        CutExtrude4.translate(TranslationCutExtrude4)
        #Part.show(CutExtrude2)
        #Part.show(CutExtrude3)
        PartBossExtrude2=PartBossExtrude1.cut(CutExtrude2)
        PartBossExtrude3=PartBossExtrude2.cut(CutExtrude3)
        PartBossExtrude4=PartBossExtrude3.cut(CutExtrude4)
        #Part.show(PartBossExtrude3)
        clampingholderTranslation=(-20.5,0,RodLength-19.5)
        PartBossExtrude4.translate(clampingholderTranslation)
        

        #chamfer
        clamping_holder6=FreeCAD.ActiveDocument.addObject("Part::Feature", "clamping_holder6")
        clamping_holder6.Shape=PartBossExtrude4
        clamping_holder6.Shape=clamping_holder6.Shape.removeSplitter()
        
        chmfr = FreeCAD.ActiveDocument.addObject("Part::Chamfer", "clamping_Holder6")
        chmfr.Base = FreeCAD.ActiveDocument.clamping_holder6
        myEdges = []
        
        myEdges.append((15, 0.5, 0.5))# (edge number, chamfer start length, chamfer end length)
        myEdges.append((18, 0.5, 0.5))
        myEdges.append((19, 0.5, 0.5))
        myEdges.append((26, 0.5, 0.5))
        myEdges.append((30, 0.5, 0.5))
        myEdges.append((37, 0.5, 0.5))
        
        chmfr.Edges = myEdges
        FreeCADGui.ActiveDocument.clamping_holder6.Visibility = False
        
        FreeCAD.ActiveDocument.recompute()
                
        chmfr.ViewObject.ShapeColor = (1.0,0.0,0.0)
        ###Clamping_Holder6_End#######################################################
        ###Clamping_Holder7##########################################################
        #Cylinder
        BossExtrude1=Part.makeCylinder(8/2,5)
        CutExtrude1=Part.makeCylinder(4/2,5)
        PartBossExtrude1=BossExtrude1.cut(CutExtrude1)
        #Part.show(PartBossExtrude1)
        

        #Cutouts
        CutExtrude2=Part.makeBox(3,1,1)
        CutExtrude3=Part.makeBox(1,0.5,5)
        CutExtrude4=Part.makeBox(3.4,3,5)
        TranslationCutExtrude2=(1,-0.5,4)
        TranslationCutExtrude3=(1.5,-0.25,0)
        TranslationCutExtrude4=(-4,-1.7,0)
        CutExtrude2.translate(TranslationCutExtrude2)
        CutExtrude3.translate(TranslationCutExtrude3)
        CutExtrude4.translate(TranslationCutExtrude4)
        #Part.show(CutExtrude2)
        #Part.show(CutExtrude3)
        PartBossExtrude2=PartBossExtrude1.cut(CutExtrude2)
        PartBossExtrude3=PartBossExtrude2.cut(CutExtrude3)
        PartBossExtrude4=PartBossExtrude3.cut(CutExtrude4)
        #Part.show(PartBossExtrude3)
        clampingholderTranslation=(0,20.5,RodLength-19.5)
        PartBossExtrude4.translate(clampingholderTranslation)


        #chamfer
        clamping_holder7=FreeCAD.ActiveDocument.addObject("Part::Feature", "clamping_holder7")
        clamping_holder7.Shape=PartBossExtrude4
        clamping_holder7.Shape=clamping_holder7.Shape.removeSplitter()

        chmfr = FreeCAD.ActiveDocument.addObject("Part::Chamfer", "clamping_Holder7")
        chmfr.Base = FreeCAD.ActiveDocument.clamping_holder7
        myEdges = []

        myEdges.append((15, 0.5, 0.5))# (edge number, chamfer start length, chamfer end length)
        myEdges.append((18, 0.5, 0.5))
        myEdges.append((19, 0.5, 0.5))
        myEdges.append((26, 0.5, 0.5))
        myEdges.append((30, 0.5, 0.5))
        myEdges.append((37, 0.5, 0.5))
        
        chmfr.Edges = myEdges
        FreeCADGui.ActiveDocument.clamping_holder7.Visibility = False
        
        FreeCAD.ActiveDocument.recompute()
                
        chmfr.ViewObject.ShapeColor = (1.0,0.0,0.0)
        ###Clamping_Holder7_End#######################################################
        ###Clamping_Holder8##########################################################
        #Cylinder
        BossExtrude1=Part.makeCylinder(8/2,5)
        CutExtrude1=Part.makeCylinder(4/2,5)
        PartBossExtrude1=BossExtrude1.cut(CutExtrude1)
        #Part.show(PartBossExtrude1)
        

        #Cutouts
        CutExtrude2=Part.makeBox(3,1,1)
        CutExtrude3=Part.makeBox(1,0.5,5)
        CutExtrude4=Part.makeBox(3.4,3,5)
        TranslationCutExtrude2=(1,-0.5,4)
        TranslationCutExtrude3=(1.5,-0.25,0)
        TranslationCutExtrude4=(-4,-1.7,0)
        CutExtrude2.translate(TranslationCutExtrude2)
        CutExtrude3.translate(TranslationCutExtrude3)
        CutExtrude4.translate(TranslationCutExtrude4)
        #Part.show(CutExtrude2)
        #Part.show(CutExtrude3)
        PartBossExtrude2=PartBossExtrude1.cut(CutExtrude2)
        PartBossExtrude3=PartBossExtrude2.cut(CutExtrude3)
        PartBossExtrude4=PartBossExtrude3.cut(CutExtrude4)
        #Part.show(PartBossExtrude3)
        #clampingholderTranslation=(0,-20.5,180.5)
        clampingholderTranslation=(0,-20.5,RodLength-19.5)
        PartBossExtrude4.translate(clampingholderTranslation)


        #chamfer
        clamping_holder8=FreeCAD.ActiveDocument.addObject("Part::Feature", "clamping_holder8")
        clamping_holder8.Shape=PartBossExtrude4
        clamping_holder8.Shape=clamping_holder8.Shape.removeSplitter()

        chmfr = FreeCAD.ActiveDocument.addObject("Part::Chamfer", "clamping_Holder8")
        chmfr.Base = FreeCAD.ActiveDocument.clamping_holder8
        myEdges = []

        myEdges.append((15, 0.5, 0.5))# (edge number, chamfer start length, chamfer end length)
        myEdges.append((18, 0.5, 0.5))
        myEdges.append((19, 0.5, 0.5))
        myEdges.append((26, 0.5, 0.5))
        myEdges.append((30, 0.5, 0.5))
        myEdges.append((37, 0.5, 0.5))
        
        chmfr.Edges = myEdges
        FreeCADGui.ActiveDocument.clamping_holder8.Visibility = False

        FreeCAD.ActiveDocument.recompute()
                
        chmfr.ViewObject.ShapeColor = (1.0,0.0,0.0)
        ###Clamping_Holder8_End#######################################################
        ###Shroud-Mount############################################################
        ##Base
        #make sketch
        x1=-30
        y1=-23
        x2=-23
        y2=-30
        x3=23
        y3=-30
        x4=30
        y4=-23
        x5=30
        y5=23
        x6=23
        y6=30
        x7=-23
        y7=30
        x8=-30
        y8=23
        x9=-30
        y9=-23
        

        #Extrude
        lshape_wire = Part.makePolygon([Base.Vector(x1, y1, 0), Base.Vector(x2, y2, 0), Base.Vector(x3, y3, 0), Base.Vector(x4, y4, 0), Base.Vector(x5, y5, 0), Base.Vector(x6, y6, 0), Base.Vector(x7, y7, 0), Base.Vector(x8, y8, 0), Base.Vector(x9, y9, 0)])
        L=Part.Face(lshape_wire)
        BasePart=  L.extrude(Base.Vector(0, 0, RodLength-7.5))
        #BasePart=  L.extrude(Base.Vector(0, 0, 192.5))
        #Part.show(BasePart)
        
        ##Cutouts
        #make sketch
        x1=-25.5
        y1=-10.56
        x2=-25.5
        y2=-23.96
        x3=-23.96
        y3=-25.5
        x4=-10.56
        y4=-25.5
        x5=-25.5
        y5=-10.56

        #Extrude
        lshape_wire = Part.makePolygon([Base.Vector(x1, y1, 0), Base.Vector(x2, y2, 0), Base.Vector(x3, y3, 0), Base.Vector(x4, y4, 0), Base.Vector(x5, y5, 0)])
        L=Part.Face(lshape_wire)
        #CutPart=  L.extrude(Base.Vector(0, 0, 192.5))
        CutPart=  L.extrude(Base.Vector(0, 0, RodLength-7.5))
        BossExtrude1=BasePart.cut(CutPart)
        
        CutPart.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 90)
        BossExtrude2=BossExtrude1.cut(CutPart)
        CutPart.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 90)
        BossExtrude3=BossExtrude2.cut(CutPart)
        CutPart.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 90)
        BossExtrude4=BossExtrude3.cut(CutPart)
        #Part.show(BossExtrude4)

        #make sketch
        x1=-7.03
        y1=-25.5
        x2=7.03
        y2=-25.5
        x3=25.5
        y3=-7.03
        x4=25.5
        y4=7.03
        x5=7.03
        y5=25.5
        x6=-7.03
        y6=25.5
        x7=-25.5
        y7=7.03
        x8=-25.5
        y8=-7.03
        x9=-7.03
        y9=-25.5
        

        #Extrude
        lshape_wire = Part.makePolygon([Base.Vector(x1, y1, 0), Base.Vector(x2, y2, 0), Base.Vector(x3, y3, 0), Base.Vector(x4, y4, 0), Base.Vector(x5, y5, 0), Base.Vector(x6, y6, 0), Base.Vector(x7, y7, 0), Base.Vector(x8, y8, 0), Base.Vector(x9, y9, 0)])
        L=Part.Face(lshape_wire)
        #CutPart2=  L.extrude(Base.Vector(0, 0, 192.5))
        CutPart2=  L.extrude(Base.Vector(0, 0, RodLength-7.5))

        Shroud=BossExtrude4.cut(CutPart2)
        #Part.show(BossExtrude5)
        
        ######################################################################################################################################################

        #BasePart
        BasePart=Part.makeBox(90,45,15)
        #Part.show(BasePart)
        
        ##Drillings
        #BigDrillings
        BigDrilling=Part.makeCylinder(9/2,15)
        TranslationBigDrilling=(15,22.5,0)
        BigDrilling.translate(TranslationBigDrilling)
        BossExtrude1=BasePart.cut(BigDrilling)
        #Part.show(BigDrilling)
        TranslationBigDrilling=(30,0,0)
        BigDrilling.translate(TranslationBigDrilling)
        BossExtrude2=BossExtrude1.cut(BigDrilling)
        #Part.show(BigDrilling)
        TranslationBigDrilling=(30,0,0)
        BigDrilling.translate(TranslationBigDrilling)
        BossExtrude3=BossExtrude2.cut(BigDrilling)
        #Part.show(BigDrilling)

        #middleDrillings
        middleDrilling=Part.makeCylinder(5/2,15)
        TranslationmiddleDrilling=(29,22.5,0)
        middleDrilling.translate(TranslationmiddleDrilling)
        BossExtrude4=BossExtrude3.cut(middleDrilling)
        #Part.show(middleDrilling)
        TranslationmiddleDrilling=(8,8,0)
        middleDrilling.translate(TranslationmiddleDrilling)
        BossExtrude5=BossExtrude4.cut(middleDrilling)
        #Part.show(middleDrilling)
        TranslationmiddleDrilling=(16,0,0)
        middleDrilling.translate(TranslationmiddleDrilling)
        BossExtrude6=BossExtrude5.cut(middleDrilling)
        #Part.show(middleDrilling)
        TranslationmiddleDrilling=(8,-8,0)
        middleDrilling.translate(TranslationmiddleDrilling)
        BossExtrude7=BossExtrude6.cut(middleDrilling)
        #Part.show(middleDrilling)
        TranslationmiddleDrilling=(-8,-8,0)
        middleDrilling.translate(TranslationmiddleDrilling)
        BossExtrude8=BossExtrude7.cut(middleDrilling)
        #Part.show(middleDrilling)
        TranslationmiddleDrilling=(-16,0,0)
        middleDrilling.translate(TranslationmiddleDrilling)
        BossExtrude9=BossExtrude8.cut(middleDrilling)
        #Part.show(middleDrilling)

        #recessmiddleDrillings
        recess=Part.makeCylinder(6.4/2,0.8)
        Translationrecess=(29,22.5,15-0.8)
        recess.translate(Translationrecess)
        BossExtrude10=BossExtrude9.cut(recess)
        #Part.show(recess)
        Translationrecess=(8,8,0)
        recess.translate(Translationrecess)
        BossExtrude11=BossExtrude10.cut(recess)
        #Part.show(recess)
        Translationrecess=(16,0,0)
        recess.translate(Translationrecess)
        BossExtrude12=BossExtrude11.cut(recess)
        #Part.show(recess)
        Translationrecess=(8,-8,0)
        recess.translate(Translationrecess)
        BossExtrude13=BossExtrude12.cut(recess)
        #Part.show(recess)
        Translationrecess=(-8,-8,0)
        recess.translate(Translationrecess)
        BossExtrude14=BossExtrude13.cut(recess)
        #Part.show(recess)
        Translationrecess=(-16,0,0)
        recess.translate(Translationrecess)
        BossExtrude15=BossExtrude14.cut(recess)
        #Part.show(recess)

        #smallDrillings
        smallDrilling=Part.makeCylinder(4.2/2,15)
        TranslationsmallDrilling=(2,15,0)
        smallDrilling.translate(TranslationsmallDrilling)
        insert=Part.makeBox(1,3.2,15)
        Translationinsert=(0,15-3.2/2,0)
        insert.translate(Translationinsert)
        BossExtrude16=BossExtrude15.cut(smallDrilling)
        BossExtrude17=BossExtrude16.cut(insert)
        #Part.show(smallDrilling)
        #Part.show(insert)

        TranslationsmallDrilling=(0,15,0)
        smallDrilling.translate(TranslationsmallDrilling)
        Translationinsert=(0,15,0)
        insert.translate(Translationinsert)
        BossExtrude18=BossExtrude17.cut(smallDrilling)
        BossExtrude19=BossExtrude18.cut(insert)
        #Part.show(smallDrilling)
        #Part.show(insert)
        
        TranslationsmallDrilling=(86,0,0)
        smallDrilling.translate(TranslationsmallDrilling)
        Translationinsert=(89,0,0)
        insert.translate(Translationinsert)
        BossExtrude20=BossExtrude19.cut(smallDrilling)
        BossExtrude21=BossExtrude20.cut(insert)
        #Part.show(smallDrilling)
        #Part.show(insert)

        TranslationsmallDrilling=(0,-15,0)
        smallDrilling.translate(TranslationsmallDrilling)
        Translationinsert=(0,-15,0)
        insert.translate(Translationinsert)
        BossExtrude22=BossExtrude21.cut(smallDrilling)
        BossExtrude23=BossExtrude22.cut(insert)
        #Part.show(smallDrilling)
        #Part.show(insert)

        
        #Stab
        stabholder=Part.makeBox(5.5,8.5,4.1)
        Translationstabholder=(15,3.25,15-4.1)
        stabholder.translate(Translationstabholder)
        BossExtrude24=BossExtrude23.cut(stabholder)
        #Part.show(stabholder)
        Translationstabholder=(0,30,0)
        stabholder.translate(Translationstabholder)
        BossExtrude25=BossExtrude24.cut(stabholder)
        #Part.show(stabholder)
        Translationstabholder=(54.5,0,0)
        stabholder.translate(Translationstabholder)
        BossExtrude26=BossExtrude25.cut(stabholder)
        #Part.show(stabholder)
        Translationstabholder=(0,-30,0)
        stabholder.translate(Translationstabholder)
        BossExtrude27=BossExtrude26.cut(stabholder)
        #Part.show(stabholder)
        
        stabdrilling=Part.makeCylinder(4.2/2,90)
        stabdrilling.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 1, 0), 90)
        Translationstabdrilling=(0,7.5,13)
        stabdrilling.translate(Translationstabdrilling)
        BossExtrude28=BossExtrude27.cut(stabdrilling)
        #Part.show(stabdrilling)

        Translationstabdrilling=(0,30,0)
        stabdrilling.translate(Translationstabdrilling)
        BossExtrude29=BossExtrude28.cut(stabdrilling)
        #Part.show(stabdrilling)
        
        stabrecess=Part.makeBox(90,3.2,1)
        Translationstabrecess=(0,7.5-3.2/2,15-1)
        stabrecess.translate(Translationstabrecess)
        BossExtrude30=BossExtrude29.cut(stabrecess)
        Translationstabrecess=(0,30,0)
        stabrecess.translate(Translationstabrecess)
        BossExtrude31=BossExtrude30.cut(stabrecess)

        #Fillets
        Cut1=Part.makeBox(4,4,15)
        Cut2=Part.makeCylinder(4,15)
        Cut3=Cut1.cut(Cut2)
        filletTranslation=(90-4,45-4,0)
        Cut3.translate(filletTranslation)
        BossExtrude32=BossExtrude31.cut(Cut3)
        #Part.show(Cut3)

        Cut3.rotate(Base.Vector(90-4, 45-4, 0),Base.Vector(0, 0, 1), -90)
        filletTranslation=(0,-45+8,0)
        Cut3.translate(filletTranslation)
        #Part.show(Cut3)
        BossExtrude33=BossExtrude32.cut(Cut3)

        Cut3.rotate(Base.Vector(90-4, 0, 0),Base.Vector(0, 0, 1), -90)
        filletTranslation=(-90+4,4,0)
        Cut3.translate(filletTranslation)
        #Part.show(Cut3)
        BossExtrude34=BossExtrude33.cut(Cut3)
        
        Cut3.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), -90)
        filletTranslation=(0,45,0)
        Cut3.translate(filletTranslation)
        #Part.show(Cut3)
        BossExtrude35=BossExtrude34.cut(Cut3)
        

        
        
        BossExtrude35.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 1, 0), 90)
        #MountTranslation=(30,-22.5,90+42.5)
        MountTranslation=(30,-22.5,90+42.5+(-200+RodLength)/2)
        BossExtrude35.translate(MountTranslation)
        #Part.show(BossExtrude35)
        fuse1=Shroud.fuse(BossExtrude35)

        if Mount == 0:
            BossExtrude35.rotate(Base.Vector(0, 0, 90+42.5+(-200+RodLength)/2-90/2),Base.Vector(0, 1, 0), 180)
            #MountTranslation=(0,0,42.5*2+90)
            #MountTranslation=(0,0,42.5*2+90+(-200+RodLength)/2)
            MountTranslation=(0,0,0)
            BossExtrude35.translate(MountTranslation)
            #Part.show(BossExtrude31)
            fuse2=fuse1.fuse(BossExtrude35)

        elif Mount == 1:
            fuse2=fuse1

        elif Mount == 2:
            BossExtrude35.rotate(Base.Vector(0, 0, 90+42.5+(-200+RodLength)/2-90/2),Base.Vector(0, 0, 1), 90)
            fuse2=fuse1.fuse(BossExtrude35)
        elif Mount == 3:
            BossExtrude35.rotate(Base.Vector(0, 0, 90+42.5+(-200+RodLength)/2-90/2),Base.Vector(0, 0, 1), 90)
            fuse3=fuse1.fuse(BossExtrude35)         
            BossExtrude36=BossExtrude35   
            BossExtrude36.rotate(Base.Vector(0, 0, 90+42.5+(-200+RodLength)/2-90/2),Base.Vector(0, 0, 1), 90)
            fuse2=fuse3.fuse(BossExtrude36)  
        elif Mount == 4:
            BossExtrude35.rotate(Base.Vector(0, 0, 90+42.5+(-200+RodLength)/2-90/2),Base.Vector(0, 0, 1), 90)
            fuse3=fuse1.fuse(BossExtrude35)         
            BossExtrude36=BossExtrude35   
            BossExtrude36.rotate(Base.Vector(0, 0, 90+42.5+(-200+RodLength)/2-90/2),Base.Vector(0, 0, 1), 90)
            fuse4=fuse3.fuse(BossExtrude36)  
            BossExtrude37=BossExtrude36
            BossExtrude37.rotate(Base.Vector(0, 0, 90+42.5+(-200+RodLength)/2-90/2),Base.Vector(0, 0, 1), 90)
            fuse2=fuse4.fuse(BossExtrude37)  




        
        Translationshroud=(0,0,-15)
        fuse2.translate(Translationshroud)
        
        #Part.show(fuse2)
          
        
        #Fillets
        mount=FreeCAD.ActiveDocument.addObject("Part::Feature", "Mount_Shroud")
        mount.Shape=fuse2
        mount.ViewObject.ShapeColor = (0.69,0.72,0.72)
        mount.ViewObject.Transparency=90
        ###Shroud_Mount_End########################################################
        #Show parts in a nice View
        App.activeDocument().recompute()
        Gui.activeDocument().activeView().viewAxometric()
        Gui.SendMsgToActiveView("ViewFit")

########################################################################
        
    def on_horizontal_slider1(self, val_X):                                                  # connection on_horizontal_slider
        #

        self.lineEdit_1.setText(str(val_X/10))
        self.affectation_X(val_X)
        #self.Darstellung(val_X)
        #self.label_6.setText(_translate("MainWindow",str(val_X), None))     # display in the label_6 (red)

        print( "on_horizontal_slider1" )                                                       # displayed on View repport 

    def on_horizontal_slider2(self, val_Y):                                                  # connection on_horizontal_slider
        #

        self.lineEdit_3.setText(str(val_Y/10))
        self.affectation_Y(val_Y)
        #self.Darstellung(val_Y)

        print( "on_horizontal_slider2" )                                                       # displayed on View repport     

    def on_horizontal_slider3(self, val_LensDiameter):                                                  # connection on_horizontal_slider
        #

        self.lineEdit_4.setText(str(val_LensDiameter/10))
        self.affectation_LensDiameter(val_LensDiameter)
        #self.Darstellung(val_LensDiameter)

        print( "on_horizontal_slider3" )                                                       # displayed on View repport     

    def on_horizontal_slider4(self, val_HolderDepth):                                                  # connection on_horizontal_slider
        #

        self.lineEdit_5.setText(str(val_HolderDepth/10))
        self.affectation_LensDiameter(val_HolderDepth)
        #self.Darstellung(val_HolderDepth)

        print( "on_horizontal_slider4" )                                                       # displayed on View repport     

    def on_horizontal_slider5(self, val_LaserDiameter):                                                  # connection on_horizontal_slider
        #

        self.lineEdit_6.setText(str(val_LaserDiameter/10))
        self.affectation_LaserDiameter(val_LaserDiameter)
        #self.Darstellung(val_LaserDiameter)

        print( "on_horizontal_slider5" )                                                       # displayed on View repport     

    def on_horizontal_slider6(self, val_LaserLength):                                                  # connection on_horizontal_slider
        #

        self.lineEdit_7.setText(str(val_LaserLength/10))
        self.affectation_LaserLength(val_LaserLength)
        #self.Darstellung(val_LaserDiameter)

        print( "on_horizontal_slider6" )                                                       # displayed on View repport  

    def on_horizontal_slider7(self, val_DisLaserLens):                                                  # connection on_horizontal_slider
        #

        self.lineEdit_8.setText(str(val_DisLaserLens/10))
        self.affectation_DisLaserLens(val_DisLaserLens)
        #self.Darstellung(val_DisLaserLens)

        print( "on_horizontal_slider7" )                                                       # displayed on View repport     


    def on_horizontal_slider8(self, val_Wavelength):                                                  # connection on_horizontal_slider
        #

        self.lineEdit_9.setText(str(val_Wavelength/10))
        self.affectation_Wavelength(val_Wavelength)
        #self.Darstellung(val_Wavelength)

        print( "on_horizontal_slider8" )                                                       # displayed on View repport  


    def on_horizontal_slider9(self, val_Power):                                                  # connection on_horizontal_slider
        #

        self.lineEdit_10.setText(str(val_Power/10))
        self.affectation_Power(val_Power)
        #self.Darstellung(val_Power)

        print( "on_horizontal_slider9" )                                                       # displayed on View repport  


    def on_horizontal_slider10(self, val_ProjHeightWidth):                                                  # connection on_horizontal_slider
        #

        self.lineEdit_11.setText(str(val_ProjHeightWidth/10))
        self.affectation_ProjHeightWidth(val_ProjHeightWidth)
        #self.Darstellung(val_ProjHeightWidth)

        print( "on_horizontal_slider10" )                                                       # displayed on View repport  


    def on_horizontal_slider11(self, val_ProjDepth):                                                  # connection on_horizontal_slider
        #

        self.lineEdit_12.setText(str(val_ProjDepth/10))
        self.affectation_ProjDepth(val_ProjDepth)
        #self.Darstellung(val_ProjDepth)

        print( "on_horizontal_slider11" )                                                       # displayed on View repport  


    def on_horizontal_slider12(self, val_WorkingDistance):                                                  # connection on_horizontal_slider
        #

        self.lineEdit_13.setText(str(val_WorkingDistance/10))
        self.affectation_WorkingDistance(val_WorkingDistance)
        #self.Darstellung(val_WorkingDistance)

        print( "on_horizontal_slider12" )                                                       # displayed on View repport  



    # lineEdit
    def on_lineEdit_1_Pressed(self):                                                        # connection on_lineEdit_1_Pressed
        val_X = float(self.lineEdit_1.text())                                                      # extract the string in the lineEdit
        val_X = round(val_X, 1)
        self.lineEdit_1.setText(str(val_X))
        #
        #here your code
        #
        self.affectation_X(float(val_X))
        try:
            self.horizontalSlider1.setValue(val_X*10)                                      # affect the value "val_X" on horizontalSlider and modify this
        except Exception:                                                                   # if error
            self.horizontalSlider1.setValue(int(0))                                          # affect the value "0" on horizontalSlider and modify this
            val_X = "0"
        print( val_X)
        #

    def on_lineEdit_2_Pressed(self):                                                        # connection on_lineEdit_2_Pressed
        comp = self.lineEdit_2.text()                                                      # extract the string in the lineEdit
        #
        #here your code
        #
        self.lineEdit_2.setText(str(comp))
        #self.affectation_X(comp)
        #print(comp)
        #return(comp)
        #

    def on_lineEdit_3_Pressed(self):                                                        # connection on_lineEdit_1_Pressed
        val_Y = float(self.lineEdit_3.text())                                                      # extract the string in the lineEdit
        val_Y = round(val_Y, 1)
        self.lineEdit_3.setText(str(val_Y))
        #
        #here your code
        #
        self.affectation_Y(float(val_Y))
        try:
            self.horizontalSlider2.setValue(val_Y*10)                                      # affect the value "val_X" on horizontalSlider and modify this
        except Exception:                                                                   # if error
            self.horizontalSlider2.setValue(int(0))                                          # affect the value "0" on horizontalSlider and modify this
            val_Y = "0"
        print( val_Y)
        #

    def on_lineEdit_4_Pressed(self):                                                        # connection on_lineEdit_1_Pressed
        val_LensDiameter = float(self.lineEdit_4.text())                                                      # extract the string in the lineEdit
        val_LensDiameter = round(val_LensDiameter, 1)
        self.lineEdit_4.setText(str(val_LensDiameter))
        #
        #here your code
        #
        self.affectation_LensDiameter(float(val_LensDiameter))
        try:
            self.horizontalSlider3.setValue(val_LensDiameter*10)                                      # affect the value "val_X" on horizontalSlider and modify this
        except Exception:                                                                   # if error
            self.horizontalSlider3.setValue(int(0))                                          # affect the value "0" on horizontalSlider and modify this
            val_LensDiameter = "0"
        print( val_LensDiameter)
        #

    def on_lineEdit_5_Pressed(self):                                                        # connection on_lineEdit_1_Pressed
        val_HolderDepth = float(self.lineEdit_5.text())                                                      # extract the string in the lineEdit
        val_HolderDepth = round(val_HolderDepth, 1)
        self.lineEdit_5.setText(str(val_HolderDepth))
        #
        #here your code
        #
        self.affectation_HolderDepth(float(val_HolderDepth))
        try:
            self.horizontalSlider4.setValue(val_HolderDepth*10)                                      # affect the value "val_X" on horizontalSlider and modify this
        except Exception:                                                                   # if error
            self.horizontalSlider4.setValue(int(0))                                          # affect the value "0" on horizontalSlider and modify this
            val_HolderDepth = "0"
        print( val_HolderDepth)
        #

    def on_lineEdit_6_Pressed(self):                                                        # connection on_lineEdit_1_Pressed
        val_LaserDiameter = float(self.lineEdit_6.text())
        val_LaserDiameter = round(val_LaserDiameter, 1)
        self.lineEdit_6.setText(str(val_LaserDiameter))
        #print (val_LaserDiameter)                                                      # extract the string in the lineEdit
        #
        #here your code
        #
        self.affectation_LaserDiameter(float(val_LaserDiameter))
        try:
            self.horizontalSlider5.setValue(val_LaserDiameter*10)                                      # affect the value "val_X" on horizontalSlider and modify this
        except Exception:                                                                   # if error
            self.horizontalSlider5.setValue(0)                                          # affect the value "0" on horizontalSlider and modify this
            val_LaserDiameter = "0"
        print( val_LaserDiameter)
        #

    def on_lineEdit_7_Pressed(self):                                                        # connection on_lineEdit_1_Pressed
        val_LaserLength = float(self.lineEdit_7.text())
        val_LaserLength = round(val_LaserLength, 1)
        self.lineEdit_7.setText(str(val_LaserLength))
        #print (val_LaserDiameter)                                                      # extract the string in the lineEdit
        #
        #here your code
        #
        self.affectation_LaserLength(float(val_LaserLength))
        try:
            self.horizontalSlider6.setValue(val_LaserLength*10)                                      # affect the value "val_X" on horizontalSlider and modify this
        except Exception:                                                                   # if error
            self.horizontalSlider6.setValue(0)                                          # affect the value "0" on horizontalSlider and modify this
            val_LaserDiameter = "0"
        print( val_LaserLength)
        #

    def on_lineEdit_8_Pressed(self):                                                        # connection on_lineEdit_1_Pressed
        val_DisLaserLens = float(self.lineEdit_8.text())
        val_DisLaserLens = round(val_DisLaserLens, 1)
        self.lineEdit_8.setText(str(val_DisLaserLens))
        #print (val_DisLaserLens)                                                      # extract the string in the lineEdit
        #
        #here your code
        #
        self.affectation_DisLaserLens(float(val_DisLaserLens))
        try:
            self.horizontalSlider7.setValue(val_DisLaserLens*10)                                      # affect the value "val_X" on horizontalSlider and modify this
        except Exception:                                                                   # if error
            self.horizontalSlider7.setValue(0)                                          # affect the value "0" on horizontalSlider and modify this
            val_DisLaserLens = "0"
        print( val_DisLaserLens)
        #

    def on_lineEdit_9_Pressed(self):                                                        # connection on_lineEdit_1_Pressed
        val_Wavelength = float(self.lineEdit_9.text())
        val_Wavelength = round(val_Wavelength, 1)
        self.lineEdit_9.setText(str(val_Wavelength))
        #print (val_Wavelength)                                                      # extract the string in the lineEdit
        #
        #here your code
        #
        self.affectation_Wavelength(float(val_Wavelength))
        try:
            self.horizontalSlider8.setValue(val_Wavelength*10)                                      # affect the value "val_X" on horizontalSlider and modify this
        except Exception:                                                                   # if error
            self.horizontalSlider8.setValue(0)                                          # affect the value "0" on horizontalSlider and modify this
            val_Wavelength = "0"
        print( val_Wavelength)
        #

    def on_lineEdit_10_Pressed(self):                                                        # connection on_lineEdit_1_Pressed
        val_Power = float(self.lineEdit_10.text())
        val_Power = round(val_Power, 1)
        self.lineEdit_10.setText(str(val_Power))
        #print (val_Power)                                                      # extract the string in the lineEdit
        #
        #here your code
        #
        self.affectation_Power(float(val_Power))
        try:
            self.horizontalSlider9.setValue(val_Power*10)                                      # affect the value "val_X" on horizontalSlider and modify this
        except Exception:                                                                   # if error
            self.horizontalSlider9.setValue(0)                                          # affect the value "0" on horizontalSlider and modify this
            val_Power = "0"
        print( val_Power)
        #

    def on_lineEdit_11_Pressed(self):                                                        # connection on_lineEdit_1_Pressed
        val_ProjHeightWidth = float(self.lineEdit_11.text())
        val_ProjHeightWidth = round(val_ProjHeightWidth, 1)
        self.lineEdit_11.setText(str(val_ProjHeightWidth))
        #print (val_ProjHeightWidth)                                                      # extract the string in the lineEdit
        #
        #here your code
        #
        self.affectation_ProjHeightWidth(float(val_ProjHeightWidth))
        try:
            self.horizontalSlider10.setValue(val_ProjHeightWidth*10)                                      # affect the value "val_X" on horizontalSlider and modify this
        except Exception:                                                                   # if error
            self.horizontalSlider10.setValue(0)                                          # affect the value "0" on horizontalSlider and modify this
            val_ProjHeightWidth = "0"
        print( val_ProjHeightWidth)
        #

    def on_lineEdit_12_Pressed(self):                                                        # connection on_lineEdit_1_Pressed
        val_ProjDepth = float(self.lineEdit_12.text())
        val_ProjDepth = round(val_ProjDepth, 1)
        self.lineEdit_12.setText(str(val_ProjDepth))
        #print (val_ProjDepth)                                                      # extract the string in the lineEdit
        #
        #here your code
        #
        self.affectation_ProjDepth(float(val_ProjDepth))
        try:
            self.horizontalSlider11.setValue(val_ProjDepth*10)                                      # affect the value "val_X" on horizontalSlider and modify this
        except Exception:                                                                   # if error
            self.horizontalSlider11.setValue(0)                                          # affect the value "0" on horizontalSlider and modify this
            val_ProjDepth = "0"
        print( val_ProjDepth)
        #

    def on_lineEdit_13_Pressed(self):                                                        # connection on_lineEdit_1_Pressed
        val_WorkingDistance = float(self.lineEdit_13.text())
        val_WorkingDistance = round(val_WorkingDistance, 1)
        self.lineEdit_13.setText(str(val_WorkingDistance))
        #print (val_WorkingDistance)                                                      # extract the string in the lineEdit
        #
        #here your code
        #
        self.affectation_WorkingDistance(float(val_WorkingDistance))
        try:
            self.horizontalSlider12.setValue(val_WorkingDistance*10)                                      # affect the value "val_X" on horizontalSlider and modify this
        except Exception:                                                                   # if error
            self.horizontalSlider12.setValue(0)                                          # affect the value "0" on horizontalSlider and modify this
            val_WorkingDistance = "0"
        print( val_WorkingDistance)
        #

    # Buttons
    def on_pushButton_3_clicked(self):    # Button Save                                     # connection on_pushButton_3_clicked
        #
        #Definition of Values
        Height = float(self.lineEdit_1.text())
        Height = round(Height,1)
        Width = float(self.lineEdit_3.text())
        Width = round(Width,1)
        DL = float(self.lineEdit_4.text())
        DL = round(DL,1)
        Thickness = float(self.lineEdit_5.text())
        Thickness = round(Thickness,1)
        LHD = float(self.lineEdit_6.text())
        LHD = round(LHD,1)
        LL = float(self.lineEdit_7.text())
        LL = round(LL,1)
        DLL = float(self.lineEdit_8.text())
        DLL = round(DLL,1)
        DOED=25.4
        RodIndex=self.cb3.currentIndex()
        if RodIndex==0:
            RodLength = 200
        elif RodIndex==1:
            RodLength = 125
        elif RodIndex==2:
            RodLength = 150
        elif RodIndex==3:
            RodLength = 170
        elif RodIndex==4:
            RodLength = 235 

        Mount=self.cb4.currentIndex()
  

        e=self.cb1.currentIndex()
        if e==0:
            print("yes")
            LensBin=1
        
        elif e==1:
            print("no")
            LensBin=0


        comp = self.lineEdit_2.text()
        g=self.cb2.currentIndex()
        if g==0:
            format=".stl"
        elif g==1:
            format=".step"
        elif g==2:
            format=".FreeCAD"
            

        #filename = "C:/Users/Steffen/AppData/Roaming/FreeCAD/Macro/testdatei.csv"
        #csvdatei = open('/Users/Steffen/AppData/Roaming/FreeCAD/Macro/testdatei.csv',"r",encoding="latin-1")
        csvdatei = open(csv_filename,"w", newline='')
        csv_writer = csv.writer(csvdatei, delimiter=';')
        #csv_reader_object = csv.reader(csvdatei)
        csv_writer.writerow(["DOE Hole Width","DOE Hole Height","Lens Diameter","Lens Holder Depth","Laser Diameter","Rod Length","Lens","Laser Length", "Dist. Laser Lens", "comp. location","file format","mounting"])
        csv_writer.writerow([Height,Width,DL,Thickness,LHD,RodLength,LensBin,LL,DLL,comp,format,Mount])

        csvdatei.close()    
        a=10
        self.Darstellung(a)         
        e=self.cb2.currentIndex()
        l=self.cb1.currentIndex()
        if e==0 and l==0:
            
            print(".stl")
            comp = self.lineEdit_2.text()                                                      # extract the string in the lineEdit
            self.lineEdit_2.setText(str(comp))
            import Mesh
            '''
            __objs__=[]
            __objs__.append(FreeCAD.getDocument("Assembly").getObject("DOE_Holder1"))
            save="%s/DOE_Holder1.stl" %comp
            Mesh.export(__objs__,save)
            del __objs__
            '''
            source = source_path + doe_halter_filename + '.STL'
            destination = "%s/DOE_Holder1_new.stl" %comp
            shutil.copy(source,destination)
            __objs__=[]
            __objs__.append(FreeCAD.getDocument("Assembly").getObject("DOE_Holder3"))
            #import Mesh
            save="%s/DOE_Holder3.stl" %comp
            Mesh.export(__objs__,save)
            print(save)
            del __objs__
            __objs__=[]
            __objs__.append(FreeCAD.getDocument("Assembly").getObject("LensHolder"))
            #import Mesh
            save="%s/LensHolder.stl" %comp
            Mesh.export(__objs__,save)
            print(save)
            del __objs__
            __objs__=[]
            __objs__.append(FreeCAD.getDocument("Assembly").getObject("LaserHolder1"))
            #import Mesh
            save="%s/LaserHolder1.stl" %comp
            Mesh.export(__objs__,save)
            print(save)
            del __objs__
            __objs__=[]
            __objs__.append(FreeCAD.getDocument("Assembly").getObject("LaserHolder2"))
            #import Mesh
            save="%s/LaserHolder2.stl" %comp
            Mesh.export(__objs__,save)
            print(save)
            del __objs__
            '''
            __objs__=[]
            __objs__.append(FreeCAD.getDocument("Assembly").getObject("cap"))
            #import Mesh
            save="%s/cap.stl" %comp
            Mesh.export(__objs__,save)
            print(save)
            del __objs__
            '''
            source = source_path + deckel_filename + '.STL'
            destination = "%s/cap_new.stl" %comp
            shutil.copy(source,destination)
            __objs__=[]
            __objs__.append(FreeCAD.getDocument("Assembly").getObject("Mount_Shroud"))
            #import Mesh
            save="%s/MountShroud.stl" %comp
            Mesh.export(__objs__,save)
            print(save)
            del __objs__
    
        elif e==0 and l==1:
            
            print(".stl")
            comp = self.lineEdit_2.text()                                                      # extract the string in the lineEdit
            self.lineEdit_2.setText(str(comp))
            import Mesh
            '''
            __objs__=[]
            __objs__.append(FreeCAD.getDocument("Assembly").getObject("DOE_Holder1"))
            save="%s/DOE_Holder1.stl" %comp
            Mesh.export(__objs__,save)
            del __objs__
            '''
            source = source_path + doe_halter_filename + '.STL'
            destination = "%s/DOE_Holder1_new.stl" %comp
            shutil.copy(source,destination)
            __objs__=[]
            __objs__.append(FreeCAD.getDocument("Assembly").getObject("DOE_Holder3"))
            #import Mesh
            save="%s/DOE_Holder3.stl" %comp
            Mesh.export(__objs__,save)
            print(save)
            del __objs__
            __objs__=[]
            __objs__.append(FreeCAD.getDocument("Assembly").getObject("LaserHolder1"))
            #import Mesh
            save="%s/LaserHolder1.stl" %comp
            Mesh.export(__objs__,save)
            print(save)
            del __objs__
            __objs__=[]
            __objs__.append(FreeCAD.getDocument("Assembly").getObject("LaserHolder2"))
            #import Mesh
            save="%s/LaserHolder2.stl" %comp
            Mesh.export(__objs__,save)
            print(save)
            del __objs__
            '''
            __objs__=[]
            __objs__.append(FreeCAD.getDocument("Assembly").getObject("cap"))
            #import Mesh
            save="%s/cap.stl" %comp
            Mesh.export(__objs__,save)
            print(save)
            del __objs__
            '''
            source =  source_path + deckel_filename + '.STL'
            destination = "%s/cap_new.stl" %comp
            shutil.copy(source,destination)
            __objs__=[]
            __objs__.append(FreeCAD.getDocument("Assembly").getObject("Mount_Shroud"))
            #import Mesh
            save="%s/MountShroud.stl" %comp
            Mesh.export(__objs__,save)
            print(save)
            del __objs__


        elif e==1 and l==0:
            print(".step")
            comp = self.lineEdit_2.text()
            self.lineEdit_2.setText(str(comp)) 
            source =  source_path + doe_halter_filename + '.STEP'
            destination = "%s/DOE_Holder1_new.step" %comp
            shutil.copy(source,destination)
            '''
            __objs__=[]
            __objs__.append(FreeCAD.getDocument("Assembly").getObject("DOE_Holder1"))
            import ImportGui
            save="%s/DOE_Holder1.step" %comp
            ImportGui.export(__objs__,save)
            print(comp)
            del __objs__
            '''
            __objs__=[]
            __objs__.append(FreeCAD.getDocument("Assembly").getObject("DOE_Holder3"))
            import ImportGui
            save="%s/DOE_Holder3.step" %comp
            ImportGui.export(__objs__,save)
            print(comp)
            print(save)
            del __objs__
            __objs__=[]
            __objs__.append(FreeCAD.getDocument("Assembly").getObject("LensHolder"))
            #import ImportGui
            save="%s/LensHolder.step" %comp
            ImportGui.export(__objs__,save)
            print(save)
            del __objs__
            __objs__=[]
            __objs__.append(FreeCAD.getDocument("Assembly").getObject("LaserHolder1"))
            #import ImportGui
            save="%s/LaserHolder1.step" %comp
            ImportGui.export(__objs__,save)
            print(save)
            del __objs__
            __objs__=[]
            __objs__.append(FreeCAD.getDocument("Assembly").getObject("LaserHolder2"))
            #import ImportGui
            save="%s/LaserHolder2.step" %comp
            ImportGui.export(__objs__,save)
            print(save)
            del __objs__
            '''
            __objs__=[]
            __objs__.append(FreeCAD.getDocument("Assembly").getObject("cap"))
            #import ImportGui
            save="%s/cap.step" %comp
            ImportGui.export(__objs__,save)
            print(save)
            del __objs__
           '''
            source =  source_path + deckel_filename + '.STEP'
            destination = "%s/cap_new.step" %comp
            shutil.copy(source,destination)
            __objs__=[]
            __objs__.append(FreeCAD.getDocument("Assembly").getObject("Mount_Shroud"))
            #import ImportGui
            save="%s/Mount_Shroud.step" %comp
            ImportGui.export(__objs__,save)
            print(save)
            del __objs__

        elif e==1 and l==1:
            print(".step")
            comp = self.lineEdit_2.text()
            self.lineEdit_2.setText(str(comp)) 
            source =  source_path + doe_halter_filename + '.STEP'
            destination = "%s/DOE_Holder1_new.step" %comp
            shutil.copy(source,destination)
            '''
            __objs__=[]
            __objs__.append(FreeCAD.getDocument("Assembly").getObject("DOE_Holder1"))
            import ImportGui
            save="%s/DOE_Holder1.step" %comp
            ImportGui.export(__objs__,save)
            print(comp)
            del __objs__
            '''
            __objs__=[]
            __objs__.append(FreeCAD.getDocument("Assembly").getObject("DOE_Holder3"))
            import ImportGui
            save="%s/DOE_Holder3.step" %comp
            ImportGui.export(__objs__,save)
            print(comp)
            print(save)
            del __objs__
            __objs__=[]
            __objs__.append(FreeCAD.getDocument("Assembly").getObject("LaserHolder1"))
            #import ImportGui
            save="%s/LaserHolder1.step" %comp
            ImportGui.export(__objs__,save)
            print(save)
            del __objs__
            __objs__=[]
            __objs__.append(FreeCAD.getDocument("Assembly").getObject("LaserHolder2"))
            #import ImportGui
            save="%s/LaserHolder2.step" %comp
            ImportGui.export(__objs__,save)
            print(save)
            del __objs__
            '''
            __objs__=[]
            __objs__.append(FreeCAD.getDocument("Assembly").getObject("cap"))
            #import ImportGui
            save="%s/cap.step" %comp
            ImportGui.export(__objs__,save)
            print(save)
            del __objs__
           '''
            source =  source_path + deckel_filename + '.STEP'
            destination = "%s/cap_new.step" %comp
            shutil.copy(source,destination)
            __objs__=[]
            __objs__.append(FreeCAD.getDocument("Assembly").getObject("Mount_Shroud"))
            #import ImportGui
            save="%s/Mount_Shroud.step" %comp
            ImportGui.export(__objs__,save)
            print(save)
            del __objs__


        elif e==2:
            print(".FreeCAD")
            comp = self.lineEdit_2.text()
            self.lineEdit_2.setText(str(comp))
            save="%s .FCStd" %comp
            #Gui.SendMsgToActiveView("SaveAs")
            App.getDocument("Assembly").saveAs(save)


        self.pushButton_1.setStyleSheet("background-color: QPalette.Base")                  # origin system color pushButton_1
        App.Console.PrintMessage("Save\r\n")
        #self.window.hide()                                                                  # hide the window and close the macro
        #
    def on_pushButton_2_clicked(self):    # Button Quit                                     # connection on_pushButton_2_clicked
        #
        App.closeDocument("Assembly")
        App.setActiveDocument("")
        App.ActiveDocument=None
        Gui.ActiveDocument=None
        #
        self.pushButton_1.setStyleSheet("background-color: QPalette.Base")                  # origin system color pushButton_1
        App.Console.PrintMessage("End\r\n")
        self.window.hide()                                                                  # hide the window and close the macro
        #
 
    def on_pushButton_1_clicked(self):    # Button Reset                                    # connection on_pushButton_1_clicked
        #
        #here your code
        #
        global switch


        #filename = "C:/Users/Steffen/AppData/Roaming/FreeCAD/Macro/testdatei.csv"
        #csvdatei = open('/Users/Steffen/AppData/Roaming/FreeCAD/Macro/testdatei.csv',"r",encoding="latin-1")
        csvdatei = open(csv_filename,"w", newline='')
        csv_writer = csv.writer(csvdatei, delimiter=';')
        #csv_reader_object = csv.reader(csvdatei)
        csv_writer.writerow(["DOE Hole Width","DOE Hole Height","Lens Diameter","Lens Holder Depth","Laser Diameter","Rod Length","Lens","Laser Length","Dist. Laser Lens","comp. location","file format","mounting"])
        csv_writer.writerow([6,6,18,5,16,200,1,50,50,"","",0])
        csvdatei.close()    



        
        self.lineEdit_1.setText("1.0")                                                        # gives the value "0" to the lineEdit_1
        self.lineEdit_2.setText("")                                                        # gives the value "0" to the lineEdit_2
        self.lineEdit_3.setText("1.0")                                                        # gives the value "0" to the lineEdit_1
        self.lineEdit_4.setText("10.0")                                                        # gives the value "0" to the lineEdit_1
        self.lineEdit_5.setText("2.0")                                                        # gives the value "0" to the lineEdit_2
        self.lineEdit_6.setText("10.0")                                                        # gives the value "0" to the lineEdit_1
        self.lineEdit_7.setText("22.0")                                                        # gives the value "0" to the lineEdit_2
        self.lineEdit_8.setText("50.0")                                                        # gives the value "0" to the lineEdit_1
        self.lineEdit_11.setText("10.0")                                                        # gives the value "0" to the lineEdit_1
        self.lineEdit_12.setText("1.0")                                                        # gives the value "0" to the lineEdit_1
        self.lineEdit_13.setText("10.0")                                                        # gives the value "0" to the lineEdit_1

        self.horizontalSlider1.setValue(10)                                                   # gives the value "0" to the horizontalSlider
        self.horizontalSlider2.setValue(10)                                                   # gives the value "0" to the horizontalSlider  
        self.horizontalSlider3.setValue(100)                                                   # gives the value "0" to the horizontalSlider
        self.horizontalSlider4.setValue(20)                                                   # gives the value "0" to the horizontalSlider  
        self.horizontalSlider5.setValue(100)                                                   # gives the value "0" to the horizontalSlider
        self.horizontalSlider6.setValue(220)                                                   # gives the value "0" to the horizontalSlider  
        self.horizontalSlider7.setValue(500)                                                   # gives the value "0" to the horizontalSlider
        self.horizontalSlider10.setValue(100)                                                   # gives the value "0" to the horizontalSlider
        self.horizontalSlider11.setValue(10)                                                   # gives the value "0" to the horizontalSlider  
        self.horizontalSlider12.setValue(100)                                                   # gives the value "0" to the horizontalSlider



        self.cb1.setCurrentText("yes")   
        self.cb2.setCurrentText(".stl")  
        self.cb3.setCurrentText("200")
        self.cb4.setCurrentText("2x, 180°")
        print( "Reset")
        a=10
        self.Darstellung(a)        


    def on_pushButton_4_clicked(self):    # Button Apply                                    # connection on_pushButton_4_clicked
        #
        #here your code
        #
        print( "Apply")


        #Definition of Values
        Height = float(self.lineEdit_1.text())
        Height = round(Height,1)
        Width = float(self.lineEdit_3.text())
        Width = round(Width,1)
        DL = float(self.lineEdit_4.text())
        DL = round(DL,1)
        Thickness = float(self.lineEdit_5.text())
        Thickness = round(Thickness,1)
        LHD = float(self.lineEdit_6.text())
        LHD = round(LHD,1)
        DOED=25.4
        LL = float(self.lineEdit_7.text())
        LL = round(LL,1)
        DLL = float(self.lineEdit_8.text())
        DLL = round(DLL,1)
        RodIndex=self.cb3.currentIndex()
        Mount=self.cb4.currentIndex()
        if RodIndex==0:
            RodLength = 200
        elif RodIndex==1:
            RodLength = 125
        elif RodIndex==2:
            RodLength = 150
        elif RodIndex==3:
            RodLength = 170
        elif RodIndex==4:
            RodLength = 235  

        e=self.cb1.currentIndex()
        if e==0:
            print("yes")
            LensBin=1
        
        elif e==1:
            print("no")
            LensBin=0


        comp = self.lineEdit_2.text()
        g=self.cb2.currentIndex()
        if g==0:
            format=".stl"
        elif g==1:
            format=".step"
        elif g==2:
            format=".FreeCAD"
            

        #filename = "C:/Users/Steffen/AppData/Roaming/FreeCAD/Macro/testdatei.csv"
        #csvdatei = open('/Users/Steffen/AppData/Roaming/FreeCAD/Macro/testdatei.csv',"r",encoding="latin-1")
        csvdatei = open(csv_filename,"w", newline='')
        csv_writer = csv.writer(csvdatei, delimiter=';')
        #csv_reader_object = csv.reader(csvdatei)
        csv_writer.writerow(["DOE Hole Width","DOE Hole Height","Lens Diameter","Lens Holder Depth","Laser Diameter","Rod Length","Lens","Laser Length", "Dist. Laser Lens","comp. location","file format","mounting"])
        csv_writer.writerow([Height,Width,DL,Thickness,LHD,RodLength,LensBin,LL,DLL,comp,format,Mount])

        csvdatei.close()        

        a=10
        self.Darstellung(a)

    def on_pushButton_5_clicked(self):    # make Suggestion for Laser                                     # connection on_pushButton_2_clicked
        #
        Wavelength = float(self.lineEdit_9.text())
        Power = float(self.lineEdit_10.text())
        print(Wavelength)
        print(Power)
        print("Searching...")
        if Wavelength <= 462.5 and Power <=3:
            print("Laser 1")
            self.label_00.setText(_translate("MainWindow","Suggested Laser: Picotronic DD405-1-3 \nWavelength: 405 nm\nPower: 1 mW\nDiameter: 11 mm\nLenght: 43.3 mm", None))     # display in the label_00
            self.lineEdit_6.setText("11.0")
            self.horizontalSlider5.setValue(110)                                                    
            self.lineEdit_7.setText("43.3") 
            self.horizontalSlider6.setValue(433)
        elif Wavelength <=468.5 and Power <=8.5 and Power >3:
            print("Laser 2")
            self.label_00.setText(_translate("MainWindow","Suggested Laser: CW405-05 \nWavelength: 405 nm\nPower: 5 mW\nDiameter: 12 mm\nLenght: 22 mm", None))     # display in the label_00
            self.lineEdit_6.setText("12.0")
            self.horizontalSlider5.setValue(120)                                                    
            self.lineEdit_7.setText("22.0") 
            self.horizontalSlider6.setValue(220)
        elif Wavelength <=468.5 and Power <=16 and Power >8.5:
            print("Laser 3")
            self.label_00.setText(_translate("MainWindow","Suggested Laser: RLDE405-12-6 \nWavelength: 405 nm\nPower: 12 mW\nDiameter: 22 mm\nLenght: 65 mm", None))     # display in the label_00
            self.lineEdit_6.setText("22.0")
            self.horizontalSlider5.setValue(220)                                                    
            self.lineEdit_7.setText("65.0") 
            self.horizontalSlider6.setValue(650)
        elif Wavelength <=468.5 and Power >16:
            print("Laser 4")
            self.label_00.setText(_translate("MainWindow","Suggested Laser: RLDE405M-20-5 \nWavelength: 405 nm\nPower: 20 mW\nDiameter: 16 mm\nLenght: 50 mm", None))     # display in the label_00
            self.lineEdit_6.setText("16.0")
            self.horizontalSlider5.setValue(160)                                                    
            self.lineEdit_7.setText("50.0") 
            self.horizontalSlider6.setValue(500)
        elif Wavelength >462.5 and Wavelength <= 585 and Power <=0.7:
            print("Laser 5")
            self.label_00.setText(_translate("MainWindow","Suggested Laser: LFD520-0.4-3 \nWavelength: 520 nm\nPower: 0.4 mW\nDiameter: 19 mm\nLenght: 86 mm", None))     # display in the label_00
            self.lineEdit_6.setText("19.0")
            self.horizontalSlider5.setValue(190)                                                    
            self.lineEdit_7.setText("86.0") 
            self.horizontalSlider6.setValue(860)
        elif Wavelength >468.5 and Wavelength<= 591 and Power >0.7 and Power<=3:
            print("Laser 6")
            self.label_00.setText(_translate("MainWindow","Suggested Laser: LFD532-1-3(16x90)-AP-NT \nWavelength: 532 nm\nPower: 1 mW\nDiameter: 16 mm\nLenght: 90 mm", None))     # display in the label_00
            self.lineEdit_6.setText("16.0")
            self.horizontalSlider5.setValue(160)                                                    
            self.lineEdit_7.setText("90.0") 
            self.horizontalSlider6.setValue(900)
        elif Wavelength >468.5 and Wavelength<= 591 and Power >3 and Power<=12.5:
            print("Laser 7")
            self.label_00.setText(_translate("MainWindow","Suggested Laser: LFD532-5-3 \nWavelength: 532 nm\nPower: 5 mW\nDiameter: 12 mm\nLenght: 60 mm", None))     # display in the label_00
            self.lineEdit_6.setText("12.0")
            self.horizontalSlider5.setValue(120)                                                    
            self.lineEdit_7.setText("60.0") 
            self.horizontalSlider6.setValue(600)
        elif Wavelength >468.5 and Wavelength<= 591 and Power >12.5:
            print("Laser 8")
            self.label_00.setText(_translate("MainWindow","Suggested Laser: CW532H-050 \nWavelength: 532 nm\nPower: 20 mW\nDiameter: 26 mm\nLenght: 100 mm", None))     # display in the label_00
            self.lineEdit_6.setText("26.0")
            self.horizontalSlider5.setValue(260)                                                    
            self.lineEdit_7.setText("100.0") 
            self.horizontalSlider6.setValue(1000)
        elif Wavelength >585 and Power <=0.7:
            print("Laser 9")
            self.label_00.setText(_translate("MainWindow","Suggested Laser: LFD650-0.4-4.5 \nWavelength: 650 nm\nPower: 0.4 mW\nDiameter: 15 mm\nLenght: 67 mm", None))     # display in the label_00
            self.lineEdit_6.setText("15.0")
            self.horizontalSlider5.setValue(150)                                                    
            self.lineEdit_7.setText("67.0") 
            self.horizontalSlider6.setValue(670)
        elif Wavelength >591 and Power >0.7 and Power <=3:
            print("Laser 10")
            self.label_00.setText(_translate("MainWindow","Suggested Laser: LFD635-1-3 \nWavelength: 650 nm\nPower: 1 mW\nDiameter: 11.9 mm\nLenght: 31.5 mm", None))     # display in the label_00
            self.lineEdit_6.setText("11.9")
            self.horizontalSlider5.setValue(119)                                                    
            self.lineEdit_7.setText("31.5") 
            self.horizontalSlider6.setValue(315)
        elif Wavelength >591 and Power >3 and Power <=14.5:
            print("Laser 11")
            self.label_00.setText(_translate("MainWindow","Suggested Laser: LFD635-5-3 \nWavelength: 650 nm\nPower: 5 mW\nDiameter: 11.9 mm\nLenght: 31.5 mm", None))     # display in the label_00
            self.lineEdit_6.setText("11.9")
            self.horizontalSlider5.setValue(119)                                                    
            self.lineEdit_7.setText("31.5") 
            self.horizontalSlider6.setValue(315)
        elif Wavelength >591 and Power >14.5:
            print("Laser 12")
            self.label_00.setText(_translate("MainWindow","Suggested Laser: RLDH650-24-3 \nWavelength: 650 nm\nPower: 24 mW\nDiameter: 14 mm\nLenght: 45 mm", None))     # display in the label_00
            self.lineEdit_6.setText("14.0")
            self.horizontalSlider5.setValue(140)                                                    
            self.lineEdit_7.setText("45.0") 
            self.horizontalSlider6.setValue(450)
        else:
            print("no compatible laser was found")





MainWindow = QtGui.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
#MainWindow.show()





#Function to clear Window
def clearAll():
    doc = FreeCAD.ActiveDocument
    for obj in doc.Objects:
        doc.removeObject(obj.Label)


#Show parts in a nice View
#App.activeDocument().recompute()
#Gui.activeDocument().activeView().viewAxometric()
#Gui.SendMsgToActiveView("ViewFit")


