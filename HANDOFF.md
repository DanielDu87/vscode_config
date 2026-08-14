============================================================

## 28. 【2026-08-14 23:28】- 默认 Copilot 权限设为绕过审批

### 修改内容

- 将 VS Code 聊天的新会话默认权限等级设为「绕过审批」（Bypass Approvals），使聊天代理执行工具和终端命令时不再逐次弹窗确认。

### 实现方式

- `settings.json` 新增 `chat.permissions.default: "autoApprove"`，为所有新建聊天会话设置默认权限等级；会话内仍可随时通过权限选择器单独调整。

### 验证

- Node.js JSONC 宽松解析 `settings.json` 通过，确认 `chat.permissions.default` 为 `autoApprove`。
- 未做图形界面端到端验证；需重启 VS Code 或新开聊天后，确认权限选择器显示「绕过审批」且工具调用不再弹确认框。

### 潜在或遗留问题

- 全局一键开关 `chat.tools.global.autoApprove`（YOLO，会忽略默认拒绝规则）未启用，保留终端命令默认拒绝清单等保护。
- 组织策略若禁用绕过审批，新会话会退回默认审批，属预期。

============================================================

## 27. 【2026-08-14 21:12】- 提示词托管到仓库 prompts 目录（VS Code 官方默认目录）

### 修改内容

- 在 VS Code User 配置仓库内新建 `prompts/` 目录，托管单一 Copilot 说明指令文件（官方 `*.instructions.md` 格式），使提示词纳入本仓库版本管理。

### 实现方式

- `prompts/代码说明.instructions.md`：frontmatter `applyTo: '**'` 自动应用。输出仅保留两节：「一、作用说明」（作用与位置合并一行、调用链以从上到下的箭头展示）与「二、代码结构」（只展示关键函数/类定义、关键调用、关键变量；代码框中注释位于代码行上方，块间空行）。
- 通用要求：中文、区分事实/推测/风险/建议、禁止工具调用与工具调用标记、不修改代码、代码符号反引号、只列实际存在元素不编造。
- **关键发现**：`User/prompts/` 是 VS Code 1.133 的官方默认用户提示词目录（`promptsHome`，与 `snippets/`、`settings/` 并列，自动以 `storage:"user"` 扫描，并纳入 Settings Sync 同步范围），无需也不能在 `chat.instructionsFilesLocations` 中重复声明；初版重复声明导致 Configure Instructions 界面条目显示两次，移除配置项后由 `promptsHome` 默认发现。

### 验证

- 宽松 JSONC 解析 `settings.json` 通过；`git diff --check` 通过。
- 指令 frontmatter 与官方字段一致。

### 潜在或遗留问题

- 内置 `/explain` 提示词写死为散文输出，需使用选中代码后手动输入「说明这段代码」触发结构化说明。
- `prompts/` 目录已纳入 Settings Sync 同步范围（若用户开启），他机可自动同步，无需手工重建。

============================================================

## 26. 【2026-08-12 16:06】- Cmd+5 启动或重启调试并打开调试面板

### 修改内容

- 将 `Cmd+5` 统一设置为无论当前状态如何都启动或重启调试，并在操作后打开调试面板。

### 实现方式

- `keybindings.json`：移除 `Cmd+5` 的单步进入绑定及旧的直接启动/重启绑定。
- 使用 `runCommands` 按状态分流：`inDebugMode` 时执行 `workbench.action.debug.restart`，未调试且有可用调试器时执行 `workbench.action.debug.start`；两条流程随后执行 `workbench.view.debug`。
- 保留 `Cmd+5` 对第五编辑器组默认快捷键的解除，以及 `Shift+Cmd+F5` 默认重启调试快捷键的解除。

### 验证

- 使用 Node.js 清理 JSONC 注释和尾逗号后解析 `keybindings.json`，通过。
- `git diff --check -- keybindings.json` 通过。
- 未进行 VS Code 图形界面验证；需实际按下 `Cmd+5` 确认启动、重启和调试面板聚焦行为。

### 潜在或遗留问题

- 当当前工作区没有可用调试器时，`Cmd+5` 不会触发启动流程；这是 VS Code `debuggersAvailable` 条件的预期限制。

============================================================

# HANDOFF

本文件记录最近 10 条关键修改。最新记录置顶，历史记录按时间从新到旧排列。
记录标题格式为 `## 序号. 【YYYY-MM-DD HH:MM】- 标题`；序号持续递增，最大为 999，达到后从 1 开始。
记录超过 10 条时自动删除底部最旧记录。实质修改完成并验证后更新一次；创建 commit 前核对并一起提交。

