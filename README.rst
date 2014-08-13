====================
collective.cropimage
====================

This package provides image cropping for images which reside in ATContentTypes fields in Plone.
Those images can be cropped without losing the original images and without adding new images to blobs.
It only sets the cropping dimension to the object annotations.

Currently tested With
---------------------

* Plone-4.3.3 and Python-2.7.x
* Image and News Item Content Types.
* collective.contentleadimage

How to crop image
-----------------

1. Activate collective.cropimage package through **Add-ons configuration** page.
2. Click link  ``Crop Image Registry`` under **Add-on Configuration**.
3. Add ID with which the crop dimension will be stored.
4. Go to content type where you want to crop images.
5. From Actions, click ``Crop Image``.
6. Select the name of ID.
7. Now you can drag over image to select the crop area.
8. Save the area.

How to use the cropped image on your template
---------------------------------------------

For example::

    <div tal:replace="structure python: context.restrictedTraverse('cropped-image')('image', 'small-image')" />

Here, **image** is the field name and **small-image** is the ID name.

collective.contentleadimage
---------------------------

``collective.cropimage`` works with  ``collective.contentleadimage``, too.
The image field name is ``leadImage``, so use cropped image like::

    <div tal:replace="structure python: context.restrictedTraverse('cropped-image')('leadImage', 'small-image')" />
