# HANDOFF

本文件记录最近 10 条关键修改。最新记录置顶，历史记录按时间从新到旧排列。
记录标题格式为 `## 序号. 【YYYY-MM-DD HH:MM】- 标题`；序号持续递增，最大为 999，达到后从 1 开始。
记录超过 10 条时自动删除底部最旧记录。实质修改完成并验证后更新一次；创建 commit 前核对并一起提交。

============================================================

## 38. 【2026-08-17 18:52】- 代码结构空行改为真实空白行

### 修改内容

- 调整 `prompts/代码说明.instructions.md` 的「二、代码结构（从上到下）」：要求代码结构中的分隔空行必须是真实空白行。
- 删除示例代码块里的 `<空行>` 占位文字。

### 实现方式

- 将“一行注释，一行代码，一行空行”明确为“一行注释，一行代码，一行真实空白行”。
- 明确禁止输出 `<空行>`、`空行`、`blank line` 或任何表示空行的占位文字。
- 示例代码块改为直接保留空白行。

### 验证

- 待执行 `git diff --check` 和目标文本检查。
- 尚未在 VS Code 图形界面用真实代码选区验证模型输出。

### 潜在或遗留问题

- Copilot 最终输出仍受模型指令遵循能力影响；需要在 VS Code 中重新触发「说明」确认实际格式。

============================================================

## 37. 【2026-08-17 18:52】- 支持不完整代码选区说明

### 修改内容

- 调整 `prompts/代码说明.instructions.md` 的通用要求：用户选择的代码不完整时，先给必要提示，再只基于已选片段正常说明。

### 实现方式

- 明确不完整选区时先提示“以下只基于当前选中片段说明，未选中的上下文不展开解读”。
- 明确不得要求用户重新选择完整函数或文件。
- 只解读已选代码中实际出现的内容，不补全、推演或展开解释未选中的上文、下文、函数体、调用方或依赖实现。
- 对缺失的上文、下文、调用方、类型、返回值或副作用，标注「无法确定」或「推测」。
- 保持只基于选中代码回答、禁止读取文件和禁止工具调用的边界不变。

### 验证

- 待执行 `git diff --check` 和目标文本检查。
- 尚未在 VS Code 图形界面用真实代码选区验证模型输出。

### 潜在或遗留问题

- Copilot 最终输出仍受模型指令遵循能力影响；需要在 VS Code 中重新触发「说明」确认实际格式。

============================================================

## 36. 【2026-08-17 18:52】- 代码结构保留源码缩进

### 修改内容

- 调整 `prompts/代码说明.instructions.md` 的「二、代码结构（从上到下）」：要求真实代码行逐字保留源码原有缩进层级。

### 实现方式

- 在代码结构规则中明确保留真实名称、写法和缩进。
- 禁止为了展示而将代码顶格、增减缩进或重新排版。
- 保持注释行与代码行的展示结构不变。

### 验证

- 待执行 `git diff --check` 和目标文本检查。
- 尚未在 VS Code 图形界面用真实代码选区验证模型输出。

### 潜在或遗留问题

- Copilot 最终输出仍受模型指令遵循能力影响；需要在 VS Code 中重新触发「说明」确认实际格式。

============================================================

## 35. 【2026-08-17 18:52】- 调用说明强制每个函数方法独立标题

### 修改内容

- 调整 `prompts/代码说明.instructions.md` 的「三、调用说明」：每一个函数、类实例化或方法调用都必须单独作为二级标题，其说明放在该标题下的独立区块中。
- 标题只写原始函数名、类名或对象方法名，不使用反引号包裹。
- 撤销针对 VS Code/Copilot 可点击源码跳转渲染行为的压制规则，不再在提示词中禁止源码引用元数据、引用卡片或可点击格式。

### 实现方式

- 加强第三章首条规则，明确不得把多个函数、类或方法合并到同一个标题下说明。
- 标题格式改为 `## 函数名`、`## 类名`、`## 对象.方法名`。
- 第三章最后一个区块结束后立即停止，不额外追加“整体来看”“关键思想”“总结”等段落。
- 保持章节结构、参数结构化格式和源码顺序要求不变。

### 验证

- 待执行 `git diff --check` 和目标文本检查。
- 尚未在 VS Code 图形界面用真实代码选区验证模型输出。

### 潜在或遗留问题

- Copilot 最终输出仍受模型指令遵循能力影响；需要在 VS Code 中重新触发「说明」确认实际格式。

============================================================

## 34. 【2026-08-17 18:52】- 说明提示词拆分为三个章节

