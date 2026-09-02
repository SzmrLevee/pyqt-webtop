import sys

from mysql.connector import Error
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QAbstractItemView,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from database import (
    add_note,
    delete_note,
    get_notes,
    initialize_database,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyQt5 Webtop Notes")
        self.resize(820, 560)
        self.setMinimumSize(720, 500)

        self.setStyleSheet(
            """
            QMainWindow {
                background: #f8fafc;
            }
            QLabel#TitleLabel {
                color: #0f172a;
                font-size: 28px;
                font-weight: 700;
            }
            QLabel#SubtitleLabel {
                color: #475569;
                font-size: 14px;
            }
            QLabel#StatusLabel {
                color: #334155;
                font-size: 14px;
            }
            QLineEdit {
                background: white;
                border: 1px solid #cbd5e1;
                border-radius: 10px;
                padding: 10px 12px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #2563eb;
            }
            QListWidget {
                background: white;
                border: 1px solid #cbd5e1;
                border-radius: 12px;
                padding: 6px;
            }
            QPushButton {
                background: #1d4ed8;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 10px 16px;
                font-size: 14px;
                font-weight: 600;
            }
            QPushButton:hover {
                background: #1e40af;
            }
            QPushButton:disabled {
                background: #94a3b8;
            }
            """
        )

        self.title_label = QLabel("PyQt5 Webtop Notes")
        self.title_label.setObjectName("TitleLabel")
        self.title_label.setAlignment(Qt.AlignCenter)

        self.subtitle_label = QLabel(
            "Böngészőből futó PyQt5 környezet MySQL háttértárral és phpMyAdmin támogatással."
        )
        self.subtitle_label.setObjectName("SubtitleLabel")
        self.subtitle_label.setAlignment(Qt.AlignCenter)
        self.subtitle_label.setWordWrap(True)

        self.status_label = QLabel("Adatbázis-kapcsolat ellenőrzése...")
        self.status_label.setObjectName("StatusLabel")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setWordWrap(True)

        self.note_input = QLineEdit()
        self.note_input.setPlaceholderText("Írj be egy új jegyzetet, majd mentsd el...")
        self.note_input.setMaxLength(255)
        self.note_input.setMinimumHeight(45)
        self.note_input.returnPressed.connect(self.save_note)

        self.add_button = QPushButton("Jegyzet hozzáadása")
        self.add_button.setMinimumHeight(45)
        self.add_button.clicked.connect(self.save_note)

        self.delete_button = QPushButton("Kijelölt jegyzet törlése")
        self.delete_button.setMinimumHeight(45)
        self.delete_button.clicked.connect(self.remove_selected_note)
        self.delete_button.setEnabled(False)

        self.refresh_button = QPushButton("Lista frissítése")
        self.refresh_button.setMinimumHeight(45)
        self.refresh_button.clicked.connect(self.load_notes)

        self.notes_list = QListWidget()
        self.notes_list.setSelectionMode(QAbstractItemView.SingleSelection)
        self.notes_list.setAlternatingRowColors(True)
        self.notes_list.itemSelectionChanged.connect(self.update_delete_button_state)

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.note_input)
        input_layout.addWidget(self.add_button)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.refresh_button)
        button_layout.addWidget(self.delete_button)

        layout = QVBoxLayout()
        layout.setContentsMargins(35, 35, 35, 35)
        layout.setSpacing(20)
        layout.addWidget(self.title_label)
        layout.addWidget(self.subtitle_label)
        layout.addWidget(self.status_label)
        layout.addLayout(input_layout)
        layout.addWidget(self.notes_list)
        layout.addLayout(button_layout)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.initialize_mysql()

    def initialize_mysql(self):
        try:
            initialize_database()

            self.status_label.setText("Sikeres MySQL-kapcsolat. Az alkalmazás használatra kész.")

            self.load_notes()

        except Error as error:
            self.status_label.setText("Nem sikerült kapcsolódni a MySQL adatbázishoz.")

            QMessageBox.critical(
                self,
                "MySQL kapcsolódási hiba",
                str(error),
            )

    def load_notes(self):
        try:
            self.notes_list.clear()

            notes = get_notes()

            if not notes:
                empty_item = QListWidgetItem("Nincsenek még jegyzetek. Adj hozzá egyet felül.")
                empty_item.setFlags(Qt.NoItemFlags)
                self.notes_list.addItem(empty_item)
                self.update_delete_button_state()
                return

            for note in notes:
                text = (
                    f"#{note['id']} – {note['text']} "
                    f"({note['created_at']})"
                )

                item = QListWidgetItem(text)
                item.setData(Qt.UserRole, note["id"])

                self.notes_list.addItem(item)

            self.notes_list.setCurrentRow(0)
            self.update_delete_button_state()

        except Error as error:
            QMessageBox.critical(
                self,
                "Lekérdezési hiba",
                str(error),
            )

    def save_note(self):
        text = self.note_input.text().strip()

        if not text:
            QMessageBox.warning(
                self,
                "Hiányzó adat",
                "Írj be egy jegyzetet!",
            )
            return

        try:
            add_note(text)
            self.note_input.clear()
            self.load_notes()

        except Error as error:
            QMessageBox.critical(
                self,
                "Mentési hiba",
                str(error),
            )

    def remove_selected_note(self):
        selected_item = self.notes_list.currentItem()

        if selected_item is None or selected_item.data(Qt.UserRole) is None:
            QMessageBox.warning(
                self,
                "Nincs kijelölés",
                "Jelölj ki egy törlendő jegyzetet!",
            )
            return

        note_id = selected_item.data(Qt.UserRole)

        answer = QMessageBox.question(
            self,
            "Törlés megerősítése",
            "Biztosan törölni szeretnéd a jegyzetet?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if answer != QMessageBox.Yes:
            return

        try:
            delete_note(note_id)
            self.load_notes()

        except Error as error:
            QMessageBox.critical(
                self,
                "Törlési hiba",
                str(error),
            )

    def update_delete_button_state(self):
        selected_item = self.notes_list.currentItem()
        has_selected_note = selected_item is not None and selected_item.data(Qt.UserRole) is not None
        self.delete_button.setEnabled(has_selected_note)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

sys.exit(app.exec_())