from unittest.mock import MagicMock, patch

import pytest
from scrapy.exceptions import CloseSpider

from src.scrapy_sentry_errors.extensions import Errors


@pytest.fixture
def crawler_mock():
    crawler = MagicMock()
    crawler.settings = {"SENTRY_DSN": "https://public@sentry.example.com/1"}
    return crawler


def test_initialization_with_valid_dsn(crawler_mock):
    extension = Errors.from_crawler(crawler_mock)
    assert extension.client is not None


def test_initialization_fails_without_dsn(crawler_mock):
    crawler_mock.settings = {"SENTRY_DSN": None}
    with pytest.raises(CloseSpider):
        Errors.from_crawler(crawler_mock)


@patch("src.scrapy_sentry_errors.extensions.sentry_sdk")
def test_error_capturing_on_spider_error(mock_sentry_sdk, crawler_mock):
    # Initialize the extension with mocked crawler
    extension = Errors.from_crawler(crawler_mock)

    # Create a mock failure object with a test exception
    mock_failure = MagicMock()
    test_exception = Exception("Test exception")
    mock_failure.value = test_exception

    # Simulate spider error
    extension.spider_error(mock_failure)

    # Verify that Sentry's capture_exception method was called with the test exception
    mock_sentry_sdk.capture_exception.assert_called_with(test_exception)
