# main.py
import os
import re
import logging

_logger = None

HEADER_PATTERN = re.compile(r"^(#{1,6})\s+(.*)")


# ----------------------------
# Logger Setup
# ----------------------------

def setup_logger(source_file: str) -> logging.Logger:
    global _logger

    base_name = os.path.basename(source_file)
    log_filename = f"errors-{base_name}.txt"

    logger = logging.getLogger("toc_app")

    if logger.handlers:
        logger.handlers.clear()

    logger.setLevel(logging.DEBUG)

    handler = logging.FileHandler(log_filename, encoding="utf-8")
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(module)s - %(message)s"
    )
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    _logger = logger

    logger.info(f"Logger initialized for {source_file}")
    return logger


def log_info(msg: str):
    if _logger:
        _logger.info(msg)


def log_error(msg: str):
    if _logger:
        _logger.error(msg)


# ----------------------------
# Markdown IO
# ----------------------------

def load_markdown(file_path: str) -> str:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        log_info(f"Loaded file: {file_path}")
        return content

    except Exception as e:
        log_error(f"Load failed: {e}")
        raise


# ----------------------------
# Header Extraction (MVP)
# ----------------------------

def extract_headers(content: str) -> list[dict]:
    headers = []

    try:
        lines = content.splitlines()

        for i, line in enumerate(lines, start=1):
            match = HEADER_PATTERN.match(line)
            if match:
                headers.append({
                    "level": len(match.group(1)),
                    "text": match.group(2).strip(),
                    "line": i
                })

        log_info(f"Extracted {len(headers)} headers")
        return headers

    except Exception as e:
        log_error(f"Header extraction failed: {e}")
        raise


# ----------------------------
# NEW: Anchor Injection
# ----------------------------

def inject_section_anchors(content: str) -> str:
    """
    Inserts HTML comment anchors above markdown headers.

    Example:
    <!-- #Title -->
    ## Title
    """

    try:
        lines = content.splitlines()
        output = []

        for line in lines:
            match = HEADER_PATTERN.match(line)

            if match:
                title = match.group(2).strip()

                anchor = f"<!-- #{title} -->"
                output.append(anchor)

            output.append(line)

        result = "\n".join(output)

        log_info("Section anchors injected")
        return result

    except Exception as e:
        log_error(f"Anchor injection failed: {e}")
        raise


# ----------------------------
# TOC Generation
# ----------------------------

def generate_toc(sections: list[dict]) -> str:
    try:
        lines = ["# Table of Contents", "", "**Load only the section(s) matching task keywords. Fallback to full load if ambiguous.**", ""]
        lines.append("| Section | Description | Keywords |")
        lines.append("|---------|-------------|----------|")

        for s in sections:
            lines.append(
                f"| {s.get('header','')} | {s.get('description','')} | {s.get('keywords','')} |"
            )

        toc = "\n".join(lines)

        log_info("TOC generated")
        return toc

    except Exception as e:
        log_error(f"TOC generation failed: {e}")
        raise


def prepend_toc(original: str, toc: str) -> str:
    return f"{toc}\n\n{original}"


# ----------------------------
# Export
# ----------------------------

def export_file(output_path: str, content: str):
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)

        log_info(f"Exported: {output_path}")

    except Exception as e:
        log_error(f"Export failed: {e}")
        raise


# ----------------------------
# Full Pipeline
# ----------------------------

def process_markdown(file_path: str, enriched_sections: list[dict], output_path: str):
    setup_logger(file_path)

    content = load_markdown(file_path)

    # NEW: inject anchors BEFORE TOC prepending
    content_with_anchors = inject_section_anchors(content)

    toc = generate_toc(enriched_sections)

    final_content = prepend_toc(content_with_anchors, toc)

    export_file(output_path, final_content)

    log_info("Processing complete")

    return final_content