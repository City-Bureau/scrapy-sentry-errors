import os
import time
import inspect
import pkg_resources

from scrapy.utils.project import get_project_settings
import sentry_sdk  # New import for Sentry SDK

settings = get_project_settings()

SENTRY_DSN = os.environ.get("SENTRY_DSN", None)


def get_client(dsn=None, **options):
    """Initializes Sentry SDK client."""
    sentry_dsn = dsn or settings.get("SENTRY_DSN", SENTRY_DSN)
    if sentry_dsn:
        sentry_sdk.init(dsn=sentry_dsn, **options)
    return sentry_sdk


def get_release(crawler):
    """Gets the release from a given crawler."""
    try:
        mod = inspect.getmodule(crawler.spidercls)
        pkg = mod.__package__.replace(".", "-")
        return pkg_resources.get_distribution(pkg).version
    except Exception:
        return None


def response_to_dict(response, spider, include_request=True, **kwargs):
    """Returns a dict based on a response from a spider"""
    d = {
        "time": time.time(),
        "status": response.status,
        "url": response.url,
        "headers": dict(response.headers),
        "body": response.body,
    }
    if include_request:
        d["request"] = response.request.to_dict(spider=spider)
    return d
