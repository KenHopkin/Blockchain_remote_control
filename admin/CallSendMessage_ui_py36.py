# -*- coding: gb2312 -*-

# 打包的时候需要使用的命令:  pyinstaller -D CallSendMessage_ui_py36.py --collect-all websockets
#
# 打包完成后，请把与该文件同文件中的 contract.txt, contract_ABI, pwd_user.txt   放入打包后可执行文件的同个文件夹
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from SendMessage_ui_py36 import *
import sendmsg_module


class MyMainWindow(QMainWindow, Ui_Form):

    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.pushButton_clicked)

    def pushButton_clicked(self):
        # domain_id
        domain_id = self.lineEdit.text()
        self.printf(self.lineEdit.text())
        # sender_id
        sender_id = self.lineEdit_2.text()
        self.printf(self.lineEdit_2.text())
        # receiver_id
        receiver_id = self.lineEdit_3.text()
        self.printf(self.lineEdit_3.text())

        # message
        message = self.lineEdit_4.text()
        self.printf(self.lineEdit_4.text())

        flag = self.comboBox.currentIndex()
        self.printf(str(self.comboBox.currentIndex()))
        msg_sent = sendmsg_module.send_message(domain_id, sender_id, receiver_id, message, flag)
        if flag == 0:
            self.printf("密文:" + msg_sent)
        self.printf("消息发送成功")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    myWin.show()
    sys.exit(app.exec_())