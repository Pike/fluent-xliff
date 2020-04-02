from .base import XLIFFer

def simple_patterns_xliff(config, destination):
    xl = XLIFFer(config)
    for locale in xl.locales:
        target_path = destination / locale
        if not target_path.is_dir():
            target_path.mkdir(parents=True)
        target_path = target_path / 'file.xlf'
        with target_path.open(mode='wb') as fh:
            fh.write(xl.xliff(locale))
        print(target_path, "written")
