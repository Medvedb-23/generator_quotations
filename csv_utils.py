import csv
from PyQt5.QtWidgets import QFileDialog, QMessageBox

def export_csv(parent, db):
    file_path, _ = QFileDialog.getSaveFileName(parent, "Сохранить CSV", "", "CSV files (*.csv)")
    if not file_path:
        return
    try:
        records = db.get_all()
        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'text', 'author', 'category', 'image_path'])
            for rec in records:
                writer.writerow([
                    rec['id'],
                    rec['text'],
                    rec['author'] or '',
                    rec['category'] or '',
                    rec['image_path'] or ''
                ])
        QMessageBox.information(parent, "Успех", f"Экспортировано {len(records)} записей в {file_path}")
        parent.statusBar().showMessage(f"Экспорт в {file_path} выполнен")
    except Exception as e:
        QMessageBox.critical(parent, "Ошибка", f"Не удалось экспортировать: {e}")

def import_csv(parent, db):
    file_path, _ = QFileDialog.getOpenFileName(parent, "Выберите CSV-файл", "data/", "CSV files (*.csv)")
    if not file_path:
        return
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader, None)
            if header is None:
                QMessageBox.warning(parent, "Ошибка", "Файл пуст")
                return
            expected = ['text', 'author', 'category', 'image_path']
            if not all(col in header for col in expected):
                QMessageBox.warning(parent, "Ошибка", "Неверный формат CSV: отсутствуют нужные колонки")
                return
            idx_text = header.index('text')
            idx_author = header.index('author') if 'author' in header else -1
            idx_category = header.index('category') if 'category' in header else -1
            idx_image = header.index('image_path') if 'image_path' in header else -1

            added = 0
            skipped = 0
            for row in reader:
                if len(row) <= max(idx_text, idx_author, idx_category, idx_image):
                    continue
                text = row[idx_text].strip()
                if not text:
                    continue
                author = row[idx_author].strip() if idx_author != -1 else ''
                category = row[idx_category].strip() if idx_category != -1 else ''
                image_path = row[idx_image].strip() if idx_image != -1 else ''

                existing = db.get_all()
                duplicate = False
                for rec in existing:
                    if rec['text'].lower() == text.lower() and rec['author'].lower() == author.lower():
                        duplicate = True
                        break
                if duplicate:
                    skipped += 1
                    continue

                data = {
                    'text': text,
                    'author': author,
                    'category': category,
                    'image_path': image_path,
                    'is_fav': 0,
                    'date': ''
                }
                db.insert(data)
                added += 1

            parent._refresh_list()
            parent._load_filters()
            QMessageBox.information(parent, "Импорт завершён",
                                    f"Добавлено: {added}\nПропущено (дубликаты): {skipped}")
            parent.statusBar().showMessage(f"Импорт из {file_path}: добавлено {added}, пропущено {skipped}")
    except Exception as e:
        QMessageBox.critical(parent, "Ошибка", f"Не удалось импортировать: {e}")