from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from mongo_op import *
from Windows.NotesWindow import NotesWindow


class RegistrationWindow(QMainWindow):
    def __init__(self, auth_window):
        super().__init__()

        self.authorization_window = auth_window

        widget = QWidget()
        layout = QVBoxLayout()

        widget.setStyleSheet("QLabel{font-size: 20px;}"
                          "QLineEdit{font-size: 20px;}"
                          "QPushButton{font-size: 20px}")

        self.setWindowTitle('Registration')
        self.setMaximumSize(QSize(400, 300))
        self.setMinimumSize(QSize(400, 300))

        self.label = QLabel()
        self.label.setText('REGISTRATION')
        self.label.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setMaximumSize(QSize(400, 70))

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Enter your username')

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText('Enter your name')

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText('Enter your password')

        self.password_input_2 = QLineEdit()
        self.password_input_2.setEchoMode(QLineEdit.Password)
        self.password_input_2.setPlaceholderText('Enter your password again')

        self.submit_button = QPushButton('Submit')
        self.submit_button.clicked.connect(self.submit_registration_data)


        self.login_dir_button = QPushButton('Login')
        self.login_dir_button.clicked.connect(self.open_auth_widnow)

        layout.addWidget(self.label)

        layout.addWidget(self.name_input)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.password_input_2)
        layout.addWidget(self.submit_button)
        layout.addWidget(self.login_dir_button)

        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.show()

    def submit_registration_data(self):
        pass
        username = self.username_input.text()
        name = self.name_input.text()
        password = self.password_input.text()
        password_2 = self.password_input_2.text()

        if password != password_2:
            print("Password arent the same")
            return

        user_id = registrate_user(username, name, password)

        if user_id == 500:
            print("Username already taken")
            return
        if user_id == 404:
            print("Something went wrong")
            return

        self.note_window = NotesWindow(user_id)
        self.close()

    def open_auth_widnow(self):
        self.authorization_window.show()
        self.close()