### 修改内容

- 调整 `prompts/代码说明.instructions.md`：删除「一、作用说明」中的调用链，将「调用说明」从「二、代码结构」中独立为「三、调用说明」。
- 更新提示词描述，使其反映整体作用、代码结构和分区块调用说明三个输出部分。

### 实现方式

- 第一章只输出整体作用。
- 第二章只输出按源码从上到下排列的代码结构代码框。
- 第三章按函数或方法分隔，每个名称作为标题并在独立区块中说明，保持源码顺序。
- 保留原有参数、返回值和不确定信息标注要求。

### 验证

- 待执行 `git diff --check` 和结构化文本检查。
- 尚未在 VS Code 图形界面用真实代码选区验证模型输出。

### 潜在或遗留问题

- Copilot 最终输出仍受模型指令遵循能力影响；需要在 VS Code 中重新触发「说明」确认实际格式。

============================================================

## 33. 【2026-08-17 18:52】- 调用说明改为按函数分区块

### 修改内容

- 调整 `prompts/代码说明.instructions.md` 的「调用说明」要求：从逐条顺序说明改为以函数或方法为分隔，每个函数名或方法名单独作为标题和独立区块。

### 实现方式

- 保留 `调用说明：` 作为第二部分入口。
- 新增标题格式约束：函数使用 `### <函数名>`，方法使用 `### <对象>.<方法名>`，且必须按源码从上到下顺序排列。
- 保留原有的函数/方法定义与调用句式、参数结构化格式要求。

### 验证

- 已通过 `git diff -- "prompts/代码说明.instructions.md" HANDOFF.md` 确认仅修改目标提示词文件与交接记录。
- 尚未在 VS Code 图形界面用真实代码选区验证模型输出。

### 潜在或遗留问题

- Copilot 最终输出仍受模型指令遵循能力影响；需要在 VS Code 中重新触发「说明」确认实际格式。

============================================================



### 修改内容

- 调整 `prompts/代码说明.instructions.md`：将原位于「一、作用说明」的“调用说明”及参数、返回值、结果解释移动到「二、代码结构（从上到下）」。

### 实现方式

- 「一、作用说明」只保留整体作用、单独一行“调用链：”和箭头调用顺序代码框，代码框结束后直接进入第二部分。
- 「二、代码结构」继续先输出“一行注释、一行代码”的代码框，再在代码框下方输出“调用说明：”。
- 函数或方法定义、调用的参数继续按名称、类型或数据结构、来源、用途分行展示，并保留返回结构和结果去向说明。

### 验证

- `git diff --check -- 'prompts/代码说明.instructions.md' HANDOFF.md` 通过。
- 已通过脚本核对第一部分不含“调用说明”，第二部分同时包含代码结构框和结构化调用说明，且调用说明位于代码框之后。
- 尚未在 VS Code 图形界面用真实代码选区验证模型输出。

### 潜在或遗留问题

- Copilot 最终格式仍受所选模型指令遵循能力影响；需在 VS Code 中重新触发「说明」确认实际输出。

============================================================

## 31. 【2026-08-15 19:40】- 提交 VS Code MCP 配置与模型授权

### 修改内容

- `mcp.json` 提交 VS Code MCP Gallery 安装的 Tavily 与 Firecrawl 服务器定义，凭据继续使用交互式输入占位符。
- `settings.json` 提交 VS Code 为上述两个 MCP 服务器写入的 `chat.mcp.serverSampling` 模型授权清单。

### 实现方式

- 按全局提交要求重新审查当前 worktree 的全部改动，不再沿用上次提交时的临时排除范围。
- 确认 Tavily 与 Firecrawl 已存在于 `~/.mcp/unified-mcp.yaml` 权威源；仓库 `mcp.json` 是 VS Code 用户配置文件，不是 `~/.mcp/sync.py` 当前管理的派生目标。
- `mcp.json` 仅保存 `${input:...}` 形式的密钥输入引用，不包含真实 API Key。

### 验证

- `uv run --with pyyaml python3 ~/.mcp/sync.py --dry-run` 通过，权威源共包含 8 个 MCP，并覆盖现有统一分发目标。
- `uv run --with pyyaml python3 ~/.mcp/test-connectivity.py` 通过，Bear、Computer Use、Context7、Firecrawl、Node REPL、Tailwind、Tavily 与 Vision 共 8 个 MCP 全部完成 initialize。
- Python JSON 解析 `mcp.json` 与 `settings.json` 通过；敏感字段检查确认未发现真实密钥；`git diff --check` 通过。

### 潜在或遗留问题

