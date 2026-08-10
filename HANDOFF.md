# HANDOFF

本文件记录最近 10 条关键修改。最新记录置顶，历史记录按时间从新到旧排列。
记录标题格式为 `## 序号. 【YYYY-MM-DD HH:MM】- 标题`；序号持续递增，最大为 999，达到后从 1 开始。
记录超过 10 条时自动删除底部最旧记录。实质修改完成并验证后更新一次；创建 commit 前核对并一起提交。

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

============================================================

## 18. 【2026-08-09 23:10】- 关闭中文输入法光标绿色方框

### 修改内容

- 在 `settings.json` 的 `smartInputPro.config` 中关闭光标装饰框，去掉文字上方的绿色方框显示。

### 实现方式

- 仅将 `smartInputPro.config.enableCursorDecorations` 从 `true` 改为 `false`，保留输入法自动切换、光标颜色和状态栏显示等其它设置不变。

### 验证

- 已完成配置修改，目标项为单一布尔开关。

### 潜在或遗留问题

- 如果绿色方框来自其他扩展或 VS Code 原生装饰，可能还需要再关对应的光标高亮项。

============================================================

## 17. 【2026-08-09 23:03】- 启用 Copilot Chat 全部代理入口

### 修改内容

- 在 `settings.json` 中显式启用 Copilot Chat 的代理模式与编辑会话入口。
- 保持 Copilot 全语言补全、内联建议、Next Edit、代码搜索、探索代理和 Claude Agent 集成开启。

### 实现方式

- 新增 `github.copilot.chat.agentMode.enabled` 与 `github.copilot.chat.editingSession.enabled`，其余已有 Copilot 配置保持不变。
- Continue 的 `continue.enableTabAutocomplete` 继续设为 `false`；控制台、快速操作与 Next Edit 功能维持开启。

### 验证

- Node.js 已成功解析 `settings.json`，确认全部 Copilot 目标开关为启用，且 Continue Tab 自动补全保持关闭。
- `git diff --check -- settings.json` 通过。

### 潜在或遗留问题

- 个别 Copilot Chat 实验功能是否显示仍取决于当前 VS Code 版本、GitHub Copilot 订阅权限及服务端灰度状态。

============================================================

## 16. 【2026-08-09 22:53】- 恢复新终端在底部面板打开

### 修改内容

- 在 `settings.json` 中将 `terminal.integrated.defaultLocation` 从 `editor` 改为 `view`，恢复新建集成终端在底部面板打开。

### 实现方式

- 保留 `workbench.panel.defaultLocation: "bottom"`，使终端视图继续位于底部；`terminal.integrated.tabs.enabled: false` 保持不变，多个会话仍不显示终端实例侧边栏。

### 验证

- Node.js 已成功解析 `settings.json`，确认终端默认位置为 `view`、面板位置为 `bottom`，且终端实例标签保持关闭。
- `git diff --check -- settings.json` 通过。

### 潜在或遗留问题

- 已打开的终端实例不一定会自动迁移；新建终端或重载 VS Code 窗口后应用该位置设置。

============================================================

## 15. 【2026-08-09 22:52】- 关闭多终端会话侧边栏

### 修改内容

- 在 `settings.json` 中将 `terminal.integrated.tabs.enabled` 设为 `false`，关闭多个集成终端会话时显示的终端实例侧边栏与标签列表。

### 实现方式

- 使用 VS Code 内置终端标签显示设置，仅隐藏终端会话列表；既有终端会话、创建终端和通过命令切换终端的功能不受影响。

### 验证

- Node.js 已成功解析 `settings.json`，并确认 `terminal.integrated.tabs.enabled` 为 `false`。
- `git diff --check -- settings.json` 通过。

### 潜在或遗留问题

- VS Code 可能需要重新加载窗口后才会刷新已打开终端的侧边栏显示。

============================================================

## 14. 【2026-08-09 21:59】- 启用 Ruff Markdown 预览格式化

### 修改内容

- 在用户级 Ruff 配置 `~/.config/ruff/ruff.toml` 的 `[format]` 段启用 `preview = true`，允许 Ruff 格式化 Markdown 中的 Python 代码块。
- 删除 VS Code 用户配置仓库根目录中仅用于临时验证的 `ruff.toml`。

### 实现方式

- 保留现有全局 Ruff 的 Python 版本、lint 与格式化规则，仅增加预览格式器开关，使未提供项目级 Ruff 配置的项目自动继承该行为。

### 验证

- `ruff format --check HANDOFF.md` 通过，确认 Ruff 自动发现用户级配置后可格式化 Markdown。
- `ruff format --config ~/.config/ruff/ruff.toml --check HANDOFF.md` 通过。
- 已确认临时 `ruff.toml` 不再存在于 VS Code 用户配置仓库根目录。

### 潜在或遗留问题

- 项目内的 `ruff.toml` 或 `pyproject.toml` 若定义 `[format] preview`，会覆盖用户级配置；应在项目配置中同步设为 `true`。
============================================================

## 13. 【2026-08-09 20:00】- 启用 GitHub Copilot 全语言补全

### 修改内容

- 在 `settings.json` 中为纯文本、Markdown 与源代码管理输入框启用 GitHub Copilot 补全，统一为所有语言和文本输入场景可用。

### 实现方式

- 保留已有的 Copilot Chat、Agent、代码搜索、内联建议与 Next Edit 配置，仅将 `github.copilot.enable` 中被显式禁用的三项改为 `true`。
- 已确认当前 VS Code 内置 GitHub Copilot Chat 0.60.0，无需另行安装扩展。

### 验证

- Node.js 已解析 `settings.json`，确认 `github.copilot.enable` 的 `*`、`plaintext`、`markdown`、`scminput` 与 `python` 均为 `true`。
- `git diff --check -- settings.json HANDOFF.md` 通过。

### 潜在或遗留问题

- Copilot 的实际可用性仍取决于 VS Code 中已登录具备 Copilot 权限的 GitHub 账户和网络连接。
- 需要重载 VS Code 窗口后，已打开的编辑器和源代码管理输入框才会完整应用新配置。

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
