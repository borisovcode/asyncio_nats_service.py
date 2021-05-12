import logging


class LoggerMixin(object):
    _logger = logging.getLogger(__name__)