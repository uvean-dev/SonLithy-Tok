"""Entry point reserved for future tokenizer training; no trainer exists yet."""

import argparse


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    parser.error("Tokenizer training is not implemented yet.")


if __name__ == "__main__":
    main()
