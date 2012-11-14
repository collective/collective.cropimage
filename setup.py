from setuptools import find_packages
from setuptools import setup

import os


long_description = (
    open(os.path.join("collective", "cropimage", "docs", "README.rst")).read() + "\n" +
    open(os.path.join("collective", "cropimage", "docs", "HISTORY.rst")).read() + "\n" +
    open(os.path.join("collective", "cropimage", "docs", "CONTRIBUTORS.rst")).read())


setup(
    name='collective.cropimage',
    version='1.3',
    description="Store cropped image dimension for farther usage.",
    long_description=long_description,
    # Get more strings from
    # http://pypi.python.org/pypi?:action=list_classifiers
    classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 4.2",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7"],
    keywords='',
    author='Taito Horiuchi',
    author_email='taito.horiuchi@gmail.com',
    url='https://github.com/collective/collective.cropimage/',
    license='BSD',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['collective'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Plone>=4.2',
        'hexagonit.testing',
        'plone.app.registry',
        'plone.browserlayer',
        'setuptools',
        'zope.i18nmessageid'],
    entry_points="""
    # -*- Entry points: -*-

    [z3c.autoinclude.plugin]
    target = plone
    """)
