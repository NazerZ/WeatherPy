import sys
import requests
import datetime as dt
from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg
import file_handler as f
import weather_object as wo

class Ui_MainWindow(object):


    print("initialize main window")
    daily_arr = []
    hourly_arr = [] 
    image = "images/01d.png"    
    temp_label= None
    uii = None
    focused_button =None

    def setupUi(self, MainWindow):
        #setup ui 
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(615, 715)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setFocusPolicy(QtCore.Qt.StrongFocus)
        MainWindow.setStyleSheet("")
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.search = QtWidgets.QLineEdit(self.centralwidget)
        self.search.returnPressed.connect(lambda: self.search_action(MainWindow))

        self.search.setGeometry(QtCore.QRect(65, 40, 412, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.search.sizePolicy().hasHeightForWidth())
        self.search.setSizePolicy(sizePolicy)
        self.search.setStyleSheet("background:transparent")
        self.search.setText("")
        self.search.setObjectName("search")
        self.search.setPlaceholderText("Enter a city")
        self.search_button = QtWidgets.QPushButton(self.centralwidget)
        self.search_button.setGeometry(QtCore.QRect(475, 40, 90, 31))
        self.search_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.search_button.setStyleSheet("QPushButton{\n"
"color:solid white;\n"
"}\n"
".QPushButton:hover:change-cursor: cursor(\'PointingHand\')")
        self.search_button.clicked.connect(lambda: self.search_action(MainWindow))
        self.search_button.setObjectName("search_button")
        self.linegraph = QtWidgets.QGraphicsView(self.centralwidget)
        self.linegraph.setGeometry(QtCore.QRect(65, 350, 500, 141))
        self.linegraph.setAutoFillBackground(True)
        self.linegraph.setStyleSheet("background:transparent")
        self.linegraph.setObjectName("linegraph")
        self.graphWidget = pg.PlotWidget(self.centralwidget)
        self.graphWidget.setLabel('bottom', "Hour")
        self.graphWidget.setLabel('left', "Temperature")
        self.plot_points(0)
        self.graphWidget.setGeometry(QtCore.QRect(65, 350, 500, 141))
        self.graphWidget.setStyleSheet("background:transparent")

        self.Day_0 = QtWidgets.QToolButton(self.centralwidget)
        self.Day_0.setEnabled(True)
        self.Day_0.setGeometry(QtCore.QRect(14, 520, 95, 104))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Day_0.sizePolicy().hasHeightForWidth())
        self.Day_0.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Day_0.setFont(font)
        self.Day_0.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Day_0.setMouseTracking(True)
        self.Day_0.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.Day_0.setToolTipDuration(0)
        self.Day_0.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.Day_0.setAutoFillBackground(False)
        self.Day_0.setText("55°F")
        self.Day_0.clicked.connect(lambda: self.date_action(MainWindow,0))
        self.Day_0.setStyleSheet("QToolButton{\n"
"background-color:rgb(128, 222, 234);\n"
"border-radius:12px;\n"
"color:solid black;\n"
"border:2px solid black;\n"
"background-image:url(%s);\n"
"background-repeat:no-repeat;\n"
"background-position:center;\n"
"\n"
"}\n"
"\n"
".QToolButton:hover{\n"
"background-color:rgb(61, 122, 182);\n"
"}\n"
""%(Ui_MainWindow.image))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../../../Work/images/01d.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Day_0.setIcon(icon)
        self.Day_0.setIconSize(QtCore.QSize(150, 150))
        self.Day_0.setAutoRepeatDelay(300)
        self.Day_0.setPopupMode(QtWidgets.QToolButton.DelayedPopup)
        self.Day_0.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.Day_0.setAutoRaise(True)
        self.Day_0.setObjectName("Day_0")
        self.f_push = QtWidgets.QPushButton(self.centralwidget)
        self.f_push.setGeometry(QtCore.QRect(470, 80, 51, 31))
        self.f_push.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.f_push.setObjectName("f_push")
        self.f_push.clicked.connect(lambda: self.unit_action(MainWindow,"imperial"))
        self.c_push = QtWidgets.QPushButton(self.centralwidget)
        self.c_push.setGeometry(QtCore.QRect(520, 80, 51, 31))
        self.c_push.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.c_push.setObjectName("c_push")
        self.c_push.clicked.connect(lambda: self.unit_action(MainWindow,"metric"))
        self.image = QtWidgets.QLabel(self.centralwidget)
        self.image.setGeometry(QtCore.QRect(440, 180, 101, 111))
        self.image.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.image.setToolTipDuration(0)
        self.image.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.image.setStyleSheet("background:transparent")
        self.image.setText("")
        self.image.setPixmap(QtGui.QPixmap("../../../../Work/images/01d.png"))
        self.image.setScaledContents(False)
        self.image.setAlignment(QtCore.Qt.AlignCenter)
        self.image.setIndent(0)
        self.image.setObjectName("image")
        self.temp_label = QtWidgets.QLabel(self.centralwidget)
        self.temp_label.setGeometry(QtCore.QRect(165, 99, 261, 91))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.temp_label.sizePolicy().hasHeightForWidth())
        self.temp_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(48)
        self.temp_label.setFont(font)
        self.temp_label.setFocusPolicy(QtCore.Qt.NoFocus)
        self.temp_label.setStyleSheet("background:transparent")
        self.temp_label.setAlignment(QtCore.Qt.AlignCenter)
        self.temp_label.setWordWrap(False)
        self.temp_label.setObjectName("temp_label")
        self.city_label = QtWidgets.QLabel(self.centralwidget)
        self.city_label.setGeometry(QtCore.QRect(165, 170, 270, 41))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.city_label.sizePolicy().hasHeightForWidth())
        self.city_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light")
        font.setPointSize(20)
        font.setKerning(True)
        self.city_label.setFont(font)
        self.city_label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.city_label.setStyleSheet("background:transparent")
        self.city_label.setAlignment(QtCore.Qt.AlignCenter)
        self.city_label.setObjectName("city_label")
        self.description_label = QtWidgets.QLabel(self.centralwidget)
        self.description_label.setGeometry(QtCore.QRect(165, 205, 261, 41))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.description_label.sizePolicy().hasHeightForWidth())
        self.description_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light")
        font.setPointSize(16)
        font.setKerning(True)
        self.description_label.setFont(font)
        self.description_label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.description_label.setStyleSheet("QLabel{\n"
"background:transparent\n"
"}")
        self.description_label.setAlignment(QtCore.Qt.AlignCenter)
        self.description_label.setObjectName("description_label")
        self.pop_label = QtWidgets.QLabel(self.centralwidget)
        self.pop_label.setGeometry(QtCore.QRect(165, 250, 261, 21))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pop_label.sizePolicy().hasHeightForWidth())
        self.pop_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light")
        font.setPointSize(14)
        font.setKerning(True)
        self.pop_label.setFont(font)
        self.pop_label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.pop_label.setStyleSheet("background:transparent")
        self.pop_label.setAlignment(QtCore.Qt.AlignCenter)
        self.pop_label.setObjectName("pop_label")
        self.Wind_label = QtWidgets.QLabel(self.centralwidget)
        self.Wind_label.setGeometry(QtCore.QRect(165, 275, 261, 21))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Wind_label.sizePolicy().hasHeightForWidth())
        self.Wind_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light")
        font.setPointSize(12)
        font.setKerning(True)
        self.Wind_label.setFont(font)
        self.Wind_label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.Wind_label.setStyleSheet("background:transparent")
        self.Wind_label.setAlignment(QtCore.Qt.AlignCenter)
        self.Wind_label.setObjectName("Wind_label")
        self.humidty_label = QtWidgets.QLabel(self.centralwidget)
        self.humidty_label.setGeometry(QtCore.QRect(165, 295, 261, 21))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.humidty_label.sizePolicy().hasHeightForWidth())
        self.humidty_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light")
        font.setPointSize(12)
        font.setKerning(True)
        self.humidty_label.setFont(font)
        self.humidty_label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.humidty_label.setStyleSheet("background:transparent")
        self.humidty_label.setAlignment(QtCore.Qt.AlignCenter)
        self.humidty_label.setObjectName("humidty_label")
        self.Day_1 = QtWidgets.QToolButton(self.centralwidget)
        self.Day_1.setEnabled(True)
        self.Day_1.setGeometry(QtCore.QRect(136, 520, 95, 104))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Day_1.sizePolicy().hasHeightForWidth())
        self.Day_1.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Day_1.setFont(font)
        self.Day_1.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Day_1.setMouseTracking(True)
        self.Day_1.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.Day_1.setToolTipDuration(0)
        self.Day_1.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.Day_1.setAutoFillBackground(False)
        self.Day_1.clicked.connect(lambda: self.date_action(MainWindow,1))
        self.Day_1.setStyleSheet("QToolButton{\n"
"background-color:rgb(128, 222, 234);\n"
"border-radius:12px;\n"
"color:black;\n"
"border:2px solid black;\n"
"background-image:url(%s);\n"
"background-repeat:no-repeat;\n"
"background-position:center;\n"
"font-weight: bold;\n"
"\n"
"}\n"
"\n"
".QToolButton:hover{\n"
"background-color:rgb(61, 122, 182);\n"
"}\n"
""%(Ui_MainWindow.image))
        self.Day_1.setText("")
        self.Day_1.setIcon(icon)
        self.Day_1.setIconSize(QtCore.QSize(150, 150))
        self.Day_1.setAutoRepeatDelay(300)
        self.Day_1.setPopupMode(QtWidgets.QToolButton.DelayedPopup)
        self.Day_1.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.Day_1.setAutoRaise(True)
        self.Day_1.setObjectName("Day_1")
        self.Day_2 = QtWidgets.QToolButton(self.centralwidget)
        self.Day_2.setEnabled(True)
        self.Day_2.setGeometry(QtCore.QRect(258, 520, 95, 104))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Day_2.sizePolicy().hasHeightForWidth())
        self.Day_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Day_2.setFont(font)
        self.Day_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Day_2.setMouseTracking(True)
        self.Day_2.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.Day_2.setToolTipDuration(0)
        self.Day_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.Day_2.setAutoFillBackground(False)
        self.Day_2.clicked.connect(lambda: self.date_action(MainWindow,2))
        self.Day_2.setStyleSheet("QToolButton{\n"
"background-color:rgb(128, 222, 234);\n"
"border-radius:12px;\n"
"color:black;\n"
"border:2px solid black;\n"
"background-image:url(%s);\n"
"background-repeat:no-repeat;\n"
"background-position:center;\n"
"font: 14pt 'Tahoma';\n"
"\n"
"}\n"
"\n"
".QToolButton:hover{\n"
"background-color:rgb(61, 122, 182);\n"
"}\n"
""%(Ui_MainWindow.image))
        self.Day_2.setText("")
        self.Day_2.setIcon(icon)
        self.Day_2.setIconSize(QtCore.QSize(150, 150))
        self.Day_2.setAutoRepeatDelay(300)
        self.Day_2.setPopupMode(QtWidgets.QToolButton.DelayedPopup)
        self.Day_2.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.Day_2.setAutoRaise(True)
        self.Day_2.setObjectName("Day_2")
        self.Day_3 = QtWidgets.QToolButton(self.centralwidget)
        self.Day_3.setEnabled(True)
        self.Day_3.setGeometry(QtCore.QRect(380, 520, 95, 104))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Day_3.sizePolicy().hasHeightForWidth())
        self.Day_3.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Day_3.setFont(font)
        self.Day_3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Day_3.setMouseTracking(True)
        self.Day_3.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.Day_3.setToolTipDuration(0)
        self.Day_3.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.Day_3.setAutoFillBackground(False)
        self.Day_3.setStyleSheet("QToolButton{\n"
"background-color:rgb(128, 222, 234);\n"
"border-radius:12px;\n"
"color:black;\n"
"border:2px solid black;\n"
"background-image:url(%s);\n"
"background-repeat:no-repeat;\n"
"background-position:center;\n"
"\n"
"}\n"
"\n"
".QToolButton:hover{\n"
"background-color:rgb(61, 122, 182);\n"
"}\n"
""%(Ui_MainWindow.image))
        self.Day_3.setText("")
        self.Day_3.setIcon(icon)
        self.Day_3.setIconSize(QtCore.QSize(150, 150))
        self.Day_3.setAutoRepeatDelay(300)
        self.Day_3.setPopupMode(QtWidgets.QToolButton.DelayedPopup)
        self.Day_3.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.Day_3.setAutoRaise(True)
        self.Day_3.setObjectName("Day_3")
        self.Day_3.clicked.connect(lambda: self.date_action(MainWindow,3))
        self.Day_4 = QtWidgets.QToolButton(self.centralwidget)
        self.Day_4.setEnabled(True)
        self.Day_4.setGeometry(QtCore.QRect(502, 520, 95, 104))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Day_4.sizePolicy().hasHeightForWidth())
        self.Day_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Day_4.setFont(font)
        self.Day_4.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Day_4.setMouseTracking(True)
        self.Day_4.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.Day_4.setToolTipDuration(0)
        self.Day_4.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.Day_4.setAutoFillBackground(False)
        self.Day_4.clicked.connect(lambda: self.date_action(MainWindow,4))
        self.Day_4.setStyleSheet("QToolButton{\n"
"background-color:rgb(128, 222, 234);\n"
"border-radius:12px;\n"
"color:black;\n"
"border:2px solid black;\n"
"background-image:url(%s);\n"
"background-repeat:no-repeat;\n"
"background-position:center;\n"
"\n"
"}\n"
"\n"
".QToolButton:hover{\n"
"background-color:rgb(61, 122, 182);\n"
"}\n"
""%(Ui_MainWindow.image))
        self.Day_4.setText("")
        self.Day_4.setIcon(icon)
        self.Day_4.setIconSize(QtCore.QSize(150, 150))
        self.Day_4.setAutoRepeatDelay(300)
        self.Day_4.setPopupMode(QtWidgets.QToolButton.DelayedPopup)
        self.Day_4.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.Day_4.setAutoRaise(True)
        self.Day_4.setObjectName("Day_4")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(14, 630, 95, 31))
        self.label.setStyleSheet("QLabel{\n"
"text-align:center\n"
"}")
        self.label.setObjectName("label")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(136, 630, 95, 31))
        self.label_3.setStyleSheet("QLabel{\n"
"text-align:center\n"
"}")
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(258, 630, 95, 31))
        self.label_4.setStyleSheet("QLabel{\n"
"text-align:center\n"
"}")
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(380, 630, 95, 31))
        self.label_5.setStyleSheet("QLabel{\n"
"text-align:center\n"
"}")
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(502, 630, 95, 31))
        self.label_6.setStyleSheet("QLabel{\n"
"text-align:center\n"
"}")
        self.label_6.setObjectName("label_6")
        self.search.raise_()
        self.image.raise_()
        self.Day_0.raise_()
        self.linegraph.raise_()
        self.humidty_label.raise_()
        self.Wind_label.raise_()
        self.pop_label.raise_()
        self.description_label.raise_()
        self.city_label.raise_()
        self.temp_label.raise_()
        self.search_button.raise_()
        self.Day_1.raise_()
        self.Day_2.raise_()
        self.Day_3.raise_()
        self.Day_4.raise_()
        self.c_push.raise_()
        self.f_push.raise_()
        self.label.raise_()
        self.label_3.raise_()
        self.label_4.raise_()
        self.label_5.raise_()
        self.label_6.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 615, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuFamous_Cities = QtWidgets.QMenu(self.menubar)
        self.menuFamous_Cities.setObjectName("menuFamous_Cities")
        self.menuOther_Cities = QtWidgets.QMenu(self.menubar)
        self.menuOther_Cities.setObjectName("menuOther_Cities")
        MainWindow.setMenuBar(self.menubar)
        

        #self.retranslateUi(t)
        t = QtCore.QCoreApplication.translate
        
        MainWindow.setWindowTitle(t("MainWindow", "Weather Forecast"))
        self.search_button.setText(t("MainWindow", "Search"))
        self.f_push.setText(t("MainWindow", "°F"))
        self.c_push.setText(t("MainWindow", "°C"))
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    """
    def retranslateUi(self,t):
        #update 
        print("RetanslateUi")
        self.label.setText(t("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt;\">%s</span></p></body></html>" %(wo.weatherObject.get_date(0))))
        self.label_3.setText(t("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt;\">%s</span></p></body></html>" %(wo.weatherObject.get_date(1))))
        self.label_4.setText(t("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt;\">%s</span></p></body></html>" %(wo.weatherObject.get_date(2))))
        self.label_5.setText(t("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt;\">%s</span></p></body></html>" %(wo.weatherObject.get_date(3))))
        self.label_6.setText(t("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt;\">%s</span></p></body></html>" %(wo.weatherObject.get_date(4))))
        #self.menuFile.setTitle(_translate("MainWindow", "Recents"))
    """

    def load_ui(self,city,int,update_button):
       # load ui components
       # grab corresponding data from daily class
       # input into ui
       # match dates with correct time zones

        _translate = QtCore.QCoreApplication.translate
        self.label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt;\">%s</span></p></body></html>" %wo.weatherObject.get_date(0)))
        self.label_3.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt;\">%s</span></p></body></html>" %wo.weatherObject.get_date(1)))
        self.label_4.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt;\">%s</span></p></body></html>" %wo.weatherObject.get_date(2)))
        self.label_5.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt;\">%s</span></p></body></html>" %wo.weatherObject.get_date(3)))
        self.label_6.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt;\">%s</span></p></body></html>" %wo.weatherObject.get_date(4)))
        self.temp_label.setText(daily.arr[int].temp)
        self.city_label.setText(city)
        self.description_label.setText(daily.arr[int].desc)
        self.pop_label.setText("Chance of Rain: " + daily.arr[int].pop)
        s=" mph"
        if Api.units == "metric":
            s= " kmh"  
        self.Wind_label.setText("Wind: " + daily.arr[int].wind + s)
        self.humidty_label.setText("Humidty:" + daily.arr[int].humidity)
        self.plot_points(int)
        if update_button == True:
            # if metric changes update ui buttons
            self.update_buttons()
        return
    def update_buttons(self):
        # metric changed: update corresponding pieces
        print("update buttons called")
        Ui_MainWindow.button_style(self.Day_0,daily.arr[0].icon)
        Ui_MainWindow.button_style(self.Day_1,daily.arr[1].icon)
        Ui_MainWindow.button_style(self.Day_2,daily.arr[2].icon)
        Ui_MainWindow.button_style(self.Day_3,daily.arr[3].icon)
        Ui_MainWindow.button_style(self.Day_4,daily.arr[4].icon)
        self.Day_0.setText(daily.arr[0].temp)
        self.Day_1.setText(daily.arr[1].temp)
        self.Day_2.setText(daily.arr[2].temp)
        self.Day_3.setText(daily.arr[3].temp)
        self.Day_4.setText(daily.arr[4].temp)
        return
    def unit_action(self,x,metric):
        #print("Temperature Metric:", metric)
        if metric == Api.units:
            # if button pressed is the same as current metric no change
            return
        
        # else change metri, call api and load ui again
        Api.set_metric(metric)
        Api.new_search(Api.city_name)

        Ui_MainWindow.load_ui(self,Api.city_name,0,True)
        return
    
    @staticmethod
    def button_style(button,icon):
        image = "images/"+icon+ ".png"
        if icon[0:2] !='13' and icon != '01n' and icon[0:2]!='50':
                button.setStyleSheet("QToolButton{\n"
                "background-color:rgb(128, 222, 234);\n"
                "border-radius:12px;\n"
                "color:black;\n"
                "border:2px solid black;\n"
                "background-image:url(%s);\n"
                "background-repeat:no-repeat;\n"
                "background-position:center;\n"
                "\n"
                "}\n"
                "\n"
                ".QToolButton:hover{\n"
                "background-color:rgb(61, 122, 182);\n"
                "}\n"
                ""%(image))
        elif icon [0:2] == '13' or icon == "01n":
                button.setStyleSheet("QToolButton{\n"
                "background-color:rgb(128, 222, 234);\n"
                "border-radius:12px;\n"
                "color:white;\n"
                "border:2px solid black;\n"
                "background-image:url(%s);\n"
                "background-repeat:no-repeat;\n"
                "background-position:center;\n"
                "\n"
                "}\n"
                "\n"
                ".QToolButton:hover{\n"
                "background-color:rgb(61, 122, 182);\n"
                "}\n"
                ""%(image))
        else:

                button.setStyleSheet("QToolButton{\n"
                "background-color:rgb(128, 222, 234);\n"
                "border-radius:12px;\n"
                "color:#000080;\n"
                "border:2px solid black;\n"
                "background-image:url(%s);\n"
                "background-repeat:no-repeat;\n"
                "background-position:center;\n"
                "\n"
                "}\n"
                "\n"
                ".QToolButton:hover{\n"
                "background-color:rgb(61, 122, 182);\n"
                "}\n"
                ""%(image))
        return

    
    def search_action(self,ui):
        #grab search bar contents
        # attempt to search

        city = self.search.text()

        if city == "":
            # if searchbar contents empty then do nothing
            return
        # else call api and load ui
        Api.new_search(city)
        Ui_MainWindow.load_ui(self,city,0,True)
        self.city_label.setText((Api.city_name + ', '+Api.country_name))
        return
        
    def date_action(self,int,x):
        #display day contents on screen
        #print("Date ACTION",self,int,x)

        #print(weatherObject.array[0])
        city = self.city_label.text()
        Ui_MainWindow.load_ui(self,city,x,False)
        return
    
    def plot_points(self,day):
        # clear current plot
        # grab corresponding date object offset by day variable
        # 

        self.graphWidget.clear()
        date = wo.weatherObject.array[0].date
        # if day = 1; date = 1/1/2023; then date + dt.timedelta(day,0) = 1/2/2023
        date = date + dt.timedelta(day,0)
        date = date.strftime("%Y-%m-%d")

        # grab hourly temperature list of corresponding date
        list = wo.weatherObject.date_table[date]

        #grab hourly(x axis) temperature(y axis) and plot points onto QtGraph 
        hour = []
        temp = []
        for i in list: 
            t = i.date.time()
            t=t.strftime('%H')
            t = int(t)
            hour.append(t)
            temp.append(i.temp)
        self.graphWidget.plot(hour,temp)
        return

