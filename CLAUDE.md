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
- Plugin toggles (EasyMotion, Sneak, Neovim backend)
- `vim.handleKeys` - Controls which keys VSCode intercepts vs passes to Vim
- `vim.textobjKeybindings` - Custom text objects (JSON format overrides .vimrc)
- Input method switching (Chinese/English auto-switch)

**Tier 2: `~/.vimrc`** - Standard Vim mappings
- Leader key: Space (``)
- System-level mappings (Ctrl+J/K for half-page scrolling)
- Text objects: `iq`→`i"`, `ie`→`i'` (also defined in settings.json for override)
- Buffer commands: `bb` (buffer switch), `bd` (buffer delete)
- Note: Limited .vimrc support in VSCode Vim (no Ex commands like `:m .+1`)

**Tier 3: `keybindings.json`** - VSCode-native shortcuts
- Option key mappings require BOTH `keybindings.json` entry AND `vim.handleKeys` entry
- Uses `vim.remap` command for Vim sequences
- Examples:
  - `Option+J/K` → Move lines down/up
  - `Option+V` → Visual block mode
  - `Option+Q` → Toggle sidebar
  - `Option+H/L` → Line start/end (Normal mode)
  - `S` → EasyMotion (Normal mode)
  - `Ctrl+D` → Clear line and enter insert mode

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

### 3. Input Method Auto-Switching

Automatically switches between Chinese (ITABC) and English (ABC) input methods:
- Uses `im-select` tool (installed via Homebrew at `/opt/homebrew/bin/im-select`)
- Switches to English when entering Normal mode
- Switches back to previous input when returning to Insert mode

### 4. Editor Settings Highlights

- **Relative line numbers** (Vim mode optimal)
- **Tab characters** (not spaces) for indentation
- **Format on save** enabled with Prettier
- **Live Server** uses Chrome Beta in private mode
- **Python interpreter** at `/Users/dyx/Code/0.python-venv/mySite-django5.0-py3.12/bin/python3`
- **Network proxy** at `http://127.0.0.1:7890`

## File Locations

**Repo files** (tracked in git):
- `settings.json` - VSCode settings
- `keybindings.json` - Keyboard shortcuts
- `snippets/` - Code snippets
- `.gitignore` - Excludes `globalStorage/`, `workspaceStorage/`, `History/`, `sync/`

**External reference** (not in repo):
- `~/.vimrc` - Referenced by `vim.vimrc.path` in settings.json

## Important Notes

- `.vimrc` has limited support in VSCode Vim (no Ex commands, complex scripts)
- For custom text objects, prefer `vim.textobjKeybindings` in settings.json over .vimrc
- Always test Option key mappings - they may not work if `vim.handleKeys` is not configured
- The `s` key is remapped to EasyMotion, overriding default Vim behavior
- Ctrl+D is remapped to clear line (not default Vim half-page down)