============================================================

## 25. 【2026-08-12 15:03】- 格式化时按文件现状推断缩进并强制 Python 4 空格

### 修改内容

- 全局开启「按文件内容推断缩进」；Python 文件单独锁定 4 空格，并在 Ruff 全局配置中强制空格缩进，使格式化时自动把 Tab / 2 空格的 Python 文件转为 4 空格。

### 实现方式

- `settings.json`：全局 `editor.detectIndentation` 从 `false` 改为 `true`，VS Code 打开文件时按已有内容推断 Tab / 空格与宽度。
- `settings.json` 的 `[python]` 段新增 `editor.detectIndentation: false` + `editor.insertSpaces: true` + `editor.tabSize: 4`，避免 Python 文件被文件现状带偏，保证编辑时新敲缩进为 4 空格。
- `~/.config/ruff/ruff.toml`：顶层新增 `indent-width = 4`，`[format]` 段新增 `indent-style = "space"`，强制 Ruff formatter 把 Tab / 2 空格的 Python 文件统一为 4 空格。
- 本次提交同时包含之前会话遗留的未提交改动：`chatLanguageModels.json`（OpenRouter 新增 deepseek-v4-flash 模型）、`keybindings.json`（Cmd+5 单步进入 / 重启调试）、`settings.json` 的 emmet、codexSwitch、chat.tools 等条目。

### 验证

- 构造 Tab 缩进与 2 空格缩进的 Python 测试文件，`ruff format` 后 `cat -t` 确认均已转为 4 空格；测试文件已清理。
- VS Code 设置为 JSONC 文本，人工核对键值正确。

### 潜在或遗留问题

- Ruff 全局配置位于 `~/.config/ruff/ruff.toml`，不在本仓库；若他机恢复需同步该文件。
- 未在 VS Code 图形界面实测保存时的格式化效果，依赖 Ruff formatter 行为一致性。

============================================================

## 24. 【2026-08-11 13:46】- 显示不可见字符与缩进参考线

### 修改内容

- 在 `settings.json` 中显示空格与 Tab 的点状不可见字符，并显示缩进层级参考线。

### 实现方式

- 将 `editor.renderWhitespace` 设为 `"all"`，以点状标记显示不可见字符；将 `editor.guides.indentation` 设为 `true`，显示缩进参考线，不改变 Tab、自动缩进或格式化配置。

### 验证

- Node.js JSONC 宽松解析 `settings.json` 通过，并确认 `editor.renderWhitespace` 为 `"all"`、`editor.guides.indentation` 为 `true`。
- `git diff --check -- settings.json HANDOFF.md` 通过。
- 未进行图形界面验证；VS Code 通常会立即应用此设置。

### 潜在或遗留问题

- 无。

============================================================

## 23. 【2026-08-11 10:30】- Ctrl+Q 切换终端显示

### 修改内容

- 为 VS Code 添加 `Ctrl+Q` 快捷键，用于显示或隐藏集成终端面板。

### 实现方式

- 绑定 VS Code 内置命令 `workbench.action.terminal.toggleTerminal`，与已有 `Ctrl+\\` 终端切换行为一致。

### 验证

- Node.js JSONC 宽松解析 `keybindings.json` 通过。
- `git diff --check -- keybindings.json HANDOFF.md` 通过。
- 未进行图形界面验证；需在 VS Code 中按 `Ctrl+Q` 确认终端面板可显示和隐藏。

### 潜在或遗留问题

- 无。

============================================================

## 22. 【2026-08-10 23:16】- 选中代码时固定使用内置聊天

### 修改内容

- 为 Vim Visual 模式补充 `Cmd+L` 快捷键，选中代码后按下该组合键也只会打开或隐藏 VS Code 内置聊天。

### 实现方式

- 依据 `auxiliaryBarVisible` 分流：隐藏时运行 `workbench.action.chat.open`，显示时运行 `workbench.action.toggleAuxiliaryBar`。
- 两条规则均限制于 `vim.mode == 'Visual' && editorTextFocus`，覆盖选中文本进入的 Vim Visual 模式。

### 验证

- 待执行 JSONC 解析与 `git diff --check`。
- 未进行图形界面验证；需在 VS Code 选中代码后按 `Cmd+L` 确认打开内置聊天。

### 潜在或遗留问题