class Api:
    code=""
    key = ""
    jsonObject =""
    zip=""
    units = "imperial"  #imperial for farenheit and metric for celsius
    city_name=""
    country_name = ""
    state=""
    api_code =0

    @staticmethod
    def new_search(city):
        #grab hourly and daily data for the searched contents
        Api.hourly(city)
        Api.daily(city)
        return
        
    def hourly(city):
        # call hourly api

        if Api.key == "":
            # if key is not initialized
            # grab key from txt file
            Api.key = f.file_handler.opentxt()

        u="https://pro.openweathermap.org/data/2.5/forecast/hourly?q="+city+"&appid="+Api.key + "&units=" +Api.units
        response=requests.get(u)
        if response.status_code == 401:
            # key is invalid
            print("key invalid")
            Api.api_code= 401
            return
        jsono=response.json()
        wo.weatherObject.jsonData = jsono
        if wo.weatherObject.jsonData['cod'] == "404" or wo.weatherObject.jsonData['cod'] == "400" :
            # invalid city
            print("city not found")
            Api.code = "404"
            return False
        else:
            # api key is valid and city is valid
            # parse json
            wo.weatherObject.jsonParse()
        return jsono
    
    def daily(city):

        if Api.key == "":
            Api.key = f.file_handler.opentxt()
        u="https://api.openweathermap.org/data/2.5/forecast/daily?q="+city+"&cnt=6&appid="+ Api.key + "&units="+Api.units
        response=requests.get(u)
        if response.status_code == 401:
            return
        jsonn = response.json()
        daily.json_object=jsonn
        if daily.json_object['cod'] == "404" or daily.json_object['cod'] == "400":
            Api.code = '404'
            return False
        else:
            daily.parse_json()
        return True

    @staticmethod
    def get_metric():
        # returns current metric
        if Api.units =="imperial":
            return "F"
        elif Api.units == "metric":
            return "C"
        return "error"

    def set_metric(string):
        # if variable string is different from current metric then update current metric
        if Api.units!=string:
            Api.units = string
        return
    def date_now():
        now =dt.now()
        now = now.strftime("%b %#d")
        return 
    



