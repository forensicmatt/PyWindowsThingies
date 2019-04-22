import sys
sys.path.append("..")
import fmt
import yaml
import argparse
from functools import partial
from winthingies.filter import Filter
from winthingies.trace import TraceProvider
from winthingies.trace import EventTraceHandler


class EventHandler(object):
    def __init__(self, output_format=None, event_filter=None):
        self.event_filter = event_filter
        self.output_format = output_format

    def custom_format(self, record):
        return fmt(self.output_format)

    def event_callback(self, lp_event_record):
        event_dict = lp_event_record.contents.as_dict()

        if self.event_filter:
            if self.event_filter.is_true(event_dict):
                if self.output_format:
                    print(self.custom_format(event_dict))
                else:
                    print(event_dict)
        else:
            if self.output_format:
                print(self.custom_format(event_dict))
            else:
                print(event_dict)


def get_arguments():
    usage = "Monitor ETW."

    arguments = argparse.ArgumentParser(
        description=usage,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    arguments.add_argument(
        "-t", "--template",
        dest="template",
        action="store",
        required=True,
        help="The template."
    )

    return arguments


def get_providers(provider_list):
    """Iterate list of provider dictionaries

    :param provider_list: (list) list of provider dictionaries
    :return: (list<TraceProvider>) list of TraceProvider objects
    """
    providers = []
    for provider_dict in provider_list:
        trace_provider = TraceProvider(
            provider_dict.get("name"),
            provider_dict.get("guid"),
            match_any_keyword=provider_dict.get("match_any_keyword", 0),
            match_all_keyword=provider_dict.get("match_all_keyword", 0)
        )
        providers.append(
            trace_provider
        )
    return providers


def main():
    arguments = get_arguments()
    options = arguments.parse_args()

    with open(options.template, "r") as template_fh:
        template_dict = yaml.load(template_fh)
        session_name = template_dict.get("session_name")
        provider_list = template_dict.get("providers")
        providers = get_providers(provider_list)

        event_filter = template_dict.get("filter", None)
        if event_filter:
            event_filter = Filter.from_dict(
                event_filter
            )

        output_format = None
        if "output" in template_dict:
            output_format = template_dict["output"].get(
                "format", None
            )

    event_handler = EventHandler(
        output_format=output_format,
        event_filter=event_filter
    )

    event_trace_handler = EventTraceHandler(
        session_name,
        providers,
        partial(EventHandler.event_callback, event_handler)
    )

    event_trace_handler.start_session()


if __name__ == "__main__":
    main()
