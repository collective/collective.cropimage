import mock
import unittest2 as unittest


class TestCropImageView(unittest.TestCase):

    def createCropImageView(self, context, request):
        from collective.cropimage.browser.template import CropImageView
        return CropImageView(context, request)

    def test_instance(self):
        context = mock.Mock()
        request = mock.Mock()
        item = self.createCropImageView(context, request)
        from collective.cropimage.browser.template import CropImageView
        self.assertTrue(isinstance(item, CropImageView))
        from Products.Five.browser import BrowserView
        self.assertTrue(issubclass(CropImageView, BrowserView))

    def test_template(self):
        context = mock.Mock()
        request = mock.Mock()
        item = self.createCropImageView(context, request)
        self.assertEqual(
            item.template.filename.split('/')[-1],
            'crop_image.pt'
        )

    @mock.patch('collective.cropimage.browser.template.IAnnotations')
    @mock.patch('collective.cropimage.browser.template.aq_inner')
    def test__call(self, aq_inner, IAnnotations):
        context = mock.Mock()
        request = mock.Mock()
        item = self.createCropImageView(context, request)
        item.request.form = {}
        item.template = mock.Mock()
        item()
        self.assertTrue(item.template.called)
        anno = IAnnotations.return_value = {}
        item.request.form = {'form.button.Save': True, 'field': 'image'}
        item.dimension = mock.Mock()
        item.dimension.return_value = {'small-image': 'dimensions'}
        item()
        self.assertEqual(
            anno,
            {'collective.cropimage.image': {'small-image': 'dimensions'}}
        )
        item.dimension.return_value = {'middle-image': 'dimensions'}
        item()
        self.assertEqual(
            anno,
            {
                'collective.cropimage.image': {
                    'small-image': 'dimensions',
                    'middle-image': 'dimensions',
                }
            }
        )

    @mock.patch('collective.cropimage.browser.template.getUtility')
    def test_ids(self, getUtility):
        getUtility.return_value = {'collective.cropimage.ids': 'Something'}
        context = mock.Mock()
        request = mock.Mock()
        item = self.createCropImageView(context, request)
        self.assertEqual(item.ids(), 'Something')

    def test_selected_id(self):
        context = mock.Mock()
        request = mock.Mock()
        request.form = {}
        item = self.createCropImageView(context, request)
        item.ids = mock.Mock(return_value=[{'id': 'ID'}])
        self.assertEqual(item.selected_id(), 'ID')
        request.form = {'id-name': 'Some ID'}
        item = self.createCropImageView(context, request)
        self.assertEqual(item.selected_id(), 'Some ID')

    @mock.patch('collective.cropimage.browser.template.getUtility')
    def test_select(self, getUtility):
        context = mock.Mock()
        request = mock.Mock()
        item = self.createCropImageView(context, request)
        getUtility.return_value = {'collective.cropimage.ids': [{'id': 'small-image'}, {'id': 'middle-image'}]}
        self.assertEqual(
            item.select(),
            '<select name="id-name" id="id-name"><option value="small-image">small-image</option><option value="middle-image">middle-image</option></select>'
        )

    @mock.patch('collective.cropimage.browser.template.getUtility')
    def test_script(self, getUtility):
        getUtility.return_value = {'collective.cropimage.ids': [{'id': 'ID'}]}
        context = mock.Mock()
        request = mock.Mock()
        item = self.createCropImageView(context, request)
        data = dict(
            id='ID',
            ratio_width=0.0,
            ratio_height=0.0,
            min_width=0.0,
            min_height=0.0,
            max_width=0.0,
            max_height=0.0,
        )
        item.ids = mock.Mock(return_value=[data])
        item.selected_id = mock.Mock(return_value='ID')
        keys = ['aspectRatio', 'minSize', 'maxSize']
        for key in keys:
            self.assertFalse(key in item.script())
        data.update({'ratio_width': 600.0})
        self.assertFalse('aspectRatio' in item.script())
        data.update({'ratio_height': 450.0})
        self.assertTrue('aspectRatio: 600.0/450.0' in item.script())
        data.update({'min_width': 60.0})
        self.assertFalse('minSize' in item.script())
        data.update({'min_height': 45.0})
        self.assertTrue('minSize: [60.0, 45.0]' in item.script())
        data.update({'max_width': 120.0})
        self.assertFalse('maxSize' in item.script())
        data.update({'max_height': 90.0})
        self.assertTrue('maxSize: [120.0, 90.0]' in item.script())

    @mock.patch('collective.cropimage.browser.template.aq_inner')
    def test_fields(self, aq_inner):
        context = mock.Mock()
        request = mock.Mock()
        item = self.createCropImageView(context, request)
        item.fields()
        self.assertTrue(aq_inner().restrictedTraverse.called)

    def test_dimension(self):
        context = mock.Mock()
        request = mock.Mock()
        item = self.createCropImageView(context, request)
        form = {
            'x1': '10',
            'x2': '20',
            'y1': '30',
            'y2': '60',
            'w': '20',
            'h': '30',
            'id-name': 'small-image',
        }
        self.assertEqual(
            item.dimension(form),
            {
                'small-image': {
                    'y1': '30', 'y2': '60', 'w': '20', 'x2': '20', 'h': '30', 'x1': '10'
                }
            }
        )

    @mock.patch('collective.cropimage.browser.template.aq_inner')
    def test_images(self, aq_inner):
        context = mock.Mock()
        request = mock.Mock()
        item = self.createCropImageView(context, request)
        item.fields = mock.Mock(return_value=['image'])
        aq_inner().getField().tag.return_value = '<img src="..." />'
        item.select = mock.Mock(return_value='<select />')
        item.previews = mock.Mock(return_value='PREVIEWS')
        self.assertEqual(
            item.images(),
            [
                {
                    'field': 'image',
                    'full-image': '<img id="cropbox" src="..." />',
                    'select': '<select />',
                    'previews': 'PREVIEWS'
                }
            ]
        )

    @mock.patch('collective.cropimage.browser.template.getMultiAdapter')
    def test_current_url(self, getMultiAdapter):
        context = mock.Mock()
        request = mock.Mock()
        item = self.createCropImageView(context, request)
        item.current_url()
        self.assertTrue(getMultiAdapter().current_page_url.called)

    @mock.patch('collective.cropimage.browser.template.IAnnotations')
    @mock.patch('collective.cropimage.browser.template.aq_inner')
    def test_previews(self, aq_inner, IAnnotations):
        context = mock.Mock()
        request = mock.Mock()
        item = self.createCropImageView(context, request)
        IAnnotations.return_value = {}
        self.assertFalse(item.previews('image'))
        IAnnotations.return_value = {'collective.cropimage.image': {'small-image': 'values'}}
        aq_inner().restrictedTraverse().return_value = '<img />'
        self.assertEqual(
            item.previews('image'),
            ['<article class="preview" id="image-small-image-preview"><h1>small-image</h1><img /></article>']
        )
