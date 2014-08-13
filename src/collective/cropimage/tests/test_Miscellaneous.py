import mock
import unittest


class TestMiscellaneous(unittest.TestCase):

    def createMiscellaneous(self, context, request):
        from collective.cropimage.browser.miscellaneous import Miscellaneous
        return Miscellaneous(context, request)

    def test_instance(self):
        context = mock.Mock()
        request = mock.Mock()
        item = self.createMiscellaneous(context, request)
        from collective.cropimage.browser.miscellaneous import Miscellaneous
        self.assertTrue(isinstance(item, Miscellaneous))

    @mock.patch('collective.cropimage.browser.miscellaneous.aq_inner')
    @mock.patch('collective.cropimage.browser.miscellaneous.getUtility')
    def test_image_fields(self, getUtility, aq_inner):
        getUtility.return_value = {'collective.cropimage.ids': []}
        context = mock.Mock()
        request = mock.Mock()
        item = self.createMiscellaneous(context, request)
        self.assertFalse(item.image_fields())
        getUtility.return_value = {'collective.cropimage.ids': ['image']}
        aq_inner().keys.return_value = ['image']
        from plone.app.blob.subtypes.image import ExtensionBlobField
        aq_inner().getField.return_value = ExtensionBlobField()
        aq_inner().Schema().keys.return_value = ['image']
        self.assertEqual(item.image_fields(), ['image'])
        from Products.Archetypes.Field import ImageField
        aq_inner().getField.return_value = ImageField()
        aq_inner().Schema().keys.return_value = ['image']
        self.assertEqual(item.image_fields(), ['image'])

    def test_has_image(self):
        context = mock.Mock()
        request = mock.Mock()
        item = self.createMiscellaneous(context, request)
        item.image_fields = mock.Mock(return_value=None)
        self.assertFalse(item.has_image())
        item.image_fields = mock.Mock(return_value=['image'])
        self.assertTrue(item.has_image())

    @mock.patch('collective.cropimage.browser.miscellaneous.IAnnotations')
    @mock.patch('collective.cropimage.browser.miscellaneous.aq_inner')
    def test_cropped_image(self, aq_inner, IAnnotations):
        context = mock.Mock()
        request = mock.Mock()
        item = self.createMiscellaneous(context, request)
        field = 'field'
        id_name = 'small-image'
        aq_inner().absolute_url.return_value = 'url'
        aq_inner().Title.return_value = 'title'
        IAnnotations.return_value = {}
        self.assertFalse(item.cropped_image(field, id_name))
        IAnnotations.return_value = {'collective.cropimage.field': None}
        self.assertFalse(item.cropped_image(field, id_name))
        IAnnotations.return_value = {'collective.cropimage.field': {'small-image': None}}
        self.assertFalse(item.cropped_image(field, id_name))
        IAnnotations.return_value = {
            'collective.cropimage.field': {
                'small-image': {
                    'w': '60',
                    'h': '45',
                    'x1': '10',
                    'x2': '70',
                    'y1': '15',
                    'y2': '60',
                }
            }
        }
        self.assertEqual(
            item.cropped_image(field, id_name),
            '<div class="crop" style="width:60px;height:45px;"><p style="clip:rect(15px 70px 60px 10px);top:-15px;left:-10px;position:absolute"><img src="url/field" alt="title" title="title" /></p></div>'
        )
