from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from Windows.NotesWindow import NotesWindow
from Windows.RegistrationWindow import RegistrationWindow
from mongo_op import *

class AuthorizationWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        widget = QWidget()
        layout = QVBoxLayout()

        widget.setStyleSheet("QLabel{font-size: 20px;}"
                          "QLineEdit{font-size: 20px;}"
                          "QPushButton{font-size: 20px}")

        self.setWindowTitle('Authorization')
        self.setMaximumSize(QSize(400, 300))
        self.setMinimumSize(QSize(400, 300))

        self.label = QLabel()
        self.label.setText('AUTHORIZATION')
        self.label.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setMaximumSize(QSize(400, 70))

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Enter your username')

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText('Enter your password')

        self.submit_button = QPushButton('Login')
        self.submit_button.clicked.connect(self.submit_login_data)


        self.login_dir_button = QPushButton('Registrate')
        self.login_dir_button.clicked.connect(self.open_registration_page)

        layout.addWidget(self.label)

        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)

        layout.addWidget(self.submit_button)
        layout.addWidget(self.login_dir_button)

        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.show()

    def submit_login_data(self):
        username = self.username_input.text()
        password = self.password_input.text()

        user_id = authorize_user(username, password)

        if user_id == 404:
            print("user not founded")
            return
        if user_id == 500:
            print("Wrong password")
            return
        self.note_window = NotesWindow(user_id)
        self.close()


    def open_registration_page(self):
        self.registration_window = RegistrationWindow(self)
        self.close()