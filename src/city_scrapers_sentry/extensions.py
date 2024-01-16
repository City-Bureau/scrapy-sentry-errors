import os
import logging
from io import StringIO

from scrapy import signals
from scrapy.exceptions import NotConfigured

from .utils import get_client, get_release, response_to_dict


class Errors(object):
    def __init__(self, dsn=None, client=None, **kwargs):
        self.client = get_client(dsn, **kwargs)  # Initialize Sentry SDK

    @classmethod
    def from_crawler(cls, crawler, dsn=None):
        release = crawler.settings.get("RELEASE", get_release(crawler))

        dsn = os.environ.get("SENTRY_DSN", crawler.settings.get("SENTRY_DSN", None))
        if dsn is None:
            raise NotConfigured("No SENTRY_DSN configured")
        extension = cls(dsn=dsn, release=release)
        crawler.signals.connect(extension.spider_error, signal=signals.spider_error)
        return extension

    def spider_error(
        self, failure, response, spider, signal=None, sender=None, *args, **kwargs
    ):
        traceback = StringIO()
        failure.printTraceback(file=traceback)

        res_dict = response_to_dict(response, spider, include_request=True)

        extra = {
            "sender": sender,
            "signal": signal,
            "failure": failure,
            "response": res_dict,
            "traceback": "\n".join(traceback.getvalue().split("\n")[-5:]),
        }
        
        with self.client.push_scope() as scope:
            for key, value in extra.items():
                scope.set_tag('spider', spider.name)
                scope.set_extra(key, value)
            self.client.capture_exception(failure.value)

        logging.log(logging.WARNING, "Sentry Exception captured")

