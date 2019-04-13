#!/usr/bin/env python
"""
Turn a gif into a party gif!
"""
from partyfy.partyfy import partyfy
from argparse import ArgumentParser, ArgumentTypeError


def main():
    """
    Launch an Athena DB Stack.
    """
    parser = ArgumentParser(description="Partyfy")
    parser.add_argument("gif", default=None, help="The gif we are partyfying")
    parser.add_argument(
        "--hue-tick",
        "-ht",
        default=36,
        type=float,
        help=(
            "How much to change the hue between frames (default: %(default)s)",
        )
    )

    args = parser.parse_args()
    partyfy(args.gif, args.hue_tick)


if __name__ == "__main__":
    main()
