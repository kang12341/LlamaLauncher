import sys
import os
import json
import re
import logging
import webbrowser
import urllib.request
from datetime import datetime
from logging.handlers import RotatingFileHandler

from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget,
                               QLineEdit, QSpinBox, QPushButton, QTextEdit,
                               QVBoxLayout, QHBoxLayout, QFileDialog, QSplitter,
                               QCheckBox, QGroupBox, QTabWidget, QLabel,
                               QComboBox, QInputDialog, QMessageBox, QGridLayout,
                               QDoubleSpinBox)
from PySide6.QtGui import QColor, QFont, QTextCursor
from PySide6.QtCore import QProcess, Qt, QTimer, QUrl

try:
    from PySide6.QtWebEngineWidgets import QWebEngineView
    WEB_ENGINE_AVAILABLE = True
except ImportError:
    WEB_ENGINE_AVAILABLE = False

from i18n import t


# ==================== QSS 深色主题样式表 ====================
DARK_STYLE = """
QMainWindow { background-color: #1e1e1e; }
QWidget {
    background-color: #1e1e1e; color: #d4d4d4;
    font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif; font-size: 14px;
}
QGroupBox {
    border: 1px solid #3c3c3c; border-radius: 6px;
    margin-top: 10px; padding-top: 15px; font-weight: bold;
}
QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 5px; }
QLineEdit, QSpinBox {
    background-color: #2d2d2d; border: 1px solid #3c3c3c;
    border-radius: 4px; padding: 6px; color: #d4d4d4;
    selection-background-color: #007acc;
}
QLineEdit:focus, QSpinBox:focus { border: 1px solid #007acc; }
QComboBox {
    background-color: #2d2d2d; border: 1px solid #3c3c3c; border-radius: 4px;
    padding: 6px 8px; color: #d4d4d4; selection-background-color: #007acc;
    min-height: 22px;
}
QComboBox:focus { border: 1px solid #007acc; }
QComboBox::drop-down {
    subcontrol-origin: padding; subcontrol-position: top right;
    width: 22px; border-left: 1px solid #3c3c3c;
    border-top-right-radius: 4px; border-bottom-right-radius: 4px;
}
QComboBox QAbstractItemView {
    background-color: #2d2d2d; border: 1px solid #3c3c3c;
    selection-background-color: #007acc; selection-color: #ffffff;
    color: #d4d4d4; outline: none; padding: 2px;
}
QComboBox QAbstractItemView::item { padding: 6px 8px; border-radius: 2px; }
QComboBox QAbstractItemView::item:hover { background-color: #094771; }
QPushButton {
    background-color: #0e639c; border: none; border-radius: 4px;
    padding: 8px 16px; color: white; font-weight: bold;
}
QPushButton:hover { background-color: #1177bb; }
QPushButton:pressed { background-color: #0d5a8a; }
QPushButton:disabled { background-color: #3c3c3c; color: #6c6c6c; }
QPushButton:checked { background-color: #1177bb; border: 1px solid #007acc; }
QPushButton#btnStop { background-color: #c53030; }
QPushButton#btnStop:hover { background-color: #e53e3e; }
QPushButton#iconBtn {
    background-color: #2d2d2d; border: 1px solid #3c3c3c; border-radius: 4px;
    padding: 0px; margin: 0px; min-width: 32px; min-height: 32px;
    max-width: 36px; max-height: 32px; color: #ffffff; font-size: 14px;
    text-align: center;
}
QPushButton#iconBtn:hover { background-color: #094771; border: 1px solid #007acc; }
QPushButton#iconBtn:pressed { background-color: #007acc; }
QPushButton#iconBtn:checked { background-color: #1177bb; border: 1px solid #007acc; }
QPushButton#iconBtn:disabled { background-color: #252526; color: #5a5a5a; border: 1px solid #2d2d2d; }
QPushButton#btnSelect {
    padding: 6px 10px;
    min-width: 80px;
    max-width: 100px;
}
QPushButton#btnSelect:hover { background-color: #1177bb; }
QPushButton#btnSelect:pressed { background-color: #0d5a8a; }
QToolBar {
    background-color: #252526; border-bottom: 1px solid #3c3c3c;
    spacing: 4px; padding: 4px;
}
QToolBar QPushButton {
    background-color: #2d2d2d; border: 1px solid #3c3c3c;
    padding: 6px 12px; font-size: 13px; color: #d4d4d4;
}
QToolBar QPushButton:hover { background-color: #094771; border: 1px solid #007acc; }
QToolBar QPushButton:checked { background-color: #1177bb; border: 1px solid #007acc; color: #ffffff; }
QTextEdit {
    background-color: #1e1e1e; border: 1px solid #3c3c3c; border-radius: 4px;
    color: #d4d4d4; font-family: 'Consolas', 'Courier New', monospace;
    font-size: 13px; padding: 5px;
}
QTabWidget::pane { border: 1px solid #3c3c3c; border-radius: 4px; }
QTabBar::tab {
    background-color: #2d2d2d; border: 1px solid #3c3c3c; border-bottom: none;
    border-top-left-radius: 4px; border-top-right-radius: 4px;
    padding: 8px 20px; margin-right: 2px;
}
QTabBar::tab:selected {
    background-color: #1e1e1e; border-bottom: 2px solid #007acc; color: #ffffff;
}
QCheckBox { spacing: 8px; }
QCheckBox::indicator {
    width: 16px; height: 16px; border-radius: 3px;
    border: 1px solid #3c3c3c; background-color: #2d2d2d;
}
QCheckBox::indicator:checked { background-color: #007acc; border: 1px solid #007acc; }
QSplitter::handle { background-color: #3c3c3c; width: 2px; }
QSpinBox::up-button, QSpinBox::down-button {
    subcontrol-origin: border; width: 0px; height: 0px; border: none;
}
QSpinBox::up-arrow, QSpinBox::down-arrow { width: 0; height: 0; }
"""




LOG_FILE = "llama_launcher_log.txt"
LOG_MAX_BYTES = 1024 * 1024
LOG_BACKUP_COUNT = 1


