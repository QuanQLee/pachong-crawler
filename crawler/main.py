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
    parser.add_argument(
        "--output-dir", "-o", type=Path, default=Path("data"),
        help="Directory to store fetched pages")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    config = {}
    if args.config:
        config = load_config(args.config)
    seeds = args.seeds or config.get("seeds", [])
    rate = args.rate if args.rate is not None else config.get("rate")
    output_dir = args.output_dir
    if "output_dir" in config and args.output_dir == Path("data"):
        output_dir = Path(config["output_dir"])

    delay = 1.0
    if rate:
        if rate <= 0:
            raise ValueError("rate must be positive")
        delay = 1.0 / rate

    from crawler import Fetcher, ObjectStore
    from hashlib import md5
    import sys

    fetcher = Fetcher(delay=delay)
    store = ObjectStore(output_dir)

    print("Starting crawler with parameters:")
    print("  Seeds:", seeds)
    print("  Rate limit:", rate, "requests/sec")
    print("  Output directory:", output_dir)

    for url in seeds:
        try:
            html = fetcher.fetch(url)
            name = md5(url.encode("utf-8")).hexdigest() + ".html"
            path = store.put(name, html.encode("utf-8"))
            print(f"Saved {url} -> {path}")
        except Exception as exc:
            print(f"Failed to fetch {url}: {exc}", file=sys.stderr)


if __name__ == "__main__":
    main()
