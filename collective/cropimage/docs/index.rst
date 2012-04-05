.. include:: README.rst

How to crop image
-----------------

1. Activate collective.cropimage package through Add-ons configuration page.
2. Click link  ``Crop Image Registry`` under **Add-on Configuration**.
3. Add ID with which the crop dimension will be stored.
4. Go to content type where you have croppable images.
5. From Actions, click ``Crop Image``.
6. Select the name of ID.
7. Now you can drag over image to select the crop area.
8. Save the area.

How to use the cropped image on your template
---------------------------------------------

For example::

	<div tal:replace="structure python: context.restrictedTraverse('cropped-image')('image', 'small-image')" />

Here, **image** is the field name and **small-image** is the ID name.

``cropped-image`` is a named view attribute of ``cropped_image`` derived from ``collective.cropimage.browser.miscellaneous.Miscellaneous`` class.

.. automodule:: collective.cropimage.browser.miscellaneous

.. autoclass:: Miscellaneous
   :members: cropped_image

collective.contentleadimage
---------------------------

``collective.cropimage`` works with  ``collective.contentleadimage``, too.
The image field name is ``leadImage``, so use cropped image like::

    <div tal:replace="structure python: context.restrictedTraverse('cropped-image')('leadImage', 'small-image')" />

Contents:

.. toctree::
    :maxdepth: 2

    INSTALL.rst
    HISTORY.rst
    LICENSE.rst
    CONTRIBUTORS.rst
    CREDITS.rst

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
