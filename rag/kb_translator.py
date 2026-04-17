import os
import logging
from pathlib import Path
from typing import Optional

from llm_client import generate_response, MOCK_MODE
from rag.kb_sync import chunk_markdown

logger = logging.getLogger(__name__)

KB_PATH = Path(__file__).parent.parent / "knowledge-base"
TRANSLATIONS_PATH = KB_PATH / "translations"

SUPPORTED_TRANSLATION_LANGS = ["es", "fr", "de", "ru", "tr"]
LANG_NAMES = {
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "ru": "Russian",
    "tr": "Turkish",
}

PRIORITY_KB_FILES = [
    "faq-payments.md",
    "faq-account-access.md",
    "escalation-rules.md",
    "refund-policy-detail.md",
    "faq-technical-issues.md",
]


def translate_section(text: str, target_language: str) -> str:
    if MOCK_MODE:
        return f"<!-- MOCK TRANSLATION: {target_language} -->\n{text}"

    prompt = (
        f"Translate the following markdown text to {target_language}. "
        "Preserve all markdown formatting, headings, table structure, bold text, "
        "bullet points, and code blocks exactly. Translate only the natural language content. "
        "Return ONLY the translated markdown, no explanation.\n\n"
        f"{text}"
    )
    result, _ = generate_response(prompt, intent="unknown")
    return result


def translate_kb_file(
    source_file: str,
    target_lang: str,
    force: bool = False,
) -> dict:
    lang_name = LANG_NAMES.get(target_lang, target_lang)
    source_path = KB_PATH / source_file
    output_path = TRANSLATIONS_PATH / target_lang / source_file

    if output_path.exists() and not force:
        return {"source": source_file, "lang": target_lang, "path": str(output_path),
                "sections": 0, "skipped": True}

    if not source_path.exists():
        logger.warning("kb_source_file_not_found", extra={"file": source_file})
        return {"source": source_file, "lang": target_lang, "path": "", "sections": 0, "skipped": True}

    with open(source_path, "r", encoding="utf-8") as f:
        content = f.read()

    chunks = chunk_markdown(content, source_file)
    translated_parts = []

    for chunk in chunks:
        translated = translate_section(chunk["text"], lang_name)
        translated_parts.append(translated)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n\n".join(translated_parts))

    logger.info("kb_file_translated",
                extra={"file": source_file, "lang": target_lang, "sections": len(chunks)})

    return {
        "source": source_file,
        "lang": target_lang,
        "path": str(output_path),
        "sections": len(chunks),
        "skipped": False,
    }


def translate_priority_kb(
    langs: Optional[list] = None,
    force: bool = False,
) -> dict:
    if langs is None:
        langs = SUPPORTED_TRANSLATION_LANGS

    translated = 0
    skipped = 0
    errors = []

    for lang in langs:
        for kb_file in PRIORITY_KB_FILES:
            try:
                result = translate_kb_file(kb_file, lang, force=force)
                if result["skipped"]:
                    skipped += 1
                else:
                    translated += 1
                    logger.info(f"Translated {kb_file} -> {lang}")
            except Exception as e:
                errors.append(f"{kb_file}/{lang}: {str(e)}")
                logger.error("kb_translation_error",
                             extra={"file": kb_file, "lang": lang, "error": str(e)})

    return {"translated": translated, "skipped": skipped, "errors": errors}


if __name__ == "__main__":
    print("Translating priority KB files (mock mode — set ANTHROPIC_API_KEY for real translations)...")
    result = translate_priority_kb()
    print(f"Done: {result['translated']} translated, {result['skipped']} skipped")
    if result["errors"]:
        print(f"Errors: {result['errors']}")
