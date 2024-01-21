scrapy-sentry-errors
=============

A simple Scrapy extension that logs spider errors to your Sentry account.

Note: while this extension captures errors from Scrapy spiders, it does not capture errors elsewhere in Scrapy's operation (e.g. the Scrapy pipeline).

Requirements: 
-----------

* Python 3.8+
* A [Sentry](http://www.getsentry.com/) account.
* The [DSN](https://docs.sentry.io/product/sentry-basics/concepts/dsn-explainer/) for your Sentry project.

Installation
------------

```
pip install city-scrapers-sentry
```

Setup
-----

Add `SENTRY_DSN` and `scrapy_sentry_errors.extensions.Errors` extension to your Scrapy project's `settings.py` file:

Example:

```
# sentry dsn
SENTRY_DSN = 'http://public:secret@example.com/1'
EXTENSIONS = {
    "scrapy_sentry_errors.extensions.Errors": 10,
}
```

Sentry spider errors will be logged to your Sentry account.

Development
-----

1. Clone this repository.
   
2. Run the dev setup script and follow the prompts. This will create a virtual environment and a `.env` file with your Sentry DSN:
```
bash ./scripts/dev_setup.sh
```

3. Simulate a failed spider run using the example Scrapy project in this repo:
```
pipenv run example
```

Acknowledgements
-----

This project began as a fork of [scrapy-sentry](https://github.com/llonchj/scrapy-sentry), which was developed by Jordi Llonch. We are grateful for his work and those of other contributors.
