from setuptools import setup, find_packages

setup(
    name="ook-translator",
    version="0.1.0",
    description="A Python tool that translates text between human language and the Librarian's Ook-based orangutan language from Terry Pratchett's Discworld.",
    author="Alma Nilsson",
    license="MIT",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "",
    ],
    entry_points={
        "console_scripts": [
            "ook-translator = ook_translator.cli:main",
        ],
    },
)