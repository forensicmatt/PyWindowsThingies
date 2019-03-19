import sys
sys.path.append("..")
import logging
import argparse
from winthingies.win32.wevtapi import *
from winthingies.win32.wevtapi_helpers import PublisherMetadata

VERSION = "0.0.1"


def get_arguments():
    usage = ("Print metadata of all registered Windows Event publishers"
             " or a specific publisher. Version: {}").format(
        VERSION
    )

    arguments = argparse.ArgumentParser(
        description=usage,
        formatter_class=argparse.RawTextHelpFormatter
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
    try:
        metadata_handle = PublisherMetadata(
            publisher_name
        )
    except WindowsError as error:
        logging.error("Error opening provider metadata {}; {}".format(
            publisher_name, error
        ))
        return

    print("----------------------------------------------")
    print("Publisher: {}".format(publisher_name))
    print("GUID: {}".format(metadata_handle.guid))
    print("----------------------------------------------")

    print("--- Keywords ---")
    keyword_mapping = metadata_handle.keyword_mapping
    if keyword_mapping:
        for keyword_value, keyword_info in keyword_mapping.items():
            desc = ""
            if keyword_info["message"]:
                desc = " [{}]".format(keyword_info["message"])

            print("0x{:016X}: {}{}".format(
                keyword_value,
                keyword_info["name"],
                desc
            ))

    print("--- Operations ---")
    opcode_mapping = metadata_handle.opcode_mapping
    if opcode_mapping:
        for opcode_value, opcode_info in opcode_mapping.items():
            desc = ""
            if opcode_info["message"]:
                desc = " [{}]".format(opcode_info["message"])

            print("0x{:016X}: {}{}".format(
                opcode_value,
                opcode_info["name"],
                desc
            ))

    print("--- Tasks ---")
    task_mapping = metadata_handle.task_mapping
    if task_mapping:
        for task_value, task_info in task_mapping.items():
            desc = ""
            if task_info["message"]:
                desc = " [{}]".format(task_info["message"])

            print("0x{:016X}: {}{}".format(
                task_value,
                task_info["name"],
                desc
            ))


def main():
    arguments = get_arguments()
    options = arguments.parse_args()

    if options.publisher:
        print_publisher_info(
            options.publisher
        )
    else:
        publisher_list_handle = EvtOpenPublisherEnum()

        publisher_list = []
        while True:
            publisher_name = EvtNextPublisherId(
                publisher_list_handle
            )
            if publisher_name is not None:
                publisher_list.append(
                    publisher_name
                )
            else:
                break

        for publisher_name in sorted(publisher_list):
            print_publisher_info(publisher_name)
            print()

        wevtapi.EvtClose(
            publisher_list_handle
        )


if __name__ == "__main__":
    main()
