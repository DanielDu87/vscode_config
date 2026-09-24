# HANDOFF

本文件记录最近 10 条关键修改。最新记录置顶，历史记录按时间从新到旧排列。
记录标题格式为 `## 序号. 【YYYY-MM-DD HH:MM】- 标题`；序号持续递增，最大为 999，达到后从 1 开始。
记录超过 10 条时自动删除底部最旧记录。实质修改完成并验证后更新一次；创建 commit 前核对并一起提交。

============================================================

## 48. 【2026-09-24 15:14】- 新增本地扩展「清空行 + 优化导入 + 格式化」命令与右键入口

### 修改内容

- 新建本地 VS Code 扩展 `~/.vscode/extensions/remove-blank-lines/`（`package.json` + `src/extension.js`，当前 v0.2.0）：注册命令 `removeBlankLines.optimizeAndFormat`（命令面板显示 "Clean: Remove Blank Lines, Optimize Imports & Format"，可直接搜索），并贡献到编辑器右键菜单（`menus.editor/context`，`1_modification` 组）。执行链：删除全部空行（含纯空格/Tab 行，单个可撤销 edit）→ 优化导入 → 格式化。
- `settings.json`：移除本轮过渡方案 `multiCommand.commands` 块（multi-command 动态注册的命令不出现在命令面板搜索，已被本地扩展替代）。
- `keybindings.json`：新增 Shift+Cmd+I 优化导入——Python 文件映射 `ruff.executeOrganizeImports`，其他语言映射内置 `editor.action.organizeImports`。
- `.vscode/extensions.json`：按字母序登记 `dyx.remove-blank-lines`。
- `.gitignore`：补充 `.handoff-backups/`（`handoff-prune.sh` 修改前备份目录）。

### 实现方式

- 「没有效果」根因：`ryuta46.multi-command` 用 `vscode.commands.registerCommand` 动态注册的命令不会进入命令面板搜索，只能经 "Multi command: Execute multi command" 两步选择器触发；本地扩展通过 `contributes.commands` + `contributes.menus` 直接提供命令面板与右键两个入口。
- 扩展内部每一步 `await`：规避 `remove-all-empty-lines` 扩展不 `await editor.edit` 导致的时序竞态；`safeExec` 吞掉「命令不存在/无 provider」错误防止链条中断。
- v0.2.0 时序修复：用户实测报 "Ruff was unable to apply edits: unspecified reason"——大改动落盘后 Ruff LSP 尚未同步 `didChange`，基于旧文档版本计算的 edits 经 `workspace.applyEdit` 应用失败（Ruff 扩展未实现过期请求取消）。修法：删空行后与 Ruff 两步命令之间各加 300ms `delay`。
- 语言路由：Python 走 `ruff.executeOrganizeImports` / `ruff.executeFormat`（不弹 provider 选择框），其他语言回退内置 `editor.action.organizeImports` / `editor.action.formatDocument`。
- 扩展位于仓库外（`~/.vscode/extensions/`），删除该文件夹即卸载；参考同目录已工作的 `remove-all-empty-lines`（无版本号后缀文件夹也能被扫描加载）。

### 验证

- `node --check` 通过（extension.js）；`package.json` JSON 解析通过；`settings.json` 尾部确认 `multiCommand` 块移除干净；`keybindings.json` 去注释去尾逗号后解析通过，Shift+Cmd+I 两条绑定确认存在。
- VS Code 实际加载与命令执行待用户重载窗口后确认（扩展目录改动需 Developer: Reload Window 生效）。

### 潜在或遗留问题

- 扩展源码在仓库外，本仓库无备份；换机需按 HANDOFF 本条记录重建，或后续将源码副本入库。
- 顶部菜单栏（File/Edit 等主菜单）为封闭 API，本地扩展无法注入，本次仅提供命令面板 + 右键两个入口。

============================================================

## 47. 【2026-09-24 11:24】- markdownlint 按熊掌记 Markdown 方言配置并接管 Markdown 格式化

### 修改内容

