#!/usr/bin/env python3
"""Validate the Dr. Dunn AI training corpus."""

import json
import sys
from pathlib import Path

CORPUS = Path(__file__).parent


def validate_jsonl(path: Path, required_keys: list[str] | None = None) -> int:
    count = 0
    with path.open() as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError as e:
                print(f"FAIL {path.name}:{i} — invalid JSON: {e}")
                sys.exit(1)
            if required_keys:
                for key in required_keys:
                    if key not in obj:
                        print(f"FAIL {path.name}:{i} — missing key '{key}'")
                        sys.exit(1)
            count += 1
    print(f"OK  {path.name} — {count} records")
    return count


def main() -> None:
    ft_count = validate_jsonl(CORPUS / "fine-tuning-dataset.jsonl")
    rag_count = validate_jsonl(CORPUS / "rag-chunks.jsonl", ["id", "text"])

    for name in ["knowledge-base.md", "system-prompt.md", "brand-voice-guidelines.md", "evaluation-rubric.md"]:
        p = CORPUS / name
        if not p.exists():
            print(f"FAIL missing {name}")
            sys.exit(1)
        print(f"OK  {name} — {p.stat().st_size} bytes")

    print(f"\nCorpus valid: {ft_count} fine-tuning pairs, {rag_count} RAG chunks")


if __name__ == "__main__":
    main()
