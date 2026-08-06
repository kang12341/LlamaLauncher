import argparse
import os
import shutil
import sys

from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QFileDialog, QMessageBox, QVBoxLayout, QHBoxLayout,
)

APP_NAME = "LlamaLauncher"
TARGET_FILES = ("LlamaLauncher.exe",)
TARGET_DIRS = ("_internal", "llama_cpp", "lang")


def payload_base():
    if getattr(sys, "frozen", False):
        return sys._MEIPASS
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "install_stage")


def install_to(target):
    if not target:
        return "请选择安装目录"
    try:
        os.makedirs(target, exist_ok=True)
        src = payload_base()
        for name in TARGET_FILES:
            shutil.copy2(os.path.join(src, name), os.path.join(target, name))
        for name in TARGET_DIRS:
            shutil.copytree(
                os.path.join(src, name),
                os.path.join(target, name),
                dirs_exist_ok=True,
            )
        return None
    except Exception as e:
        return str(e)


def run_gui():
    app = QApplication(sys.argv)

    win = QWidget()
    win.setWindowTitle("Llama Launcher 安装程序")
    win.resize(560, 160)

    layout = QVBoxLayout(win)
    layout.addWidget(QLabel("选择安装目录："))

    default_dir = os.path.join(os.path.expanduser("~"), "LlamaLauncher")
    entry = QLineEdit(default_dir)
    layout.addWidget(entry)

    row = QHBoxLayout()
    status = QLabel("")
    layout.addWidget(status)

    def browse():
        selected = QFileDialog.getExistingDirectory(win, "选择安装目录", entry.text())
        if selected:
            entry.setText(selected)

    def do_install():
        err = install_to(entry.text().strip())
        if err:
            status.setText("安装失败：" + err)
            status.setStyleSheet("color: #c00000;")
            return
        status.setText("安装完成")
        status.setStyleSheet("color: #007000;")
        reply = QMessageBox.question(win, "安装完成", "安装完成，是否打开安装目录？")
        if reply == QMessageBox.StandardButton.Yes:
            os.startfile(entry.text().strip())

    browse_btn = QPushButton("浏览...")
    browse_btn.clicked.connect(browse)
    install_btn = QPushButton("安装")
    install_btn.clicked.connect(do_install)
    row.addWidget(browse_btn)
    row.addWidget(install_btn)
    layout.addLayout(row)

    win.show()
    app.exec()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--install-dir")
    args = parser.parse_args()
    if args.install_dir:
        err = install_to(args.install_dir)
        if err:
            print("ERROR: " + err)
            return 1
        print("OK")
        return 0
    run_gui()
    return 0


if __name__ == "__main__":
    sys.exit(main())
