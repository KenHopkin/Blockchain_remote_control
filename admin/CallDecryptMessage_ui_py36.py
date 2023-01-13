# -*- coding: gb2312 -*-
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from DecryptMessage_ui_py36 import *
import decryptmsg_module


class MyMainWindow(QMainWindow, Ui_Form):

    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.pushButton_clicked)

    def pushButton_clicked(self):
        # encrypted message
        encrypted_message = self.lineEdit.text()
        self.printf(self.lineEdit.text())
        # secret key
        secret_key = self.lineEdit_2.text()
        self.printf(self.lineEdit_2.text())

        self.printf(decryptmsg_module.decrypt(encrypted_message.encode('ascii'), secret_key))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    myWin.show()
    sys.exit(app.exec_())