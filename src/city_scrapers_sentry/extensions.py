import logging
from io import StringIO

from scrapy import signals
from scrapy.exceptions import NotConfigured

import sentry_sdk 

class Errors(object):
    def __init__(self, dsn=None, **kwargs):
        self.client = self.get_client(dsn, **kwargs)

    def get_client(self, dsn, **options):
        sentry_sdk.init(dsn=dsn, **options)
        return sentry_sdk

    @classmethod
    def from_crawler(cls, crawler, dsn=None):
        dsn = crawler.settings.get("SENTRY_DSN")
        if dsn is None:
            raise NotConfigured("No SENTRY_DSN configured")
        extension = cls(dsn=dsn)
        crawler.signals.connect(extension.spider_error, signal=signals.spider_error)
        return extension

    def spider_error(self, failure):
        traceback = StringIO()
        failure.printTraceback(file=traceback)
        self.client.capture_exception(failure.value)
        logging.log(logging.WARNING, "Sentry Exception captured")

