import sys
from PyQt6.QtWidgets import QApplication, QLabel, QWidget
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QFont

class TransparentOverlay(QWidget):
    def __init__(self):
        super().__init__()

        # Fenster ohne Rahmen + immer im Vordergrund
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint
        )

        # Hintergrund transparent
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Fenstergröße
        self.resize(400, 200)

        # Text
        label = QLabel("Hallo Welt 👋", self)
        label.setFont(QFont("Arial", 32))
        label.setStyleSheet("color: white;")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.resize(400, 200)

        # Variable zum Verschieben
        self.drag_position = None

    # Maus gedrückt → Startpunkt merken
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    # Maus bewegen → Fenster verschieben
    def mouseMoveEvent(self, event):
        if self.drag_position and event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()

    # Maus losgelassen
    def mouseReleaseEvent(self, event):
        self.drag_position = None
        event.accept()


app = QApplication(sys.argv)
window = TransparentOverlay()
window.show()
sys.exit(app.exec())
