import argparse
import json
import yaml
from pathlib import Path


def load_config(path: Path) -> dict:
    """Load configuration from a YAML or JSON file."""
    if not path.exists():
        raise FileNotFoundError(f"Config file {path} does not exist")
    with path.open("r", encoding="utf-8") as f:
        if path.suffix.lower() in {".yaml", ".yml"}:
            return yaml.safe_load(f) or {}
        elif path.suffix.lower() == ".json":
            return json.load(f)
        else:
            raise ValueError("Unsupported config file format: %s" % path.suffix)


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Start crawl jobs")
    parser.add_argument(
        "--config", "-c", type=Path, help="Path to YAML or JSON configuration file")
    parser.add_argument(
        "--seed", "-s", action="append", dest="seeds",
        help="Seed URL to start crawling from. Can be specified multiple times.")
    parser.add_argument(
        "--rate", "-r", type=float, default=None,
        help="Maximum requests per second (rate limit)")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    config = {}
    if args.config:
        config = load_config(args.config)
    seeds = args.seeds or config.get("seeds", [])
    rate = args.rate if args.rate is not None else config.get("rate")

    # Placeholder for starting crawl jobs
    print("Starting crawler with parameters:")
    print("  Seeds:", seeds)
    print("  Rate limit:", rate, "requests/sec")


if __name__ == "__main__":
    main()
