LIGHT_STYLESHEET = """
QMainWindow {
    background-color: #faf7f2;
}
QPushButton {
    background-color: #d48c6b;
    color: white;
    border: none;
    padding: 8px 18px;
    border-radius: 6px;
    font-weight: bold;
    font-size: 13px;
}
QPushButton:hover {
    background-color: #c47a58;
}
QPushButton:pressed {
    background-color: #b06846;
}
QTextEdit#lbl_quotation {
    color: #4a3a30;
    font-family: "Georgia", serif;
    background: transparent;
    border: none;
    line-height: 1.5;
    selection-background-color: transparent;
    padding: 0;
    margin: 0;
}
QLabel#lbl_author {
    font-size: 13pt;
    font-style: italic;
    color: #8a7a6a;
    font-family: "Georgia", serif;
}
QLabel#lbl_image {
    background-color: #f5efe8;
    border: 2px dashed #ddd6cc;
    border-radius: 12px;
}
QListWidget {
    background-color: white;
    border: 1px solid #ddd6cc;
    border-radius: 6px;
    padding: 6px;
    font-size: 12px;
    color: #3a3a3a;
    outline: none;
}
QListWidget::item {
    padding: 6px 8px;
    border-radius: 4px;
}
QListWidget::item:selected {
    background-color: #f0e6dc;
    color: #4a3a30;
}
QListWidget::item:hover {
    background-color: #f5ede6;
}
QComboBox {
    background-color: white;
    border: 1px solid #ddd6cc;
    border-radius: 4px;
    padding: 5px 8px;
    color: #3a3a3a;
    font-size: 12px;
}
QComboBox:hover {
    border-color: #d48c6b;
}
QComboBox::drop-down {
    border: none;
    width: 20px;
}
QComboBox::down-arrow {
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid #8a7a6a;
}
QStatusBar {
    background-color: #faf7f2;
    color: #6a5a4a;
    font-size: 11px;
}
QMenuBar {
    background-color: #faf7f2;
    color: #4a3a30;
}
QMenuBar::item:selected {
    background-color: #f0e6dc;
}
QMenu {
    background-color: #ffffff;
    color: #4a3a30;
}
QMenu::item:selected {
    background-color: #f0e6dc;
}
QLabel {
    color: #4a3a30;
}
QScrollBar:vertical {
    background: #f0ebe4;
    width: 12px;
    border-radius: 6px;
}
QScrollBar::handle:vertical {
    background: #d0c8bc;
    border-radius: 6px;
    min-height: 20px;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}
"""

DARK_STYLESHEET = """
QMainWindow {
    background-color: #1a1e26;
}
QPushButton {
    background-color: #5a7a9a;
    color: #f0f0f0;
    border: none;
    padding: 8px 18px;
    border-radius: 6px;
    font-weight: bold;
    font-size: 13px;
}
QPushButton:hover {
    background-color: #6a8aaa;
}
QPushButton:pressed {
    background-color: #4a6a8a;
}
QTextEdit#lbl_quotation {
    color: #f0ece0;
    font-family: "Georgia", serif;
    background: transparent;
    border: none;
    line-height: 1.5;
    selection-background-color: transparent;
    padding: 0;
    margin: 0;
}
QLabel#lbl_author {
    font-size: 13pt;
    font-style: italic;
    color: #c0b8a8;
    font-family: "Georgia", serif;
}
QLabel#lbl_image {
    background-color: #262c38;
    border: 2px dashed #4a505a;
    border-radius: 12px;
    color: #c0b8a8;
}
QListWidget {
    background-color: #262c38;
    border: 1px solid #3a4050;
    border-radius: 6px;
    padding: 6px;
    font-size: 12px;
    color: #e8e4d8;
    outline: none;
}
QListWidget::item {
    padding: 6px 8px;
    border-radius: 4px;
}
QListWidget::item:selected {
    background-color: #4a6a8a;
    color: #ffffff;
}
QListWidget::item:hover {
    background-color: #3a4050;
}
QComboBox {
    background-color: #262c38;
    border: 1px solid #3a4050;
    border-radius: 4px;
    padding: 5px 8px;
    color: #e8e4d8;
    font-size: 12px;
}
QComboBox:hover {
    border-color: #5a7a9a;
}
QComboBox::drop-down {
    border: none;
    width: 20px;
}
QComboBox::down-arrow {
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid #c0b8a8;
}
QStatusBar {
    background-color: #1a1e26;
    color: #c0b8a8;
    font-size: 11px;
}
QMenuBar {
    background-color: #1a1e26;
    color: #e8e4d8;
}
QMenuBar::item:selected {
    background-color: #262c38;
}
QMenu {
    background-color: #262c38;
    color: #e8e4d8;
}
QMenu::item:selected {
    background-color: #4a6a8a;
}
QLabel {
    color: #e8e4d8;
}
QScrollBar:vertical {
    background: #262c38;
    width: 12px;
    border-radius: 6px;
}
QScrollBar::handle:vertical {
    background: #4a505a;
    border-radius: 6px;
    min-height: 20px;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}
"""