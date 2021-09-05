import FreeCAD as App
import PySide
from PySide import QtCore, QtGui
import csv
import os.path
import os
from stat import S_ISDIR

from .cad import make_parts, close_document, save_parts
from .laser import suggest_laser


global switch ; switch = 0

csv_filename = 'testdatei_write.csv'



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
    def __init__(self):
        self.params = None
    
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
        self.label_2.setGeometry(QtCore.QRect(25, 643, 150, 25))                           # label coordinates 
        self.label_2.setObjectName(_fromUtf8("label_2"))                                    # label name                                   # Color text
        self.label_2.setText(_translate("MainWindow", "comp. Location", None))                 # same resultt with "<b>Hello world</b>"
        
        self.label_3 = QtGui.QLabel(self.widget)                                            # labels displayed on widget
        self.label_3.setGeometry(QtCore.QRect(205, 665, 400, 25))                           # label coordinates 
        self.label_3.setObjectName(_fromUtf8("label_3"))                                    # label name                                   # Color text
        self.label_3.setFont(font)
        self.label_3.setText(_translate("MainWindow", "e.g.: C:/Users/ITO/Desktop/Testdatei", None))                 # same resultt with "<b>Hello world</b>"

        self.label_4 = QtGui.QLabel(self.widget)                                            # labels displayed on widget
        self.label_4.setGeometry(QtCore.QRect(465, 665, 120, 25))                           # label coordinates 
        self.label_4.setObjectName(_fromUtf8("label_4"))                                    # label name                                   # Color text
        self.label_4.setFont(font)
        self.label_4.setText(_translate("MainWindow", "file format", None))                 # same resultt with "<b>Hello world</b>"
 
        self.label_5 = QtGui.QLabel(self.widget)                                            # labels displayed on widget
        self.label_5.setGeometry(QtCore.QRect(25, 547, 160, 50))                           # label coordinates 
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
        self.label_10.setGeometry(QtCore.QRect(25, 573, 190, 45))                           # label coordinates 
        self.label_10.setObjectName(_fromUtf8("label_10"))                                    # label name                                   # Color text
        self.label_10.setText(_translate("MainWindow", "Rod Length [mm]", None))                 # same resultt with "<b>Hello world</b>"

        self.label_11 = QtGui.QLabel(self.widget)                                            # labels displayed on widget
        self.label_11.setGeometry(QtCore.QRect(25, 297, 190, 45))                           # label coordinates 
        self.label_11.setObjectName(_fromUtf8("label_11"))                                    # label name                                   # Color text
        self.label_11.setText(_translate("MainWindow", "Laser Length [mm]", None))                 # same resultt with "<b>Hello world</b>"

        self.label_12 = QtGui.QLabel(self.widget)                                            # labels displayed on widget
        self.label_12.setGeometry(QtCore.QRect(25, 448, 190, 45))                           # label coordinates 
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
        self.label_15.setGeometry(QtCore.QRect(25, 598, 190, 45))                           # label coordinates 
        self.label_15.setObjectName(_fromUtf8("label_15"))                                    # label name                                   # Color text
        self.label_15.setText(_translate("MainWindow", "Mounting element", None))                 # same resultt with "<b>Hello world</b>"

        self.label_16 = QtGui.QLabel(self.widget)                                            # labels displayed on widget
        self.label_16.setGeometry(QtCore.QRect(25, 473, 190, 45))                           # label coordinates 
        self.label_16.setObjectName(_fromUtf8("label_16"))                                    # label name                                   # Color text
        self.label_16.setText(_translate("MainWindow", "Projection Height/Width [mm]", None))                 # same resultt with "<b>Hello world</b>"

        self.label_17 = QtGui.QLabel(self.widget)                                            # labels displayed on widget
        self.label_17.setGeometry(QtCore.QRect(25, 498, 190, 45))                           # label coordinates 
        self.label_17.setObjectName(_fromUtf8("label_17"))                                    # label name                                   # Color text
        self.label_17.setText(_translate("MainWindow", "Projection Depth [mm]", None))                 # same resultt with "<b>Hello world</b>"

        self.label_18 = QtGui.QLabel(self.widget)                                            # labels displayed on widget
        self.label_18.setGeometry(QtCore.QRect(25, 522, 190, 45))                           # label coordinates 
        self.label_18.setObjectName(_fromUtf8("label_18"))                                    # label name                                   # Color text
        self.label_18.setText(_translate("MainWindow", "Working Distance [cm]", None))                 # same resultt with "<b>Hello world</b>"
        
        self.label_19 = QtGui.QLabel(self.widget)                                            # labels displayed on widget
        self.label_19.setGeometry(QtCore.QRect(25, 53, 190, 45))                           # label coordinates 
        self.label_19.setObjectName(_fromUtf8("label_19"))                                    # label name                                   # Color text
        self.label_19.setText(_translate("MainWindow", "Weighting Power", None))                 # same resultt with "<b>Hello world</b>"
        
        self.label_20 = QtGui.QLabel(self.widget)                                            # labels displayed on widget
        self.label_20.setGeometry(QtCore.QRect(464, 53, 190, 45))                           # label coordinates 
        self.label_20.setObjectName(_fromUtf8("label_20"))                                    # label name                                   # Color text
        self.label_20.setText(_translate("MainWindow", "Weighting Wavelength", None))                 # same resultt with "<b>Hello world</b>"
        
        self.label_21 = QtGui.QLabel(self.widget)                                            # labels displayed on widget
        self.label_21.setGeometry(QtCore.QRect(25, 423, 190, 45))                           # label coordinates 
        self.label_21.setObjectName(_fromUtf8("label_21"))                                    # label name                                   # Color text
        self.label_21.setText(_translate("MainWindow", "Dist. DOE-Laser [mm]", None))                 # same resultt with "<b>Hello world</b>"

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
        self.horizontalSlider7.setRange(100, 1000)                                                 #value*10 to get to get one decimal digit
        self.horizontalSlider7.setGeometry(QtCore.QRect(205, 463, 230, 18))                     # coordinates position
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
        self.horizontalSlider10.setGeometry(QtCore.QRect(205,488, 230, 18))                     # coordinates position
        self.horizontalSlider10.setOrientation(QtCore.Qt.Horizontal)                          # orientation Horizontal
        self.horizontalSlider10.setInvertedAppearance(False)                                  # displacement rigth to left or left to rigth value "True" or "False"
        self.horizontalSlider10.setObjectName(_fromUtf8("horizontalSlider10"))                  # object Name
        self.horizontalSlider10.valueChanged.connect(self.on_horizontal_slider10)               # connect on "def on_horizontal_slider:" for execute action

        #        section horizontalSlider 
        self.horizontalSlider11 = QtGui.QSlider(self.widget)                                  # create horizontalSlider
        self.horizontalSlider11.setRange(10, 20000)                                                 #value*10 to get to get one decimal digit
        self.horizontalSlider11.setGeometry(QtCore.QRect(205, 513, 230, 18))                     # coordinates position
        self.horizontalSlider11.setOrientation(QtCore.Qt.Horizontal)                          # orientation Horizontal
        self.horizontalSlider11.setInvertedAppearance(False)                                  # displacement rigth to left or left to rigth value "True" or "False"
        self.horizontalSlider11.setObjectName(_fromUtf8("horizontalSlider11"))                  # object Name
        self.horizontalSlider11.valueChanged.connect(self.on_horizontal_slider11)               # connect on "def on_horizontal_slider:" for execute action

        #        section horizontalSlider 
        self.horizontalSlider12 = QtGui.QSlider(self.widget)                                  # create horizontalSlider
        self.horizontalSlider12.setRange(100, 10000)                                                 #value*10 to get to get one decimal digit
        self.horizontalSlider12.setGeometry(QtCore.QRect(205, 538, 230, 18))                     # coordinates position
        self.horizontalSlider12.setOrientation(QtCore.Qt.Horizontal)                          # orientation Horizontal
        self.horizontalSlider12.setInvertedAppearance(False)                                  # displacement rigth to left or left to rigth value "True" or "False"
        self.horizontalSlider12.setObjectName(_fromUtf8("horizontalSlider12"))                  # object Name
        self.horizontalSlider12.valueChanged.connect(self.on_horizontal_slider12)               # connect on "def on_horizontal_slider:" for execute action
        
        #        section horizontalSlider 
        self.horizontalSlider13 = QtGui.QSlider(self.widget)                                  # create horizontalSlider
        self.horizontalSlider13.setRange(0, 100)                                                 #value*10 to get to get one decimal digit
        self.horizontalSlider13.setGeometry(QtCore.QRect(205, 70, 230, 18))                     # coordinates position
        self.horizontalSlider13.setOrientation(QtCore.Qt.Horizontal)                          # orientation Horizontal
        self.horizontalSlider13.setInvertedAppearance(False)                                  # displacement rigth to left or left to rigth value "True" or "False"
        self.horizontalSlider13.setObjectName(_fromUtf8("horizontalSlider13"))                  # object Name
        self.horizontalSlider13.valueChanged.connect(self.on_horizontal_slider13)               # connect on "def on_horizontal_slider:" for execute action
        self.horizontalSlider13.setValue(50)
        
        #        section horizontalSlider 
        self.horizontalSlider14 = QtGui.QSlider(self.widget)                                  # create horizontalSlider
        self.horizontalSlider14.setRange(500, 1000)                                                 #value*10 to get to get one decimal digit
        self.horizontalSlider14.setGeometry(QtCore.QRect(205,438, 230, 18))                     # coordinates position
        self.horizontalSlider14.setOrientation(QtCore.Qt.Horizontal)                          # orientation Horizontal
        self.horizontalSlider14.setInvertedAppearance(False)                                  # displacement rigth to left or left to rigth value "True" or "False"
        self.horizontalSlider14.setObjectName(_fromUtf8("horizontalSlider14"))                  # object Name
        self.horizontalSlider14.valueChanged.connect(self.on_horizontal_slider14)               # connect on "def on_horizontal_slider:" for execute action

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
        self.cb1.setGeometry(QtCore.QRect(465, 564, 120, 25))
        self.cb1.addItem("yes")
        self.cb1.addItem("no")
        self.cb1.currentIndexChanged.connect(self.selectionchange1)

