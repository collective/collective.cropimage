from Acquisition import aq_inner
from Products.Archetypes.Field import ImageField
from Products.Five.browser import BrowserView
from plone.app.blob.subtypes.image import ExtensionBlobField
from plone.registry.interfaces import IRegistry
from zope.annotation.interfaces import IAnnotations
from zope.component import getUtility


class Miscellaneous(BrowserView):

    def image_fields(self):
        """Returns list of field names."""
        registry = getUtility(IRegistry)
        ids = registry['collective.cropimage.ids']
        context = aq_inner(self.context)
        if hasattr(context, 'Schema') and len(ids) > 0:
            keys = [key for key in context.Schema().keys() if isinstance(
                    context.getField(key), ExtensionBlobField) or isinstance(
                    context.getField(key), ImageField)]
            return keys

    def has_image(self):
        """Returns True if there are any available field names else False."""
        return self.image_fields()

    def cropped_image(self, field, id_name):
        """Retuns html tag for the cropped image.

        :param field: Field name.
        :type field: str

        :param id_name: ID name.
        :type id_name: str
        """
        context = aq_inner(self.context)
        anno = IAnnotations(context)
        name = 'collective.cropimage.{0}'.format(field)
        data = anno[name][id_name] if anno.get(name) is not None and anno.get(name).get(id_name) is not None else None
        if data is not None:
            width = 'width:{0}px;'.format(data['w'])
            height = 'height:{0}px;'.format(data['h'])
            html = '<div class="crop" style="{0}{1}">'.format(width, height)
            if 'x1' in data:
                data['x'] = data['x1']
                data['y'] = data['y1']
            clip = 'clip:rect({0}px {1}px {2}px {3}px);'.format(data['y'], data['x2'], data['y2'], data['x'])
            top = 'top:-{0}px;'.format(data['y'])
            left = 'left:-{0}px;'.format(data['x'])
            html += '<p style="{0}{1}{2}position:absolute">'.format(clip, top, left)
            src = '{0}/{1}'.format(context.absolute_url(), field)
            title = context.Title()
            html += '<img src="{0}" alt="{1}" title="{1}" />'.format(src, title)
            html += '</p>'
            html += '</div>'
            return html
