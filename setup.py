from setuptools import find_packages
from setuptools import setup

import os

long_description = (
    open(os.path.join("collective", "cropimage", "docs", "README.rst")).read() + "\n" +
    open(os.path.join("collective", "cropimage", "docs", "HISTORY.rst")).read() + "\n" +
    open(os.path.join("collective", "cropimage", "docs", "CONTRIBUTORS.rst")).read()
)

setup(
    name='collective.cropimage',
    version='1.2.1',
    description="Store cropped image dimension for farther usage.",
    long_description=long_description,
    # Get more strings from
    # http://pypi.python.org/pypi?:action=list_classifiers
    classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 4.1",
        "Framework :: Plone :: 4.2",
        "Programming Language :: Python",
    ],
    keywords='',
    author='Taito Horiuchi',
    author_email='taito.horiuchi@gmail.com',
    url='http://packages.python.org/collective.cropimage/',
    license='BSD',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['collective'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'hexagonit.testing',
        'plone.app.registry',
        'plone.browserlayer',
        'setuptools',
        'zope.i18nmessageid',
    ],
    entry_points="""
    # -*- Entry points: -*-

    [z3c.autoinclude.plugin]
    target = plone
    """,
)
