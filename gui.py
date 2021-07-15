import FreeCAD as App
import PySide
from PySide import QtCore, QtGui
import csv
import shutil

from .cad import make_parts, close_document


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
        pass

    def selectionchange2 (self):
        pass

    def selectionchange3 (self):
        pass

    def selectionchange4 (self):
        pass

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
        #DOED=25.4
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
        make_parts(csv_filename)         
        e=self.cb2.currentIndex()
        l=self.cb1.currentIndex()
        if e==0 and l==0:
            
            print(".stl")
            comp = self.lineEdit_2.text()                                                      # extract the string in the lineEdit
            self.lineEdit_2.setText(str(comp))
            import Mesh
            '''
            __objs__=[]
            __objs__.append(App.getDocument("Assembly").getObject("DOE_Holder1"))
            save="%s/DOE_Holder1.stl" %comp
            Mesh.export(__objs__,save)
            del __objs__
            '''
            source = source_path + doe_halter_filename + '.STL'
            destination = "%s/DOE_Holder1_new.stl" %comp
            shutil.copy(source,destination)
            __objs__=[]
            __objs__.append(App.getDocument("Assembly").getObject("DOE_Holder3"))
            #import Mesh
            save="%s/DOE_Holder3.stl" %comp
            Mesh.export(__objs__,save)
            print(save)
            del __objs__
            __objs__=[]
            __objs__.append(App.getDocument("Assembly").getObject("LensHolder"))
            #import Mesh
            save="%s/LensHolder.stl" %comp
            Mesh.export(__objs__,save)
            print(save)
            del __objs__
            __objs__=[]
            __objs__.append(App.getDocument("Assembly").getObject("LaserHolder1"))
            #import Mesh
            save="%s/LaserHolder1.stl" %comp
            Mesh.export(__objs__,save)
            print(save)
            del __objs__
            __objs__=[]
            __objs__.append(App.getDocument("Assembly").getObject("LaserHolder2"))
            #import Mesh
            save="%s/LaserHolder2.stl" %comp
            Mesh.export(__objs__,save)
            print(save)
            del __objs__
            '''
            __objs__=[]
            __objs__.append(App.getDocument("Assembly").getObject("cap"))
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
            __objs__.append(App.getDocument("Assembly").getObject("Mount_Shroud"))
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
            __objs__.append(App.getDocument("Assembly").getObject("DOE_Holder1"))
            save="%s/DOE_Holder1.stl" %comp
            Mesh.export(__objs__,save)
            del __objs__
            '''
            source = source_path + doe_halter_filename + '.STL'
            destination = "%s/DOE_Holder1_new.stl" %comp
            shutil.copy(source,destination)
            __objs__=[]
            __objs__.append(App.getDocument("Assembly").getObject("DOE_Holder3"))
            #import Mesh
            save="%s/DOE_Holder3.stl" %comp
            Mesh.export(__objs__,save)
            print(save)
            del __objs__
            __objs__=[]
            __objs__.append(App.getDocument("Assembly").getObject("LaserHolder1"))
            #import Mesh
            save="%s/LaserHolder1.stl" %comp
            Mesh.export(__objs__,save)
            print(save)
            del __objs__
            __objs__=[]
            __objs__.append(App.getDocument("Assembly").getObject("LaserHolder2"))
            #import Mesh
            save="%s/LaserHolder2.stl" %comp
            Mesh.export(__objs__,save)
            print(save)
            del __objs__
            '''
            __objs__=[]
            __objs__.append(App.getDocument("Assembly").getObject("cap"))
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
            __objs__.append(App.getDocument("Assembly").getObject("Mount_Shroud"))
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
            __objs__.append(App.getDocument("Assembly").getObject("DOE_Holder1"))
            import ImportGui
            save="%s/DOE_Holder1.step" %comp
            ImportGui.export(__objs__,save)
            print(comp)
            del __objs__
            '''
            __objs__=[]
            __objs__.append(App.getDocument("Assembly").getObject("DOE_Holder3"))
            import ImportGui
            save="%s/DOE_Holder3.step" %comp
            ImportGui.export(__objs__,save)
            print(comp)
            print(save)
            del __objs__
            __objs__=[]
            __objs__.append(App.getDocument("Assembly").getObject("LensHolder"))
            #import ImportGui
            save="%s/LensHolder.step" %comp
            ImportGui.export(__objs__,save)
            print(save)
            del __objs__
            __objs__=[]
            __objs__.append(App.getDocument("Assembly").getObject("LaserHolder1"))
            #import ImportGui
            save="%s/LaserHolder1.step" %comp
            ImportGui.export(__objs__,save)
            print(save)
            del __objs__
            __objs__=[]
            __objs__.append(App.getDocument("Assembly").getObject("LaserHolder2"))
            #import ImportGui
            save="%s/LaserHolder2.step" %comp
            ImportGui.export(__objs__,save)
            print(save)
            del __objs__
            '''
            __objs__=[]
            __objs__.append(App.getDocument("Assembly").getObject("cap"))
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
            __objs__.append(App.getDocument("Assembly").getObject("Mount_Shroud"))
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
            __objs__.append(App.getDocument("Assembly").getObject("DOE_Holder1"))
            import ImportGui
            save="%s/DOE_Holder1.step" %comp
            ImportGui.export(__objs__,save)
            print(comp)
            del __objs__
            '''
            __objs__=[]
            __objs__.append(App.getDocument("Assembly").getObject("DOE_Holder3"))
            import ImportGui
            save="%s/DOE_Holder3.step" %comp
            ImportGui.export(__objs__,save)
            print(comp)
            print(save)
            del __objs__
            __objs__=[]
            __objs__.append(App.getDocument("Assembly").getObject("LaserHolder1"))
            #import ImportGui
            save="%s/LaserHolder1.step" %comp
            ImportGui.export(__objs__,save)
            print(save)
            del __objs__
            __objs__=[]
            __objs__.append(App.getDocument("Assembly").getObject("LaserHolder2"))
            #import ImportGui
            save="%s/LaserHolder2.step" %comp
            ImportGui.export(__objs__,save)
            print(save)
            del __objs__
            '''
            __objs__=[]
            __objs__.append(App.getDocument("Assembly").getObject("cap"))
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
            __objs__.append(App.getDocument("Assembly").getObject("Mount_Shroud"))
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
        #DOED=25.4
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

        make_parts(csv_filename)

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







#Show parts in a nice View
#App.activeDocument().recompute()
#Gui.activeDocument().activeView().viewAxometric()
#Gui.SendMsgToActiveView("ViewFit")


