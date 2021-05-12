import argparse


class ArgumentParserMixin(object):
    _argument_parser = None
    _argument_parser_options = None

    @property
    def argument_parser(self):
        if self._argument_parser is None:
            self._argument_parser = argparse.ArgumentParser()
        return self._argument_parser

    def argument_parser_add(self, *args, **kwargs):
        self.argument_parser.add_argument(*args, **kwargs)

    def argument_parser_parse(self, *args, **kwargs):
        self._argument_parser_options = self.argument_parser.parse_args(*args, **kwargs)

    @property
    def argument_parser_options(self):
        if self._argument_parser_options is None:
            self.argument_parser_parse()
        return self._argument_parser_options
