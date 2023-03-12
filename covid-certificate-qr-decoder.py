#!./venv/bin/python3
from cose.messages import CoseMessage, Sign1Message
import argparse
import base45
import cbor2
import json
import sys
import zlib

usage_notice = """
- The `covid-certificate-qr-decoder.py` script can decode a COVID vaccination certificate base45 string (recognizable by the "HC1:" prefix), decompress the data, decode it again as a COSE message based on the CBOR tag, deserialize the resulting bytestring, print it out, and exit.

- This script works in pair with its best buddy script "webcam_capture_QR_code.py":

    python3 ./webcam_capture_QR_code.py | python3 ./covid-certificate-qr-decoder.py
"""


def extract_str_from_stdin(argparser):
    # If stdin is coming from a pipe
    if not sys.stdin.isatty():
        input_bytes = sys.stdin.buffer.read()
        input_str = input_bytes.decode('ASCII')
    # If stdin is coming from a terminal
    else:
        argparser.print_help()
        sys.exit()
    return input_str


def decode_and_extract_details(input_str):
    expected_prefix = 'HC1:'
    for line in input_str.splitlines():
        if line.startswith(expected_prefix):
            line = line[4:]
            decoded_bytes = base45.b45decode(line)
            decompressed = zlib.decompress(decoded_bytes)
            msg = CoseMessage.decode(decompressed)
            phdr, uhdr = msg._hdr_repr()
            # Deserialize a bytestring. Payload is the most interesting part, the others are rather boring
            payload = cbor2.loads(msg.payload)
            return (phdr, uhdr, msg.signature, msg.key, payload)
        else:
            # Print only this message and no traceback
            raise SystemExit(f"Invalid COVID Certificate base45 string: {expected_prefix!r} prefix is expected.")


def print_decoded_details(args, input_str):
    # A try block to fix "TypeError: cannot unpack non-iterable NoneType object"
    try:
        phdr, uhdr, signature, key, payload = decode_and_extract_details(input_str)
    except TypeError:
        sys.exit()
    if args.quiet or args.silent:
        # Print only the decoded payload as a JSON one-liner
        print(json.dumps(payload, ensure_ascii=False))
    else:
        # Print all details
        print("\n==Raw COVID Certificate base45 string==\n")
        print(input_str)
        print("\n==PHDR==\n")
        print(phdr)
        print("\n==UHDR==\n")
        print(uhdr)
        print("\n==SIGNATURE==\n")
        print(signature, "\n")
        print("==KEY==\n")
        print(key, "\n")
        print("==PAYLOAD==\n")
        print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(usage=usage_notice)
    argparser.add_argument(
        "-s", "--silent",
        action="store_true",
        help="print nothing but the decoded payload as a JSON one-liner"
    )
    argparser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="print nothing but the decoded payload as a JSON one-liner"
    )
    input_str = extract_str_from_stdin(argparser)
    args = argparser.parse_args()
    print_decoded_details(args, input_str)
