# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This is a personal VSCode configuration repository synced to multiple remotes (GitHub & Gitee). It contains editor settings, Vim plugin configuration, keybindings, and code snippets.

## Git Commands

```bash
# Push to both remotes
git push -u origin main && git push gitee main

# Pull from both remotes
git pull origin main && git pull gitee main
```

## Configuration Architecture

This repository uses a **hybrid Vim configuration approach** across multiple files:

### 1. Three-Tier Configuration System

**Tier 1: `settings.json`** - VSCode Vim plugin settings

- Plugin toggles (EasyMotion, Sneak, Neovim backend disabled)
- `vim.handleKeys` - Controls which keys VSCode intercepts vs passes to Vim
- `vim.textobjKeybindings` - Custom text objects (JSON format overrides .vimrc)
- Smart Input Pro configuration (Chinese/English auto-switch based on context)
- Code Runner executorMap (Node.js path: `/opt/homebrew/bin/node`)

**Tier 2: `~/.vimrc`** - Standard Vim mappings

- Leader key: Comma (`,`)
- System-level mappings (Ctrl+J/K for half-page scrolling)
- Text objects: `iq`→`i"`, `ie`→`i'`
- Note: Limited .vimrc support in VSCode Vim (no Ex commands like `:m .+1`)

**Tier 3: `keybindings.json`** - VSCode-native shortcuts

- Option key mappings require BOTH `keybindings.json` entry AND `vim.handleKeys` entry
- Uses `vim.remap` command for Vim sequences
- Smart file runner (Cmd+3): HTML→Live Server, Python→execInTerminal, JS/TS→Code Runner

### 2. Critical Configuration Pattern

**Option Key Mappings** require two steps:

Step 1 - Add to `keybindings.json`:

```json
{
	"key": "alt+h",
	"command": "vim.remap",
	"when": "vim.mode == 'Normal'",
	"args": { "after": ["^"] }
}
```

Step 2 - Add to `settings.json` vim.handleKeys:

```json
"vim.handleKeys": {
  "<A-h>": false  // Prevent Vim plugin from intercepting
}
```

### 3. Input Method Auto-Switching (Smart Input Pro)

The configuration uses **Smart Input Pro** extension for intelligent Chinese/English switching:

- **Cursor colors**: Green for English mode, Red for Chinese mode
- **Context-aware switching**: Automatically switches based on file type and cursor position
- **Vim mode switching**: Normal/Visual → English, Insert → Mother Tongue
- **Regex-based rules**: Adds space between Chinese characters when typing English

Key language rules:
- Code files (.js, .py, .html, etc.): Default to English in strings, comments in Chinese
- Markdown files: Strings in Chinese, comments in Chinese

### 4. Editor Settings Highlights

- **Relative line numbers** (Vim mode optimal)
- **Tab characters** (not spaces) for indentation
- **Format on save** enabled with Prettier
- **Python interpreter** at `/Users/dyx/Code/0.python-venv/mySite-django5.0-py3.12/bin/python3`
- **Python language server**: Pylance
- **Network proxy** at `http://127.0.0.1:7890`

## Key Shortcut Reference

| Shortcut | Action | Mode |
|----------|--------|------|
| `Ctrl+\` | Toggle terminal | All |
| `Option+Q` | Toggle sidebar | All |
| `Option+H/L` | Line start/end | Normal |
| `Option+J/K` | Move line down/up | Non-Insert |
| `Option+V` | Visual block mode | All |
| `Option+D` | Delete line | Insert |
| `Option+Z` | Center cursor | Normal |
| `Ctrl+D` | Clear line + Insert mode | Normal/Insert |
| `Cmd+1` | Next error/warning | All |
| `Cmd+2` | Format document | All |
| `Cmd+3` | Smart file run | Editor focus |
| `Cmd+I` | AceJump | All |
| `Cmd+R` | Find/replace | Editor focus |
| `S` | EasyMotion | Normal |
| `Alt+-/=` | Prev/next tab | All |

## File Locations

**Repo files** (tracked in git):

- `settings.json` - VSCode settings
- `keybindings.json` - Keyboard shortcuts
- `snippets/` - Code snippets (c.json, html.json)
- `.gitignore` - Excludes `globalStorage/`, `workspaceStorage/`, `History/`, `sync/`, `.claude/`

**External reference** (not in repo):

- `~/.vimrc` - Referenced by `vim.vimrc.path` in settings.json

**To be created on commit**:

- `.vscode/extensions.json` - Auto-generated from `code --list-extensions`

## Installed Extensions

Key extensions installed:
- **Vim**: `vscodevim.vim`
- **Python**: `ms-python.python`, `ms-python.vscode-pylance`
- **Docker**: `ms-vscode-remote.remote-ssh`, `ms-azuretools.vscode-docker`
- **Web**: `ritwickdey.liveserver`, `esbenp.prettier-vscode`
- **Tailwind**: `bradlc.vscode-tailwindcss`
- **Input**: `xiaolvpuzi.smart-input-pro-vscode`
- **Runner**: `formulahendry.code-runner`

## Important Notes

- `.vimrc` has limited support in VSCode Vim (no Ex commands, complex scripts)
- For custom text objects, prefer `vim.textobjKeybindings` in settings.json over .vimrc
- Always test Option key mappings - they may not work if `vim.handleKeys` is not configured
- The `s` key is remapped to EasyMotion (via settings.json), overriding default Vim behavior
- Ctrl+D is remapped to clear line (not default Vim half-page down)
- Leader key in `.vimrc` is comma `,`, but settings.json may override to space

---

## 开发工作流程指南

### 通用规则

- **始终使用中文回答**
- **所有配置文件每一行都要以英文逗号结尾**（除了最后一项和注释行）
- **所有配置文件保持Tab缩进**
- **不要主动提交**，等用户明确指示
- **提交前必须运行** `code --list-extensions` 更新 `.vscode/extensions.json`

### 提交流程

```bash
# 1. 获取当前时间
date "+%Y-%m-%d %H:%M"

# 2. 更新扩展列表
code --list-extensions > .vscode/extensions.json

# 3. 添加更改
git add .

# 4. 提交（严格遵循格式）
git commit -m "+2026-02-03 15:52 具体的中文提交信息"

# 5. 推送到两个远程仓库
git push origin main && git push gitee main
```

**提交信息格式**: `+YYYY-MM-DD HH:MM 中文描述`（使用 `+` 而非日期空格）
