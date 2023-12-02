from Windows.AuthorizationWindow import AuthorizationWindow
from PyQt5.QtWidgets import *
from mongo_op import *
import sys


app = QApplication(sys.argv)

login_register_window = AuthorizationWindow()

sys.exit(app.exec())

# test()