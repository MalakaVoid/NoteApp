from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from Windows.AddNoteWindow import AddNoteWindow
from mongo_op import *
from Windows.EditNoteWindow import EditNoteWindow
from Windows.DeleteRecoverWindow import DeleteRecoverWindow


class DeletedNotesWindow(QMainWindow):
    def __init__(self, current_user_id, notes_window):
        self.notes_window = notes_window
        super().__init__()
        self.user_id = current_user_id
        self.setWindowTitle(f'Deleted notes')
        self.setMaximumSize(QSize(550, 700))
        self.setMinimumSize(QSize(550, 700))
        self.search_flag = False
        self.creation()

    def creation(self):
        widget = QWidget()
        layout = QVBoxLayout()

        scroll_inner_widget = QWidget()
        scroll_layout = QVBoxLayout()
        scroll_inner_widget.setLayout(scroll_layout)
        arr = self.fill_notes()

        for each in arr:
            scroll_layout.addWidget(each)

        box_layout = QHBoxLayout()
        box_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))

        scroll = QScrollArea()
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        scroll.setWidget(scroll_inner_widget)


        button_deleted = QPushButton('Back')
        button_deleted.clicked.connect(self.deleted_notes_btn)

        layout.addWidget(scroll)
        layout.addLayout(box_layout)
        layout.addWidget(button_deleted)
        widget.setStyleSheet("QLineEdit{font-size: 20px;}"
                             "QPushButton{font-size: 20px;}")

        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.show()

    def fill_notes(self):
        user_notes = get_deleted_notes(self.user_id)

        if user_notes is None or len(user_notes) < 1:
            return []

        arr_of_buttons = []
        for note in user_notes:
            if note is not None:
                arr_of_buttons.append(self.create_note_element(note))
        return arr_of_buttons

    def create_note_element(self, note):
        note_title = note['title']

        note_creation_year = note['creation_date'].strftime('%d.%m.%Y %H:%M:%S')

        text = (f' {note_title}\n'
                f' {note_creation_year}')
        button = QPushButton(text)

        button.setStyleSheet("QPushButton { text-align: center; font: bold; font-size: 20px;}")
        button.setMinimumSize(QSize(500, 60))

        button.clicked.connect(lambda checked, arg=note: self.note_clicked(arg))
        return button


    def note_clicked(self, note):
        self.recover_window = DeleteRecoverWindow(self.user_id, note, self)
        self.close()

    def deleted_notes_btn(self):
        self.notes_window.creation()
        self.close()