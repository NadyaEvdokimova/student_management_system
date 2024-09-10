from PyQt6.QtWidgets import QLabel, QGridLayout, QPushButton, QDialog, QMessageBox
import sqlite3


class DeleteDialog(QDialog):
    def __init__(self, table):
        super().__init__()
        self.table = table
        self.setWindowTitle("Detete Student Data")

        layout = QGridLayout()
        confirmation = QLabel("Are you sure you want to delete?")

        # Add delete button
        yes = QPushButton("Yes")
        yes.clicked.connect(self.delete_student)
        no = QPushButton("No")
        no.clicked.connect(self.cancel)

        layout.addWidget(confirmation, 0, 0, 1, 2)
        layout.addWidget(yes, 1, 0)
        layout.addWidget(no, 1, 1)
        self.setLayout(layout)

    def delete_student(self):
        index = self.table.currentRow()
        # Get id from selected row
        student_id = self.table.item(index, 0).text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("DELETE FROM students WHERE id = ?",
                       (student_id, ))
        connection.commit()
        cursor.close()
        connection.close()
        self.close()
        confirmation_message = QMessageBox()
        confirmation_message.setWindowTitle("Success")
        confirmation_message.setText("the record was deleted successfully!")
        confirmation_message.exec()

    def cancel(self):
        self.close()