- 新增 `.markdownlint.json`：按熊掌记（Bear）Markdown 方言调整规则——MD003 强制 ATX 标题（Bear 禁 setext）、MD018 关闭（行首 `#tag` 是标签非缺空格标题）、MD013 关闭（软换行不限行长）、MD024 关闭（同级重复标题合法）、MD040 关闭（代码块可不带语言）、MD046 强制 ``` 围栏（Bear 禁缩进代码块）、MD048 强制反引号围栏（官方仅支持 ```，`~` 是下划线语法）、MD041 关闭（笔记不必以标题开头）。
- `settings.json`：`markdownlint.config` 弃用改为 `markdownlint.configFile` 指向同目录 `.markdownlint.json`（绝对路径绑定本机用户名，跨机器需改）；`[markdown].editor.defaultFormatter` 由 `charliermarsh.ruff`（Python 格式化器，无法处理 Markdown）改为 `davidanson.vscode-markdownlint`，配合全局 `editor.formatOnSave` 实现保存时按熊掌记规则自动修复。
- 同一提交包含本任务前已存在的用户配置变更：`keybindings.json`+`tasks.json` 将 Cmd+3 Python 运行改为任务「运行当前 Python 文件（zshrc 环境）」（经 `/Users/dyx/.local/bin/python-run`）；`settings.json` 新增 `pasteAndIndent.selectAfter`；`.vscode/extensions.json` 同步实际安装列表，新增 00.python-paste-pro、davidanson.vscode-markdownlint、ms-toolsai.datawrangler、openai.codex-audio。

### 实现方式

