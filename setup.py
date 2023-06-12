from setuptools import setup

setup(
    name='refid2bib',
    version='0.1',
    author='Casey Schneider-Mizell',
    author_email='caseysm@gmail.com',
    description='Package to get bibtex from various reference ids',
    packages=setuptools.find_packages(),
    install_requires=[
        'feedparser',
        'nameparser',
        'requests'
    ],
    scripts=['cli/refid2bib']
)
