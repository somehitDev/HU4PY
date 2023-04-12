# -*- coding: utf-8 -*-
from setuptools import setup
from hufpy import __name__, __author__, __email__, __version__


with open("requirements.txt", "r", encoding = "utf-8") as reqr:
    requires = [
        item.strip()
        for item in reqr.read().split("\n")
    ]

with open("README.md", "r", encoding = "utf-8") as rmr:
    readme = rmr.read()


setup(
    # publish informations
    name = __name__,
    author = __author__,
    author_email = __email__,
    url = "https://github.com/oyajiDev/hufpy",
    version = __version__,
    python_requires = ">=3.9",
    install_requires = requires,
    setup_requires = requires,
    license = "MIT license",
    description = "Html Ui For Python",
    long_description = readme,
    long_description_content_type = "text/markdown",
    # package informations
    packages = [
        __name__, f"{__name__}/widgets",
        f"{__name__}/assets", f"{__name__}/assets/fonts", f"{__name__}/assets/icons", f"{__name__}/assets/styles"
    ],
    package_data = {
        "": [
            "*.ttf",
            "*.icns", "*.ico", "*.png",
            "*.css", "*.js", "*.html"
        ]
    },
    include_package_data = True,
    zip_safe = True
)
