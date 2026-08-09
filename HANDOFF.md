# HANDOFF

本文件记录最近 10 条关键修改。最新记录置顶，历史记录按时间从新到旧排列。
记录标题格式为 `## 序号. 【YYYY-MM-DD HH:MM】- 标题`；序号持续递增，最大为 999，达到后从 1 开始。
记录超过 10 条时自动删除底部最旧记录。实质修改完成并验证后更新一次；创建 commit 前必须核对，并与对应修改一起提交。

============================================================

## 12. 【2026-08-09 19:53】- 关闭 GitLens 跟随行 Blame 显示

### 修改内容

- 在 `settings.json` 中将 `gitlens.currentLine.enabled` 设为 `false`，关闭光标所在行的内联 Git blame 注释。
- 移除 `ipynbTranslator.zhipuApiKey` 的明文值，避免将凭据提交至远程仓库。

### 实现方式

- 使用 GitLens 18.3.0 的当前行注释开关，仅停用随光标变化的显示；手动打开文件 blame 注释的功能不受影响。

### 验证

- 已核对已安装 GitLens 扩展的配置定义，确认 `gitlens.currentLine.enabled` 为合法布尔设置。
- Node.js JSON 解析通过，确认 `gitlens.currentLine.enabled` 为 `false`。
- `git diff --check -- settings.json HANDOFF.md` 通过。

### 潜在或遗留问题

- 已打开的编辑器可能需要重载 VS Code 窗口或重新打开文件后，现有内联注释才会消失。
- 已移除的 API 密钥应在对应服务端轮换，旧密钥仍可能存在于本机历史版本或此前同步的位置。

============================================================

## 11. 【2026-08-09 19:25】- 启用 Notebook 输出自动换行

### 修改内容

- 在 `settings.json` 中将 `notebook.output.wordWrap` 设为 `true`，使 `.ipynb` 单元格输出按可视区域换行。

### 实现方式

- 使用 VS Code Notebook 内置输出配置，仅影响 Notebook 输出显示，不改写笔记本内容或代码单元。

### 验证

- Node.js 已确认 `settings.json` 可解析，`notebook.output.wordWrap` 为 `true`。
- `HANDOFF.md` 已确认保留 10 条记录，最新记录为第 11 条。
- `git diff --check -- settings.json HANDOFF.md` 通过。

### 潜在或遗留问题

- 已打开的 Notebook 可能需要重新加载窗口或重新打开后才刷新显示。

============================================================

## 10. 【2026-08-09 15:50】- 为集成终端启用 Python 原生彩色错误

### 修改内容

- 在 `terminal.integrated.env.osx` 中设置 `PYTHON_COLORS: "1"`，使 Python 3.13 及以上版本的 traceback 输出 ANSI 颜色。

### 实现方式

- 通过 VS Code 集成终端环境变量生效，不改变 `python.execInTerminal` 官方运行路径或项目源码。
- Agent 项目已同步升级到 Python 3.14.6，可直接使用 CPython 原生彩色 traceback。

### 验证

- Node.js JSONC 解析通过，确认 `PYTHON_COLORS` 为 `"1"`。
- Python 3.14.6 的强制 traceback 已检测到 ANSI 颜色转义码。
- `git diff --check` 通过。

### 潜在或遗留问题

- 已打开的集成终端不会继承新环境变量；需关闭并新建终端，或重载 VS Code 窗口。

============================================================

## 9. 【2026-08-09 15:46】- 隐藏底部终端的实例标签栏

### 修改内容

- 将 `terminal.integrated.tabs.enabled` 设为 `false`，隐藏底部集成终端右侧的终端实例标签和切换栏。

### 实现方式

- 保留终端面板默认位置为底部，以及多终端创建和切换功能；仅隐藏终端标签栏的界面。

### 验证

- Node.js JSONC 解析通过，且确认 `terminal.integrated.tabs.enabled` 为 `false`。
- `git diff --check` 通过。
- VS Code 需要重新加载窗口后才会刷新终端标签栏显示，未执行图形界面验证。

### 潜在或遗留问题

- 隐藏标签栏后，需要通过终端面板右上角的下拉菜单或命令面板切换多个终端实例。

============================================================

## 8. 【2026-08-09 15:44】- Command+3 运行 Python 前清空终端

