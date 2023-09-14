from setuptools import setup

setup(
    name="pgcrow",
    version="0.7.0",
    description="Pygame framework for making simple games",
    author="KentAugust",
    author_email="kentaugustone@gmail.com",
    url="https://github.com/KentAugust/pycrow",
    package_dir={"pgcrow": "src", "pgcrow.examples": "examples"},
    install_requires=['pygame-ce>=2.3.1'],
)
