import ujson
import logging
import argparse
from winthingies.process import iterate_processes

logging.basicConfig(
    level=logging.INFO
)


def get_arguments():
    usage = """List Processes."""

    arguments = argparse.ArgumentParser(
        description=usage,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    arguments.add_argument(
        "-n", "--name",
        dest="name",
        action="store",
        required=False,
        default=None,
        help="Processes with a specific name."
    )

    return arguments


def main():
    arguments = get_arguments()
    options = arguments.parse_args()

    for process in iterate_processes():
        if process.name:
            if options.name:
                if process.name.lower() == options.name.lower():
                    print(ujson.dumps(process.as_dict()))
            else:
                print(ujson.dumps(process.as_dict()))


if __name__ == "__main__":
    main()