- 无。

============================================================
## 21. 【2026-08-10 21:49】- 调整 Copilot 与 EasyMotion 快捷键

### 修改内容

- 在 Vim Normal 与 Insert 模式中，将 `Cmd+I` 统一改为启动 Copilot 内联聊天生成代码。
- 在 Vim Normal 与 Insert 模式中，将 `Cmd+L` 统一改为依据辅助侧边栏状态打开或隐藏 VS Code 侧边 AI 聊天；在聊天输入框内再次按下也会隐藏面板。
- 显式解除 Continue 默认的 `Cmd+I` 和 `Cmd+L` 绑定，防止 Copilot 打开后快捷键被 Continue 面板接管。
- 将原本绑定到 Normal 模式 `Cmd+I` 的 EasyMotion 全屏字符跳转改为 `Cmd+K`。

### 实现方式

- `Cmd+I` 使用 VS Code 内置 `inlineChat.start` 命令；`Cmd+L` 以 `auxiliaryBarVisible` 分流，隐藏时执行 `workbench.action.chat.open`，显示时执行 `workbench.action.toggleAuxiliaryBar`。
- 通过 `-continue.focusEdit` 和 `-continue.focusContinueInput` 注销 Continue 提供的无条件默认键位。
- 保留既有 `vim.remap` 的 `<leader><leader>s` 序列，仅替换其原生触发键位为 `Cmd+K`。

### 验证

- 已通过 Node.js JSONC 宽松解析校验 `keybindings.json`。
- `git diff --check -- keybindings.json HANDOFF.md` 通过。
- 未做图形界面端到端验证；需在 VS Code 的 Vim Normal 与 Insert 模式分别试按 `Cmd+I`、`Cmd+L`，再在 Normal 模式试按 `Cmd+K`。

### 潜在或遗留问题

- Copilot Chat 实际可用性仍取决于 VS Code 登录的 GitHub 账户具备 Copilot 权限。

============================================================

## 20. 【2026-08-10 14:41】- 区分 Vim 模式的 Cmd+I

### 修改内容

- 保留 Vim Normal 模式下 `Cmd+I` 触发 EasyMotion 全屏字符跳转。
- 新增 Vim Insert 模式下 `Cmd+I` 打开 Copilot 内联聊天，用于生成或编辑当前代码。
- 将 `deepseek-v4-flash` 推理强度设为 `low`，将 `glm-4.6v-flash` 设为 `none`。
- 禁止恢复终端持久化进程，并关闭 Qwen Copilot 推理模式。

### 实现方式

- 在 `keybindings.json` 中为同一快捷键配置互斥的 `vim.mode` 条件；Insert 模式调用 VS Code 内置命令 `inlineChat.start`。
- 通过 `chatLanguageModels.json` 的模型配置降低对应模型的推理开销；在 `settings.json` 中使用 VS Code 和 Qwen Copilot 的现有配置项。

### 验证

- Node.js JSONC 宽松解析 `keybindings.json` 通过。
- `git diff --check -- keybindings.json` 通过。
- 未做图形界面端到端验证；需在 VS Code 中分别进入 Vim Normal 与 Insert 模式试按 `Cmd+I`。

### 潜在或遗留问题

- Copilot Chat 实际可用性仍取决于 VS Code 登录的 GitHub 账户具备 Copilot 权限。

============================================================

## 19. 【2026-08-09 23:34】- 关闭相同单词绿色高亮框

### 修改内容

- 关闭 VS Code 光标落在文字上时，对相同单词 / 选中文本的绿色高亮框。
- 恢复 Vim 普通模式块状光标，撤销本次误改。

### 实现方式

- 新增 `editor.occurrencesHighlight: "off"`，关闭同词出现高亮。
- 设置 `editor.selectionHighlight: false`、`editor.selectionHighlightMultiline: false`，关闭选中文本匹配高亮。
- 将 `vim.cursorStylePerMode.normal` 恢复为 `block`。

### 验证

- 以 JSONC 宽松解析校验 `settings.json` 通过。
- 确认 `occurrencesHighlight=off`、`selectionHighlight=false`、`selectionHighlightMultiline=false`、`vim.cursorStylePerMode.normal=block`。
- 未做图形界面端到端验证；VS Code 通常会立即应用这些编辑器设置。

### 潜在或遗留问题

- 若仍看到绿色高亮，可能来自查找匹配、语义高亮或主题色；可再关 `editor.find` 相关高亮或检查主题。
