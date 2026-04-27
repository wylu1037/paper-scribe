# Layout Style Reference

Use this reference when converting educational images/PDFs into polished editable Word, Markdown, or HTML.

## General principles

- Prefer clarity over decoration. The document should look intentionally designed, not merely OCR dumped.
- Use a stable grid: consistent margins, predictable indentation, and aligned question blocks.
- Keep typography calm: one body font, one heading style, restrained bold, and limited accent color.
- Use whitespace to separate sections instead of excessive borders.
- Preserve semantic structure so the output remains editable.

## Exam paper style

Best for worksheets, mock exams, test papers, answer sheets, and problem sets.

- Page: A4-friendly, print-safe margins, clear title/header area.
- Header: subject, grade, unit, time, total score, name/class fields if present or useful.
- Sections: use numbered headings such as “一、选择题”, “二、填空题”, “三、解答题”.
- Questions: keep original numbering; indent subparts consistently.
- Options: align A/B/C/D options in one or two columns when space allows.
- Answer spaces: use editable underlines, blank lines, or bordered answer boxes rather than images.
- Tables: use real tables with consistent borders and cell padding.
- Page breaks: insert between major sections only when it improves printability.
- Answer keys: place in a separate section or separate file; visually distinguish from questions.

## Study note style

Best for image notes, class notes, mind-map-like screenshots, and compact knowledge summaries.

- Title block: concise title plus optional metadata such as subject/chapter/source date.
- Hierarchy: H1 for document title, H2 for major topics, H3 for concepts or examples.
- Cards: use light callout blocks for definitions, formulas, reminders, and common mistakes.
- Emphasis: use bold for keywords; avoid excessive color.
- Formulas: display important formulas separately and keep them editable.
- Examples: separate “例题”, “解析”, and “结论” so learners can scan quickly.
- Review checklist: when useful, end with a short “易错点 / 复习要点”.

## Markdown conventions

- Use Markdown tables only for simple rectangular tables; use HTML tables if merged cells are necessary.
- Use LaTeX math syntax for formulas.
- Use blockquotes for notes and cautions:
  - `> 重点：...`
  - `> 易错：...`
- Keep image placeholders explicit: `![图 1：待重绘的几何图](...)`.

## HTML conventions

- Produce self-contained HTML unless the user requests otherwise.
- Include print CSS for A4 output.
- Use CSS variables for colors and spacing.
- Use restrained styles: off-white background, white content cards, subtle shadows for screen, no shadow for print.
- Avoid external CDNs unless the user explicitly allows external dependencies.

## Word conventions

- Use built-in heading levels where possible.
- Prefer real paragraphs, lists, tables, and equations over positioned text boxes.
- Avoid using one giant image per page.
- Use page breaks sparingly and intentionally.
- Keep source images only for diagrams or illegible regions that need manual redraw.

## OCR uncertainty markers

Use these markers consistently:

- `[待核对: 原文可能为“...”]` for uncertain text.
- `[图示待重绘: 简短说明]` for diagrams not redrawn.
- `[缺失: 页面边缘被裁切]` for visibly missing source content.
- `[公式待核对: ...]` for uncertain formulas.

## Final self-check

Before reporting completion, verify:

1. Page order is correct.
2. Every visible question/note block is represented.
3. Numbering and option labels are continuous.
4. Tables and formulas are editable when possible.
5. Uncertain content is marked, not guessed.
6. Output format matches the user request, with Word as default.
