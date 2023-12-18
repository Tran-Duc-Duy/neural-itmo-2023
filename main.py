# ///////////////////////////////////////////////////////////////
#
# BY: WANDERSON M.PIMENTA
# PROJECT MADE WITH: Qt Designer and PySide6
# V: 1.0.0
#
# This project can be used freely for all uses, as long as they maintain the
# respective credits only in the Python scripts, any information in the visual
# interface (GUI) can be modified without any implication.
#
# There are limitations on Qt licenses if you want to use your products
# commercially, I recommend reading them on the official website:
# https://doc.qt.io/qtforpython/licenses.html
#
# ///////////////////////////////////////////////////////////////
import cv2
from keras.models import load_model
from keras_preprocessing.image import img_to_array
from keras.preprocessing import image
from PIL import ImageFont, ImageDraw, Image 
import numpy as np
from PySide6.QtCore import Qt, QTimer, Slot

import subprocess
import sys
import os
import platform
# import AI
from AI.emotion_demo import test
# from login_window import LoginWindow
# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////
from modules import *
from postgres_class import connectPostgreSQL
from widgets import *
os.environ["QT_FONT_DPI"] = "96" # FIX Problem for High DPI and Scale above 100%


from login import Ui_Form
from sql_class import connectMySQL

# SET AS GLOBAL WIDGETS
# ///////////////////////////////////////////////////////////////
widgets = None

