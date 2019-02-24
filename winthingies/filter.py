import jmespath


class Filter(object):
    def __init__(self, query):
        self.expression = jmespath.compile(
            query
        )

    def is_true(self, dictionary):
        this = self.expression.search(
            dictionary
        )

        return bool(this)

    @staticmethod
    def from_dict(filter_dict):
        return Filter(
            filter_dict.get("query")
        )
