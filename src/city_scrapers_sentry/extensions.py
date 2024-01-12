"""
Send signals to Sentry

Use SENTRY_DSN setting to enable sending information
"""
import os
import logging
from io import StringIO

from scrapy import signals
from scrapy.exceptions import NotConfigured

from .utils import get_client, get_release, response_to_dict


class Errors(object):
    def __init__(self, dsn=None, client=None, **kwargs):
        self.client = client if client else get_client(dsn, **kwargs)

    @classmethod
    def from_crawler(cls, crawler, client=None, dsn=None):
        release = crawler.settings.get("RELEASE", get_release(crawler))

        dsn = os.environ.get(
            "SENTRY_DSN", crawler.settings.get("SENTRY_DSN", None))
        if dsn is None:
            raise NotConfigured('No SENTRY_DSN configured')
        o = cls(dsn=dsn, release=release)
        crawler.signals.connect(o.spider_error, signal=signals.spider_error)
        return o

    def spider_error(self, failure, response, spider,
                     signal=None, sender=None, *args, **kwargs):
        traceback = StringIO()
        failure.printTraceback(file=traceback)

        res_dict = response_to_dict(response, spider, include_request=True)

        extra = {
            'sender': sender,
            'spider': spider.name,
            'signal': signal,
            'failure': failure,
            'response': res_dict,
            'traceback': "\n".join(traceback.getvalue().split("\n")[-5:]),
        }
        msg = self.client.captureMessage(
            message=u"[{}] {}".format(spider.name, repr(failure.value)),
            extra=extra)  # , stack=failure.stack)

        ident = self.client.get_ident(msg)

        logging.log(logging.WARNING, "Sentry Exception ID '%s'" % ident)

        return ident
