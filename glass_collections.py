import sys
import os
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import QApplication, QLabel, QWidget
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import io
import keyboard  # pip install keyboard

# Use matplotlib's internal mathtext (no LaTeX installation needed)
from matplotlib import rc
rc('text', usetex=False)

class LatexOverlay(QWidget):
    def __init__(self, pages):
        super().__init__()
        self.pages = pages
        self.index = 0

        # Overlay window flags
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool |
            Qt.WindowType.WindowTransparentForInput  # Click-Through
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.resize(600, 300)

        # Label to display LaTeX image
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.resize(600, 300)

        # Initial display
        self.update_page()

        # Global hotkeys
        keyboard.add_hotkey("right", self.next_page)
        keyboard.add_hotkey("left", self.prev_page)
        keyboard.add_hotkey("ctrl+alt+e", self.shutdown_program)

    def render_latex(self, latex_str):
        """Render LaTeX string to a QPixmap with white text"""
        fig, ax = plt.subplots()
        fig.patch.set_alpha(0.0)  # Transparent figure background
        ax.axis('off')
        ax.text(0.5, 0.5, f"${latex_str}$", fontsize=32,
                ha='center', va='center', color='white')  # <-- White text
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=150, bbox_inches='tight', transparent=True)
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
overlay = LatexOverlay(pages)
overlay.show()
sys.exit(app.exec())
