---
name: paper-scribe
description: Use this skill whenever the user wants to convert exam papers, worksheet photos, handwritten or printed study notes, Xiaohongshu/online shared images, PDFs, scanned pages, screenshots, or local images into editable Word, Markdown, or HTML. This skill is especially important when the user asks for clean typography, rigorous layout, printable worksheets, reconstructed tables/formulas, beautiful note pages, or preserving/rebuilding visual structure. Default to Word-first output unless the user asks otherwise, and use this skill even if the user only says “把这张图转成可编辑文档”, “整理成 Word”, “PDF 转 Markdown”, “试卷重排版”, or “图片笔记转 HTML”.
---

# Paper / Notes to Editable Documents

Use this skill to turn educational images, screenshots, scanned pages, PDFs, and online resources into editable documents with careful OCR, reconstruction, and typesetting.

Default output priority: **Word (.docx) first**, then Markdown or HTML when requested or useful as an intermediate review format.

## First response

Start by confirming three things if they are not already clear:

1. **Authorization**: Ask the user to confirm they have the right to transform the material, or that this is for personal study/fair use. Do not help bypass paywalls, platform download restrictions, DRM, watermarks, access controls, or mass-copy protected resources.
2. **Target format**: Default to Word. Ask only if the user likely needs Markdown/HTML instead.
3. **Source access**: Ask for the file path, uploaded file, image, PDF, or public URL. For authenticated/private URLs, ask the user to export or provide the file rather than trying to bypass access.

If the user already provided files and a target format, proceed without extra ceremony.

## Core workflow

When local files or directories are available, first run the bundled workspace script to inventory inputs and detect dependencies:

```bash
python scripts/convert_workspace.py <input-file-or-directory> --output-dir <output-dir>
```

Use its `report.json`, `conversion-plan.md`, and `conversion-plan.html` as the starting point. The script intentionally does not invent OCR text; it reports missing dependencies such as `pdftoppm`, `tesseract`, and `python-docx` so the user gets a clear next step.

1. **Inventory the source**
   - Identify file type: image, multi-image set, PDF, screenshot, webpage, or mixed sources.
   - Determine whether pages are exams, answer keys, lecture notes, handwritten notes, tables, diagrams, or mixed layouts.
   - For PDFs, distinguish text PDFs from scanned PDFs. Text PDFs should preserve selectable text when reliable; scanned PDFs need OCR.

2. **Extract content faithfully**
   - Preserve question numbers, sub-question hierarchy, options, blanks, score markers, answer areas, tables, captions, and page order.
   - Reconstruct math with editable notation where possible: Word equation style when generating Word, LaTeX-style math in Markdown/HTML.
   - Mark uncertain OCR text visibly as `[待核对: ...]` rather than silently inventing content.
   - Do not fabricate missing problems, answers, diagrams, or source text.

3. **Decide whether to preserve or re-layout**
   - Preserve the original structure when the source is already clear and printable.
   - Re-layout only when it improves readability, alignment, spacing, or visual hierarchy.
   - For exams, prioritize rigor: stable numbering, consistent indentation, answer blanks, table borders, page breaks, and print-friendly spacing.
   - For notes, prioritize reading flow: clear headings, cards/blocks, callouts, formula blocks, and visual rhythm.

4. **Build the editable output**
   - Word-first: create a `.docx` if tooling is available. Use clean paragraph styles, heading levels, tables, page breaks, and editable text instead of screenshots.
   - Markdown: use semantic headings, lists, tables, blockquotes/callouts, and LaTeX math where appropriate.
   - HTML: use a self-contained, tidy layout with readable typography and print styles when the user wants visual polish or online display.
   - Keep any unavoidable embedded images cropped and labeled, especially diagrams that cannot be reliably redrawn.

5. **Quality pass before final answer**
   - Check page/order completeness.
   - Check numbering continuity and indentation.
   - Check tables, formulas, units, punctuation, and option labels.
   - Check whether uncertain text is explicitly marked.
   - Check the output opens or renders when possible.
   - State what was generated and what still needs manual verification.

## Layout guidance

Read [layout-style.md](references/layout-style.md) when the task involves visual redesign, polished notes, printable exams, or HTML/Markdown styling.

Use the visual spirit of clean design systems: generous whitespace, strong hierarchy, simple borders, restrained color, card-like note blocks, and print-safe contrast. Do not copy proprietary assets, exact branding, or repository-specific files unless the user provides permission and files.

## Handling common sources

### Xiaohongshu or online shared images

- Ask for screenshots, exported images, or a public URL the user is allowed to use.
- Do not automate login, scraping, anti-bot bypass, bulk downloading, watermark removal, or access-control circumvention.
- If the image has platform overlays, crop only user-provided images when needed for readability; do not remove attribution or ownership marks unless the user owns the material.

### PDF exam papers or notes

- If selectable text is present, extract text and compare with page rendering when possible.
- If scanned, OCR each page and preserve page sequence.
- For exams, reproduce headers, sections, score boxes, tables, and answer spaces in editable form.
- For answer keys, keep answers visually distinct from questions.

### Local images

- Inspect image quality first: rotation, blur, perspective distortion, contrast, shadows, missing edges.
- If quality is too poor, ask for a clearer image rather than guessing.
- For multi-image notes, sort by filename or visible page number; ask if order is ambiguous.

## Output conventions

When returning results, include:

- The generated file path(s).
- A short conversion note: source count, output format, major layout choices.
- A verification note listing uncertain OCR regions or diagrams left as images.

Do not claim the conversion is perfect if OCR uncertainty remains.

## Refusal and caution boundaries

Refuse or redirect when the user asks to:

- Bypass paywalls, DRM, login gates, platform anti-scraping, or download restrictions.
- Remove watermarks or attribution from third-party content they do not own.
- Bulk-copy a commercial workbook, textbook, paid course, or protected question bank.
- Generate a misleading “original” document that hides its source or ownership.

Offer safe alternatives: process user-owned files, summarize allowed excerpts, create a clean template from scratch, or transform a small excerpt for personal study when appropriate.
