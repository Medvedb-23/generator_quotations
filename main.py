import sys
import random
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QMessageBox, QListWidgetItem, QInputDialog
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QClipboard
from PyQt5.uic import loadUi
from database import DatabaseManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('main_window.ui', self)

        layout = self.centralWidget().layout()
        if layout:
            layout.setStretch(0, 1)
            layout.setStretch(1, 2)

        self.db = DatabaseManager()
        self.db.init_db()

        self._apply_styles()
        self._bind_signals()

        self._refresh_list()
        self._load_filters()

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

    def _refresh_list(self, author=None, category=None):
        self.list_quotations.clear()
        try:
            if author and author != "Все":
                records = self.db.get_by_author(author)
            elif category and category != "Все":
                records = self.db.get_by_category(category)
            else:
                records = self.db.get_all()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить данные: {e}")
            return

        for rec in records:
            item = QListWidgetItem(rec['text'])
            item.setData(Qt.UserRole, rec['id'])
            self.list_quotations.addItem(item)

        self.statusBar().showMessage(f"Загружено {len(records)} цитат")

    def _load_filters(self):
        try:
            records = self.db.get_all()
            authors = set()
            categories = set()
            for rec in records:
                if rec['author']:
                    authors.add(rec['author'])
                if rec['category']:
                    categories.add(rec['category'])

            self.combo_author.clear()
            self.combo_author.addItem("Все")
            self.combo_author.addItems(sorted(authors))

            self.combo_category.clear()
            self.combo_category.addItem("Все")
            self.combo_category.addItems(sorted(categories))
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить фильтры: {e}")

    def _on_add(self):
        text, ok = QInputDialog.getText(self, "Добавить цитату", "Введите текст цитаты:")
        if not ok or not text.strip():
            if ok:
                QMessageBox.warning(self, "Ошибка", "Текст не может быть пустым")
            return
        author, ok2 = QInputDialog.getText(self, "Автор", "Введите автора (необязательно):")
        category, ok3 = QInputDialog.getText(self, "Категория", "Введите категорию (необязательно):")
        data = {
            'text': text.strip(),
            'author': author.strip() if ok2 else '',
            'category': category.strip() if ok3 else '',
            'is_fav': 0,
            'date': '',
            'image_path': ''
        }
        try:
            self.db.insert(data)
            self._refresh_list()
            self._load_filters()
            self.statusBar().showMessage("Цитата добавлена")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить: {e}")

    def _on_edit(self):
        item = self.list_quotations.currentItem()
        if not item:
            QMessageBox.warning(self, "Внимание", "Выберите цитату для редактирования")
            return
        rec_id = item.data(Qt.UserRole)
        rec = self.db.get_by_id(rec_id)
        if not rec:
            QMessageBox.critical(self, "Ошибка", "Запись не найдена")
            return

        new_text, ok1 = QInputDialog.getText(self, "Редактировать текст", "Новый текст:", text=rec['text'])
        if not ok1:
            return
        if not new_text.strip():
            QMessageBox.warning(self, "Ошибка", "Текст не может быть пустым")
            return
        new_author, ok2 = QInputDialog.getText(self, "Автор", "Автор:", text=rec['author'] or '')
        new_category, ok3 = QInputDialog.getText(self, "Категория", "Категория:", text=rec['category'] or '')

        data = {
            'id': rec_id,
            'text': new_text.strip(),
            'author': new_author.strip() if ok2 else rec['author'],
            'category': new_category.strip() if ok3 else rec['category'],
            'is_fav': rec['is_fav'],
            'date': rec['date'],
            'image_path': rec['image_path']
        }
        try:
            self.db.update(data)
            self._refresh_list()
            self._load_filters()
            self.statusBar().showMessage("Цитата обновлена")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось обновить: {e}")

    def _on_delete(self):
        item = self.list_quotations.currentItem()
        if not item:
            QMessageBox.warning(self, "Внимание", "Выберите цитату для удаления")
            return
        reply = QMessageBox.question(
            self, "Подтверждение",
            f"Удалить цитату: '{item.text()[:50]}...'?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            rec_id = item.data(Qt.UserRole)
            try:
                self.db.delete(rec_id)
                self._refresh_list()
                self._load_filters()
                self.statusBar().showMessage("Цитата удалена")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось удалить: {e}")

    def _on_random(self):
        count = self.list_quotations.count()
        if count > 0:
            index = random.randint(0, count - 1)
            item = self.list_quotations.item(index)
            self.lbl_quotation.setText(item.text())
            self.lbl_author.setText("Автор (загрузите детали)")
            self.statusBar().showMessage("Случайная цитата")
        else:
            QMessageBox.information(self, "Информация", "Список цитат пуст")

    def _on_copy(self):
        text = self.lbl_quotation.text()
        if text and text != "Нажмите 'Случайная цитата'":
            QApplication.clipboard().setText(text)
            self.statusBar().showMessage("Цитата скопирована")
        else:
            QMessageBox.information(self, "Информация", "Нет цитаты для копирования")

    def _on_item_clicked(self, item):
        self.lbl_quotation.setText(item.text())
        rec_id = item.data(Qt.UserRole)
        try:
            rec = self.db.get_by_id(rec_id)
            if rec:
                self.lbl_author.setText(rec['author'] or "Неизвестный автор")
            else:
                self.lbl_author.setText("Автор не найден")
        except:
            self.lbl_author.setText("Автор (ошибка)")
        self.statusBar().showMessage(f"Выбрано: {item.text()[:30]}...")

    def _on_filter_changed(self):
        author = self.combo_author.currentText()
        category = self.combo_category.currentText()
        author_filter = None if author == "Все" else author
        category_filter = None if category == "Все" else category
        self._refresh_list(author_filter, category_filter)

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self, "Выход",
            "Вы уверены?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
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