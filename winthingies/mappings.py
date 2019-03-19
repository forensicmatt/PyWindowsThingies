import logging
from winthingies.win32.wevtapi import *
from winthingies.win32.wevtapi_helpers import PublisherMetadata


class PublisherMapping(object):
    def __init__(self):
        self.mapping = {}
        self._enum_publisher_info()

    def _enum_publisher_info(self):
        """Enumerate publisher info.

        :return: (None)
        """
        publisher_list_handle = EvtOpenPublisherEnum()
        while True:
            publisher_name = EvtNextPublisherId(
                publisher_list_handle
            )
            if publisher_name is not None:
                self.enum_publisher_info(
                    publisher_name
                )
            else:
                break

        wevtapi.EvtClose(
            publisher_list_handle
        )

    def enum_publisher_info(self, publisher_name):
        try:
            metadata_handle = PublisherMetadata(
                publisher_name
            )
        except WindowsError as error:
            logging.error("Error opening provider metadata {}; {}".format(
                publisher_name, error
            ))
            return

        self.mapping[metadata_handle.guid] = {
            "guid_str": str(metadata_handle.guid),
            "name": publisher_name,
            "keywords": metadata_handle.keyword_mapping,
            "operations": metadata_handle.opcode_mapping,
            "tasks": metadata_handle.task_mapping
        }

    def get_keyword_name(self, guid, keyword):
        """Get the name representing the keyword.

        :param guid:
        :param keyword:
        :return:
        """
        keyword_name_list = []
        pub_info = self.mapping.get(str(guid), None)
        if pub_info is not None:
            for keyword_int, keyword_info in pub_info['keywords'].items():
                if keyword & keyword_int:
                    keyword_name_list.append(
                        keyword_info['name']
                    )

        return "|".join(keyword_name_list)

    def get_opcode_name(self, guid, opcode_value):
        """Get the name representing the opcode.

        :param guid:
        :param keyword:
        :return:
        """
        pub_info = self.mapping.get(str(guid), None)
        if pub_info is not None:
            opcode_info = pub_info['operations'].get(opcode_value, None)
            if opcode_info is not None:
                return opcode_info['name']

        return str(opcode_value)

    def get_task_name(self, guid, task_value):
        """Get the name representing the task.

        :param guid:
        :param keyword:
        :return:
        """
        pub_info = self.mapping.get(str(guid), None)
        if pub_info is not None:
            task_info = pub_info['tasks'].get(task_value, None)
            if task_info is not None:
                return task_info['name']

        return str(task_value)
