#!/usr/bin/env python3
"""Prepare editable document conversion workspace for paper-scribe."""

from __future__ import annotations

import argparse
import html
import json
import shutil
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".heic", ".tif", ".tiff"}
PDF_EXTS = {".pdf"}


@dataclass
class DependencyStatus:
    name: str
    available: bool
    purpose: str
    install_hint: str | None = None


@dataclass
class SourceFile:
    path: str
    kind: str
    size_bytes: int


def module_available(name: str) -> bool:
    import importlib.util

    return importlib.util.find_spec(name) is not None


def dependency_report() -> list[DependencyStatus]:
    return [
        DependencyStatus("pdftoppm", shutil.which("pdftoppm") is not None, "render scanned PDFs to page images", "brew install poppler"),
        DependencyStatus("pdftotext", shutil.which("pdftotext") is not None, "extract selectable PDF text", "brew install poppler"),
        DependencyStatus("tesseract", shutil.which("tesseract") is not None, "local OCR engine", "brew install tesseract tesseract-lang"),
        DependencyStatus("pypdf", module_available("pypdf"), "lightweight PDF text probing", "python -m pip install pypdf"),
        DependencyStatus("python-docx", module_available("docx"), "generate editable .docx files", "python -m pip install python-docx"),
        DependencyStatus("Pillow", module_available("PIL"), "inspect and pre-process images", "python -m pip install pillow"),
    ]


def iter_sources(inputs: Iterable[Path]) -> list[SourceFile]:
    files: list[Path] = []
    for item in inputs:
        if item.is_dir():
            files.extend(p for p in item.rglob("*") if p.is_file())
        elif item.is_file():
            files.append(item)

    sources: list[SourceFile] = []
    for path in sorted(files):
        suffix = path.suffix.lower()
        if suffix in IMAGE_EXTS:
            kind = "image"
        elif suffix in PDF_EXTS:
            kind = "pdf"
        else:
            continue
        sources.append(SourceFile(str(path), kind, path.stat().st_size))
    return sources


def probe_pdf_text(path: Path, max_pages: int = 2) -> dict[str, object]:
    if not module_available("pypdf"):
        return {"available": False, "reason": "pypdf is not installed"}

    from pypdf import PdfReader

    reader = PdfReader(str(path))
    page_count = len(reader.pages)
    samples: list[dict[str, object]] = []
    for index, page in enumerate(reader.pages[:max_pages]):
        text = page.extract_text() or ""
        samples.append({"page": index + 1, "chars": len(text.strip()), "preview": text.strip()[:300]})
    likely_scanned = all(sample["chars"] == 0 for sample in samples)
    return {"available": True, "pages": page_count, "samples": samples, "likely_scanned": likely_scanned}


def write_markdown(output_dir: Path, sources: list[SourceFile], deps: list[DependencyStatus], pdf_probes: dict[str, object]) -> None:
    lines = [
        "# paper-scribe 转换工作区",
        "",
        "## 输入盘点",
        "",
    ]
    if not sources:
        lines.append("未发现支持的图片或 PDF 输入。")
    else:
        for source in sources:
            lines.append(f"- `{source.path}` — {source.kind}, {source.size_bytes} bytes")

    lines.extend(["", "## 依赖检测", ""])
    for dep in deps:
        status = "可用" if dep.available else "缺失"
        hint = f"；建议：`{dep.install_hint}`" if (not dep.available and dep.install_hint) else ""
        lines.append(f"- **{dep.name}**：{status} — {dep.purpose}{hint}")

    lines.extend(["", "## PDF 探测", ""])
    if not pdf_probes:
        lines.append("未提供 PDF。")
    else:
        for path, probe in pdf_probes.items():
            lines.append(f"### `{path}`")
            lines.append("")
            lines.append(f"```json\n{json.dumps(probe, ensure_ascii=False, indent=2)}\n```")

    lines.extend([
        "",
        "## Word-first 重建建议",
        "",
        "1. 若 PDF 为扫描型，先安装 poppler 与 OCR，再渲染逐页图片并识别。",
        "2. 若图片/扫描页中有公式、表格、几何图，优先保留结构并标记不确定处。",
        "3. 若缺少 `python-docx`，先输出 Markdown/HTML 审稿稿；安装后再生成 `.docx`。",
        "4. 不要编造 OCR 未识别内容，使用 `[待核对: ...]`、`[图示待重绘: ...]`。",
    ])
    (output_dir / "conversion-plan.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_html(output_dir: Path) -> None:
    plan = (output_dir / "conversion-plan.md").read_text(encoding="utf-8")
    escaped = html.escape(plan)
    content = f"""<!doctype html>
<html lang=\"zh-CN\">
<head>
  <meta charset=\"utf-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
  <title>paper-scribe 转换工作区</title>
  <style>
    body {{ margin: 0; background: #f7f5ef; color: #1f2933; font-family: -apple-system, BlinkMacSystemFont, \"Segoe UI\", \"Noto Sans CJK SC\", sans-serif; }}
    main {{ max-width: 920px; margin: 40px auto; padding: 32px; background: #fffdf8; border: 1px solid #e6dfd2; border-radius: 18px; box-shadow: 0 18px 50px rgba(31,41,51,.08); }}
    pre {{ white-space: pre-wrap; line-height: 1.7; font-family: \"SFMono-Regular\", Consolas, monospace; }}
    @media print {{ body {{ background: white; }} main {{ margin: 0; max-width: none; box-shadow: none; border: 0; }} }}
  </style>
</head>
<body><main><pre>{escaped}</pre></main></body>
</html>
"""
    (output_dir / "conversion-plan.html").write_text(content, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare paper-scribe conversion workspace.")
    parser.add_argument("inputs", nargs="+", help="Input files or directories")
    parser.add_argument("--output-dir", required=True, help="Directory for generated workspace files")
    args = parser.parse_args()

    inputs = [Path(value).expanduser().resolve() for value in args.inputs]
    missing = [path for path in inputs if not path.exists()]
    if missing:
        for path in missing:
            print(f"missing input: {path}", file=sys.stderr)
        return 2

    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    deps = dependency_report()
    sources = iter_sources(inputs)
    pdf_probes = {
        source.path: probe_pdf_text(Path(source.path))
        for source in sources
        if source.kind == "pdf"
    }

    report = {
        "inputs": [str(path) for path in inputs],
        "sources": [asdict(source) for source in sources],
        "dependencies": [asdict(dep) for dep in deps],
        "pdf_probes": pdf_probes,
    }
    (output_dir / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_markdown(output_dir, sources, deps, pdf_probes)
    write_html(output_dir)

    print(f"wrote {output_dir / 'report.json'}")
    print(f"wrote {output_dir / 'conversion-plan.md'}")
    print(f"wrote {output_dir / 'conversion-plan.html'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
