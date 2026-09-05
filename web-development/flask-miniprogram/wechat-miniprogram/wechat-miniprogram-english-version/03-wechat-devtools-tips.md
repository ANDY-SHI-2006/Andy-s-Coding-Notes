[← Previous: Mini Program Configuration](02-miniprogram-configuration.md) | [Next: Template Syntax →](04-template-syntax.md)

# 3 WeChat DevTools Tips

This chapter collects several practical tips in WeChat DevTools that noticeably improve development efficiency: quickly creating pages, common keyboard shortcuts, file auto save, appearance and theme settings, and font size adjustment.

## 3.1 Quickly Creating Mini Program Pages

When adding a new page, you don't need to create the folder and files by hand: simply add the page path to the `pages` array in `app.json`. After saving, DevTools **automatically creates the page directory and its four base files** (`.js`, `.json`, `.wxml`, `.wxss`).

```json
{
  "pages": [
    "pages/index/index",
    "pages/logs/logs",
    "pages/test/test",
    "pages/demo/demo"
  ]
}
```

For example, append `"pages/demo/demo"` to the `pages` array and save — the tool will generate the `pages/demo/` directory along with the four files `demo.js`, `demo.json`, `demo.wxml`, and `demo.wxss`.

![[ch03-01.png]]

> Tip: the first entry in the `pages` array is the mini program's home page. Reorder the array to change the home page.

## 3.2 Keyboard Shortcuts

Two ways to view and configure shortcuts:

- Option 1: `File` → `Preferences` → `Keyboard Shortcuts` (`Ctrl+K Ctrl+S`)
- Option 2: `Settings` → `Keyboard Shortcuts`

Common shortcuts:

| Action | Shortcut |
| --- | --- |
| Single-line comment | `Ctrl + /` |
| Multi-line (block) comment | `Shift + Alt + A` |
| Format document | `Shift + Alt + F` |
| Cut | `Ctrl + X` |
| Copy | `Ctrl + C` |
| Paste | `Ctrl + V` |

> Note: wxml, js, and wxss files use different comment syntaxes (wxml uses `<!-- -->`, js uses `//` and `/* */`, wxss uses `/* */`). When you use the comment shortcut, the tool automatically inserts the comment marker that matches the current file type.

## 3.3 File Auto Save

Auto save is enabled by default. You can toggle it in the menu bar via `File` → `Auto Save`.

![[ch03-02.png]]

For finer control, go to `File` → `Preferences` → `Settings` and adjust the `Files: Auto Save` option (e.g. `afterDelay`, which saves automatically after a short delay).

## 3.4 Appearance and Theme

Entry: `Settings` → `Appearance` → `Theme`.

What you can configure:

- **Theme**: dark / light / follow system (applies to the whole interface except the debugger).
- **Debugger theme**: dark / light / follow system / follow custom appearance.
- **Custom appearance**: use the default appearance or a custom one; dark and light appearance configurations can be edited separately, and the tool can ask for adaptation when the editor theme changes.
- **Title content**: the information shown in the main window title bar (current file or project name).

![[ch03-03.png]]

## 3.5 Font Size Adjustment

Entry: `File` → `Preferences` → `Settings`, then edit the common settings directly:

- `Editor: Font Size`: controls the editor font size in pixels (e.g. `16`).
- `Editor: Font Family`: controls the editor font family (e.g. `Consolas`).
- `Editor: Tab Size`: the tab width (e.g. `2`).

![[ch03-04.png]]

![[ch03-05.png]]

[← Previous: Mini Program Configuration](02-miniprogram-configuration.md) | [Next: Template Syntax →](04-template-syntax.md)
