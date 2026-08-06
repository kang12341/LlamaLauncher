# LlamaLauncher

PySide6 桌面启动器，用于管理本地 llama.cpp server：模型切换、运行参数、日志、内嵌 WebUI 和实时生成速度显示。

## 功能

- 多模型管理：导入、删除、切换模型
- 运行参数：GPU 层数、上下文长度、端口、温度、Top-P、随机种子、线程数
- 日志面板：行号显示、1MB 轮转落盘到 `llama_launcher_log.txt`
- 内嵌 llama-server WebUI，也可用系统浏览器打开
- 实时生成速度：解析 `tg = x t/s` 日志，并轮询 `/metrics` 作为补充
- 中英文界面，文案放在 `lang/zh_CN.json`、`lang/en_US.json`，可直接修改

## 运行

```bash
pip install PySide6
python llama_launcher2.py
```

首次启动后会在程序目录生成 `config.json`，模型路径和参数都在里面。

## 打包

启动器（onedir，小 exe + `_internal` 环境文件夹）：

```bash
python -m PyInstaller --noconfirm --onedir --windowed --name LlamaLauncher llama_launcher2.py
```

安装程序（单文件，内含启动器、llama_cpp 运行库和 lang 映射）：

```bash
python -m PyInstaller --noconfirm --onefile --windowed --name LlamaLauncher_Setup installer.py --add-data "install_stage\LlamaLauncher.exe;." --add-data "install_stage\_internal;_internal" --add-data "install_stage\llama_cpp;llama_cpp" --add-data "install_stage\lang;lang"
```

## 目录结构

```text
llama_launcher2.py  主程序
i18n.py             内置文案（外部 JSON 缺失时的兜底）
lang/               中英文外部映射文件
installer.py        安装器程序
LlamaLauncher.spec  启动器 PyInstaller 配置
LlamaLauncher_Setup.spec 安装器 PyInstaller 配置
```

## 说明

`llama-server.exe` 属于 llama.cpp 项目，不包含在本仓库内。安装结构为：

```text
安装目录/
  LlamaLauncher.exe
  _internal/       运行环境
  llama_cpp/       llama-server.exe 及其运行库
  lang/            语言映射
```