class MainWindow(QMainWindow):
    def __init__(self,user_id):
        QMainWindow.__init__(self)
        self.USER_ID = user_id
        # self.mysql = connectMySQL()
        self.mysql = connectPostgreSQL()
        # SET AS GLOBAL WIDGETS
        # ///////////////////////////////////////////////////////////////
        self.ui = Ui_MainWindow()
        
        self.ui.setupUi(self)
        global widgets
        widgets = self.ui

        # USE CUSTOM TITLE BAR | USE AS "False" FOR MAC OR LINUX
        # ///////////////////////////////////////////////////////////////
        Settings.ENABLE_CUSTOM_TITLE_BAR = True


        # for AI 
        self.face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.classifier = load_model('.\emotion_detection.h5')
        self.class_labels = ['Giận dữ', 'Ghê sợ', 'Sợ hãi', 'Hạnh phúc', 'Buồn', 'Bất ngờ', 'Trung lập']
        self.font = ImageFont.truetype("./arial.ttf", 32)
        self.b, self.g, self.r, self.a = 0, 255, 0, 0
        self.cap = cv2.VideoCapture(0)
        self.is_emotion_detection_running = False
        # for AI end 
        # APP NAME
        # ///////////////////////////////////////////////////////////////
        title = "ITMO University"
        description = "Project Neural"
        # APPLY TEXTS
        self.setWindowTitle(title)
        widgets.titleRightInfo.setText(description)

        # TOGGLE MENU
        # ///////////////////////////////////////////////////////////////
        widgets.toggleButton.clicked.connect(lambda: UIFunctions.toggleMenu(self, True))

        # SET UI DEFINITIONS
        # ///////////////////////////////////////////////////////////////
        UIFunctions.uiDefinitions(self)

        # QTableWidget PARAMETERS
        # ///////////////////////////////////////////////////////////////
        widgets.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # BUTTONS CLICK
        # ///////////////////////////////////////////////////////////////

        # LEFT MENUS
        widgets.btn_home.clicked.connect(self.buttonClick)
        widgets.btn_duy.clicked.connect(self.buttonClick)
        widgets.open_camera.clicked.connect(self.toggle_emotion_detection)

        # EXTRA LEFT BOX
        def openCloseLeftBox():
            UIFunctions.toggleLeftBox(self, True)
        widgets.toggleLeftBox.clicked.connect(openCloseLeftBox)
        widgets.extraCloseColumnBtn.clicked.connect(openCloseLeftBox)

        # EXTRA RIGHT BOX
        def openCloseRightBox():
            UIFunctions.toggleRightBox(self, True)
        widgets.settingsTopBtn.clicked.connect(openCloseRightBox)

        # SHOW APP
        # ///////////////////////////////////////////////////////////////
        self.show()

        # SET CUSTOM THEME
        # ///////////////////////////////////////////////////////////////
        useCustomTheme = False
        themeFile = "themes\py_dracula_light.qss"

        # SET THEME AND HACKS
        if useCustomTheme:
            # LOAD AND APPLY STYLE
            UIFunctions.theme(self, themeFile, True)

            # SET HACKS
            AppFunctions.setThemeHack(self)

        # SET HOME PAGE AND SELECT MENU
        # ///////////////////////////////////////////////////////////////
        widgets.stackedWidget.setCurrentWidget(widgets.home)
        widgets.btn_home.setStyleSheet(UIFunctions.selectMenu(widgets.btn_home.styleSheet()))



    # AI fun
        
    @Slot()
    def toggle_emotion_detection(self):
        if not self.is_emotion_detection_running:
            self.start_emotion_detection()
        else:
            self.stop_emotion_detection()

    def start_emotion_detection(self):
        if not self.cap.isOpened():
            self.cap = cv2.VideoCapture(0)
        widgets.open_camera.setText("Pause camera")
        self.is_emotion_detection_running = True
        widgets.open_camera.clicked.disconnect()
        widgets.open_camera.clicked.connect(self.toggle_emotion_detection)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def stop_emotion_detection(self):
        if self.timer is not None:
            self.timer.stop()
            self.timer = None
        self.cap.release()
        widgets.open_camera.setText("Play camera")
        self.is_emotion_detection_running = False
        widgets.open_camera.clicked.disconnect()
        widgets.open_camera.clicked.connect(self.toggle_emotion_detection)

    def update_frame(self):
        ret, frame = self.cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        if ret:
            labels = []
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_classifier.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                roi_gray = gray[y:y+h, x:x+w]
                roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)
                roi = roi_gray.astype('float') / 255.0
                roi = img_to_array(roi)
                roi = np.expand_dims(roi, axis=0)
                preds = self.classifier.predict(roi)[0]
                label = self.class_labels[preds.argmax()]
                img_pil = Image.fromarray(frame)
                draw = ImageDraw.Draw(img_pil)
                draw.text((50, 80), label, font=self.font, fill=(self.b, self.g, self.r, self.a))
                frame = np.array(img_pil)

            height, width, channel = frame.shape
            bytes_per_line = channel * width
            image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(image)
            widgets.image_label.setPixmap
            height, width, channel = frame.shape
            bytes_per_line = channel * width
            image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(image)
            widgets.image_label.setPixmap(pixmap)

    def closeEvent(self, event):
        self.stop_emotion_detection()
        event.accept()
    # AI fun end 
        
    # BUTTONS CLICK
    # Post here your functions for clicked buttons
    # ///////////////////////////////////////////////////////////////
    def buttonClick(self):
        # GET BUTTON CLICKED
        btn = self.sender()
        btnName = btn.objectName()

        # SHOW HOME PAGE
        if btnName == "btn_home":
            widgets.stackedWidget.setCurrentWidget(widgets.home)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW WIDGETS PAGE
        # if btnName == "btn_widgets":
        #     widgets.stackedWidget.setCurrentWidget(widgets.widgets)
        #     UIFunctions.resetStyle(self, btnName)
        #     btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW NEW PAGE
        # if btnName == "btn_new":
        #     widgets.stackedWidget.setCurrentWidget(widgets.new_page) # SET PAGE
        #     UIFunctions.resetStyle(self, btnName) # RESET ANOTHERS BUTTONS SELECTED
        #     btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet())) # SELECT MENU

        # SHOW DUY PAGE
        if btnName == "btn_duy":
            widgets.stackedWidget.setCurrentWidget(widgets.duy_page) # SET PAGE
            UIFunctions.resetStyle(self, btnName) # RESET ANOTHERS BUTTONS SELECTED
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet())) # SELECT MENU

        # PRINT BTN NAME
        print(f'Button "{btnName}" pressed!')


    # RESIZE EVENTS
    # ///////////////////////////////////////////////////////////////
    def resizeEvent(self, event):
        # Update Size Grips
        UIFunctions.resize_grips(self)

    # MOUSE CLICK EVENTS
    # ///////////////////////////////////////////////////////////////
    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        self.dragPos = event.globalPos()

        # PRINT MOUSE EVENTS
        if event.buttons() == Qt.LeftButton:
            print('Mouse click: LEFT CLICK')
        if event.buttons() == Qt.RightButton:
            print('Mouse click: RIGHT CLICK')


