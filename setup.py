from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

setup(
    name="mr_python",
    version="0.7.5",
    description="An API binding and ETL toolset for the mediumroast.io application.",
    long_description = (here / 'README.md').read_text(encoding='utf-8'),
    author="Michael Hay",
    url="https://github.com/mediumroast/mr_python",
    author_email="michael.hay@mediumroast.io",
    classifiers=[ 
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Application Frameworks',

        # Pick your license as you wish
        'License :: OSI Approved :: Apache Software License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate you support Python 3. These classifiers are *not*
        # checked by 'pip install'. See instead 'python_requires' below.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
    ],
    scripts=['cli/list_interactions.py', 'cli/list_studies.py', 'cli/list_companies.py', 'cli/list_raw_objects.py'],
    packages=['mr_python', 'mr_python/transformers', 'mr_python/extractors', 'mr_python/loaders', 'mr_python/api'],
    python_requires='>=3.6, <4',
    project_urls={  # Optional
        'Bug Reports': 'https://github.com/mediumroast/mr_python/issues',
        'Source': 'https://github.com/mediumroast/mr_python',
    },
)