#        section comboBox2
        self.cb2 = QtGui.QComboBox(self.widget)
        self.cb2.setGeometry(QtCore.QRect(465, 645, 120, 23))
        self.cb2.addItem(".stl")
        self.cb2.addItem(".step")
        self.cb2.addItems([".FreeCAD"])
        self.cb2.currentIndexChanged.connect(self.selectionchange2)

#        section comboBox3
        self.cb3 = QtGui.QComboBox(self.widget)
        self.cb3.setGeometry(QtCore.QRect(465, 590, 120, 23))
        self.cb3.addItem("260")
        self.cb3.addItem("125")
        self.cb3.addItems(["150","170","235", "200", "110","90"])
        self.cb3.currentIndexChanged.connect(self.selectionchange3)

#        section comboBox4
        self.cb4 = QtGui.QComboBox(self.widget)
        self.cb4.setGeometry(QtCore.QRect(465, 614, 120, 23))
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
        self.lineEdit_2.setGeometry(QtCore.QRect(205, 645, 250, 22))                          # coordinates position
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
        self.lineEdit_8.setGeometry(QtCore.QRect(465, 461, 120, 22))                          # coordinates position
        self.lineEdit_8.setObjectName(_fromUtf8("lineEdit_8"))                              # name of object
        self.lineEdit_8.setText("10.0")                                                        # text by default
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
        self.lineEdit_11.setGeometry(QtCore.QRect(465, 486, 120, 22))                          # coordinates position
        self.lineEdit_11.setObjectName(_fromUtf8("lineEdit_11"))                              # name of object
        self.lineEdit_11.setText("10.0")                                                        # text by default
        self.lineEdit_11.returnPressed.connect(self.on_lineEdit_11_Pressed)                  # connect on def "on_lineEdit_2_Pressed" for execute actionn   # for validate the data with press on return touch
        #self.lineEdit_11.textChanged.connect(self.on_lineEdit_10_Pressed)                     # connect on def "on_lineEdit_2_Pressed" for execute actionn   # with tips key char by char
                                                                                            # a tooltip can be set to all objects

