from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from mongo_op import *
# from database_controller import add_note
# from settings import *


class AddNoteWindow(QMainWindow):
    def __init__(self, current_user_id, note_window):
        super().__init__()

        self.user_id = current_user_id
        self.note_window = note_window

        widget = QWidget()
        layout = QVBoxLayout()

        widget.setStyleSheet("QLabel{font-size: 20px;}"
                             "QLineEdit{font-size: 20px;}"
                             "QPushButton{font-size: 20px;}"
                             "QPlainTextEdit{font-size: 20px}")

        self.setWindowTitle('New Note')
        self.setMaximumSize(QSize(450, 400))
        self.setMinimumSize(QSize(450, 400))

        self.label = QLabel(self)
        self.label.setText('Add new note')

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText('Enter a title')

        self.text_input = QPlainTextEdit(widget)
        self.text_input.setPlaceholderText('Enter a description')

        self.add_button = QPushButton('Add Note')
        self.add_button.clicked.connect(self.add_new_note)

        layout.addWidget(self.label)

        layout.addWidget(self.title_input)
        layout.addWidget(self.text_input)

        layout.addWidget(self.add_button)

        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.title_input.setFocus()
        self.reset_fields()
        self.show()

    def add_new_note(self):
        title = self.title_input.text()
        text = self.text_input.toPlainText()
        if title == "" or text == "":
            return
        code = add_note(self.user_id, title, text)
        if code == 404:
            print("Something went wrong")

        self.note_window.creation()
        self.note_window.show()
        self.close()

    def reset_fields(self):
        self.title_input.clear()
        self.text_input.clear()