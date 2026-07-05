from database import DatabaseManager
import sys
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QListWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QClipboard
from PyQt5.uic import loadUi

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('main_window.ui', self)
        self.db = DatabaseManager()
        self.db.init_db()

        layout = self.centralWidget().layout()
        if layout:
            layout.setStretch(0, 1)
            layout.setStretch(1, 2)

        self._apply_styles()
        self._bind_signals()
        self._fill_test_data()
        self.statusBar().showMessage("Готов к работе")

    def _apply_styles(self):
        self.setStyleSheet("""
            QMainWindow { background-color: #f0f0f0; }
            QPushButton {
                background-color: #5c9ded;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #4a8bd4; }
            QPushButton:pressed { background-color: #3a7abc; }
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
        """)

    def _bind_signals(self):
        self.btn_add.clicked.connect(self._on_add)
        self.btn_edit.clicked.connect(self._on_edit)
        self.btn_delete.clicked.connect(self._on_delete)
        self.btn_random.clicked.connect(self._on_random)
        self.btn_copy.clicked.connect(self._on_copy)
        self.list_quotations.itemClicked.connect(self._on_item_clicked)
        self.combo_author.currentIndexChanged.connect(self._on_filter_changed)
        self.combo_category.currentIndexChanged.connect(self._on_filter_changed)

    def _fill_test_data(self):
        test_quotes = [
            "Жизнь — это то, что происходит, пока вы строите планы.",
            "Будьте сами собой, остальные роли уже заняты.",
            "Я мыслю, следовательно, существую.",
            "Тот, кто может изменить мир, начинает с себя."
        ]
        for quote in test_quotes:
            self.list_quotations.addItem(quote)
        self.combo_author.addItems(["Все", "Джон Леннон", "Оскар Уайльд", "Декарт"])
        self.combo_category.addItems(["Все", "Мотивация", "Философия"])

    def _on_add(self):
        print("Добавить")
        self.statusBar().showMessage("Добавление (заглушка)")

    def _on_edit(self):
        item = self.list_quotations.currentItem()
        if item:
            print(f"Редактировать: {item.text()}")
            self.statusBar().showMessage(f"Редактирование: {item.text()[:30]}...")
        else:
            QMessageBox.warning(self, "Внимание", "Выберите цитату")

    def _on_delete(self):
        item = self.list_quotations.currentItem()
        if item:
            print(f"Удалить: {item.text()}")
            self.statusBar().showMessage(f"Удаление: {item.text()[:30]}...")
        else:
            QMessageBox.warning(self, "Внимание", "Выберите цитату")

    def _on_random(self):
        count = self.list_quotations.count()
        if count > 0:
            index = random.randint(0, count - 1)
            item = self.list_quotations.item(index)
            self.lbl_quotation.setText(item.text())
            self.lbl_author.setText("Автор (заглушка)")
            self.statusBar().showMessage("Случайная цитата")
        else:
            QMessageBox.information(self, "Информация", "Список пуст")

    def _on_copy(self):
        text = self.lbl_quotation.text()
        if text and text != "Нажмите 'Случайная цитата'":
            QApplication.clipboard().setText(text)
            self.statusBar().showMessage("Цитата скопирована")
        else:
            QMessageBox.information(self, "Информация", "Нет цитаты для копирования")

    def _on_item_clicked(self, item):
        self.lbl_quotation.setText(item.text())
        self.lbl_author.setText("Автор (из списка)")
        self.statusBar().showMessage(f"Выбрано: {item.text()[:30]}...")

    def _on_filter_changed(self):
        author = self.combo_author.currentText()
        category = self.combo_category.currentText()
        print(f"Фильтр: автор={author}, категория={category}")
        self.statusBar().showMessage(f"Фильтр: {author} / {category}")

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self, "Выход",
            "Вы уверены?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            if hasattr(self, 'db'):
                self.db.close()
            event.accept()
        else:
            event.ignore()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()