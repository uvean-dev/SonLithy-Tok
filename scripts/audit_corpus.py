"""Entry point reserved for future corpus audits; no audit implementation exists yet."""

import argparse


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    parser.error("Corpus auditing is not implemented yet.")


if __name__ == "__main__":
    main()
