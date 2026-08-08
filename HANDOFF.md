# HANDOFF

本文件记录最近 10 条关键修改。最新记录置顶，历史记录按时间从新到旧排列。
记录标题格式为 `## 序号. 【YYYY-MM-DD HH:MM】- 标题`；序号持续递增，最大为 999，达到后从 1 开始。
记录超过 10 条时自动删除底部最旧记录。实质修改完成并验证后更新一次；创建 commit 前必须核对，并与对应修改一起提交。

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

============================================================

## 2. 【2026-07-22 11:40】- 为 Python 启用 Pylance 自动补全 + Copilot 行内 AI 补全

### 修改内容

- 在 `settings.json` 的 `[python]` 块中开启 `editor.quickSuggestions` 全开（other/comments/strings 都为 `on`），并将 `editor.quickSuggestionsDelay` 设为 `0`；同时启用 `editor.suggestOnTriggerCharacters`、`editor.acceptSuggestionOnEnter: "on"`、`editor.parameterHints.enabled`、`editor.wordBasedSuggestions: "allDocuments"`。
- 在 `// Python` 注释下新增 Pylance 补全与索引配置：`python.analysis.autoImportCompletions`、`completeFunctionParens`、`fixImportUndefined`、`importFormat`、`indexing`、`autoSearchPaths`、`useLibraryCodeForTypes` 等显式置为 `true`。
- 在全局新增 GitHub Copilot 行内 AI 补全：`github.copilot.enable` 仅作用于 `python` 和 `jupyter`；`github.copilot.inlineSuggest.enable: true`。

### 实现方式

- VSCode 1.129+ 已将 `GitHub Copilot`（含 `inlineSuggest` 与 chat）作为内置 `copilot` 扩展提供；`code --install-extension github.copilot` 会尝试降级内置 `github.copilot-chat` 失败，因此未单独安装。
- Pylance 端通过 `python.languageServer: "Pylance"` 已存在，补充 `python.analysis.*` 让其建立工作区索引、自动补全未导入符号、补全函数括号并使用库代码推断类型。
- Copilot 行内建议依赖 `inlineSuggest`；通过 `github.copilot.enable` 把 Copilot 限定在 Python 文件，避免其它语言被 AI 建议干扰。
- `[python]` 块的 `editor.*` 仅在该语言文件生效；`github.copilot.*` 与 `python.analysis.*` 放在全局是因为它们在 VS Code 中不识别为 `[python]` 范围内的键。

### 验证

- `git diff --check -- settings.json` 通过。
- 在 `/Applications/VSCode.app/Contents/Resources/app/extensions/copilot/package.json` 检索到 `github.copilot.enable` 和 `inlineSuggest.enabled` 合法配置键。
- 未在 VS Code 进程内实际键入 Python 代码做端到端补全验证；以上仅配置项合法性与已安装扩展就绪。

### 潜在或遗留问题

- 内置 Copilot 需登录 GitHub 账户并有有效订阅才能真正给出建议；如果账号未登录，仅 Pylance 自身补全生效。
- `editor.wordBasedSuggestions: "allDocuments"` 会在所有已打开文档中搜索单词作为补全，可能在大型项目中带来轻微性能开销；如不需要可改回 `"matchingDocuments"`。
- 当前 `python.analysis.extraPaths` 与 `packageIndexDepths` 显式置空数组，依赖默认搜索路径；如果项目使用了非标准 `src/` 布局，需要在每项目 `.vscode/settings.json` 中覆盖。

============================================================

## 1. 【2026-07-22 11:22】- 将 Python 格式化器切换为 YAPF（Tab 缩进、宽度 4、等号左右带空格）

### 修改内容

- 在 `settings.json` 中将 `[python]` 块的 `editor.defaultFormatter` 从 `ms-python.autopep8` 改为 `eeyore.yapf`，并设置 `editor.insertSpaces = false`、`editor.tabSize = 4`、`editor.formatOnSave = true`。
- 在全局添加 `yapf.args`，传入样式：`{based_on_style: pep8, use_tabs: true, indent_width: 4, continuation_align_style: fixed, spaces_around_default_or_named_assign: true}`，以保证缩进为 Tab、宽度 4，且 `=` 左右带空格。
- 通过 `code --install-extension eeyore.yapf --force` 安装 YAPF 扩展（v2026.1.108140646），用于提供 LSP 格式化服务。

### 实现方式

- `eeyore.yapf` 扩展在 LSP `initialize` 时读取 VS Code 全局 `yapf.args`，并把它透传给 `yapf` 的 `--style` 参数，从而在保存时让 YAPF 用 Tab 输出并加空格。
- VS Code 的 `[python]` 块只声明 Tab 编辑与格式化器选择；YAPF 的样式细节必须放在全局，因此 `yapf.args` 放在文件根作用域。

### 验证

- 直接调用扩展捆绑的 YAPF（`/Users/dyx/.vscode/extensions/eeyore.yapf-2026.1.108140646/bundled/libs` + `tool-libs` 作为 `PYTHONPATH`）用同一 `--style` 格式化测试文件，输出字节流确认：
  - 缩进为单字节 Tab（0x09），每级一个。
  - `value = 1`、`other = value + 2`、`def f(x = 1)` 等位置 `=` 左右各有 1 个空格。
- `git diff --check -- settings.json` 通过。
- 未在 VS Code 进程内触发端到端“保存文件 → YAPF 改写”操作；上述单元级验证已覆盖关键样式参数。

### 潜在或遗留问题

- 如果 `eeyore.yapf` 扩展未激活（例如 LSP 启动失败或 Python 解释器不兼容），保存时可能退回到其它格式化器；当前扩展未额外设置 `yapf.interpreter`，依赖默认行为。
- YAPF 的 `spaces_around_default_or_named_assign: true` 作用于函数默认实参和具名赋值；如果不想要对具名赋值加空格，需要拆分为 `spaces_around_default_or_named_assigns` 之外的更细粒度控制。

============================================================
