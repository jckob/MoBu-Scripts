import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi

import os
import sys

#fix pyqt5 in mobu


class Login(QDialog):
    def __init__(self):
        super(Login, self).__init__()
        ui_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "login.ui")
        loadUi(ui_path, self)
        self.loginButton.clicked.connect(self.loginfunction)


    def loginfunction(self):
        print("logged")


app = QApplication(sys.argv)
mainWindow = Login()
widget= QtWidgets.QStackedWidget()
widget.addWidget(mainWindow)
widget.setFixedHeight(480)
widget.setFixedWidth(620)

widget.show()
app.exec_()