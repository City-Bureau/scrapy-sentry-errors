import logging
from io import StringIO
from typing import Any, Dict, Optional

import sentry_sdk
from scrapy import signals
from scrapy.crawler import Crawler
from scrapy.exceptions import CloseSpider
from twisted.python.failure import Failure


class Errors(object):
    """Handles error reporting and capturing exceptions using Sentry."""

    def __init__(
        self, dsn: Optional[str] = None, **kwargs: Optional[Dict[str, Any]]
    ) -> None:
        self.client = self.get_client(dsn, **kwargs)

    def get_client(
        self, dsn: Optional[str], **options: Optional[Dict[str, Any]]
    ) -> sentry_sdk:
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
        cls, crawler: Crawler, dsn: Optional[str] = None
    ) -> "Errors":  # noqa
        """
        Create an instance of Errors from a Scrapy crawler.

        Args:
            crawler (scrapy.crawler.Crawler): The Scrapy crawler instance.
            dsn (str): The Sentry DSN.

        Returns:
            Errors: The Errors instance.

        Raises:
            CloseSpider: If no SENTRY_DSN is configured.
        """
        dsn = crawler.settings.get("SENTRY_DSN")
        if dsn is None:
            logging.log(logging.ERROR, "SENTRY_DSN is not configured")
            raise CloseSpider(
                reason="SENTRY_DSN must be configured to enable \
                    scrapy-sentry-errors extension"
            )

        extension = cls(dsn=dsn)
        crawler.signals.connect(extension.spider_error, signal=signals.spider_error)
        logging.log(logging.INFO, "Scrapy integration active")
        return extension

    def spider_error(self, failure: Failure) -> None:
        """
        Handle spider errors by capturing exceptions and logging them to Sentry.

        Args:
            failure (twisted.python.failure.Failure): The failure instance.
        """
        traceback = StringIO()
        failure.printTraceback(file=traceback)
        self.client.capture_exception(failure.value)
        logging.log(
            logging.INFO, "Exception captured by scrapy-sentry-errors extension"
        )