### 修改内容

- Python 文件的 `Cmd+3` 改为依次聚焦、清空当前集成终端，再调用 `python.execInTerminal` 运行当前文件。

### 实现方式

- 使用 VS Code 内置 `runCommands` 和 `workbench.action.terminal.clear`，保留 Python 扩展的官方运行命令、所选解释器和环境激活流程。
- 不使用 Code Runner 的 `clearPreviousOutput`，因此清屏行为与官方 Python 运行路径兼容。

### 验证

- Node.js JSONC 解析通过，并确认 Python `Cmd+3` 的命令序列为终端聚焦、清屏、`python.execInTerminal`。
- `git diff --check` 通过。
- VS Code 需要重新加载窗口后才会应用新的用户级快捷键，未执行图形界面端到端按键验证。

### 潜在或遗留问题

- 每次 Python `Cmd+3` 会清空当前活动集成终端的全部可见滚动历史，而非仅清除上一次 Python 命令输出。

============================================================

## 7. 【2026-08-09 15:02】- Command+3 改用官方 Python 运行命令

### 修改内容

- 将 Python 文件中 `Cmd+3` 的命令从 `code-runner.run` 改为 Python 扩展的 `python.execInTerminal`。
- 保留 JavaScript、TypeScript、C 和 C++ 的 `Cmd+3` Code Runner 映射，以及 HTML 的 Live Server 映射。

### 实现方式

- Python 扩展会以 `Python: Select Interpreter` 选中的项目解释器在集成终端运行当前文件，与 Pylance、调试器和环境激活行为一致。
- Python 快捷键不再经过 Code Runner 与自定义 `python-run` wrapper；wrapper 继续保留给已有的兼容场景。

### 验证

- 安装的 `ms-python.python` 扩展已声明 `python.execInTerminal`，显示名称为 `Run Python File in Terminal`。
- Node.js JSONC 解析通过，且确认 `Cmd+3` 在 Python 文件中映射至 `python.execInTerminal`。
- `git diff --check` 通过。
- VS Code 需要重新加载窗口后才会应用新的用户级快捷键，未执行图形界面端到端按键验证。

### 潜在或遗留问题

- Python 项目需通过状态栏或 `Python: Select Interpreter` 选择正确的项目虚拟环境；本次 Agent 项目已配置为 `.venv/bin/python`。

============================================================

## 6. 【2026-08-08 13:26】- 统一 VS Code、Vim 与扩展配置

### 修改内容

- 更新 `settings.json` 与 `keybindings.json`：`Ctrl+Shift+D` 负责复制当前行，`Cmd+D` 负责逐次添加相同单词选择，`Ctrl+D` 在 Normal/Insert 模式都清空当前行并进入插入态；`ciq` / `cie` 通过 VSCodeVim 支持的 operator-pending 映射处理双引号 / 单引号文本对象。
- 移除本机残留的 `wenfangdu.jump` 扩展目录，消除 `Esc` 触发 `setDecorations` 异常的来源。

### 实现方式

- 全局 `editor.formatOnSave`、`editor.insertSpaces`、`editor.tabSize` 和 `editor.acceptSuggestionOnEnter` 作为唯一通用设置；Python 保留 Ruff 专属格式化、修复和导入排序。
- `.vimrc` 仅保留终端 Vim 的基础搜索、剪贴板和 `K` 映射，VS Code 专属映射统一在 `settings.json` 与 `keybindings.json`；移除不受当前 VSCodeVim 支持的 `vim.textobjKeybindings` 与劫持普通 `q` 的错误键位，避免 `ciq` 多余输入和 `cie` 误操作整份文档。
- BTT 的 `Option+1/3` 不在本仓库修改；`Cmd+1` 和 `Cmd+3` 继续由 VS Code 使用，互不抢占。

### 验证

- Node.js JSONC 解析通过 `settings.json`、快捷键、任务、模型、扩展和全部片段文件。
- `vim -Nu /Users/dyx/.vimrc -n -es +'qa!'` 通过。
- `extensions-template.json` 保留 15 个核心推荐扩展；`.vscode/extensions.json` 在提交前同步为当前实际安装的 30 个扩展。
- 失效 YAPF、Autopep8、Prettier、Copilot、Jump Extension 和旧 Leader 引用检索为空；`git diff --check` 通过。

