"""Entry point reserved for future throughput benchmarks; no benchmark exists yet."""

import argparse


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    parser.error("Tokenizer benchmarking is not implemented yet.")


if __name__ == "__main__":
    main()
