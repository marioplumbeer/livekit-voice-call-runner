import argparse
from enum import Enum

from livekit_voice_call_runner.cli import inbound, outbound


class Direction(str, Enum):
    OUTBOUND = "outbound"
    INBOUND = "inbound"


def run() -> None:
    parser = argparse.ArgumentParser(prog="livekit_voice_call_runner")
    parser.add_argument(
        "--direction",
        choices=list(Direction),
        type=Direction,
        required=True,
        help=(
            f"Direction of the call: '{Direction.OUTBOUND.value}' to dial out, "
            f"'{Direction.INBOUND.value}' to listen for incoming calls."
        ),
    )
    parser.add_argument(
        "--instructions-path",
        required=True,
        help="Path to the file containing the instructions for the call agent.",
    )
    parser.add_argument(
        "--phone-number",
        help="Phone number to call (outbound only).",
    )
    args = parser.parse_args()

    if args.direction == Direction.OUTBOUND and not args.phone_number:
        parser.error("--phone-number is required for outbound direction")

    if args.direction == Direction.OUTBOUND:
        outbound.run(args)
    else:
        inbound.run(args)