- `chat.mcp.serverSampling` 是 VS Code 自动维护的模型白名单，后续安装模型或调整 MCP 授权时可能产生较大配置差异。

============================================================

## 30. 【2026-08-15 19:25】- 更新图标主题与聊天会话视图

### 修改内容

- `settings.json` 将工作台图标主题从 `a-file-icon-vscode` 切换为 `vscode-icons`，并关闭聊天会话视图。

### 实现方式

- 提交 `workbench.iconTheme: "vscode-icons"` 与 `chat.viewSessions.enabled: false` 两项明确的用户偏好。
- `chat.mcp.serverSampling` 属 VS Code 自动写回的机器相关模型白名单，本次不暂存、不提交，也不丢弃工作区内容。
- `mcp.json` 中 Tavily/Firecrawl 已存在于 `~/.mcp/unified-mcp.yaml` 权威源，但 VS Code `mcp.json` 尚未纳入统一同步器宿主矩阵，因此本次继续保留为未提交本地改动。

### 验证

- `uv run --with pyyaml python3 ~/.mcp/sync.py --dry-run` 通过，确认 Tavily 和 Firecrawl 已在统一权威源及现有全端分发目标中。
- 已核对 `settings.json` 相对 HEAD 仅有 `workbench.iconTheme`、`chat.viewSessions.enabled` 和 `chat.mcp.serverSampling` 三个顶层变化；本次索引只包含前两项。
- VS Code 内置 CLI 返回的扩展清单与已提交 `.vscode/extensions.json` 一致。

### 潜在或遗留问题

- `mcp.json` 与 `chat.mcp.serverSampling` 仍是未提交本地改动；VS Code MCP 宿主需正式纳入统一同步矩阵并完成全端验证后再提交。

============================================================

## 29. 【2026-08-15 11:40】- 调用链仅保留调用元素与返回值

### 修改内容

- 调整 `prompts/代码说明.instructions.md` 的箭头调用顺序代码框：参数、变量和对象均不作为节点显示，只保留调用方、函数、方法、类和返回值。

### 实现方式

- 调用链节点统一使用 `<真实名称>（<类型>）` 格式，允许的类型仅为 `调用方`、`函数`、`方法`、`类`、`返回值`；禁止使用 `参数`、`变量` 和 `对象` 类型。
- 示例链路已移除 `file_path（参数）`、`documents（变量）`、`document_chunks（变量）`、`text_splitter（对象）`、`vector_store（对象）`，保留“调用方（调用方） → `build_retriever（函数）` → `file_reader（函数）` → `RecursiveCharacterTextSplitter（类）` → `split_documents（方法）` → `InMemoryVectorStore（类）` → `add_documents（方法）` → `as_retriever（方法）` → `VectorStoreRetriever（返回值）`”。
- 参数、变量和对象仍在代码框后的“调用说明”中结构化解释；对象可用于说明方法由谁调用，不影响完整性。
- 保持整体作用 → 单独一行“调用链：” → 箭头调用顺序代码框 → “调用说明：”及结构化参数说明的顺序；「代码结构」继续使用“一行注释，一行代码”。
- 提交时将 VS Code MCP Gallery 可再生成缓存目录 `mcp/` 加入 `.gitignore`；`mcp.json` 和 `settings.json` 的既有本地改动因尚未完成统一 MCP 同步、全端验证及用途确认，本次不暂存、不提交，也不丢弃。
- 使用 `/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code --list-extensions` 刷新 `.vscode/extensions.json`：新增 LLDB、Swift、Chat Customizations Evaluations 和 Codex Switch，移除当前未安装的 Qwen IDE Companion。

### 验证

- `git diff --check -- '.gitignore' 'prompts/代码说明.instructions.md' HANDOFF.md` 通过。
- 已通过脚本核对调用链示例不含参数、变量和对象节点，只保留调用方、函数、方法、类和返回值；“调用说明”及第二部分格式保持不变。
- 已确认 `mcp/` 下 4 个未跟踪文件为 VS Code MCP Gallery 可再生成缓存并由 `.gitignore` 排除；`mcp.json` 与 `settings.json` 保留为未提交本地改动。
- VS Code 内置 CLI 刷新扩展清单成功，共记录 53 个当前已安装扩展；清单已检查为非空、唯一且按名称排序。
- 尚未在 VS Code 图形界面用真实代码选区验证模型输出。

### 潜在或遗留问题

- Copilot 最终格式仍受所选模型指令遵循能力影响；需在 VS Code 中重新触发「说明」确认实际输出。

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
