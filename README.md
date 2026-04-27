# paper-scribe-skill

`paper-scribe` 是一个 Claude skill，用于把试卷、练习册照片、扫描 PDF、学习笔记截图和本地图片整理成可编辑的 Word、Markdown 或 HTML 文档。

这个仓库提供的是 **community npx installer**：它会把仓库里的 [skill/](skill/) 复制到本机 Claude 用户级 skills 目录。它不是 Claude 官方 plugin marketplace 安装方式。

## 安装

```bash
npx -y paper-scribe-skill
```

默认会安装到：

```text
~/.claude/skills/paper-scribe
```

安装前预览：

```bash
npx -y paper-scribe-skill --dry-run
```

覆盖已有安装：

```bash
npx -y paper-scribe-skill --force
```

安装到自定义 skills 根目录：

```bash
npx -y paper-scribe-skill --target ~/.claude/skills
```

注意：`--target` 指向 skills 根目录，最终目录始终是 `<target>/paper-scribe`。

## 本地开发验证

```bash
node bin/install.cjs --dry-run --target /tmp/paper-scribe-skills-test
node bin/install.cjs --target /tmp/paper-scribe-skills-test --force
test -f /tmp/paper-scribe-skills-test/paper-scribe/SKILL.md
test -f /tmp/paper-scribe-skills-test/paper-scribe/scripts/convert_workspace.py
npm pack --dry-run
```

## 卸载

```bash
rm -rf ~/.claude/skills/paper-scribe
```

## 仓库结构

```text
skill/
├── SKILL.md
├── references/
│   └── layout-style.md
└── scripts/
    └── convert_workspace.py

bin/
└── install.cjs
```

## 使用边界

这个 skill 会要求用户确认有权转换材料，且不会帮助绕过付费墙、DRM、登录限制、平台反爬、下载限制或水印/署名保护。