class daily:
    json_object =""
    arr=[]
    city = ""

    def __init__(self,temp,id,desc,desc2,icon,humidity,wind,pop):
        self.temp = temp
        self.humidity = humidity
        self.id = id
        self.desc = desc
        self.desc2 = desc2
        self.icon = icon
        self.wind = wind
        self.pop = pop
    

    @staticmethod
    def clear():
        daily.json_object = ""
        daily.arr = []
        daily.city = ""
        wo.weatherObject.array = []
        wo.weatherObject.date_table = {}
        wo.weatherObject.table={}
        wo.weatherObject.jsonData = ""
    

    @staticmethod
    def parse_json():
        # parse json and store important data

        Api.city_name = daily.json_object["city"]["name"]
        #daily.city = daily.json_object["city"]["name"]
        daily.arr = []
        Api.city_name=daily.json_object["city"]["name"]
        Api.country_name = daily.json_object["city"]["country"]
        for i in daily.json_object["list"]:
            temp = str(round(i["temp"]["max"]))+ chr(176)+Api.get_metric()
            id = str(i["weather"][0] ["id"])
            desc = i["weather"][0]["main"]
            desc2 = i["weather"][0]["description"]
            icon = i["weather"][0]["icon"]
            humidity = str(i["humidity"])
            wind = str(round(i["speed"]))
            pop = str(int(i["pop"]*100)) + '%'
            node = daily(temp,id,desc,desc2,icon,humidity,wind,pop)
            # store all data as a daily node

            # append node to static array and call on later to retrieve
            daily.arr.append(node)
            #print(temp + "\n" + str(id) + "\n" + desc + "\n" +str(icon) + "\n" +str(humidity) + "\n" +str(wind) + "\n" +str(pop) +"\n")
            Ui_MainWindow.daily_arr = daily.arr


    def __str__(self):
        return f"\nTemp: {self.temp} \nHumidty: {self.humidity} \nDescription: {self.desc} \nDescription2: {self.desc2} \nWind: {self.wind}\n%rain:{self.pop}\nID:{self.id}\nIcon:{self.icon}"
    def __repr__(self):
                    return f"\nTemp: {self.temp} \nHumidty: {self.humidity} \nDescription: {self.desc} \nDescription2: {self.desc2} \nWind: {self.wind}\n%rain:{self.pop}\nID:{self.id}\nIcon:{self.icon}"
    

def main():
    Api.new_search("New York City")
    """
    for i in daily.arr:
        print(i,"Printing")
    #print("\n",Api.daily("Bellerose"))
    
    """
    #for keys,v in weatherObject.date_table.items():
       #print(keys)
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    if Api.api_code != 401:
        ui.setupUi(MainWindow)
        MainWindow.show()
        ui.load_ui(Api.city_name,0,True)
        sys.exit(app.exec_())

if __name__ == "__main__":
    main()
    print("main")
