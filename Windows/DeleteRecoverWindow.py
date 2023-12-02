from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from mongo_op import *


class DeleteRecoverWindow(QMainWindow):
    def __init__(self, current_user_id, note, deleted_notes_window):
        super().__init__()

        self.user_id = current_user_id
        self.note = note
        self.deleted_notes_window = deleted_notes_window

        widget = QWidget()
        layout = QVBoxLayout()

        widget.setStyleSheet("QLabel{font-size: 20px; font-weight: bold;}"
                             "QLineEdit{font-size: 20px;}"
                             "QPushButton{font-size: 20px;}"
                             "QPlainTextEdit{font-size: 20px; border: none; outline: none;}")

        self.setWindowTitle(f"{self.note['title']}")
        self.setMaximumSize(QSize(450, 400))
        self.setMinimumSize(QSize(450, 400))

        self.label1 = QLabel(self)
        self.label1.setText(note['title'])

        self.label2 = QPlainTextEdit()
        self.label2.setPlainText(note['text'])
        self.label2.setReadOnly(True)

        self.recover_button = QPushButton('Recover')
        self.recover_button.clicked.connect(self.recover_note)

        self.delete_note_button = QPushButton('Delete Forever')
        self.delete_note_button.clicked.connect(self.delete_note)

        self.back_btn = QPushButton('Back')
        self.back_btn.clicked.connect(self.back_to_notes)

        # layout.addWidget(self.label)
        layout.addWidget(self.label1)
        layout.addWidget(self.label2)

        layout.addWidget(self.recover_button)
        layout.addWidget(self.delete_note_button)
        layout.addWidget(self.back_btn)

        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.show()



    def delete_note(self):
        code = delete_note_forever(self.note['_id'], self.user_id)
        if code == 404:
            print("Something went wrong")
        self.back_to_notes()

    def recover_note(self):
        code = recover_note(self.note, self.user_id)
        if code == 404:
            print("Something went wrong")
        self.back_to_notes()

    def back_to_notes(self):
        self.deleted_notes_window.creation()
        self.close()