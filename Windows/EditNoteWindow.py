from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from mongo_op import *


class EditNoteWindow(QMainWindow):
    def __init__(self, current_user_id, note, notes_window):
        super().__init__()

        self.user_id = current_user_id
        self.note = note
        self.notes_window = notes_window

        widget = QWidget()
        layout = QVBoxLayout()

        widget.setStyleSheet("QLabel{font-size: 20px; font-weight: bold;}"
                             "QLineEdit{font-size: 20px;}"
                             "QPushButton{font-size: 20px;}"
                             "QPlainTextEdit{font-size: 20px}")

        self.setWindowTitle(f"{self.note['title']}")
        self.setMaximumSize(QSize(450, 400))
        self.setMinimumSize(QSize(450, 400))

        self.label = QLabel(self)
        self.label.setText('Edit note')

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText('Enter a title')

        self.text_input = QPlainTextEdit(widget)
        self.text_input.setPlaceholderText('Enter a description')

        self.save_button = QPushButton('Save Note')
        self.save_button.clicked.connect(self.save_note)

        self.delete_note_button = QPushButton('Delete Note')
        self.delete_note_button.clicked.connect(self.delete_note)

        self.back_btn = QPushButton('Back')
        self.back_btn.clicked.connect(self.back_to_notes)

        layout.addWidget(self.label)

        layout.addWidget(self.title_input)
        layout.addWidget(self.text_input)

        layout.addWidget(self.save_button)
        layout.addWidget(self.delete_note_button)
        layout.addWidget(self.back_btn)

        self.title_input.setText(f"{self.note['title']}")
        self.text_input.setPlainText(f"{self.note['text']}")

        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.show()

    def save_note(self):
        title = self.title_input.text()
        text = self.text_input.toPlainText()

        code = update_note(self.note['_id'], text, title)
        if code == 404:
            print("Somethong went wrong")

        self.setWindowTitle(f"{self.note['title']} (SAVED)")


    def delete_note(self):
        code = delete_note(self.note, self.user_id)
        if code == 404:
            print("Something went wrong")
        self.back_to_notes()


    def back_to_notes(self):
        self.notes_window.creation()
        self.close()


    def reset_fields(self):
        self.title_input.clear()
        self.text_input.clear()