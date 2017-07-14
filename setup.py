from setuptools import setup, find_packages


with open('json2jqq/version.py') as inp:
    exec(inp.read())


with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='json2jqq',
    version=__version__,
    install_requires=requirements,
    author='Toshihiro Kamiya',
    author_email='kamiya@mbj.nifty.com',
    entry_points="""
      [console_scripts]
      json2jqq = json2jqq:main
      """,
    packages=find_packages(),
    url='https://github.com/tos-kamiya/json2jqq/',
    license='License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
    description='CLI Tool to extract query templates for jq tool from json data',
)
