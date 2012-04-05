Installation
============

Use zc.buildout and the plone.recipe.zope2instance
recipe to manage your project:

* Add ``collective.cropimage`` to the list of eggs to install like::

    [buildout]
    ...
    eggs =
        ...
        collective.cropimage

* Re-run buildout, e.g. with::

    $ ./bin/buildout
