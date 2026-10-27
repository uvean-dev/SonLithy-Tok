"""Entry point reserved for future tokenizer evaluation; no evaluator exists yet."""

import argparse


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    parser.error("Tokenizer evaluation is not implemented yet.")


if __name__ == "__main__":
    main()
