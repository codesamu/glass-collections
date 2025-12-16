import sys
import os
from PyQt6.QtWidgets import QApplication, QLabel, QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
import keyboard  # pip install keyboard

class Overlay(QWidget):
    def __init__(self, texts):
        super().__init__()
        self.texts = texts
        self.index = 0

        # Fenster ohne Rahmen + immer oben + Click-Through
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool |
            Qt.WindowType.WindowTransparentForInput  # Click-Through
        )

        # Hintergrund transparent
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Fenstergröße
        self.resize(400, 200)

        # Label
        self.label = QLabel(self.texts[self.index], self)
        self.label.setFont(QFont("Arial", 32))
        self.label.setStyleSheet("color: white;")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.resize(400, 200)

        # Globale Hotkeys registrieren
        keyboard.on_press_key("right", lambda _: self.next_text())
        keyboard.on_press_key("left", lambda _: self.prev_text())
        # Neue Kombination: CTRL + ALT + E → komplette Python-Instanz beenden
        keyboard.add_hotkey("ctrl+alt+e", self.shutdown_program)

    def next_text(self):
        self.index = (self.index + 1) % len(self.texts)
        self.label.setText(self.texts[self.index])

    def prev_text(self):
        self.index = (self.index - 1) % len(self.texts)
        self.label.setText(self.texts[self.index])

    def shutdown_program(self):
        keyboard.unhook_all()   # Hotkeys entfernen
        os._exit(0)             # Sofortiges Beenden der kompletten Python-Instanz

# Liste der Texte
texts = ["Text 1", "Text 2", "Text 3", "Text 4"]

app = QApplication(sys.argv)
overlay = Overlay(texts)
overlay.show()
sys.exit(app.exec())
