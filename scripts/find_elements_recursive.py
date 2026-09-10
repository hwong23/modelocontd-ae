#!/usr/bin/env python3
"""Find ArchiMate elements recursively within a model layer.

Example:
    python3 scripts/find_elements_recursive.py --layer application --prefix ApplicationComponent_
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


def find_elements(model_root: Path, layer: str, prefix: str):
    layer_dir = model_root / layer
    if not layer_dir.exists():
        raise FileNotFoundError(f"Layer directory not found: {layer_dir}")

    results = []
    for xml_path in sorted(layer_dir.rglob("*.xml")):
        if not xml_path.name.startswith(prefix):
            continue

        text = xml_path.read_text(encoding="utf-8", errors="ignore")
        name_match = re.search(r'name="([^"]+)"', text)
        id_match = re.search(r'identifier="([^"]+)"', text) or re.search(r'id="([^"]+)"', text)

        results.append({
            "name": name_match.group(1) if name_match else xml_path.stem,
            "id": id_match.group(1) if id_match else "",
            "file": xml_path.relative_to(model_root.parent),
        })

    return results


def main():
    parser = argparse.ArgumentParser(description="Recursively list ArchiMate elements inside a model layer.")
    parser.add_argument("--layer", default="application", help="Layer folder under model/, e.g. application, business")
    parser.add_argument("--prefix", default="ApplicationComponent_", help="Filename prefix to filter, e.g. ApplicationComponent_")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    model_root = repo_root / "model"
    elements = find_elements(model_root, args.layer, args.prefix)

    print(f"COUNT {len(elements)}")
    for item in elements:
        print(f"{item['name']} | {item['file']}")


if __name__ == "__main__":
    main()
