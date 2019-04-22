import sys
sys.path.append("..")
import ujson
import logging
import argparse
from winthingies.handle import iterate_handles

logging.basicConfig(
    level=logging.DEBUG
)


def get_arguments():
    usage = """Print Open Handles. I recommend using the --type param.
Some handle enumeration can cause hanging. Working on fix...
"""

    arguments = argparse.ArgumentParser(
        description=usage,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    arguments.add_argument(
        "-p", "--pid",
        dest="pid",
        action="store",
        required=False,
        default=None,
        type=int,
        help="A specific PID."
    )

    arguments.add_argument(
        "-t", "--type",
        dest="type",
        action="store",
        required=False,
        default=None,
        help="Only print specific handle types. [File, Key, etc.]"
    )

    return arguments


def main():
    arguments = get_arguments()
    options = arguments.parse_args()

    for handle in iterate_handles(pid=options.pid):
        if options.type is not None:
            try:
                if handle.type_name:
                    if handle.type_name.lower() == options.type.lower():
                        print(ujson.dumps(handle.as_dict()))
            except Exception as error:
                logging.debug(error)
        else:
            print(ujson.dumps(handle.as_dict()))


if __name__ == "__main__":
    main()
