# Project Conventions

This is an Obsidian notes vault covering programming courses. AI agents must read this file before modifying content.

## Core rule: bilingual content sync

Most course content exists in paired Chinese and English versions. **Any content modification requested by the user must be applied identically to both language versions** — same structural change in both, with prose translated accordingly.

If the user explicitly asks for a change in only one version, still point out that the other version now diverges.

## Two structural patterns

### Pattern A: folder pairs (chapter-per-file)

Used by: `python/`, `devops/network-basics/`, `C++/`, `web-development/django/`, `devops/linux/`, `tools/photoshop/`.

- Paired folders: `xxx-中文版/` ↔ `xxx-english-version/` (C++ uses `c++-english-version/`).
- Numbered chapter files: `01-变量与Python基础.md` ↔ `01-variables-and-python-basics.md` (same numbers, names in the folder's language).
- Each folder has a `README.md` with a table of contents in that folder's language.
- Chapter files carry navigation links at top/bottom, in the folder's language, pointing to that folder's file names (e.g. `[下一篇：xxx →](02-xxx.md)` ↔ `[Next: xxx →](02-xxx.md)`).
- Section numbering (e.g. `1.1.2`) is identical across languages.
- The English C++ folder additionally groups chapters into `phase1-fundamentals/` etc.; the Chinese folder is flat.

### Pattern B: single-file pairs

Used by: `tools/LaTeX/`, `tools/markdown/`, `tools/Microsoft/Microsoft Outlook/`, `devops/command-line/`.

- Two md files side by side: `XX-中文版.md` + `XX-English version.md`.
- Images live in a shared `image/` subfolder, referenced with Obsidian wikilinks: `![[name.png]]` (optionally `![[name.png|width]]`).

## Code comment language by area

- `python/` folders: code comments stay in English in both versions.
- `devops/network-basics/`: Chinese comments in the Chinese version, English comments in the English version (md code blocks and `examples/` scripts alike).

## devops/network-basics shared assets

- `image/` holds images shared by both language versions, referenced with wikilinks (e.g. `![[tcp-three-way-handshake.png]]`).
- `examples/zh/` and `examples/en/` hold the runnable example scripts — identical code, Chinese vs English comments. **Any change to an example must be applied to both copies**, and to the matching code blocks in both language versions of the chapter.
- Chapter links point to `../examples/zh/...` (Chinese) and `../examples/en/...` (English).

## Repository root

- Three READMEs exist side by side: `README.md`, `README-中文版.md`, `README-English version.md`. If a change affects what a README describes, check which of them need updating.
- `Recommended Textbooks/` folders and `C++/c++-exercises/` hold non-chapter content; treat them as appendices unless asked otherwise.

## Git workflow

- Commit style: conventional-prefix messages such as `docs(network-basics): ... (zh+en)`; older commits may be plain Chinese summaries — either is acceptable, prefer the conventional-prefix style.
- Only commit when the user asks; never push to a remote without an explicit request.
