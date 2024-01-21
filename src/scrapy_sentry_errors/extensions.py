import logging
from io import StringIO
from typing import Optional

from scrapy import signals
from scrapy.exceptions import NotConfigured

import sentry_sdk


class Errors(object):
    """Handles error reporting and capturing exceptions using Sentry."""

    def __init__(self, dsn: Optional[str] = None, **kwargs: Optional[str]) -> None:
        self.client = self.get_client(dsn, **kwargs)

    def get_client(self, dsn: Optional[str], **options: Optional[str]) -> sentry_sdk:
        """
        Get the Sentry client.

        Args:
            dsn (str): The Sentry DSN.
            **options: Additional options to pass to the Sentry SDK.

        Returns:
            sentry_sdk: The initialized Sentry client.
        """
        sentry_sdk.init(dsn=dsn, **options)
        return sentry_sdk

    @classmethod
    def from_crawler(
        cls, crawler: "scrapy.crawler.Crawler", dsn: Optional[str] = None
    ) -> "Errors":
        """
        Create an instance of Errors from a Scrapy crawler.

        Args:
            crawler (scrapy.crawler.Crawler): The Scrapy crawler instance.
            dsn (str): The Sentry DSN.

        Returns:
            Errors: The Errors instance.

        Raises:
            NotConfigured: If no SENTRY_DSN is configured.
        """
        dsn = crawler.settings.get("SENTRY_DSN")
        if dsn is None:
            raise NotConfigured("No SENTRY_DSN configured")
        extension = cls(dsn=dsn)
        crawler.signals.connect(extension.spider_error, signal=signals.spider_error)
        return extension

    def spider_error(self, failure: "twisted.python.failure.Failure") -> None:
        """
        Handle spider errors by capturing exceptions and logging them to Sentry.

        Args:
            failure (twisted.python.failure.Failure): The failure instance.
        """
        traceback = StringIO()
        failure.printTraceback(file=traceback)
        self.client.capture_exception(failure.value)
        logging.log(logging.WARNING, "Sentry Exception captured")
