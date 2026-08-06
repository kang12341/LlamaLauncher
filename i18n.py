# i18n.py
"""多语言配置文件 - 所有界面文本的中英文映射"""

import os
import sys
import json

TRANSLATIONS = {
    "zh_CN": {
        # 窗口标题
        "window_title": "🦙 Llama Server Launcher Pro - 多模型版",

        # 顶部工具栏
        "chat_hide": "💬 隐藏聊天",
        "chat_show": "💬 显示聊天",
        "chat_hide_tooltip": "隐藏右侧聊天面板（释放更多空间给日志）",
        "chat_show_tooltip": "显示右侧聊天面板",
        "status_idle": "● 空闲",
        "status_starting": "● 启动中",
        "status_running": "● 运行中",
        "status_error": "● 异常",

        # 配置区
        "config_group": "🛠️ 模型配置",
        "llama_server": "llama-server:",
        "model_select": "📦 模型选择:",
        "model_path": "📁 模型地址:",
        "no_model": "(未导入任何模型)",
        "no_model_hint": "(未导入任何模型，请点击 ➕ 导入)",
        "params_group": "⚙ 运行参数:",
        "ngl_label": "GPU层数",
        "ctx_label": "上下文",
        "port_label": "端口",
        "temp_label": "温度",
        "top_p_label": "Top-P",
        "seed_label": "随机种子",
        "threads_label": "线程数",


        # 按钮
        "btn_browse": "📂 浏览",
        "btn_add_model": "➕",
        "btn_del_model": "🗑",
        "btn_toggle_path": "👁",
        "btn_path_hide": "🙈",
        "btn_start": "▶  启动服务",
        "btn_stop": "■  停止服务",
        "btn_open_webui": "🌐  浏览器打开",
        "chk_show_lineno": "显示日志行号",

        # 提示
        "tip_add_model": "导入新模型到列表",
        "tip_del_model": "从列表中删除当前模型",
        "tip_toggle_path": "显示/隐藏模型地址",
        "tip_path_hide": "隐藏模型地址",
        "tip_path_show": "显示模型地址",

        # Tab
        "tab_log_settings": "日志设置",
        "tab_chat": "💬 聊天界面",

        # 聊天页占位
        "chat_waiting_title": "等待服务启动",
        "chat_waiting_text": "启动 llama-server 后将自动加载内置聊天界面",
        "chat_loading_title": "⏳ 模型加载中...",
        "chat_loading_text": "等待服务监听端口成功",
        "chat_stopped_title": "服务已停止",
        "chat_stopped_text": "重新启动服务加载聊天界面",
        "chat_no_engine_title": "⚠️ PySide6.QtWebEngineWidgets 未安装",
        "chat_no_engine_text": '请使用"在浏览器打开WebUI"按钮',

        # 日志消息
        "log_model_imported": "✅ 已导入模型: {name} -> {path}",
        "log_model_deleted": "🗑️ 已删除模型: {name}",
        "log_model_switched": "🔀 已切换到模型: {name}",
        "log_model_missing": "⚠️ 模型文件不存在: {path}",
        "log_models_missing": "⚠️ 检测到 {n} 个模型文件不存在，请检查或删除",
        "log_start_separator": "========== 🚀 开始启动 llama-server ==========",
        "log_model_param": "模型: {name}  ({path})",
        "log_exe_param": "执行程序: {path}",
        "log_args_param": "参数: {args}",
        "log_listening": "🚀 启动完成: http://127.0.0.1:{port}/",
        "log_stopping": "⏳ 正在终止服务...",
        "log_killed": "⚠️ 等待关闭超时，强制结束进程",
        "log_stopped": "\n>>> 服务已停止，退出码: {code}",
        "log_no_model_selected": "❌ 错误：未选择任何模型，请先点击 ➕ 导入模型",
        "log_no_exe": "❌ 错误：请先选择有效的 llama-server 执行程序！",
        "log_model_not_found": "❌ 错误：模型文件不存在：{path}",
        "log_save_fail": "⚠️ 保存配置失败: {err}",
        "log_load_fail": "⚠️ 读取配置失败: {err}",

        # 弹窗
        "warn_running": "警告",
        "warn_running_model": "服务运行中，无法导入新模型\n请先停止服务",
        "warn_running_delete": "服务运行中，无法删除模型\n请先停止服务",
        "info_duplicate": "提示",
        "info_duplicate_text": "该模型已在列表中：{name}",
        "confirm_delete_title": "确认删除",
        "confirm_delete_text": "确定要从列表中删除模型吗？\n\n名称: {name}\n路径: {path}",
        "input_name_title": "设置模型名称",
        "input_name_prompt": "请输入模型显示名称：",
        "file_choose_model": "选择GGUF模型",
        "file_choose_exe": "选择 llama-server 执行程序",
        "filter_gguf": "GGUF模型 (*.gguf);;所有文件 (*.*)",
        "filter_exe": "可执行文件 (*.exe);;所有文件 (*.*)",
        "yes": "是",
        "no": "否",

        # 语言切换
        "lang_label": "🌐 语言:",
        "stat_tps": "生成 {rate} tok/s",
    },

    "en_US": {
        # Window
        "window_title": "🦙 Llama Server Launcher Pro - Multi-Model",

        # Top toolbar
        "chat_hide": "💬 Hide Chat",
        "chat_show": "💬 Show Chat",
        "chat_hide_tooltip": "Hide chat panel (free up space for logs)",
        "chat_show_tooltip": "Show chat panel",
        "status_idle": "● Idle",
        "status_starting": "● Starting",
        "status_running": "● Running",
        "status_error": "● Error",

        # Config
        "config_group": "🛠️ Model Config",
        "llama_server": "llama-server:",
        "model_select": "📦 Model:",
        "model_path": "📁 Model Path:",
        "no_model": "(No model imported)",
        "no_model_hint": "(No model imported, click ➕ to add)",
        "params_group": "⚙ Runtime:",
        "ngl_label": "GPU layers",
        "ctx_label": "context window",
        "port_label": "port",
        "temp_label": "Temperature",
        "top_p_label": "Top-P",
        "seed_label": "Seed",
        "threads_label": "Threads",

        # Buttons
        "btn_browse": "📂 Browse",
        "btn_add_model": "➕",
        "btn_del_model": "🗑",
        "btn_toggle_path": "👁",
        "btn_path_hide": "🙈",
        "btn_start": "▶  Start",
        "btn_stop": "■  Stop",
        "btn_open_webui": "🌐  Open Browser",
        "chk_show_lineno": "Show log line numbers",

        # Tooltips
        "tip_add_model": "Import new model",
        "tip_del_model": "Remove current model from list",
        "tip_toggle_path": "Show/hide model path",
        "tip_path_hide": "Hide model path",
        "tip_path_show": "Show model path",

        # Tabs
        "tab_log_settings": "Log Settings",
        "tab_chat": "💬 Chat",

        # Chat placeholders
        "chat_waiting_title": "Waiting for service",
        "chat_waiting_text": "Start llama-server to load chat UI",
        "chat_loading_title": "⏳ Loading model...",
        "chat_loading_text": "Waiting for port to open",
        "chat_stopped_title": "Service Stopped",
        "chat_stopped_text": "Restart service to load chat UI",
        "chat_no_engine_title": "⚠️ PySide6.QtWebEngineWidgets not installed",
        "chat_no_engine_text": 'Please use the "Open Browser" button',

        # Log messages
        "log_model_imported": "✅ Model imported: {name} -> {path}",
        "log_model_deleted": "🗑️ Model deleted: {name}",
        "log_model_switched": "🔀 Switched to: {name}",
        "log_model_missing": "⚠️ Model file missing: {path}",
        "log_models_missing": "⚠️ {n} model file(s) missing, please check or delete",
        "log_start_separator": "========== 🚀 Starting llama-server ==========",
        "log_model_param": "Model: {name}  ({path})",
        "log_exe_param": "Executable: {path}",
        "log_args_param": "Args: {args}",
        "log_listening": "🚀 Ready: http://127.0.0.1:{port}/",
        "log_stopping": "⏳ Stopping service...",
        "log_killed": "⚠️ Timeout, force killed",
        "log_stopped": "\n>>> Service stopped, exit code: {code}",
        "log_no_model_selected": "❌ Error: no model selected, click ➕ to import",
        "log_no_exe": "❌ Error: invalid llama-server path!",
        "log_model_not_found": "❌ Error: model file not found: {path}",
        "log_save_fail": "⚠️ Save config failed: {err}",
        "log_load_fail": "⚠️ Load config failed: {err}",

        # Dialogs
        "warn_running": "Warning",
        "warn_running_model": "Service is running, cannot import\nPlease stop the service first",
        "warn_running_delete": "Service is running, cannot delete\nPlease stop the service first",
        "info_duplicate": "Info",
        "info_duplicate_text": "Model already in list: {name}",
        "confirm_delete_title": "Confirm Delete",
        "confirm_delete_text": "Remove this model from the list?\n\nName: {name}\nPath: {path}",
        "input_name_title": "Set Model Name",
        "input_name_prompt": "Enter model display name:",
        "file_choose_model": "Choose GGUF Model",
        "file_choose_exe": "Choose llama-server Executable",
        "filter_gguf": "GGUF models (*.gguf);;All files (*.*)",
        "filter_exe": "Executables (*.exe);;All files (*.*)",
        "yes": "Yes",
        "no": "No",

        # Language
        "lang_label": "🌐 Language:",
        "stat_tps": "Gen {rate} tok/s",
    },
}


def _app_base_dir():
    """exe 打包后以 exe 所在目录为基准，开发时以脚本目录为基准"""
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


def load_external_translations():
    """从 lang/zh_CN.json、lang/en_US.json 读取外部映射并覆盖内置文案"""
    lang_dir = os.path.join(_app_base_dir(), "lang")
    for lang in TRANSLATIONS:
        path = os.path.join(lang_dir, f"{lang}.json")
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict):
                TRANSLATIONS[lang].update(data)
        except Exception:
            pass


load_external_translations()


def t(key, lang="zh_CN", **kwargs):
    """获取翻译文本，支持占位符替换"""
    text = TRANSLATIONS.get(lang, TRANSLATIONS["zh_CN"]).get(
        key, TRANSLATIONS["zh_CN"].get(key, key)
    )
    if kwargs:
        try:
            return text.format(**kwargs)
        except (KeyError, IndexError):
            return text
    return text
