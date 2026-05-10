from setuptools import setup, find_packages

setup(
    name="marathi-coref",

    version="0.1.0",

    author="Mansi Jangle",

    description="Marathi Coreference Resolution Library",

    packages=find_packages(),

    install_requires=[
        "stanza"
    ],

    python_requires=">=3.9",
)