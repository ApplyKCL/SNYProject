import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QDialog, QVBoxLayout, QGridLayout
from PyQt5.QtCore import Qt, pyqtSignal

class VirtualKeyboard(QDialog):
    keyPressed = pyqtSignal(str)

    def __init__(self, parent=None):
        super(VirtualKeyboard, self).__init__(parent, Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.initUI()
        self.focused_line_edit = None
        self.setMouseTracking(True)
        self.dragPosition = None

    def set_focused_line_edit(self, line_edit):
        self.focused_line_edit = line_edit

    def initUI(self):
        self.layout = QVBoxLayout(self)
        self.button_layout = QGridLayout()

        self.caps_lock = False

        buttons = [
            ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
            ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
            ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';'],
            ['z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/'],
            ['CAPS LOCK', 'DELETE', 'SPACE', 'ENTER', 'CLOSE']
        ]

        for i, row in enumerate(buttons):
            for j, key in enumerate(row):
                button = QPushButton(key, self)
                button.clicked.connect(self.handle_key_press)
                button.setStyleSheet("""
                    QPushButton {
                        font: 12px;
                        background-color: #CCCCCC;
                        border: 1px solid black;
                        border-radius: 5px;
                    }
                    QPushButton:pressed {
                        background-color: #888888;
                    }
                """)

                if key in ['CAPS LOCK', 'DELETE', 'SPACE', 'ENTER', 'CLOSE']:
                    button.setFixedSize(110, 50)
                    self.button_layout.addWidget(button, i, j * 2, 1, 2)
                else:
                    button.setFixedSize(50, 50)
                    self.button_layout.addWidget(button, i, j)

        self.button_layout.setSpacing(5)
        self.layout.addLayout(self.button_layout)
        self.layout.setContentsMargins(10, 10, 10, 10)

    def handle_key_press(self):
        key = self.sender().text()
        if key == "CAPS LOCK":
            self.caps_lock = not self.caps_lock
            return

        if key == "SPACE":
            key = " "
        elif key == "ENTER":
            key = "\n"
        elif key == "DELETE":
            if self.focused_line_edit:
                text = self.focused_line_edit.text()
                new_text = text[:-1]
                self.focused_line_edit.setText(new_text)
            return
        elif key == "CLOSE":
            self.close()
            return
        else:
            key = key.upper() if self.caps_lock else key.lower()

        self.keyPressed.emit(key)
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.dragPosition is not None:
            self.move(event.globalPos() - self.dragPosition)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPosition = None
            event.accept()
            
    def line_edit_clicked(self, line_edit, virtual_keyboard):
        if not virtual_keyboard:
            virtual_keyboard = VirtualKeyboard()
            virtual_keyboard.set_focused_line_edit(line_edit)
            virtual_keyboard.keyPressed.connect(line_edit.insert)
            virtual_keyboard.move(self.pos().x() + 300, self.pos().y())
            virtual_keyboard.show()
        else:
            virtual_keyboard.close()
            virtual_keyboard = None
        return virtual_keyboard