def _setup_file_logger(log_file=None, max_bytes=None, backup_count=None):
    """配置日志落盘：单文件 1MB，溢出后轮转为 .1 备份"""
    if log_file is None:
        log_file = LOG_FILE
    if max_bytes is None:
        max_bytes = LOG_MAX_BYTES
    if backup_count is None:
        backup_count = LOG_BACKUP_COUNT
    logger = logging.getLogger("llama_launcher_file")
    if getattr(logger, "_file_handler_ready", False):
        return logger
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = RotatingFileHandler(
        log_file, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    logger.addHandler(handler)
    logger._file_handler_ready = True
    return logger


def _app_dir():
    """exe 打包后以 exe 所在目录为基准，开发时以脚本目录为基准"""
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


class LlamaLauncher(QMainWindow):
    CONFIG_PATH = "config.json"
    SUPPORTED_LANGS = ["zh_CN", "en_US"]

    def __init__(self):
        super().__init__()
        self.process = QProcess()
        self.raw_logs = []
        self.is_service_running = False

        # 多模型
        self.models = []
        self.active_model_index = -1
        self.show_model_path = False
        self.show_chat_panel = True
        self._loading_config = False

        # 语言
        self.lang = "zh_CN"

        # 进程信号
        self.process.readyReadStandardOutput.connect(self.on_stdout)
        self.process.readyReadStandardError.connect(self.on_stderr)
        self.process.finished.connect(self.on_process_exit)
        self._stop_timer = QTimer(self)
        self._stop_timer.setSingleShot(True)
        self._stop_timer.timeout.connect(self.kill_process)

        self.show_line_num = True
        self._chat_mode = "waiting"
        self._file_logger = _setup_file_logger()
        self._tokens_per_sec = 0.0
        self._prompt_tokens = 0
        self._eval_tokens = 0
        self._ctx_tokens = 0
        self._active_ctx = 0
        self._metrics_available = False
        self._last_predicted_tokens = None
        self._last_predicted_seconds = 0.0
        self._stats_timer = QTimer(self)
        self._stats_timer.setInterval(1500)
        self._stats_timer.timeout.connect(self.fetch_stats)
        self._metrics_fetch_failed = False

        self.init_ui()
        self.load_config()
        self.apply_language()
        self.update_model_buttons_state()
        self.apply_path_visibility()
        self.validate_models()
        self.apply_chat_visibility()

    # ==================== 多语言 ====================
    def apply_language(self):
        """刷新所有 UI 文本为当前语言"""
        self.setWindowTitle(t("window_title", self.lang))

        # 顶部
        self.title_label.setText(t("window_title", self.lang))
        self.btn_toggle_chat.setText(
            t("chat_hide" if self.show_chat_panel else "chat_show", self.lang))
        self.btn_toggle_chat.setToolTip(
            t("chat_hide_tooltip" if self.show_chat_panel else "chat_show_tooltip", self.lang))
        self.lbl_status.setText(t("status_idle", self.lang))
        self.lbl_status.setStyleSheet(
            "color: #6c6c6c; padding: 0 12px; font-weight: bold;")

        # 配置区
        self.config_group.setTitle(t("config_group", self.lang))
        self.lbl_exe.setText(t("llama_server", self.lang))
        self.lbl_model_select.setText(t("model_select", self.lang))
        self.lbl_model_path_label.setText(t("model_path", self.lang))
        self.lbl_params.setText(t("params_group", self.lang))
        self.lbl_ngl.setText(t("ngl_label", self.lang))
        self.lbl_ctx.setText(t("ctx_label", self.lang))
        self.lbl_port.setText(t("port_label", self.lang))
        self.lbl_temp.setText(t("temp_label", self.lang))
        self.lbl_top_p.setText(t("top_p_label", self.lang))
        self.lbl_seed.setText(t("seed_label", self.lang))
        self.lbl_threads.setText(t("threads_label", self.lang))

        # 按钮
        self.btn_select_exe.setText(t("btn_browse", self.lang))
        self.btn_add_model.setText(t("btn_add_model", self.lang))
        self.btn_add_model.setToolTip(t("tip_add_model", self.lang))
        self.btn_del_model.setText(t("btn_del_model", self.lang))
        self.btn_del_model.setToolTip(t("tip_del_model", self.lang))
        self.btn_toggle_path.setText(
            t("btn_path_hide" if self.show_model_path else "btn_toggle_path", self.lang))
        self.btn_toggle_path.setToolTip(
            t("tip_path_hide" if self.show_model_path else "tip_toggle_path", self.lang))

        self.btn_start.setText(t("btn_start", self.lang))
        self.btn_stop.setText(t("btn_stop", self.lang))
        self.btn_open_webui.setText(t("btn_open_webui", self.lang))
        self.chk_lineno.setText(t("chk_show_lineno", self.lang))

        # Tab
        self.tabs.setTabText(0, t("tab_log_settings", self.lang))
        self.right_header.setText(t("tab_chat", self.lang))

        # 语言下拉框
        self.lang_combo.blockSignals(True)
        self.lang_combo.setCurrentText(self.lang)
        self.lang_combo.blockSignals(False)
        self.lbl_lang.setText(t("lang_label", self.lang))
        self.refresh_stats_labels()

        # 聊天占位
        if WEB_ENGINE_AVAILABLE:
            self.apply_chat_placeholder(self._chat_mode)
        else:
            self.chat_fallback.setText(
                t("chat_no_engine_title", self.lang) + "\n" +
                t("chat_no_engine_text", self.lang))

    def apply_chat_placeholder(self, mode="waiting"):
        """刷新聊天面板占位 HTML；running 时保留已加载的 WebUI"""
        if not WEB_ENGINE_AVAILABLE:
            return
        self._chat_mode = mode
        if mode == "running":
            return
        if mode == "waiting":
            title = t("chat_waiting_title", self.lang)
            text = t("chat_waiting_text", self.lang)
        elif mode == "loading":
            title = t("chat_loading_title", self.lang)
            text = t("chat_loading_text", self.lang)
        elif mode == "stopped":
            title = t("chat_stopped_title", self.lang)
            text = t("chat_stopped_text", self.lang)
        else:
            return
        self.web_view.setHtml(f"""
        <div style="display:flex; justify-content:center; align-items:center; height:100vh; background:#1e1e1e; color:#888; font-family:sans-serif;">
            <div style="text-align:center;">
                <h2>{title}</h2>
                <p>{text}</p>
            </div>
        </div>
        """)

    def on_lang_changed(self, lang):
        if lang != self.lang:
            self.lang = lang
            self.apply_language()
            self.save_config()

    # ==================== UI 构造 ====================
    def make_icon_btn(self, parent_layout, text, tooltip, slot, checkable=False):
        b = QPushButton(text)
        b.setObjectName("iconBtn")
        b.setFixedSize(36, 32)
        b.setToolTip(tooltip)
        b.setCheckable(checkable)
        b.setCursor(Qt.CursorShape.PointingHandCursor)
        b.clicked.connect(slot)
        parent_layout.addWidget(b)
        return b

    def init_ui(self):
        # ========== 顶部工具栏 ==========
        toolbar = QWidget()
        toolbar.setFixedHeight(44)
        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(8, 4, 8, 4)
        toolbar_layout.setSpacing(6)

        self.title_label = QLabel()
        self.title_label.setStyleSheet("""
            QLabel { color: #ffffff; font-size: 14px; font-weight: bold;
                     padding: 0 12px; border-right: 1px solid #3c3c3c; }
        """)
        toolbar_layout.addWidget(self.title_label)

        self.btn_toggle_chat = QPushButton()
        self.btn_toggle_chat.setCheckable(True)
        self.btn_toggle_chat.setChecked(True)
        self.btn_toggle_chat.setFixedHeight(32)
        self.btn_toggle_chat.toggled.connect(self.on_chat_visibility_toggled)
        toolbar_layout.addWidget(self.btn_toggle_chat)

        self.lbl_lang = QLabel()
        toolbar_layout.addWidget(self.lbl_lang)

        self.lang_combo = QComboBox()
        self.lang_combo.addItems(self.SUPPORTED_LANGS)
        self.lang_combo.setFixedSize(90, 32)
        self.lang_combo.currentTextChanged.connect(self.on_lang_changed)
        toolbar_layout.addWidget(self.lang_combo)

        toolbar_layout.addStretch()

        self.lbl_status = QLabel()
        self.lbl_status.setStyleSheet("color: #6c6c6c; padding: 0 12px; font-weight: bold;")
        toolbar_layout.addWidget(self.lbl_status)

        # ========== 中心 ==========
        center_widget = QWidget()
        self.setCentralWidget(center_widget)
        main_layout = QVBoxLayout(center_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addWidget(toolbar)

        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
        content_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.addWidget(content_widget, stretch=1)

        # ========== 左侧 ==========
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 5, 0)

        # 用 GridLayout 替代 QFormLayout，精确控制每行 input 起点
        self.config_group = QGroupBox()
        grid = QGridLayout(self.config_group)
        grid.setHorizontalSpacing(10)
        grid.setVerticalSpacing(10)
        grid.setContentsMargins(12, 18, 12, 12)

        LABEL_MIN_WIDTH = 130

        # Row 0: llama-server
        self.lbl_exe = QLabel()
        self.lbl_exe.setMinimumWidth(LABEL_MIN_WIDTH)
        self.lbl_exe.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.edit_exe = QLineEdit()
        self.edit_exe.setMinimumWidth(200)
        self.btn_select_exe = QPushButton()
        self.btn_select_exe.setObjectName("btnSelect")
        self.btn_select_exe.setFixedSize(90, 32)
        self.btn_select_exe.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_select_exe.clicked.connect(self.select_exe_file)

        grid.addWidget(self.lbl_exe, 0, 0, Qt.AlignmentFlag.AlignRight)
        grid.addWidget(self.edit_exe, 0, 1)
        grid.addWidget(self.btn_select_exe, 0, 2)

        # Row 1: 模型选择
        self.lbl_model_select = QLabel()
        self.lbl_model_select.setMinimumWidth(LABEL_MIN_WIDTH)
        self.lbl_model_select.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        model_row = QWidget()
        model_row_layout = QHBoxLayout(model_row)
        model_row_layout.setContentsMargins(0, 0, 0, 0)
        model_row_layout.setSpacing(4)

        self.model_combo = QComboBox()
        self.model_combo.setMinimumWidth(180)
        self.model_combo.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)
        self.model_combo.currentIndexChanged.connect(self.on_model_changed)
        model_row_layout.addWidget(self.model_combo, stretch=1)

        self.btn_add_model = self.make_icon_btn(model_row_layout, "➕", "", self.add_model)
        self.btn_del_model = self.make_icon_btn(model_row_layout, "🗑", "", self.delete_model)
        self.btn_toggle_path = self.make_icon_btn(
            model_row_layout, "👁", "", self.on_path_visibility_toggled, checkable=True)

        grid.addWidget(self.lbl_model_select, 1, 0, Qt.AlignmentFlag.AlignRight)
        grid.addWidget(model_row, 1, 1, 1, 2)

        # Row 2: 模型地址
        self.lbl_model_path_label = QLabel()
        self.lbl_model_path_label.setMinimumWidth(LABEL_MIN_WIDTH)
        self.lbl_model_path_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        self.lbl_model_path = QLabel()
        self.lbl_model_path.setStyleSheet("""
            QLabel {
                color: #9cdcfe; background-color: #252526;
                border: 1px solid #3c3c3c; border-radius: 4px;
                padding: 6px 8px; font-family: 'Consolas', 'Courier New', monospace;
                font-size: 12px;
            }
        """)
        self.lbl_model_path.setWordWrap(True)
        self.lbl_model_path.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.lbl_model_path.setMinimumHeight(32)
        self.lbl_model_path.hide()

        grid.addWidget(self.lbl_model_path_label, 2, 0,
                       Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
        grid.addWidget(self.lbl_model_path, 2, 1, 1, 2)

        # Row 3: 参数 + 按钮
        self.lbl_params = QLabel()
        self.lbl_params.setMinimumWidth(LABEL_MIN_WIDTH)
        self.lbl_params.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        # 内部子布局
        self.sp_ngl = QSpinBox()
        self.sp_ngl.setRange(0, 99)
        self.sp_ngl.setValue(20)
        self.sp_ngl.setMinimumWidth(90)
        self.sp_ngl.setFixedHeight(32)
        self.sp_ngl.valueChanged.connect(self.on_settings_changed)

        self.sp_ctx = QSpinBox()
        self.sp_ctx.setRange(128, 65536)
        self.sp_ctx.setValue(2048)
        self.sp_ctx.setMinimumWidth(90)
        self.sp_ctx.setFixedHeight(32)
        self.sp_ctx.valueChanged.connect(self.on_settings_changed)

        self.edit_port = QLineEdit("8080")
        self.edit_port.setMaximumWidth(120)
        self.edit_port.setFixedHeight(32)
        self.edit_port.textChanged.connect(self.on_settings_changed)

        self.sp_temp = QDoubleSpinBox()
        self.sp_temp.setRange(0.0, 2.0)
        self.sp_temp.setDecimals(2)
        self.sp_temp.setSingleStep(0.1)
        self.sp_temp.setValue(0.8)
        self.sp_temp.setMinimumWidth(90)
        self.sp_temp.setFixedHeight(32)
        self.sp_temp.valueChanged.connect(self.on_settings_changed)

        self.sp_top_p = QDoubleSpinBox()
        self.sp_top_p.setRange(0.0, 1.0)
        self.sp_top_p.setDecimals(2)
        self.sp_top_p.setSingleStep(0.05)
        self.sp_top_p.setValue(0.95)
        self.sp_top_p.setMinimumWidth(90)
        self.sp_top_p.setFixedHeight(32)
        self.sp_top_p.valueChanged.connect(self.on_settings_changed)

        self.sp_seed = QSpinBox()
        self.sp_seed.setRange(-1, 2147483647)
        self.sp_seed.setValue(-1)
        self.sp_seed.setMinimumWidth(90)
        self.sp_seed.setFixedHeight(32)
        self.sp_seed.valueChanged.connect(self.on_settings_changed)

        self.sp_threads = QSpinBox()
        self.sp_threads.setRange(0, 128)
        self.sp_threads.setValue(0)
        self.sp_threads.setMinimumWidth(90)
        self.sp_threads.setFixedHeight(32)
        self.sp_threads.valueChanged.connect(self.on_settings_changed)

        self.lbl_ngl = QLabel()
        self.lbl_ngl.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.lbl_ctx = QLabel()
        self.lbl_ctx.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.lbl_port = QLabel()
        self.lbl_port.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.lbl_temp = QLabel()
        self.lbl_temp.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.lbl_top_p = QLabel()
        self.lbl_top_p.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.lbl_seed = QLabel()
        self.lbl_seed.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.lbl_threads = QLabel()
        self.lbl_threads.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        param_widget = QWidget()
        param_layout = QGridLayout(param_widget)
        param_layout.setContentsMargins(0, 0, 0, 0)
        param_layout.setHorizontalSpacing(10)
        param_layout.setVerticalSpacing(6)
        param_layout.addWidget(self.lbl_ngl, 0, 0, Qt.AlignmentFlag.AlignRight)
        param_layout.addWidget(self.sp_ngl, 0, 1)
        param_layout.addWidget(self.lbl_ctx, 0, 2, Qt.AlignmentFlag.AlignRight)
        param_layout.addWidget(self.sp_ctx, 0, 3)
        param_layout.addWidget(self.lbl_port, 1, 0, Qt.AlignmentFlag.AlignRight)
        param_layout.addWidget(self.edit_port, 1, 1)
        param_layout.addWidget(self.lbl_temp, 1, 2, Qt.AlignmentFlag.AlignRight)
        param_layout.addWidget(self.sp_temp, 1, 3)
        param_layout.addWidget(self.lbl_top_p, 2, 0, Qt.AlignmentFlag.AlignRight)
        param_layout.addWidget(self.sp_top_p, 2, 1)
        param_layout.addWidget(self.lbl_seed, 2, 2, Qt.AlignmentFlag.AlignRight)
        param_layout.addWidget(self.sp_seed, 2, 3)
        param_layout.addWidget(self.lbl_threads, 3, 0, Qt.AlignmentFlag.AlignRight)
        param_layout.addWidget(self.sp_threads, 3, 1)
        param_layout.setColumnStretch(1, 1)
        param_layout.setColumnStretch(3, 1)

        self.btn_start = QPushButton()
        self.btn_start.setObjectName("btnStart")
        self.btn_start.setFixedHeight(32)
        self.btn_start.clicked.connect(self.start_server)

        self.btn_stop = QPushButton()
        self.btn_stop.setObjectName("btnStop")
        self.btn_stop.setFixedHeight(32)
        self.btn_stop.clicked.connect(self.stop_server)
        self.btn_stop.setEnabled(False)

        self.btn_open_webui = QPushButton()
        self.btn_open_webui.setFixedHeight(32)
        self.btn_open_webui.clicked.connect(self.open_webui_browser)
        self.btn_open_webui.setEnabled(False)

        btn_widget = QWidget()
        btn_layout = QVBoxLayout(btn_widget)
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_layout.setSpacing(6)
        btn_layout.addWidget(self.btn_start)
        btn_layout.addWidget(self.btn_stop)
        btn_layout.addWidget(self.btn_open_webui)

        pab_layout = QHBoxLayout()
        pab_layout.setContentsMargins(0, 0, 0, 0)
        pab_layout.setSpacing(10)
        pab_layout.addWidget(param_widget, stretch=1)
        pab_layout.addWidget(btn_widget, stretch=1)
        pab_widget = QWidget()
        pab_widget.setLayout(pab_layout)
        pab_widget.setMinimumHeight(170)

        grid.addWidget(self.lbl_params, 3, 0,
                       Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
        grid.addWidget(pab_widget, 3, 1, 1, 2)

        # 关键：固定标签列宽度
        grid.setColumnMinimumWidth(0, LABEL_MIN_WIDTH)
        grid.setColumnStretch(0, 0)
        grid.setColumnStretch(1, 1)
        grid.setColumnStretch(2, 0)

        left_layout.addWidget(self.config_group)

        # ========== 日志设置 Tab ==========
        self.tabs = QTabWidget()
        tab_log_settings = QWidget()
        tab_log_settings_layout = QVBoxLayout(tab_log_settings)

        self.chk_lineno = QCheckBox()
        self.chk_lineno.setChecked(self.show_line_num)
        self.chk_lineno.clicked.connect(self.toggle_line_num)

        tab_log_settings_layout.addWidget(self.chk_lineno)
        tab_log_settings_layout.addStretch()

        self.tabs.addTab(tab_log_settings, "")

        self.stats_widget = QWidget()
        stats_layout = QHBoxLayout(self.stats_widget)
        stats_layout.setContentsMargins(8, 0, 8, 0)
        stats_layout.setSpacing(12)
        self.lbl_stat_tps = QLabel()
        self.lbl_stat_tps.setStyleSheet("color: #9cdcfe; font-size: 12px;")
        stats_layout.addWidget(self.lbl_stat_tps)
        self.tabs.setCornerWidget(self.stats_widget, Qt.Corner.TopRightCorner)

        left_layout.addWidget(self.tabs)

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        left_layout.addWidget(self.log_text, stretch=1)

        # ========== 右侧聊天 ==========
        self.right_panel = QWidget()
        right_layout = QVBoxLayout(self.right_panel)
        right_layout.setContentsMargins(5, 0, 0, 0)

        self.right_header = QLabel()
        self.right_header.setStyleSheet(
            "font-size: 16px; font-weight: bold; color: #ffffff; padding: 5px;")
        right_layout.addWidget(self.right_header)

        if WEB_ENGINE_AVAILABLE:
            self.web_view = QWebEngineView()
            right_layout.addWidget(self.web_view, stretch=1)
        else:
            fallback = QLabel()
            fallback.setAlignment(Qt.AlignmentFlag.AlignCenter)
            fallback.setStyleSheet("color: #d83030; font-size: 16px;")
            right_layout.addWidget(fallback)
            self.chat_fallback = fallback

        # ========== 分割器 ==========
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.splitter.addWidget(left_panel)
        self.splitter.addWidget(self.right_panel)
        self.splitter.setSizes([450, 830])
        self.splitter.setStretchFactor(0, 1)
        self.splitter.setStretchFactor(1, 2)
        self.splitter.setCollapsible(0, False)
        self.splitter.setCollapsible(1, True)
        content_layout.addWidget(self.splitter)

    # ==================== 状态管理 ====================
    def set_ui_state(self, state):
        if state == "idle":
            self.is_service_running = False
            self.btn_start.setEnabled(True)
            self.btn_stop.setEnabled(False)
            self.btn_open_webui.setEnabled(False)
            self.edit_exe.setEnabled(True)
            self.lbl_status.setText(t("status_idle", self.lang))
            self.lbl_status.setStyleSheet("color: #6c6c6c; padding: 0 12px; font-weight: bold;")
        elif state == "starting":
            self.is_service_running = True
            self.btn_start.setEnabled(False)
            self.btn_stop.setEnabled(True)
            self.btn_open_webui.setEnabled(False)
            self.edit_exe.setEnabled(False)
            self.lbl_status.setText(t("status_starting", self.lang))
            self.lbl_status.setStyleSheet("color: #d7ba7d; padding: 0 12px; font-weight: bold;")
        elif state == "running":
            self.is_service_running = True
            self.btn_start.setEnabled(False)
            self.btn_stop.setEnabled(True)
            self.btn_open_webui.setEnabled(True)
            self.lbl_status.setText(t("status_running", self.lang))
            self.lbl_status.setStyleSheet("color: #4ec9b0; padding: 0 12px; font-weight: bold;")
        if state == "running":
            self._stats_timer.start()
        else:
            self._stats_timer.stop()
        self.update_model_buttons_state()

    # ==================== 聊天面板 ====================
    def on_chat_visibility_toggled(self, checked):
        self.show_chat_panel = checked
        self.apply_chat_visibility()
        self.apply_language()
        if not self._loading_config:
            self.save_config()

    def apply_chat_visibility(self):
        if self.show_chat_panel:
            self.btn_toggle_chat.setChecked(True)
            if self.right_panel.parent() is None:
                self.splitter.addWidget(self.right_panel)
                self.splitter.setSizes([450, 830])
            self.right_panel.show()
        else:
            self.btn_toggle_chat.setChecked(False)
            self.right_panel.setParent(None)
            self.right_panel.hide()

    # ==================== 模型管理 ====================
    def add_model(self):
        if self.is_service_running:
            QMessageBox.warning(self, t("warn_running", self.lang),
                                t("warn_running_model", self.lang))
            return
        path, _ = QFileDialog.getOpenFileName(
            self, t("file_choose_model", self.lang),
            filter=t("filter_gguf", self.lang))
        if not path:
            return
        for m in self.models:
            if m["path"] == path:
                QMessageBox.information(self, t("info_duplicate", self.lang),
                                        t("info_duplicate_text", self.lang, name=m["name"]))
                self.model_combo.setCurrentIndex(self.models.index(m))
                return
        default_name = os.path.splitext(os.path.basename(path))[0]
        name, ok = QInputDialog.getText(
            self, t("input_name_title", self.lang),
            t("input_name_prompt", self.lang), text=default_name)
        if not ok:
            return
        if not name.strip():
            name = default_name
        new_model = {
            "name": name.strip(), "path": path,
            "ngl": self.sp_ngl.value(), "ctx": self.sp_ctx.value(),
            "port": self.current_port(),
            "temp": self.sp_temp.value(),
            "top_p": self.sp_top_p.value(),
            "seed": self.sp_seed.value(),
            "threads": self.sp_threads.value(),
        }
        self.models.append(new_model)
        size_str = self._format_size(path)
        self.model_combo.addItem(name.strip() + size_str)
        self.model_combo.setCurrentIndex(len(self.models) - 1)
        self.log(t("log_model_imported", self.lang, name=name.strip(), path=path), is_error=False)
        self.update_model_buttons_state()
        self.save_config()

    def delete_model(self):
        if self.active_model_index < 0 or not self.models:
            return
        if self.is_service_running:
            QMessageBox.warning(self, t("warn_running", self.lang),
                                t("warn_running_delete", self.lang))
            return
        model = self.models[self.active_model_index]
        reply = QMessageBox.question(
            self, t("confirm_delete_title", self.lang),
            t("confirm_delete_text", self.lang, name=model['name'], path=model['path']),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No)
        if reply != QMessageBox.StandardButton.Yes:
            return
        del self.models[self.active_model_index]
        self.model_combo.removeItem(self.active_model_index)
        if not self.models:
            self.active_model_index = -1
            self.model_combo.setCurrentIndex(-1)
        else:
            new_idx = min(self.active_model_index, len(self.models) - 1)
            self.model_combo.setCurrentIndex(new_idx)
        self.log(t("log_model_deleted", self.lang, name=model['name']), is_error=False)
        self.update_model_buttons_state()
        self.save_config()

    def apply_model_settings(self, index):
        """把模型保存的参数同步到 UI，不写配置、不打日志"""
        if index < 0 or index >= len(self.models):
            return
        model = self.models[index]
        self._loading_config = True
        try:
            self.sp_ngl.setValue(int(model.get("ngl", 20)))
            self.sp_ctx.setValue(int(model.get("ctx", 2048)))
            self.edit_port.setText(str(model.get("port", "8080")))
            self.sp_temp.setValue(float(model.get("temp", 0.8)))
            self.sp_top_p.setValue(float(model.get("top_p", 0.95)))
            self.sp_seed.setValue(int(model.get("seed", -1)))
            self.sp_threads.setValue(int(model.get("threads", 0)))
        finally:
            self._loading_config = False
        self.apply_path_visibility()

    def on_model_changed(self, index):
        if self._loading_config:
            return
        if index < 0 or index >= len(self.models):
            self.active_model_index = -1
            return
        self.active_model_index = index
        model = self.models[index]
        self.apply_model_settings(index)
        self.validate_single_model(index)
        self.log(t("log_model_switched", self.lang, name=model['name']), is_error=False)
        self.save_config()

    def on_settings_changed(self):
        if self._loading_config or self.active_model_index < 0:
            return
        if 0 <= self.active_model_index < len(self.models):
            m = self.models[self.active_model_index]
            m["ngl"] = self.sp_ngl.value()
            m["ctx"] = self.sp_ctx.value()
            m["port"] = self.current_port()
            m["temp"] = self.sp_temp.value()
            m["top_p"] = self.sp_top_p.value()
            m["seed"] = self.sp_seed.value()
            m["threads"] = self.sp_threads.value()
            self.save_config()

    def on_path_visibility_toggled(self, checked):
        self.show_model_path = checked
        self.apply_path_visibility()
        self.apply_language()
        if not self._loading_config:
            self.save_config()

    def apply_path_visibility(self):
        if self.show_model_path:
            if 0 <= self.active_model_index < len(self.models):
                self.lbl_model_path.setText(self.models[self.active_model_index]["path"])
            elif self.models:
                self.lbl_model_path.setText(self.models[0]["path"])
            else:
                self.lbl_model_path.setText(t("no_model_hint", self.lang))
            self.lbl_model_path.show()
        else:
            self.lbl_model_path.hide()

    def update_model_buttons_state(self):
        has_models = len(self.models) > 0
        running = self.is_service_running
        self.btn_del_model.setEnabled(has_models and not running)
        self.model_combo.setEnabled(not running)
        self.btn_add_model.setEnabled(not running)
        self.btn_toggle_path.setEnabled(has_models)

    def validate_models(self):
        invalid = 0
        for i, m in enumerate(self.models):
            if i >= self.model_combo.count():
                break
            if not os.path.exists(m["path"]):
                self.model_combo.setItemText(i, f"⚠ {m['name']} (missing)")
                invalid += 1
            else:
                self.model_combo.setItemText(i, m["name"] + self._format_size(m["path"]))
        if invalid > 0:
            self.log(t("log_models_missing", self.lang, n=invalid), is_error=True)

    def validate_single_model(self, index):
        if index < 0 or index >= len(self.models):
            return
        m = self.models[index]
        if not os.path.exists(m["path"]):
            self.model_combo.setItemText(index, f"⚠ {m['name']} (missing)")
            self.log(t("log_model_missing", self.lang, path=m["path"]), is_error=True)
        else:
            self.model_combo.setItemText(index, m["name"] + self._format_size(m["path"]))

    def _format_size(self, path):
        try:
            size_mb = os.path.getsize(path) / (1024 * 1024)
            if size_mb < 1024:
                return f"  ({size_mb:.0f}MB)"
            return f"  ({size_mb/1024:.2f}GB)"
        except OSError:
            return ""

    # ==================== 日志 ====================
    def log(self, msg, is_error=False, force_split=False):
        if is_error:
            self._file_logger.error(msg)
        else:
            self._file_logger.info(msg)
        self.raw_logs.append((msg, is_error, force_split))
        current_line_num = len(self.raw_logs)
        display_msg = msg
        color = "#e06c75" if is_error else "#abb2bf"
        line_num_html = f"<span style='color: #61afef; margin-right: 8px;'>[{current_line_num:04d}]</span>" if self.show_line_num else ""
        safe_msg = display_msg.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        split_html = ""
        if force_split and current_line_num > 1:
            split_html = "<hr style='border: 0; border-top: 1px solid #3c3c3c; margin: 5px 0;'>"
        log_entry_html = f"{split_html}{line_num_html}<span style='color: {color};'>{safe_msg}</span><br>"
        cursor = self.log_text.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        cursor.insertHtml(log_entry_html)
        self.log_text.setTextCursor(cursor)
        self.log_text.ensureCursorVisible()

    def refresh_log_display(self):
        self.log_text.clear()
        for idx, (msg, is_error, force_split) in enumerate(self.raw_logs, start=1):
            display_msg = msg
            color = "#e06c75" if is_error else "#abb2bf"
            line_num_html = f"<span style='color: #61afef; margin-right: 8px;'>[{idx:04d}]</span>" if self.show_line_num else ""
            safe_msg = display_msg.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            split_html = "<hr style='border: 0; border-top: 1px solid #3c3c3c; margin: 5px 0;'>" if force_split and idx > 1 else ""
            cursor = self.log_text.textCursor()
            cursor.movePosition(QTextCursor.MoveOperation.End)
            cursor.insertHtml(f"{split_html}{line_num_html}<span style='color: {color};'>{safe_msg}</span><br>")
        self.log_text.ensureCursorVisible()

    def toggle_line_num(self):
        self.show_line_num = self.chk_lineno.isChecked()
        self.refresh_log_display()

    def current_port(self):
        """返回去除空格后的端口，空值回退到 8080"""
        return self.edit_port.text().strip() or "8080"

    def reset_stats(self):
        self._tokens_per_sec = 0.0
        self._prompt_tokens = 0
        self._eval_tokens = 0
        self._ctx_tokens = 0
        self._active_ctx = self.sp_ctx.value()
        self._metrics_available = False
        self._last_predicted_tokens = None
        self._last_predicted_seconds = 0.0
        self._metrics_fetch_failed = False
        self.refresh_stats_labels()

    def update_stats(self, text):
        """从 llama-server 日志里解析词元统计"""
        m = re.search(r"prompt eval count\s*=\s*(\d+)\s*token(?:s|\(s\))", text)
        if m:
            self._prompt_tokens = int(m.group(1))
        m = re.search(
            r"(?<!prompt )eval count\s*=\s*(\d+)\s*token(?:s|\(s\))\s*\(\s*([\d.]+)\s*tokens per second\)",
            text)
        if m:
            self._eval_tokens = int(m.group(1))
            self._tokens_per_sec = float(m.group(2))
        m = re.search(r"eval speed\s*=\s*([\d.]+)\s*tokens/s", text)
        if m:
            self._tokens_per_sec = float(m.group(1))
        m = re.search(r"\btg\s*=\s*([\d.]+)\s*t/s", text)
        if m:
            self._tokens_per_sec = float(m.group(1))
        if not self._metrics_available:
            self._ctx_tokens = self._prompt_tokens + self._eval_tokens
        self.refresh_stats_labels()

    def refresh_stats_labels(self):
        self.lbl_stat_tps.setText(
            t("stat_tps", self.lang, rate=f"{self._tokens_per_sec:.2f}"))

    def fetch_stats(self):
        if self.process.state() != QProcess.Running:
            return
        try:
            with urllib.request.urlopen(
                    f"http://127.0.0.1:{self.current_port()}/metrics",
                    timeout=1) as resp:
                text = resp.read().decode("utf-8", errors="ignore")
            self.update_metrics_from_text(text)
            self._metrics_fetch_failed = False
        except Exception as e:
            if not self._metrics_fetch_failed:
                self._file_logger.warning(f"metrics 获取失败: {e}")
                self._metrics_fetch_failed = True

    def update_metrics_from_text(self, text):
        m = re.search(r"llamacpp:predicted_tokens_seconds\s+([\d.]+)", text)
        if m and float(m.group(1)) > 0:
            self._tokens_per_sec = float(m.group(1))
        prompt_total = None
        predicted_total = None
        seconds_total = None
        m = re.search(r"llamacpp:prompt_tokens_total\s+(\d+)", text)
        if m:
            prompt_total = int(m.group(1))
        m = re.search(r"llamacpp:tokens_predicted_total\s+(\d+)", text)
        if m:
            predicted_total = int(m.group(1))
        m = re.search(r"llamacpp:tokens_predicted_seconds_total\s+([\d.]+)", text)
        if m:
            seconds_total = float(m.group(1))
        if prompt_total is not None and predicted_total is not None:
            self._ctx_tokens = prompt_total + predicted_total
            self._metrics_available = True
        if predicted_total is not None and seconds_total is not None:
            if (self._last_predicted_tokens is not None and
                    seconds_total >= self._last_predicted_seconds):
                dt = seconds_total - self._last_predicted_seconds
                dtokens = predicted_total - self._last_predicted_tokens
                if dt > 0 and dtokens > 0:
                    self._tokens_per_sec = dtokens / dt
            self._last_predicted_tokens = predicted_total
            self._last_predicted_seconds = seconds_total
        self.refresh_stats_labels()

    # ==================== 进程 ====================
    def on_stdout(self):
        data = self.process.readAllStandardOutput().data().decode("utf-8", errors="ignore")
        text = data.strip()
        if text:
            force_split = any(k in text.lower() for k in ["processing task", "get_availabl", "system info", "load time"])
            self.log(text, is_error=False, force_split=force_split)
            self.update_stats(text)
            if "listening on" in text.lower():
                port = self.current_port()
                self.log(t("log_listening", self.lang, port=port), is_error=False)
                self.set_ui_state("running")
                if WEB_ENGINE_AVAILABLE and self.show_chat_panel:
                    self.apply_chat_placeholder("running")
                    self.web_view.setUrl(QUrl(f"http://127.0.0.1:{port}/"))

    def on_stderr(self):
        data = self.process.readAllStandardError().data().decode("utf-8", errors="ignore")
        text = data.strip()
        if text:
            error_keywords = ["error:", "failed:", "fatal:", "panic:"]
            is_err = any(k in text.lower() for k in error_keywords)
            self.log(text, is_error=is_err, force_split=True)
            self.update_stats(text)
            if "listening on" in text.lower():
                port = self.current_port()
                self.log(t("log_listening", self.lang, port=port), is_error=False)
                self.set_ui_state("running")
                if WEB_ENGINE_AVAILABLE and self.show_chat_panel:
                    self.apply_chat_placeholder("running")
                    self.web_view.setUrl(QUrl(f"http://127.0.0.1:{port}/"))

    def on_process_exit(self, exit_code, exit_status):
        if self._stop_timer.isActive():
            self._stop_timer.stop()
        self.log(t("log_stopped", self.lang, code=exit_code), is_error=True)
        self.set_ui_state("idle")
        if WEB_ENGINE_AVAILABLE and self.show_chat_panel:
            self.apply_chat_placeholder("stopped")

    def stop_server(self):
        if self.process.state() == QProcess.Running:
            self.process.terminate()
            self.log(t("log_stopping", self.lang), is_error=False)
            self._stop_timer.start(3000)

    def kill_process(self):
        if self.process.state() == QProcess.Running:
            self.process.kill()
            self.log(t("log_killed", self.lang), is_error=True)

    def start_server(self):
        if self.active_model_index < 0 or not self.models:
            self.log(t("log_no_model_selected", self.lang), is_error=True)
            return
        exe_path = self.edit_exe.text().strip()
        model = self.models[self.active_model_index]
        model_path = model["path"]
        if not exe_path or not os.path.exists(exe_path):
            self.log(t("log_no_exe", self.lang), is_error=True)
            return
        if not model_path or not os.path.exists(model_path):
            self.log(t("log_model_not_found", self.lang, path=model_path), is_error=True)
            return
        args = [
            "-m", model_path,
            "-ngl", str(self.sp_ngl.value()),
            "-c", str(self.sp_ctx.value()),
            "--port", self.current_port(),
            "--metrics",
        ]
        if self.sp_threads.value() > 0:
            args.extend(["--threads", str(self.sp_threads.value())])
        args.extend([
            "--temp", str(self.sp_temp.value()),
            "--top-p", str(self.sp_top_p.value()),
            "--seed", str(self.sp_seed.value()),
        ])
        self.reset_stats()
        if self._stop_timer.isActive():
            self._stop_timer.stop()
        self.set_ui_state("starting")
        self.log(t("log_start_separator", self.lang), is_error=False, force_split=True)
        self.log(t("log_model_param", self.lang, name=model['name'], path=model_path), is_error=False)
        self.log(t("log_exe_param", self.lang, path=exe_path), is_error=False)
        self.log(t("log_args_param", self.lang, args=' '.join(args)), is_error=False)
        self.save_config()
        self.process.start(exe_path, args)
        if WEB_ENGINE_AVAILABLE and not self.show_chat_panel:
            self.show_chat_panel = True
            self.btn_toggle_chat.setChecked(True)
            self.apply_chat_visibility()
        if WEB_ENGINE_AVAILABLE:
            self.apply_chat_placeholder("loading")

    def open_webui_browser(self):
        port = self.current_port()
        webbrowser.open(f"http://127.0.0.1:{port}/")

    def select_exe_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, t("file_choose_exe", self.lang),
            filter=t("filter_exe", self.lang))
        if path:
            self.edit_exe.setText(path)

    # ==================== 配置 ====================
    def save_config(self):
        if self._loading_config:
            return
        cfg = {
            "exe_path": self.edit_exe.text(),
            "models": self.models,
            "active_model_index": self.model_combo.currentIndex(),
            "show_model_path": self.show_model_path,
            "show_chat_panel": self.show_chat_panel,
            "show_line_num": self.show_line_num,
            "lang": self.lang,
            "window_size": [self.size().width(), self.size().height()],
            "window_pos": [self.pos().x(), self.pos().y()],
        }
        try:
            with open(self.CONFIG_PATH, "w", encoding="utf-8") as f:
                json.dump(cfg, f, ensure_ascii=False, indent=2)
        except Exception as e:
            self.log(t("log_save_fail", self.lang, err=str(e)), is_error=True)

    def load_config(self):
        default_exe = os.path.join(_app_dir(), "llama_cpp", "llama-server.exe")
        if os.path.exists(default_exe):
            self.edit_exe.setText(default_exe)
        if not os.path.exists(self.CONFIG_PATH):
            return
        self._loading_config = True
        try:
            with open(self.CONFIG_PATH, "r", encoding="utf-8") as f:
                cfg = json.load(f)

            if "window_size" in cfg:
                w, h = cfg["window_size"]
                self.resize(w, h)
            if "window_pos" in cfg:
                x, y = cfg["window_pos"]
                self.move(x, y)

            self.lang = cfg.get("lang", "zh_CN")
            if self.lang not in self.SUPPORTED_LANGS:
                self.lang = "zh_CN"

            self.edit_exe.setText(cfg.get("exe_path", ""))
            self.models = cfg.get("models", [])
            self.model_combo.clear()
            for m in self.models:
                self.model_combo.addItem(m.get("name", "未命名"))
            active_idx = cfg.get("active_model_index", 0)
            if 0 <= active_idx < len(self.models):
                self.model_combo.setCurrentIndex(active_idx)
                self.active_model_index = active_idx
            elif self.models:
                self.model_combo.setCurrentIndex(0)
                self.active_model_index = 0
            self.show_model_path = cfg.get("show_model_path", False)
            self.btn_toggle_path.setChecked(self.show_model_path)
            self.show_chat_panel = cfg.get("show_chat_panel", True)
            self.btn_toggle_chat.setChecked(self.show_chat_panel)
            self.show_line_num = cfg.get("show_line_num", True)
            self.chk_lineno.setChecked(self.show_line_num)
        except Exception as e:
            self.log(t("log_load_fail", "zh_CN", err=str(e)), is_error=True)
        finally:
            self._loading_config = False

        if self.models:
            idx = min(max(self.active_model_index, 0), len(self.models) - 1)
            self.apply_model_settings(idx)

    def closeEvent(self, event):
        self.save_config()
        if self.process.state() == QProcess.Running:
            self.process.terminate()
            self.log(t("log_stopping", self.lang), is_error=False)
            if not self.process.waitForFinished(3000):
                self.log(t("log_killed", self.lang), is_error=True)
                self.process.kill()
                self.process.waitForFinished(1000)
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(DARK_STYLE)
    win = LlamaLauncher()
    win.show()
    sys.exit(app.exec())
