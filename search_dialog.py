from PyQt6.QtWidgets import QLineEdit, QPushButton, QDialog, QVBoxLayout, QMessageBox
import sqlite3
from PyQt6.QtCore import Qt


class SearchDialog(QDialog):
    def __init__(self, tabel):
        super().__init__()
        self.table = tabel
        self.setWindowTitle("Search Student")
        self.setFixedWidth(300)
        self.setFixedHeight(300)
        layout = QVBoxLayout()

        # Add student name widget
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # Add submit button
        button = QPushButton("Search")
        button.clicked.connect(self.search_student)
        layout.addWidget(button)

        self.setLayout(layout)

    def search_student(self):
        name = self.student_name.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        result = cursor.execute('SELECT * FROM students WHERE name = ?', (name, ))
        rows = list(result)
        self.table.clearSelection()
        for row in rows:
            student_id, student_name, course, mobile_number = row
            items = self.table.findItems(student_name, Qt.MatchFlag.MatchFixedString)
            for item in items:
                row_line = item.row()
                for column in range(self.table.columnCount()):
                    self.table.item(row_line, column).setSelected(True)
        # Handle no matching records found with pop-up dialog.
        if not rows:
            msg = QMessageBox()
            msg.setWindowTitle("No Records")
            msg.setText("No matching records found")
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.exec()
        cursor.close()
        connection.close()
        self.close()