class LoginWindow(QWidget):
    def __init__(self):
        super(LoginWindow, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self._startPos = None
        self._endPos = None
        self._tracking = False

        # self.mysql = connectMySQL()
        self.mysql = connectPostgreSQL()
        ## initialize QPushButtons in the login window.
        self.ui.backBtn.setFocusPolicy(Qt.NoFocus)
        self.ui.createBtn.setFocusPolicy(Qt.NoFocus)
        self.ui.exitBtn.setFocusPolicy(Qt.NoFocus)
        self.ui.registerBtn.setFocusPolicy(Qt.NoFocus)
        self.ui.loginBtn.setFocusPolicy(Qt.NoFocus)

        ## show login window when start app 
        self.ui.funcWidget.setCurrentIndex(0)

        ## hide the frame and background of the app 
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)


    ## Make the window movable after hide window frame ///////////////////////////
    def mouseMoveEvent(self, a0: QMouseEvent) -> None:
        if self._tracking:
            self._endPos = a0.pos() - self._startPos
            self.move(self.pos() + self._endPos)

    def mousePressEvent(self, a0: QMouseEvent) -> None:
        if a0.button() == Qt.LeftButton:
            self._startPos = QPoint(a0.x(), a0.y())
            self._tracking = True

    def mouseReleaseEvent(self, a0: QMouseEvent) -> None:
        if a0.button() == Qt.LeftButton:
            self._tracking = False
            self._startPos = None
            self._endPos = None
    ## ============================================================================


    ## login window //////////////////////////////////////////////////////////////
    @Slot()
    def on_exitBtn_clicked(self):
        """
        function for exit button
        """
        msgBox = QMessageBox(self)
        msgBox.setWindowIcon(QIcon("./static/icon/key-6-128.ico"))
        msgBox.setIconPixmap(QPixmap("./static/icon/question-mark-7-48.ico"))
        msgBox.setWindowTitle("Exit?")
        msgBox.setText("Are you sure to EXIT???")
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        reply = msgBox.exec()

        if reply == QMessageBox.Yes:
            self.close()
        else:
            return

    @Slot()
    def on_registerBtn_clicked(self):
        """
        function for going to register page
        """
        self.ui.funcWidget.setCurrentIndex(1)


    ## register window ///////////////////////////////////////////////////////////
    @Slot()
    def on_backBtn_clicked(self):
        """
        function for going back to login page from register page
        """
        self.ui.funcWidget.setCurrentIndex(0)

    @Slot()
    def on_loginBtn_clicked(self):
        """
        function for login app
        """
        username = self.ui.lineEdit.text().strip()
        password = self.ui.lineEdit_2.text().strip()

        ## check if input username and password.
        if not username and not password:
            self.warning_messagebox("Please input username and password")
            return

        ## Search and check the input account information in database.
        result = self.mysql.check_username(username=username)
        if result and len(result) == 1:
            if result[0]["password"] == password:
                user_id = result[0]["user_id"]
                # pass the user_id to main window and show it.
                main_window = MainWindow(user_id=user_id)
                main_window.show()
                self.close()
            else:
                self.warning_messagebox("Password is wrong. Please try again.")
                self.ui.lineEdit_2.clear()
        else:
            self.warning_messagebox("Username is wrong. Please try again.")
            self.ui.lineEdit.clear()
            self.ui.lineEdit_2.clear()


    @Slot()
    def on_createBtn_clicked(self):
        """
        Create a login account.
        """
        user_name = self.ui.lineEdit_3.text().strip()
        password = self.ui.lineEdit_4.text().strip()

        if user_name and password:
            ## check the username if exist in database.
            result = self.mysql.check_username(username=user_name)
            if result:
                self.warning_messagebox(content="The username is already in database. Please try another one.")
            else:
                result = self.mysql.create_login_account(user_name=user_name, password=password)
                if result:
                    content = f"Something is wrong: {result}. Please try again"
                    self.warning_messagebox(content=content)
                else:
                    ## Successfully create login account. clear input and gotiếp.
                    self.warning_messagebox(content="Successfully create login account.")

                    self.ui.lineEdit_3.clear()
                    self.ui.lineEdit_4.clear()
                    self.ui.funcWidget.setCurrentIndex(0)

                    ## Create default configuaration data for the new account
                    # get user_id
                    result_1 = self.mysql.check_username(username=user_name)
                    user_id = result_1[0]["user_id"]
                    result_2 = self.mysql.check_config_data(user_id=user_id)
                    if not result_2:
                        result_3 = self.mysql.create_config_data(user_id=user_id)
                        if result_3:
                            content = f"Something is wrong: {result_3}. Please create configuration data after login."
                            self.warning_messagebox(content=content)



    def warning_messagebox(self, content):
        """
        Common messagebox function
        """
        ## Create QMessageBox
        msgBox = QMessageBox(self)
        msgBox.setWindowIcon(QIcon("./static/icon/key-6-128.ico"))
        msgBox.setIconPixmap(QPixmap("./static/icon/exclamation-48.ico"))
        msgBox.setWindowTitle("Warning")
        msgBox.setText(content)
        msgBox.setStandardButtons(QMessageBox.Close)

        msgBox.exec_()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))
    # window = MainWindow()
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())
