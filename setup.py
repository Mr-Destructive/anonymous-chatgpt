import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

VERSION = "0.1.2"
PACKAGE_NAME = "anonymous-chatgpt"
AUTHOR = "Meet Gor"
AUTHOR_EMAIL = "gormeet711@gmail.com"
URL = "https://github.com/Mr-Destructive/anonymous-chatgpt"

DESCRIPTION = (
    "A Python Client to interact with OpenAI's ChatGPT(GPT-3) model without authentication"
)
README = (pathlib.Path(__file__).parent / "README.md").read_text(encoding="utf-8")

INSTALL_REQUIRES = [
    "requests",
    #"rich",
]

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=README,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    install_requires=INSTALL_REQUIRES,
    packages=find_packages(),
    entry_points={"console_scripts": ["chatgpt = anonymous_chatgpt.app:main"]},
)

