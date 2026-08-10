## 根因

`ciq` 与 `cie` 的异常来自两套不兼容且彼此冲突的映射：

- `settings.json` 的 `vim.textobjKeybindings` 不是当前已安装 VSCodeVim `1.32.4` 支持的设置，并且其 `before` 将 `iq`、`ie` 写成了单个字符串而不是独立按键。
- `keybindings.json` 将普通模式下的单个 `q` 直接绑定为 `vim.remap`。`vim.remap` 不会用 `args.before` 识别此前已输入的 `ci`，因此该绑定会劫持原生 `q`，导致 `ciq` 出现多余或异常输入。
- `ie` 在 VSCodeVim 中本来就是内置文本对象，含义为“整份文档（去除首尾空白）”；故 `cie` 被解析成改变整份文档，造成删除范围过大。

## 实施步骤

1. 在 `settings.json` 删除无效的 `vim.textobjKeybindings` 配置，改用 VSCodeVim 官方支持的 `vim.operatorPendingModeKeyBindingsNonRecursive`：

   ```jsonc
   "vim.operatorPendingModeKeyBindingsNonRecursive": [
     {
       "before": ["i", "q"],
       "after": ["i", "\""]
     },
     {
       "before": ["i", "e"],
       "after": ["i", "'"]
     }
   ]
   ```

   这使 `ciq`、`diq`、`yiq` 映射为双引号内文本对象；`cie`、`die`、`yie` 映射为单引号内文本对象，只在操作符等待状态生效。

2. 在 `keybindings.json` 删除错误的单键 `q` / `vim.remap` 条目，使普通 Vim 的 `q` 宏录制行为恢复，避免它污染 `ciq` 的按键序列。

3. 同步 `CLAUDE.md`、`GEMINI.md` 中关于自定义文本对象的描述，明确映射位于 `vim.operatorPendingModeKeyBindingsNonRecursive`，不再引用无效的 `vim.textobjKeybindings`。

4. 更新当前 `HANDOFF.md` 记录，说明 `ciq` / `cie` 的根因、修复方式与重新加载窗口要求。

5. 验证：解析 `settings.json` 与 `keybindings.json` 的 JSONC；检索确认无效设置和独立 `q` 绑定不再存在；执行 `git diff --check`。最后需要重载 VS Code 窗口后，在双引号、单引号文本中手动验证 `ciq` / `cie`。