import sys
import random

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton,
    QSlider, QHBoxLayout, QLineEdit, QMessageBox
)
from PyQt6.QtCore import Qt


class PasswordGeneratorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Random Password Generator")
        self.setGeometry(450, 200, 400, 400)

        self.setWindowIcon(QIcon('icons8-password-96.png'))

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layouts
        main_layout = QVBoxLayout()
        control_layout = QHBoxLayout()

        # Length Slider
        self.length_slider_label = QLabel("Password Length: 10")
        main_layout.addWidget(self.length_slider_label)

        self.length_slider = QSlider(Qt.Orientation.Horizontal)
        self.length_slider.setMinimum(6)
        self.length_slider.setMaximum(15)
        self.length_slider.setValue(10)
        self.length_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.length_slider.setTickInterval(1)
        self.length_slider.setSingleStep(1)
        self.length_slider.valueChanged.connect(self.update_length_label)
        main_layout.addWidget(self.length_slider)

        # Strength Slider
        self.strength_slider_label = QLabel("Password Strength: 🟢 Strong")
        main_layout.addWidget(self.strength_slider_label)

        self.strength_slider = QSlider(Qt.Orientation.Horizontal)
        self.strength_slider.setMinimum(1)
        self.strength_slider.setMaximum(4)
        self.strength_slider.setValue(2)
        self.strength_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.strength_slider.setTickInterval(1)
        self.strength_slider.setSingleStep(1)
        self.strength_slider.valueChanged.connect(self.update_strength_label)
        main_layout.addWidget(self.strength_slider)

        # Generate Button
        self.generate_button = QPushButton("Generate Password")
        self.generate_button.clicked.connect(self.generate_password)
        control_layout.addWidget(self.generate_button)

        # Copy Button
        self.copy_button = QPushButton("Copy to Clipboard")
        self.copy_button.clicked.connect(self.copy_to_clipboard)
        control_layout.addWidget(self.copy_button)

        # Reset Button
        self.reset_button = QPushButton("Reset Limits")
        self.reset_button.clicked.connect(self.reset_limits)
        control_layout.addWidget(self.reset_button)

        # Password Display
        self.label = QLabel("Generated Password:")
        main_layout.addWidget(self.label)

        self.password_display = QLineEdit()
        self.password_display.setReadOnly(True)
        main_layout.addWidget(self.password_display)

        main_layout.addLayout(control_layout)
        central_widget.setLayout(main_layout)

        # Apply CSS
        with open("style.css", "r") as f:
            self.setStyleSheet(f.read())

    def copy_to_clipboard(self):
        clipboard = QApplication.clipboard()
        if not self.password_display.text():
            self.show_popup_message("No password to copy!")
            return
        clipboard.setText(self.password_display.text())
        self.show_popup_message("Password copied to clipboard!")

    def show_popup_message(self, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setText(message)
        msg_box.setWindowTitle("Info")
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)

        # Apply custom styles
        msg_box.setStyleSheet(
            "QMessageBox {"
            "    background-color: #ffffff;"
            "    color: #000000;"
            "    border: 1px solid #cccccc;"
            "    border-radius: 10px;"
            "}"
            "QLabel {"
            "    color: #000000;"
            "}"
            "QPushButton {"
            "    background-color: #007bff;"
            "    color: #ffffff;"
            "    border: none;"
            "    border-radius: 5px;"
            "    padding: 10px;"
            "}"
            "QPushButton:hover {"
            "    background-color: #0056b3;"
            "}"
        )

        msg_box.exec()

    def update_length_label(self, value):
        self.length_slider_label.setText(f"Password Length: {value}")

    def update_strength_label(self, value):
        strength_texts = {
            1: "🔵 Weak",
            2: "🟢 Strong",
            3: "🟠 Very Strong",
            4: "🔴 Ultra Strong"
        }
        self.strength_slider_label.setText(f"Password Strength: {strength_texts[value]}")

    def generate_password(self):
        length = self.length_slider.value()
        strength = self.strength_slider.value()

        if strength == 1:
            chars = "abcdefghijklmnopqrstuvwxyz"
        elif strength == 2:
            chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        elif strength == 3:
            chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()"
        else:
            chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-=[]{}|;:,.<>?/`~"

        password = ''.join(random.choice(chars) for _ in range(length))
        self.password_display.setText(password)

    def reset_limits(self):
        self.length_slider.setValue(10)
        self.strength_slider.setValue(2)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PasswordGeneratorApp()
    window.show()
    sys.exit(app.exec())
