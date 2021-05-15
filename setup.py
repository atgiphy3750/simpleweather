from setuptools import setup

setup(
    name="simple-weather",
    packages=["simple-weather"],
    include_package_data=True,
    install_requires=["Flask", "requests", "Frozen-Flask"],
)
