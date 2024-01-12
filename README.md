city-scrapers-sentry
=============

A Scrapy extension that logs spider errors to Sentry.

This project began as a fork of [scrapy-sentry](https://github.com/llonchj/scrapy-sentry), which was developed by Jordi Llonch. We are grateful for their work and contributions.

Note: while this extension captures errors from Scrapy spiders, it does not capture errors elsewhere in Scrapy's operation (e.g. the Scrapy pipeline).

Requisites: 
-----------

* [Sentry server](http://www.getsentry.com/)

Installation
------------

```
pip install city-scrapers-sentry
```

Setup
-----

Add `SENTRY_DSN` and `city_scrapers_sentry.extensions.Errors` extension to your Scrapy Project `settings.py`.

Example:

```
# sentry dsn
SENTRY_DSN = 'http://public:secret@example.com/1'
EXTENSIONS = {
    "city_scrapers_sentry.extensions.Errors": 10,
}
```

Development
-----

1. Install [pipenv](https://pipenv.pypa.io/en/latest/) if you don't have it already.

2. At the project root, create a .env file and include the following. Replace `<your-sentry-dsn>` with your Sentry DSN:
```
SENTRY_DSN=<your-sentry-dsn>
```
3. Activate pipenv's virtual environment and install dependencies. Your environment variables will be loaded from the .env file:
```
pipenv sync --dev
```

4. Enter the example_project directory:
```
cd example_project
```

5. Simulate a failed spider run. If properly configured, the spider will log an error to your Sentry account:
```
scrapy crawl example
```