### 潜在或遗留问题

- BetterTouchTool 中仍保留 `Option+1/3` 专属和全局规则；按用户要求未修改 BTT，若其全局条件与 Code 专属规则同时命中，需在 BTT 图形界面单独确认。
- VS Code 需要重新加载窗口后才会应用更新后的用户配置。

============================================================

## 5. 【2026-08-08 11:27】- 修复 Vim 模式 Esc 触发 Jump 扩展异常并配置 EasyMotion 快捷键

### 修改内容

- 将 `Cmd+I` 配置为仅在 VSCodeVim Normal 模式下直接触发 EasyMotion 全屏字符跳转。

### 实现方式

- VS Code 扩展主机日志定位到 `wenfangdu.jump` v0.8.0 的 `Jump.setDecorations` 对未定义编辑器调用；该扩展而非 VSCodeVim 在 `Esc` 退出跳转模式时抛出异常。
- `Cmd+I` 使用模式限定的 `vim.remap` 映射为 `<leader><leader>s`；按下后输入目标字符即可跳转。

### 验证

- 使用 Node.js 按 JSONC 规则解析 `keybindings.json`，通过。
- `git diff --check` 通过。
- 未在 VS Code 图形界面中重新加载窗口，因此未执行端到端按键验证。

### 潜在或遗留问题

- VS Code 需要重新加载窗口后才会应用新的 `Cmd+I` 键位。

============================================================

## 4. 【2026-08-08 11:15】- 同步 VS Code 新增配置并清理无效凭据

### 修改内容

- 更新 `settings.json`，同步当前 VS Code 的全局编辑器、终端、扩展和工作台配置。
- 移除未安装 `tktbtranslation` 扩展遗留的有道 API `appKey` 与密钥配置。
- 更新 `chatLanguageModels.json`，保留 DeepSeek `deepseek-v4-flash` 的高推理强度设置，并消除重复 `settings` 键。

### 实现方式

- 采用 VS Code 当前生成的用户配置排序和内容，保留本地 PostgreSQL 连接配置；其密码字段为空。
- 未使用的翻译扩展配置直接从用户设置中删除，避免把 API 凭据纳入版本控制。
- 合并重复对象键，确保 JSON 解析时模型配置不被静默覆盖。

### 验证

- `node -e` 已通过两个 JSON 文件解析。
- `git diff --check` 通过。
- 已检索确认两个有道配置键及其原始值均不再出现。
- `bash /Users/dyx/ai_coding_rules/scripts/rules-audit.sh` 通过。

### 潜在或遗留问题

- 当前配置仍包含本机 PostgreSQL 用户名与 `127.0.0.1` 连接信息；密码为空，未发现其他凭据。

============================================================

## 3. 【2026-07-27 16:34】- 仅清理当前打开文件的空行任务

### 修改内容

- 将 `tasks.json` 的 `Remove Extra Blank Lines` 改为调用仓库内的 `remove_blank_lines.py`，并仅把 VS Code 的 `${file}` 传给脚本。
- 新增 `.vscode/remove_blank_lines.py`：过滤完全空白、仅含空格或 Tab 的行，并以 UTF-8 和末尾换行写回目标文件。

### 实现方式

- 移除原来依赖 `/Users/dyx/Code/外部工具/删除空行.py` 的命令和模拟 `Cmd+Option+R` 回退编辑器的 AppleScript。
- 任务为用户级配置，脚本参数使用本仓库的绝对路径，避免在任意打开的工作区中解析 `${workspaceFolder}` 失败。
- 任务使用 VS Code 原生 `process` 执行器直接启动 Python，避免 shell 对带空格路径或参数的二次解析。

### 验证

- `python3 -c 'import ast, json; ...'` 已通过 `tasks.json` JSON 解析和脚本 AST 语法检查。
- `git diff --check` 通过。
- 已核对任务保留 Python 可执行文件、脚本绝对路径和 `${file}` 两个独立参数。
- 未在 VS Code 界面中执行任务；实际运行前应先保存当前文件，避免外部写入与未保存缓冲区冲突。

### 潜在或遗留问题

- 该任务会永久删除目标文件内的所有空白行；VS Code 的撤销能力取决于编辑器如何处理外部文件变更。
