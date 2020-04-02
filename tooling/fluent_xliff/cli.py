import argparse
from pathlib import Path

from compare_locales.paths import TOMLParser, ProjectFiles

from .simple import simple_patterns_xliff


def get_config(toml_path):
    c = TOMLParser().parse(toml_path)
    return c


def main():
    p = argparse.ArgumentParser()
    p.add_argument("toml")
    p.add_argument("dest", type=Path)
    p.add_argument("--kind", choices=["simple"], default="simple")
    args = p.parse_args()
    config = get_config(args.toml)
    if args.kind == "simple":
        return simple_patterns_xliff(config, args.dest)
