import sys
sys.path.append("..")
import argparse
from winthingies.win32.wevtapi import *
from winthingies.win32.wevtapi_helpers import get_keyword_mapping


def get_arguments():
    usage = """Print publisher information."""

    arguments = argparse.ArgumentParser(
        description=usage
    )

    arguments.add_argument(
        "-p", "--publisher",
        dest="publisher",
        action="store",
        required=False,
        default=None,
        help="A specific publisher."
    )

    return arguments


def print_publisher_info(publisher_name):
    print("----------------------------------------------")
    print("Publisher: {}".format(publisher_name))
    print("----------------------------------------------")
    metadata_handle = EvtOpenPublisherMetadata(
        publisher_name
    )

    mapping = get_keyword_mapping(
        metadata_handle
    )
    for keyword_value, keyword_info in mapping.items():
        desc = ""
        if keyword_info["desc"]:
            desc = " [{}]".format(keyword_info["desc"])

        print("0x{:016X}: {}{}".format(
            keyword_value,
            keyword_info["name"],
            desc
        ))

    wevtapi.EvtClose(
        metadata_handle
    )


def main():
    arguments = get_arguments()
    options = arguments.parse_args()

    if options.publisher:
        print_publisher_info(
            options.publisher
        )
    else:
        raise(Exception("All providers not yet implemented."))


if __name__ == "__main__":
    main()
