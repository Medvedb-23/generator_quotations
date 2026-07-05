import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('main_window.ui', self)

        layout = self.centralWidget().layout()
        if layout is not None:
            layout.setStretch(0, 1)
            layout.setStretch(1, 2)

        self._apply_styles()

    def _apply_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QPushButton {
                background-color: #5c9ded;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4a8bd4;
            }
            QPushButton:pressed {
                background-color: #3a7abc;
            }
            QLabel#lbl_quotation {
                font-size: 16pt;
                font-weight: bold;
                color: #333;
            }
            QLabel#lbl_author {
                font-size: 12pt;
                font-style: italic;
                color: #666;
            }
            QListWidget {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 4px;
            }
            QComboBox {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 4px;
            }
            QLabel#lbl_image {
                background-color: #f5f5f5;
                border: 2px dashed #bbb;
                border-radius: 8px;
            }
        """)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()