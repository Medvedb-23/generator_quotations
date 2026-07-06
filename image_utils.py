import os
import shutil
import time
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

def copy_image_to_assets(source_path, dest_folder="assets"):
    if not source_path or not os.path.exists(source_path):
        return None
    os.makedirs(dest_folder, exist_ok=True)
    ext = os.path.splitext(source_path)[1]
    new_name = f"img_{int(time.time())}{ext}"
    dest_path = os.path.join(dest_folder, new_name)
    try:
        shutil.copy2(source_path, dest_path)
        return dest_path
    except Exception:
        return None

def load_scaled_pixmap(path, target_width, target_height):
    if not path or not os.path.exists(path):
        return None
    pixmap = QPixmap(path)
    if pixmap.isNull():
        return None
    if target_width <= 0 or target_height <= 0:
        target_width, target_height = 200, 200
    return pixmap.scaled(target_width, target_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)