#        section lineEdit 12
        self.lineEdit_12 = QtGui.QLineEdit(self.widget)                                      # create object lineEdit_2
        self.lineEdit_12.setGeometry(QtCore.QRect(465, 511, 120, 22))                          # coordinates position
        self.lineEdit_12.setObjectName(_fromUtf8("lineEdit_12"))                              # name of object
        self.lineEdit_12.setText("1.0")                                                        # text by default
        self.lineEdit_12.returnPressed.connect(self.on_lineEdit_12_Pressed)                  # connect on def "on_lineEdit_2_Pressed" for execute actionn   # for validate the data with press on return touch
        #self.lineEdit_12.textChanged.connect(self.on_lineEdit_12_Pressed)                     # connect on def "on_lineEdit_2_Pressed" for execute actionn   # with tips key char by char
                                                                                            # a tooltip can be set to all objects

#        section lineEdit 13
        self.lineEdit_13 = QtGui.QLineEdit(self.widget)                                      # create object lineEdit_2
        self.lineEdit_13.setGeometry(QtCore.QRect(465, 536, 120, 22))                          # coordinates position
        self.lineEdit_13.setObjectName(_fromUtf8("lineEdit_13"))                              # name of object
        self.lineEdit_13.setText("10.0")                                                        # text by default
        self.lineEdit_13.returnPressed.connect(self.on_lineEdit_13_Pressed)                  # connect on def "on_lineEdit_2_Pressed" for execute actionn   # for validate the data with press on return touch
        #self.lineEdit_13.textChanged.connect(self.on_lineEdit_13_Pressed)                     # connect on def "on_lineEdit_2_Pressed" for execute actionn   # with tips key char by char
                                                                                            # a tooltip can be set to all objects

