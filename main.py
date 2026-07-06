import sys
import os
import random
import logging
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QMessageBox, QListWidgetItem,
    QInputDialog, QFileDialog, QShortcut
)
from PyQt5.QtCore import Qt, QSettings
from PyQt5.QtGui import QClipboard, QTextOption, QKeySequence
from PyQt5.uic import loadUi
from PIL import Image
from database import DatabaseManager
from styles import LIGHT_STYLESHEET, DARK_STYLESHEET
from image_utils import copy_image_to_assets, load_scaled_pixmap
from csv_utils import export_csv, import_csv

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('main_window.ui', self)

        self.actionImport.setText("Импорт CSV...\tCtrl+I")
        self.actionExport.setText("Экспорт CSV...\tCtrl+E")
        self.actionDarkTheme.setText("Тёмная тема\tCtrl+T")

        self.btn_add.setToolTip("Добавить новую цитату (Ctrl+N)")
        self.btn_edit.setToolTip("Редактировать выбранную цитату (Ctrl+Shift+E)")
        self.btn_delete.setToolTip("Удалить выбранную цитату (Delete)")
        self.btn_random.setToolTip("Показать случайную цитату (Ctrl+R)")
        self.btn_copy.setToolTip("Скопировать цитату в буфер (Ctrl+C)")
        self.btn_load_image.setToolTip("Загрузить изображение для цитаты")

        self.lbl_quotation.setWordWrapMode(QTextOption.WrapAtWordBoundaryOrAnywhere)
        self.lbl_quotation.document().setDocumentMargin(0)
        self.lbl_image.setScaledContents(False)

        layout = self.centralWidget().layout()
        if layout:
            layout.setStretch(0, 1)
            layout.setStretch(1, 2)

        self.db = DatabaseManager()
        self.db.init_db()

        self.current_image_path = None
        self.current_display_path = None

        self.settings = QSettings("MyCompany", "QuotationGenerator")
        geometry = self.settings.value("geometry")
        if geometry:
            self.restoreGeometry(geometry)

        self._apply_theme(self.settings.value("theme", "light"))

        self._bind_signals()
        self._setup_shortcuts()
        self._refresh_list()
        self._load_filters()

        self._display_image(None)
        self._set_quotation_text("Нажмите 'Случайная цитата'")
        self.statusBar().showMessage("Готов к работе")

    def _apply_theme(self, theme):
        if theme == "dark":
            self.setStyleSheet(DARK_STYLESHEET)
            self.actionDarkTheme.setChecked(True)
            self.current_theme = "dark"
        else:
            self.setStyleSheet(LIGHT_STYLESHEET)
            self.actionDarkTheme.setChecked(False)
            self.current_theme = "light"
        self.settings.setValue("theme", self.current_theme)
        if self.current_display_path:
            self._display_image(self.current_display_path)
        else:
            self._display_image(None)

    def _toggle_theme(self, checked):
        if checked:
            self._apply_theme("dark")
        else:
            self._apply_theme("light")

    def _toggle_theme_shortcut(self):
        self.actionDarkTheme.trigger()

    def _set_quotation_text(self, text):
        if text and text != "Нажмите 'Случайная цитата'":
            self.lbl_quotation.setText(f'"{text}"')
        else:
            self.lbl_quotation.setText(text)
        self.lbl_quotation.setAlignment(Qt.AlignCenter)

    def _bind_signals(self):
        self.btn_add.clicked.connect(self._on_add)
        self.btn_edit.clicked.connect(self._on_edit)
        self.btn_delete.clicked.connect(self._on_delete)
        self.btn_random.clicked.connect(self._on_random)
        self.btn_copy.clicked.connect(self._on_copy)
        self.btn_load_image.clicked.connect(self._on_load_image)
        self.actionImport.triggered.connect(lambda: import_csv(self, self.db))
        self.actionExport.triggered.connect(lambda: export_csv(self, self.db))
        self.actionDarkTheme.triggered.connect(self._toggle_theme)
        self.list_quotations.itemClicked.connect(self._on_item_clicked)
        self.combo_author.currentIndexChanged.connect(self._on_filter_changed)
        self.combo_category.currentIndexChanged.connect(self._on_filter_changed)

    def _setup_shortcuts(self):
        QShortcut(QKeySequence("Ctrl+R"), self, self._on_random)
        QShortcut(QKeySequence("Ctrl+C"), self, self._on_copy)
        QShortcut(QKeySequence("Ctrl+N"), self, self._on_add)
        QShortcut(QKeySequence("Ctrl+E"), self, lambda: export_csv(self, self.db))
        QShortcut(QKeySequence("Ctrl+I"), self, lambda: import_csv(self, self.db))
        QShortcut(QKeySequence("Delete"), self, self._on_delete)
        QShortcut(QKeySequence("Ctrl+Shift+E"), self, self._on_edit)
        QShortcut(QKeySequence("Ctrl+T"), self, self._toggle_theme_shortcut)

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
            logger.error(f"Refresh error: {e}")
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
            authors = {rec['author'] for rec in records if rec['author']}
            categories = {rec['category'] for rec in records if rec['category']}
            self.combo_author.clear()
            self.combo_author.addItem("Все")
            self.combo_author.addItems(sorted(authors))
            self.combo_category.clear()
            self.combo_category.addItem("Все")
            self.combo_category.addItems(sorted(categories))
        except Exception as e:
            logger.error(f"Load filters error: {e}")
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить фильтры: {e}")

    def _display_image(self, path):
        self.current_display_path = path
        if not path or not os.path.exists(path):
            self.lbl_image.clear()
            self.lbl_image.setText("Нет изображения")
            self.lbl_image.setAlignment(Qt.AlignCenter)
            return
        scaled = load_scaled_pixmap(path, self.lbl_image.width(), self.lbl_image.height())
        if scaled is None:
            self.lbl_image.clear()
            self.lbl_image.setText("Ошибка загрузки")
            self.lbl_image.setAlignment(Qt.AlignCenter)
            return
        self.lbl_image.setPixmap(scaled)
        self.lbl_image.setText("")
        self.lbl_image.setAlignment(Qt.AlignCenter)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.current_display_path:
            self._display_image(self.current_display_path)

    def _get_input_data(self, title, text_label, author_label, category_label, existing=None):
        if existing is not None:
            existing_dict = dict(existing)
        else:
            existing_dict = None
        default_text = existing_dict['text'] if existing_dict else ''
        default_author = existing_dict.get('author', '') if existing_dict else ''
        default_category = existing_dict.get('category', '') if existing_dict else ''

        text, ok = QInputDialog.getText(self, title, text_label, text=default_text)
        if not ok or not text.strip():
            if ok:
                QMessageBox.warning(self, "Ошибка", "Текст не может быть пустым")
            return None
        author, _ = QInputDialog.getText(self, title, author_label, text=default_author)
        category, _ = QInputDialog.getText(self, title, category_label, text=default_category)
        return {
            'text': text.strip(),
            'author': author.strip(),
            'category': category.strip()
        }

    def _on_add(self):
        data = self._get_input_data("Добавить цитату",
                                    "Введите текст цитаты:",
                                    "Автор (необязательно):",
                                    "Категория (необязательно):")
        if not data:
            return
        image_path = self.current_image_path if self.current_image_path else ""
        data['image_path'] = image_path
        data['is_fav'] = 0
        data['date'] = ''
        try:
            self.db.insert(data)
            self._refresh_list()
            self._load_filters()
            self.current_image_path = None
            self._display_image(image_path if image_path else None)
            self.statusBar().showMessage("Цитата добавлена")
        except Exception as e:
            logger.error(f"Add error: {e}")
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
        data = self._get_input_data("Редактировать цитату",
                                    "Новый текст:",
                                    "Автор:",
                                    "Категория:",
                                    existing=rec)
        if not data:
            return
        if self.current_image_path:
            new_image_path = copy_image_to_assets(self.current_image_path)
            if new_image_path is None:
                QMessageBox.warning(self, "Ошибка", "Не удалось сохранить изображение")
                new_image_path = rec['image_path']
        else:
            new_image_path = rec['image_path']
        data['id'] = rec_id
        data['image_path'] = new_image_path
        data['is_fav'] = rec['is_fav']
        data['date'] = rec['date']
        try:
            self.db.update(data)
            self._refresh_list()
            self._load_filters()
            self.current_image_path = None
            self._display_image(new_image_path if new_image_path else None)
            self.statusBar().showMessage("Цитата обновлена")
        except Exception as e:
            logger.error(f"Edit error: {e}")
            QMessageBox.critical(self, "Ошибка", f"Не удалось обновить: {e}")

    def _on_delete(self):
        item = self.list_quotations.currentItem()
        if not item:
            QMessageBox.warning(self, "Внимание", "Выберите цитату для удаления")
            return
        reply = QMessageBox.question(
            self, "Подтверждение",
            f"Удалить цитату: '{item.text()[:50]}...'?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            rec_id = item.data(Qt.UserRole)
            try:
                self.db.delete(rec_id)
                self._refresh_list()
                self._load_filters()
                self._display_image(None)
                self.statusBar().showMessage("Цитата удалена")
            except Exception as e:
                logger.error(f"Delete error: {e}")
                QMessageBox.critical(self, "Ошибка", f"Не удалось удалить: {e}")

    def _on_random(self):
        count = self.list_quotations.count()
        if count == 0:
            QMessageBox.information(self, "Информация", "Список цитат пуст")
            return
        idx = random.randint(0, count - 1)
        item = self.list_quotations.item(idx)
        self._set_quotation_text(item.text())
        rec = self.db.get_by_id(item.data(Qt.UserRole))
        if rec:
            self.lbl_author.setText(rec['author'] or "Неизвестный автор")
            self._display_image(rec['image_path'])
        else:
            self.lbl_author.setText("Автор не найден")
        self.statusBar().showMessage("Случайная цитата")

    def _on_copy(self):
        text = self.lbl_quotation.toPlainText()
        if text and text != "Нажмите 'Случайная цитата'":
            QApplication.clipboard().setText(text)
            self.statusBar().showMessage("Цитата скопирована в буфер")
        else:
            QMessageBox.information(self, "Информация", "Нет цитаты для копирования")

    def _on_load_image(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Выберите изображение", "",
            "Images (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        if not path:
            return
        try:
            Image.open(path)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Некорректный файл изображения:\n{e}")
            return
        saved_path = copy_image_to_assets(path)
        if saved_path is None:
            QMessageBox.critical(self, "Ошибка", "Не удалось сохранить изображение")
            return
        current_item = self.list_quotations.currentItem()
        if current_item is not None:
            rec_id = current_item.data(Qt.UserRole)
            rec = self.db.get_by_id(rec_id)
            if rec:
                data = dict(rec)
                data['image_path'] = saved_path
                data['id'] = rec_id
                try:
                    self.db.update(data)
                    self._refresh_list()
                    self._load_filters()
                    self._display_image(saved_path)
                    self.statusBar().showMessage(f"Изображение привязано к цитате: {os.path.basename(saved_path)}")
                    self.current_image_path = None
                    return
                except Exception as e:
                    logger.error(f"Auto-update error: {e}")
                    QMessageBox.critical(self, "Ошибка", f"Не удалось привязать изображение: {e}")
                    return
        self.current_image_path = saved_path
        self._display_image(saved_path)
        self.statusBar().showMessage(f"Загружено (для новой цитаты): {os.path.basename(saved_path)}")

    def _on_item_clicked(self, item):
        self._set_quotation_text(item.text())
        rec = self.db.get_by_id(item.data(Qt.UserRole))
        if rec:
            self.lbl_author.setText(rec['author'] or "Неизвестный автор")
            self._display_image(rec['image_path'])
        else:
            self.lbl_author.setText("Автор не найден")
        self.statusBar().showMessage(f"Выбрано: {item.text()[:30]}...")

    def _on_filter_changed(self):
        author = self.combo_author.currentText()
        category = self.combo_category.currentText()
        self._refresh_list(
            None if author == "Все" else author,
            None if category == "Все" else category
        )

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self, "Выход",
            "Вы уверены?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.settings.setValue("geometry", self.saveGeometry())
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