- Bear 方言依据：官方 FAQ（bear.app/zh/faq/how-to-use-markdown-in-bear/）确认 CommonMark 基线、代码块仅 ``` 围栏；标题/删除线/下划线/高亮等语法与 markdownlint 默认规则不冲突，未调整。
- markdownlint VSCode 扩展 v0.62.1 README 确认其注册为 Markdown 格式化器（格式化 = 应用规则修复），`markdownlint.config` 已弃用。
- `markdownlint.run: onType`、severity 降级（Error→Warning→Information）均为插件默认值，未显式写入。

### 验证

- `.markdownlint.json` 与 `settings.json` 剔除注释后 JSON 解析通过；`markdownlint.configFile` 路径解析正确。
- 扩展列表由实际安装路径 `code --list-extensions` 实时生成，diff 仅含上述 4 处新增。
- 尚未在 VS Code 中实测保存 .md 文件的自动修复行为（需重载窗口）。

### 潜在或遗留问题

- `markdownlint.configFile` 为 `/Users/dyx/...` 绝对路径，仓库同步到其他用户名/系统机器时该行需按实际路径修改。
- markdownlint「格式化」仅修复违规项，不重排表格/换行；如需排版级格式化需另配 Prettier（与熊掌记软换行段落有冲突风险，暂不引入）。

============================================================

## 46. 【2026-09-18 13:12】- 收窄「代码说明」指令文件的触发条件

### 修改内容

- `prompts/代码说明.instructions.md`：将原第 7 行单句触发描述（「请求『说明』等相似操作……若与说明无关直接回答」）替换为独立的「适用判定（先判定，后执行）」章节；frontmatter `description` 同步补充适用边界。
- 同一提交包含本任务前已存在的用户配置变更：`settings.json` 开启 `git.enableSmartCommit`，新增 `stats.glmApiKey`/`stats.claudeApiKey`（值与已确认公开的 `glmStatus.apiKey` 相同，本机未安装对应 stats 扩展）；`.vscode/extensions.json` 按实际安装列表同步，移除 glm-chat-provider、glm-status-vscode。

### 实现方式

- 判定要求三个条件同时成立：存在代码选区、请求针对整个选区而非局部、请求目的是通篇讲解（列举「说明」「解释这段代码」「讲解」及 'Write an explanation for the active selection as paragraphs of text.' 等明确说法）。
- 显式列出五类不适用情形（无选区提问、有选区但问具体点、修改/重构/追问类、只要答案不要通篇结构、拿不准），规定拿不准时默认不适用且本文件后续规则一概不生效；「通用要求」「输出结构」正文未改动。
- 动机：instruction 文件随 `applyTo: '**'` 注入每次对话，原触发词「说明」为高频动词、排除条款过弱，普通询问会被套用结构化输出；同目录 `加注释.instructions.md` 因触发词列表明确未出现此问题。
- 更新前检查 `.gitignore` 已覆盖本仓库实际产物类型，本次改动未引入新文件类别，无需完善；仓库无 Docker 场景，不创建 `.dockerignore`。

### 验证

- `prettier --write prompts/代码说明.instructions.md` 通过，仅归一 frontmatter 引号与多余空行，正文与示例代码块不变。
- `git diff --check` 通过；`git diff --stat` 确认本次改动仅限该文件（`settings.json` 的改动为本轮任务前已存在，未触碰）。
- 尚未在 VS Code Chat 中分别用普通询问和真实选区实测触发行为。

### 潜在或遗留问题

- 门控效果取决于宿主模型对注入指令的遵循度，需在 VS Code 中用普通问题回归验证；若仍偶发误触发，可再收紧 `applyTo` 或改为按需显式调用。

============================================================

## 45. 【2026-09-17 13:01】- 关闭聊天输入框补全并新增模型与预览配置

### 修改内容

- `settings.json` 关闭 Copilot 聊天输入框的内联补全（`github.copilot.completions.chat.enabled` 改为 `false`），不影响编辑器代码补全。
- `chatLanguageModels.json` 新增「公司账号」自定义端点（glm-5.3，chat-completions）与 GLM 供应商条目（`reasoningEffort: max`），并修复 GLM 条目重复的 `settings` 键。
- `settings.json` 新增 markdown-preview-enhanced 系列配置、glmStatus 状态栏配置、关闭终端粘性滚动、开启 chat 检查点文件变更显示；PDF 改用 cweijan.officeViewer、Markdown 改用 cweijan.markdownViewer 打开；深色主题固定 GitHub Dark Dimmed；移除 `vscode-office.editMode` 与中文符号替换规则。
- `.vscode/extensions.json` 同步实际安装列表：新增 glm-chat-provider、glm-status-vscode、vscode-yaml、mobile-canvas、markdown-preview-enhanced，移除 markdown-all-in-one。

### 实现方式

- `github.copilot.completions.chat.enabled` 的作用经内置 copilot 扩展 `package.json` 定义确认（"是否在聊天中启用内联补全"，默认 `false`），仅控制聊天输入框，不涉及 `editor.inlineSuggest.enabled`。
- GLM 条目删除重复 `settings` 键中的空对象一份，保留含 `reasoningEffort` 的配置，与 JSONC 后键生效行为一致。

### 验证

- `git diff --check` 通过；`settings.json`、`chatLanguageModels.json` 剔除注释后 JSON 解析通过。
- 扩展列表由 `code --list-extensions` 实时生成，diff 仅含上述 6 处增删。

### 潜在或遗留问题

- `glmStatus.apiKey` 与「公司账号」服务器地址已按用户确认随仓库提交到公开远程（GitHub/Gitee）。
- `/usr/local/bin/code` 符号链接指向不存在的 `/Applications/VSCode.app`，本次改用实际路径执行；如需修复可重建该链接。

============================================================

## 44. 【2026-08-18 23:48】- 保存不自动优化导入并关闭终端自动激活

### 修改内容

- `settings.json` 将 Python 保存动作调整为不自动修复、不自动整理导入，避免 Ruff 顺带删除未使用导入。
- 关闭 Python Environments 扩展的终端自动激活，打开集成终端时不再自动进入 `/Users/dyx/Code/Agent/.venv`。

### 实现方式

- 修改 `[python].editor.codeActionsOnSave` 的 `source.fixAll.ruff` 与 `source.organizeImports.ruff` 为 `"never"`；Ruff 仍负责保存时格式化。
- 将 `python-envs.terminal.autoActivationType` 由 `"command"` 改为 `"off"`。
- 三处均保留注释说明原始/恢复值，方便以后改回 `"always"` 或 `"command"`。

### 验证

- 剔除注释与尾逗号后 JSONC 解析通过，目标配置值均为预期值。
- `git diff --check` 通过，`settings.json` 最终 diff 仅含上述配置变更。

### 潜在或遗留问题

- 手动整理导入需通过命令面板或快捷键触发；`python-envs.terminal.autoActivationType` 属 machine 级设置，需重载窗口后生效。

============================================================

## 43. 【2026-08-18 11:47】- 代码结构注释点明结果特征

### 修改内容

- 调整 `prompts/代码说明.instructions.md` 的「二、代码结构（从上到下）」：注释说明产物或作用时直接点明结果特征，不用「可用的」「通用的」这类空泛词。

### 实现方式

- 在注释规则后补充：说明产物或作用时直接点明结果特征，例如写「用于构建一个按相似度检索的检索器」而非「用于构建一个可用的检索器」。

### 验证

- `git diff --check -- prompts/代码说明.instructions.md HANDOFF.md` 通过。
- `rg -n '不用「可用的」「通用的」这类空泛词' prompts/代码说明.instructions.md` 已确认目标规则存在。
- 尚未在 VS Code 图形界面用真实代码选区验证模型输出。

### 潜在或遗留问题

- Copilot 最终输出仍受模型指令遵循能力影响；需要在 VS Code 中重新触发「说明」确认实际格式。

============================================================

## 42. 【2026-08-18 11:47】- 代码结构注释参数用词规范化

### 修改内容

- 调整 `prompts/代码说明.instructions.md` 的「二、代码结构（从上到下）」：注释涉及参数时要求用完整说法，不写「接收……参数」这类省略。

### 实现方式

- 在注释规则后补充：涉及参数时用「接受……作为参数」「接收一个……实例作为参数」等完整说法。
- 示例注释由「接收嵌入模型参数」改为「接收一个嵌入模型实例作为参数」。

### 验证

- `git diff --check -- prompts/代码说明.instructions.md HANDOFF.md` 通过。
- `rg -n '接受……作为参数|接收一个……实例作为参数' prompts/代码说明.instructions.md` 已确认目标规则存在。
- 尚未在 VS Code 图形界面用真实代码选区验证模型输出。

### 潜在或遗留问题

- Copilot 最终输出仍受模型指令遵循能力影响；需要在 VS Code 中重新触发「说明」确认实际格式。

============================================================

## 41. 【2026-08-18 11:47】- 整体作用每步交代操作与产物

### 修改内容

- 调整 `prompts/代码说明.instructions.md` 的「一、作用说明」：整体作用依次描述每一步处理时，每步必须同时交代「操作与产物」。
- 要求每步用一句话或一个分句点出操作与产物，不再展开产物内部细节。
- 若该步带有影响结果形态的关键参数或配置（如搜索类型、返回数量），在点出操作与产物时顺带说明该参数带来的结果特征，不展开全部参数细节。

### 实现方式

- 在第一章整体作用规则后新增一条规则，并给出示例：最后一步封装检索器时点明搜索类型为相似度匹配并返回最相关的 3 个片段。

### 验证

- `git diff --check -- prompts/代码说明.instructions.md` 通过。
- `rg -n '每步必须同时交代「操作与产物」|得到/生成/返回/切分成' prompts/代码说明.instructions.md` 已确认目标规则存在。
- 尚未在 VS Code 图形界面用真实代码选区验证模型输出。

### 潜在或遗留问题

- Copilot 最终输出仍受模型指令遵循能力影响；需要在 VS Code 中重新触发「说明」确认实际格式。

============================================================

## 40. 【2026-08-18 10:45】- 代码结构强化保留原有缩进

### 修改内容

- 调整 `prompts/代码说明.instructions.md` 的「二、代码结构（从上到下）」：明确代码框内必须保持选中代码原有缩进。

### 实现方式

- 在第二章代码结构规则中补充“代码框内必须保持选中代码原有缩进”。
- 保留原有“真实代码行必须逐字保留源码原有缩进层级，不得顶格、增减缩进或重新排版”的约束。

### 验证

- `git diff --check -- prompts/代码说明.instructions.md HANDOFF.md` 通过。
- `rg -n '代码框内必须保持选中代码原有缩进|真实代码行必须逐字保留源码原有缩进层级' prompts/代码说明.instructions.md HANDOFF.md` 已确认目标规则存在。
- 尚未在 VS Code 图形界面用真实代码选区验证模型输出。

### 潜在或遗留问题

- Copilot 最终输出仍受模型指令遵循能力影响；需要在 VS Code 中重新触发「说明」确认实际格式。

============================================================

## 39. 【2026-08-18 10:23】- 调用说明补充调用结果动作

### 修改内容

- 调整 `prompts/代码说明.instructions.md` 的「三、调用说明」：每个函数、类实例化或方法调用区块的第一行，除说明调用动作外，还必须说明调用后得到什么。
- 函数调用句式补充“构建/创建/计算/返回……”，类实例化补充“创建……实例”，方法调用补充“获取/读取/生成/更新……”。

### 实现方式

- 更新第三章标题下第一行动作说明规则，使 `file_reader` 这类函数可写成“调用 `file_reader` 函数，构建/创建……”。
- 同步更新“调用函数或方法时使用以下格式”的模板首行，要求输出结果动作而不是只写“调用……函数/方法”。

### 验证

- `git diff --check -- prompts/代码说明.instructions.md` 通过。
- `rg -n '每个标题下第一行|调用 `函数或对象\.方法名`|构建/创建/获取/读取/生成/更新' prompts/代码说明.instructions.md` 已确认目标规则存在。
- 尚未在 VS Code 图形界面用真实代码选区验证模型输出。

### 潜在或遗留问题

- Copilot 最终输出仍受模型指令遵循能力影响；需要在 VS Code 中重新触发「说明」确认实际格式。

============================================================
