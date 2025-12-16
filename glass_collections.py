import sys
import os
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import QApplication, QLabel, QWidget
from PyQt6.QtGui import QPixmap, QScreen
from PyQt6.QtCore import Qt
import io
import keyboard

# Use matplotlib internal mathtext (no LaTeX installation)
from matplotlib import rc
rc('text', usetex=False)

class LatexOverlay(QWidget):
    def __init__(self, pages, text_color="#f6f6f6"):  # Default white
        super().__init__()
        self.pages = pages
        self.index = 0
        self.text_color = text_color  # <-- Accept hex color code

        # Overlay window flags
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool |
            Qt.WindowType.WindowTransparentForInput  # Click-Through
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Window size
        self.width = 400
        self.height = 150
        self.resize(self.width, self.height)

        # Position at bottom-right corner
        screen: QScreen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()
        x = screen_geometry.width() - self.width - 20  # 20 px margin from right
        y = screen_geometry.height() - self.height - 40 # 40 px margin from bottom
        self.move(x, y)

        # Label for LaTeX image
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.resize(self.width, self.height)

        # Initial display
        self.update_page()

        # Global hotkeys
        keyboard.add_hotkey("right", self.next_page)
        keyboard.add_hotkey("left", self.prev_page)
        keyboard.add_hotkey("esc", self.shutdown_program)

    def render_latex(self, latex_str):
        """Render LaTeX string to a QPixmap with the given color (hex or name)"""
        fig, ax = plt.subplots(figsize=(self.width/100, self.height/100), dpi=100)
        fig.patch.set_alpha(0.0)  # Transparent background
        ax.axis('off')
        ax.text(0.5, 0.5, f"${latex_str}$", fontsize=24,
                ha='center', va='center', color=self.text_color)
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=100, bbox_inches='tight', transparent=True)
        plt.close(fig)
        buf.seek(0)
        pix = QPixmap()
        pix.loadFromData(buf.getvalue())
        return pix

    def update_page(self):
        latex_code = self.pages[self.index]
        pix = self.render_latex(latex_code)
        self.label.setPixmap(pix)

    def next_page(self):
        self.index = (self.index + 1) % len(self.pages)
        self.update_page()

    def prev_page(self):
        self.index = (self.index - 1) % len(self.pages)
        self.update_page()

    def shutdown_program(self):
        keyboard.unhook_all()
        os._exit(0)

# Example LaTeX pages
pages = [
    r"P \times V = \nu R T",
    r"E = m c^2",
    r"\int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}"
]

app = QApplication(sys.argv)
overlay = LatexOverlay(pages, text_color="#f6f6f6")  # <-- Hex color here
overlay.show()
sys.exit(app.exec())
