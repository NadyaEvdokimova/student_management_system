from PyQt6.QtWidgets import QLineEdit, QPushButton, QDialog, QVBoxLayout, QComboBox
import sqlite3


class EditDialog(QDialog):
    def __init__(self, table):
        super().__init__()
        self.table = table
        self.setWindowTitle("Update Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)
        layout = QVBoxLayout()
        # Get student name from selected row
        index = self.table.currentRow()
        student_name = self.table.item(index, 1).text()
        # Get course name from selected row
        course_name = self.table.item(index, 2).text()
        # Get phone from selected row
        phone = self.table.item(index, 3).text()
        # Get id from selected row
        self.student_id = self.table.item(index, 0).text()
        # Add student name widget
        self.student_name = QLineEdit(student_name)
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # Add combo box of courses
        self.course_name = QComboBox()
        courses = ["Biology", "Math", "Astronomy", "Physics"]
        self.course_name.addItems(courses)
        self.course_name.setCurrentText(course_name)
        layout.addWidget(self.course_name)

        # Add mobile widget
        self.mobile = QLineEdit(phone)
        self.mobile.setPlaceholderText("Mobile")
        layout.addWidget(self.mobile)

        # Add submit button
        button = QPushButton("Update")
        button.clicked.connect(self.edit_student)
        layout.addWidget(button)

        self.setLayout(layout)

    def edit_student(self):
        name = self.student_name.text()
        course = self.course_name.itemText(self.course_name.currentIndex())
        mobile = self.mobile.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("UPDATE students SET name = ?, course = ?, mobile = ? WHERE id = ?",
                       (name, course, mobile, self.student_id))
        connection.commit()
        cursor.close()
        connection.close()
        self.close()
