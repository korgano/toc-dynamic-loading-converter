# toc-dynamic-loading-converter
Converts old Markdown LLM Prompts/Agents.md to [Warner Bell's TOC-Based Dynamic Loading](https://gist.github.com/Warner-Bell/e3a34a82214d370cdc9fa816d349c16b)

## What This Does
This GUI provides you a method to easily create a table of contents at the top of your prompt/AI targeted Markdown file, enabling more efficient token utilization and AI performance.

```
TOC-Based Dynamic Loading transforms the Table of Contents into a routing mechanism. The model loads only relevant sections based on user request keywords instead of the entire document.

Measured results: 44-63% token reduction, 30-40% faster processing, 82% targeted loading success, 18% fallback rate.

Note: Fallback rate depends on keyword mapping granularity. Tighter mappings yield lower fallback rates.
```

## How to Use
- Download code (`main.py` and `gui.py`).
- Make sure both files are in the same folder.
- Run `gui.py` via terminal/PowerShell/PyCharm/etc...
