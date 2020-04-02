from .base import XLIFFer

def simple_patterns_xliff(config, destination):
    xl = XLIFFer(config)
    for locale in xl.locales:
        xl.xliff(locale)
