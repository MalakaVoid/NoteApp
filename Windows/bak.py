from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from Windows.AddNoteWindow import AddNoteWindow
from mongo_op import *
# from settings import *
# from database_controller import get_user_notes, search_note
# from Windows.NewNoteWindow import NewNoteWindow
# from Windows.EditNoteWindow import EditNoteWindow


class NotesWindow(QMainWindow):
    def __init__(self, current_user_id):
        super().__init__()

        self.user_id = current_user_id

        widget = QWidget()
        layout = QVBoxLayout()

        self.setWindowTitle(f'Notes')
        self.setMaximumSize(QSize(550, 700))
        self.setMinimumSize(QSize(550, 700))

        self.scroll_inner_widget = QWidget()
        self.scroll_layout = QVBoxLayout()
        self.scroll_inner_widget.setLayout(self.scroll_layout)
        self.fill_notes()

        self.new_note_windows = list()

        box_layout = QHBoxLayout()
        box_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText('Enter text to find in note')
        self.search_input.setMinimumSize(QSize(535, 30))

        self.search_button = QPushButton('Search')
        self.search_button.clicked.connect(self.search_note)

        box_layout.addWidget(self.search_input)
        box_layout.addWidget(self.search_button)

        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.scroll.setWidget(self.scroll_inner_widget)

        self.button_send = QPushButton('Create New Note')
        self.button_send.clicked.connect(self.new_note_button_clicked)

        layout.addWidget(self.scroll)
        layout.addLayout(box_layout)
        layout.addWidget(self.button_send)

        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.show()

    def fill_notes(self):
        self.clear_scroll()
        user_notes = get_notes(self.user_id)
        if user_notes is None or len(user_notes) < 1:
            return

        for note in user_notes:
            self.create_note_element(note)

    def refill_notes(self, notes_list):
        pass
        # self.clear_scroll()
        # if notes_list is None or len(notes_list) < 1:
        #     return
        #
        # for note_document in reversed(notes_list):
        #     self.create_note_element(note_document)

    def create_note_element(self, note):
        # box_layout = QHBoxLayout()
        # box_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding))

        note_title = note['title']

        note_creation_year = note['creation_date'].strftime('%d.%m.%Y %H:%M:%S')

        text = (f' {note_title}\n'
                f' {note_creation_year}')
        button = QPushButton(text)

        button.setStyleSheet("QPushButton { text-align: center; font: bold; font-size: 20px;}")
        button.setMinimumSize(QSize(500, 60))

        button.clicked.connect(lambda checked, arg=note: self.note_clicked(arg))
        # box_layout.addWidget(button)

        # self.scroll_layout.addLayout(box_layout)
        self.scroll_layout.addWidget(button)

    def clear_scroll(self):
        # while self.scroll_layout.layout().count() > 0:
        #     self.scroll_layout.itemAt(0).widget().setParent(None)
        # for i in reversed(range(self.scroll_layout.count())):
        #     self.scroll_layout.itemAt(i).widget().setParent(None)
        self.scroll_layout = QVBoxLayout()
        self.scroll_inner_widget = QWidget()
        self.scroll_inner_widget.setLayout(self.scroll_layout)
        self.scroll.setWidget(self.scroll_inner_widget)

        # for i in reversed(range(self.scroll_layout.count())):
        #     t_layout = self.scroll_layout.itemAt(i).layout()
        #     if t_layout is not None:
        #         for j in reversed(range(t_layout.count())):
        #             widget_removed = t_layout.itemAt(j).widget()
        #             if widget_removed is not None:
        #                 widget_removed.setParent(None)
        #         t_layout.setParent(None)

    def note_clicked(self, note):
        pass
        # self.edit_note_window = EditNoteWindow(self.user_id, note, self.main_window)
        # self.edit_note_window.show()
        #
        # self.close()

    def search_note(self):
        pass
        # search_text = self.search_input_field.text()
        #
        # if len(search_text) < 1:
        #     print('Enter something to search!')
        #     self.fill_notes_scroll_widget()
        #     return
        #
        # self.search_input_field.setText('')
        #
        # notes_list = search_note(search_text, self.user_id, self.date)
        # if len(notes_list) < 1:
        #     print('Bad search request!')
        #     return
        # else:
        #     self.refill_notes(notes_list)

    def new_note_button_clicked(self):
        self.add_note_window = AddNoteWindow(self.user_id, self)
        self.close()
        # new_notes_window = NewNoteWindow(self.user_id, self.date, self.main_window)
        # self.new_note_windows.append(new_notes_window)
        #
        # self.close()
        # new_notes_window.show()