#        section lineEdit 14
        self.lineEdit_14 = QtGui.QLineEdit(self.widget)                                      # create object lineEdit_2
        self.lineEdit_14.setGeometry(QtCore.QRect(465, 436, 120, 22))                          # coordinates position
        self.lineEdit_14.setObjectName(_fromUtf8("lineEdit_14"))                              # name of object
        self.lineEdit_14.setText("50.0")                                                        # text by default
        self.lineEdit_14.returnPressed.connect(self.on_lineEdit_14_Pressed)                  # connect on def "on_lineEdit_2_Pressed" for execute actionn   # for validate the data with press on return touch
        #self.lineEdit_14.textChanged.connect(self.on_lineEdit_14_Pressed)                     # connect on def "on_lineEdit_2_Pressed" for execute actionn   # with tips key char by char
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
        self.label_19.setFont(font)
        self.label_20.setFont(font)
        self.label_21.setFont(font)
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
        self.lineEdit_14.setFont(font4)





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
        
    def affectation_Weighting (self,val_Weighting0):                                                        # connection affectation_X
        val_Weighting = float(val_Weighting0)                                                              # extract the value and transform it in float
        #
        #here your code
        #
        print( val_Weighting0)
        return (float(val_Weighting))
        #
        
    def affectation_DistLaserDOE (self,val_DistLaserDOE0):                                                        # connection affectation_X
        val_DistLaserDOE = float(val_DistLaserDOE0)                                                              # extract the value and transform it in float
        #
        #here your code
        #
        print( val_DistLaserDOE0)
        return (float(val_DistLaserDOE))
        #

    def selectionchange1 (self):
        lens = self.cb1.currentIndex()
        if lens==1:
            self.horizontalSlider7.setEnabled(False)
            self.lineEdit_8.setEnabled(False)
            
        else:
            self.horizontalSlider7.setEnabled(True)
            self.lineEdit_8.setEnabled(True)
            
    def selectionchange2 (self):
        pass

    def selectionchange3 (self):
        pass

    def selectionchange4 (self):
        pass
    
    
    def check_Rodlength(self):
        DLD = float(self.lineEdit_14.text())
        DLD = round(DLD,1) 
        
        LL = float(self.lineEdit_7.text())
        LL = round(LL,1)
        
        DLL = float(self.lineEdit_8.text())
        DLL = round(DLL,1)
        
        Thickness = float(self.lineEdit_5.text())
        Thickness = round(Thickness,1)
        
        lock=0
        
        RodIndex=self.cb3.currentIndex()       
        
        if LL > 40:
            Thickness_new = float(self.lineEdit_5.text())+5
            Thickness_new = round(Thickness,1)
        
        else:
            Thickness_new = float(self.lineEdit_5.text())+2*5
            Thickness_new = round(Thickness,1)
            
        Rodlength_needed=DLD+LL+7.5-2        


        if Rodlength_needed>90 or DLD-17<Thickness_new:
            self.cb3.model().item(7).setEnabled(False)
            print(RodIndex)
            
            if RodIndex==7:
                lock=1
            else:
                pass
        else:
            self.cb3.model().item(7).setEnabled(True)
            

        if Rodlength_needed>110 or DLD-17<Thickness_new:
            self.cb3.model().item(6).setEnabled(False)
            
            if RodIndex==6:
                lock=1
            else:
                pass
        else:
            self.cb3.model().item(6).setEnabled(True)
           
            
        if Rodlength_needed>125 or DLD-17<Thickness_new:
            self.cb3.model().item(1).setEnabled(False)
            
            if RodIndex==1:
                lock=1
            else:
                pass
            
        else:
            self.cb3.model().item(1).setEnabled(True)
            
    
        if Rodlength_needed>150 or DLD-17<Thickness_new:
            self.cb3.model().item(2).setEnabled(False)
            
            if RodIndex==2:
                lock=1
            else:
                pass
            
        else:
            self.cb3.model().item(2).setEnabled(True)
            
            
        if Rodlength_needed>170 or DLD-17<Thickness_new:
            self.cb3.model().item(3).setEnabled(False)
            
            if RodIndex==3:
                lock=1
            else:
                pass
            
        else:
            self.cb3.model().item(3).setEnabled(True)
           
            
        if Rodlength_needed>200 or DLD-17<Thickness_new:
            self.cb3.model().item(5).setEnabled(False)
            
            if RodIndex==5:
                lock=1
            else:
                pass
           
        else:
            self.cb3.model().item(5).setEnabled(True)
            
            
        if Rodlength_needed>235 or DLD-17<Thickness_new:
            self.cb3.model().item(4).setEnabled(False)

            if RodIndex==4:
                lock=1
            else:
                pass
        else:
            self.cb3.model().item(4).setEnabled(True)
            
        if Rodlength_needed>260 or DLD-17<Thickness_new or DLL<Thickness/2+5 or DLD-17<DLL+Thickness/2+5 or lock==1:
            #self.cb3.setEnabled(False)
            self.pushButton_3.setEnabled(False)
            self.pushButton_4.setEnabled(False)
            lock=0
        elif Rodlength_needed<260 and DLD-17>Thickness_new and DLL>Thickness/2+5 and DLD-17>DLL+Thickness/2+5 and lock==0:
            #self.cb3.setEnabled(True)
            self.pushButton_3.setEnabled(True)
            self.pushButton_4.setEnabled(True)
            lock=0
        else:
            pass
        lock=0
 
        '''       
        if DLL<Thickness/2+5:
            self.pushButton_3.setEnabled(False)
            self.pushButton_4.setEnabled(False)

            
        elif DLD-17<DLL+Thickness/2+5:
            self.pushButton_3.setEnabled(False)
            self.pushButton_4.setEnabled(False)

        elif:
            self.pushButton_3.setEnabled(True)
            self.pushButton_4.setEnabled(True)
        else:
            pass
        '''
            
        ########################################################################
        
    def on_horizontal_slider1(self, val_X):                                                  # connection on_horizontal_slider
        #

        self.lineEdit_1.setText(str(val_X/10))
        self.affectation_X(val_X)
        #self.Darstellung(val_X)
        #self.label_6.setText(_translate("MainWindow",str(val_X), None))     # display in the label_6 (red)

        print( "on_horizontal_slider1" )   
                                                    # displayed on View repport


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

        print( "on_horizontal_slider4" )
        self.check_Rodlength()                                                       # displayed on View repport     

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

        print( "on_horizontal_slider6" )  
        self.check_Rodlength()                                                     # displayed on View repport  

    def on_horizontal_slider7(self, val_DisLaserLens):                                                  # connection on_horizontal_slider
        #

        self.lineEdit_8.setText(str(val_DisLaserLens/10))
        self.affectation_DisLaserLens(val_DisLaserLens)
        #self.Darstellung(val_DisLaserLens)

        print( "on_horizontal_slider7" )  
        self.check_Rodlength()                                                     # displayed on View repport     


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
        
    def on_horizontal_slider13(self, val_Weighting):                                                  # connection on_horizontal_slider
        #

        #self.lineEdit_13.setText(str(val_WorkingDistance/10))
        self.affectation_Weighting(val_Weighting)
        #self.Darstellung(val_WorkingDistance)

        print( "on_horizontal_slider13" )                                                       # displayed on View repport  
        
    def on_horizontal_slider14(self, val_DistLaserDOE):                                                  # connection on_horizontal_slider
        #

        self.lineEdit_14.setText(str(val_DistLaserDOE/10))
        self.affectation_DistLaserDOE(val_DistLaserDOE)
        #self.Darstellung(val_WorkingDistance)

        print( "on_horizontal_slider14" ) 
        self.check_Rodlength()



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
            val_LaserLength = "0"
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
        
    def on_lineEdit_14_Pressed(self):                                                        # connection on_lineEdit_1_Pressed
        val_DistLaserDOE = float(self.lineEdit_14.text())
        val_DistLaserDOE = round(val_DistLaserDOE, 1)
        self.lineEdit_14.setText(str(val_DistLaserDOE))
        #print (val_WorkingDistance)                                                      # extract the string in the lineEdit
        #
        #here your code
        #
        self.affectation_DistLaserDOE(float(val_DistLaserDOE))
        try:
            self.horizontalSlider14.setValue(val_DistLaserDOE*10)                                      # affect the value "val_X" on horizontalSlider and modify this
        except Exception:                                                                   # if error
            self.horizontalSlider14.setValue(0)                                          # affect the value "0" on horizontalSlider and modify this
            val_DistLaserDOE = "0"
        print( val_DistLaserDOE)
        #


    def save_parameters(self, filename):
        Width, Height, DL, Thickness, LHD, RodLength, LensBin, LL, DLL, Mount, DLD = self.params
        with open(filename,"w", newline='') as csvdatei:
            csv_writer = csv.writer(csvdatei, delimiter=';')
            csv_writer.writerow(["DOE Hole Width","DOE Hole Height","Lens Diameter","Lens Holder Depth","Laser Diameter","Rod Length","Lens","Laser Length", "Dist. Laser Lens","mounting", "Dist. Laser DOE"])
            csv_writer.writerow([Height,Width,DL,Thickness,LHD,RodLength,LensBin,LL,DLL,Mount,DLD])



    def read_parameters(self):
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
        DLD = float(self.lineEdit_14.text())
        DLD = round(DLD,1)
        #DOED=25.4
        RodIndex=self.cb3.currentIndex()
        if RodIndex==0:
            RodLength = 260
        elif RodIndex==1:
            RodLength = 125
        elif RodIndex==2:
            RodLength = 150
        elif RodIndex==3:
            RodLength = 170
        elif RodIndex==4:
            RodLength = 235
        elif RodIndex==5:
            RodLength = 200
        elif RodIndex==6:
            RodLength = 110
        elif RodIndex==7:
            RodLength = 90

            
            

        Mount=self.cb4.currentIndex()
  

        e=self.cb1.currentIndex()
        if e==0:
            print("Lens yes")
            LensBin = 1
        
        elif e==1:
            print("Lens no")
            LensBin = 0

        new_params = ( 
                Width,
                Height,
                DL,
                Thickness,
                LHD,
                RodLength,
                LensBin,
                LL,
                DLL,
                Mount,
                DLD
                )
        params_changed = not (self.params == new_params)
        self.params = new_params
        return params_changed

    # Buttons
    def on_pushButton_3_clicked(self):    # Button Save                                     # connection on_pushButton_3_clicked
        changed = self.read_parameters()
        if changed:
            # Only recompute parts if parameters changed
            make_parts(params=self.params)

        format_ = self.cb2.currentIndex()
        lens = self.cb1.currentIndex()
        dest = self.lineEdit_2.text()
        self.lineEdit_2.setText(str(dest))
        try:
            mode = os.stat(dest).st_mode
        except FileNotFoundError:
            print('Folder "{}" not found.'.format(dest))
            return
        if S_ISDIR(mode):
            self.save_parameters(os.path.join(dest, csv_filename))
            save_parts(format_, lens, dest)
        else:
            print('"{}" is not a valid folder.'.format(dest))

        self.pushButton_1.setStyleSheet("background-color: QPalette.Base")                  # origin system color pushButton_1
        App.Console.PrintMessage("Save\r\n")
        #self.window.hide()                                                                  # hide the window and close the macro
        #
    def on_pushButton_2_clicked(self):    # Button Quit                                     # connection on_pushButton_2_clicked
        #
        close_document()
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
        make_parts(csv_filename)        


    def on_pushButton_4_clicked(self):    # Button Apply                                    # connection on_pushButton_4_clicked
        #
        #here your code
        #
        print( "Apply")
        changed = self.read_parameters()
        if changed:
            # Only recompute parts if parameters changed
            make_parts(params=self.params)

    def on_pushButton_5_clicked(self):    # make Suggestion for Laser                                     # connection on_pushButton_2_clicked
    
        Wavelength = float(self.lineEdit_9.text())
        Power = float(self.lineEdit_10.text())
        #Weighting=float(self.horizontalSlider13.getValue())
        Weighting=self.horizontalSlider13.value()/100
        
        lmodule = suggest_laser(Wavelength,Power,Weighting)
        Name = str(lmodule[0][0])
        wavelength = str(lmodule[0][1])
        power = str(lmodule[0][2]) 
        diameter= str(lmodule[0][3])
        length= str(lmodule[0][4])
        #print(einzeldaten)
        text=("Suggested Laser: " + Name + "\nWavelength: " + wavelength + " nm\nPower: " + power + " mW\nDiameter: " + diameter + " mm\nLenght: " + length + " mm")
        print(text)
        self.label_00.setText(_translate("MainWindow",str(text), None))     # display in the label_00
        
        self.lineEdit_6.setText(diameter)
        self.lineEdit_7.setText(length)
        
        self.horizontalSlider5.setValue(int(lmodule[0][3])*10) 
        self.horizontalSlider6.setValue(int(lmodule[0][4])*10) 






MainWindow = QtGui.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
#MainWindow.show()
