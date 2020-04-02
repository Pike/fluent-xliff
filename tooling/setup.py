from setuptools import setup

setup(
    name="fluent-xliff",
    entry_points={
        "console_scripts": [
            "fluent-xliff=fluent_xliff.cli:main"
        ]
    },
    packages=[
        "fluent_xliff",
    ],
    install_requires=[
        "compare-locales",
    ]
)
