#!/usr/bin/env python3
"""
Simple manifest generator for demo.
Reads a YAML config and outputs a flattened manifest JSON suitable for reuse.
"""
import argparse
import json
import sys
from pathlib import Path
import yaml

def load_yaml(path: Path):
    if not path.exists():
        print(f"Config not found: {path}", file=sys.stderr)
        sys.exit(2)
    with path.open() as f:
        return yaml.safe_load(f) or {}

def flatten(d, parent_key="", sep="."):
    items = {}
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.update(flatten(v, new_key, sep=sep))
        else:
            items[new_key] = v
    return items

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--config", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args()

    cfg = load_yaml(args.config)
    manifest = {
        "source_config": str(args.config),
        "generated_from": cfg,
        "flat": flatten(cfg)
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w") as f:
        json.dump(manifest, f, indent=2)
    print(str(args.out))

if __name__ == "__main__":
    main()
