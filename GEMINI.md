# Gemini

## 目录概述

该目录是 Visual Studio Code 的用户配置目录，用于存储所有用户级别的设置、快捷键、代码片段、扩展数据和状态。它的核心功能是同步和管理一套高度定制化的、以 Vim 模式为中心的开发环境。

## 关键文件与架构

本配置采用了一套分层的混合式 Vim 配置方案，主要涉及以下几个文件：

1.  **`settings.json` (第一层 - VS Code Vim 插件配置)**
    - **核心角色**: 控制 VS Code 原生功能和 Vim 插件 (`vscodevim.vim`) 的行为。
    - **主要配置**:
        - 启用/禁用 Vim 插件功能（如 EasyMotion, Sneak）。
        - 通过 `vim.handleKeys` 控制特定快捷键由 VS Code 还是 Vim 处理，这是实现`Option`键自定义的关键。
        - 通过 `vim.textobjKeybindings` 定义自定义文本对象。
        - 配置编辑器外观、字体（JetBrains Mono）、缩进（使用 Tab）、主题（Atom One Dark）。
        - 集成 Prettier 实现保存时自动格式化。
        - 配置 "Smart Input Pro" 插件，实现普通模式和插入模式下中英文输入法的自动切换。
        - 指定了外部 `~/.vimrc` 文件的路径。

2.  **`~/.vimrc` (第二层 - 传统 Vim 映射)**
    - **核心角色**: 定义标准 Vim 脚本和快捷键映射，由 `vscodevim.vim` 插件加载。
    - **注意**: 此文件未包含在此目录中，但由 `settings.json` 引用。VS Code 的 Vim 插件对其支持有限（例如，不支持 Ex 命令）。

3.  **`keybindings.json` (第三层 - VS Code 原生快捷键)**
    - **核心角色**: 定义 VS Code 级别的快捷键，用于覆盖默认行为或调用特定命令，包括通过 `vim.remap` 调用 Vim 命令序列。
    - **主要配置**:
        - 将 `Alt+J/K` 映射为在 Normal 模式下上下移动行。
        - 将 `Alt+H/L` 映射为在 Normal 模式下移动到行首/行尾。
        - 将 `Cmd+3` 设置为智能运行键，根据文件类型（HTML, Python, JS/TS）执行不同操作。
        - 重写了大量默认快捷键以适配 Vim 操作习惯。

## 主要使用惯例

- **Vim 为中心**: 所有配置都围绕提供流畅的 Vim 体验展开。
- **格式化**:
    - 使用 `Tab` 进行缩进，而非空格。
    - 开启了保存时自动格式化（`formatOnSave`），主要使用 Prettier。
- **Git 提交**: `CLAUDE.md` 文件中提到了一个特定的 Git 提交信息格式 `+%Y-%m-%d %H:%M 内容`，并要求使用中文填写内容。
- **输入法**: 配置了进入 Vim 普通模式时自动切换到英文输入法，进入插入模式时切换回中文输入法。
- **语言**: 偏好使用中文进行交互。

* 每次提交时，通过vscode命令行工具获取已经安装的插件，更新.vscode/extensions.json.vscode/extensions.json文件
