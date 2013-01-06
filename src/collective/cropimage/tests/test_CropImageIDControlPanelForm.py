import mock
import unittest


class TestCropImageIDControlPanelForm(unittest.TestCase):

    def createInstance(self):
        """Create CropImageIDControlPanelForm instance."""
        from collective.cropimage.browser.template import CropImageIDControlPanelForm
        return CropImageIDControlPanelForm(mock.Mock(), mock.Mock())

    def test_instance(self):
        item = self.createInstance()
        from collective.cropimage.browser.template import CropImageIDControlPanelForm
        self.assertTrue(isinstance(item, CropImageIDControlPanelForm))
        from plone.z3cform.crud.crud import CrudForm
        self.assertTrue(issubclass(CropImageIDControlPanelForm, CrudForm))

    def test_update_schema(self):
        item = self.createInstance()
        from collective.cropimage.browser.template import IID
        self.assertTrue(item.update_schema is IID)

    def test_label(self):
        item = self.createInstance()
        self.assertEqual(item.label, u'Crop Image ID')

    @mock.patch('collective.cropimage.browser.template.crud.CrudForm.update')
    def test_update(self, crud_form_update):
        item = self.createInstance()
        form = mock.Mock()
        form.widgets = {
            'id': mock.Mock(),
            'ratio_width': mock.Mock(),
            'ratio_height': mock.Mock(),
            'min_width': mock.Mock(),
            'min_height': mock.Mock(),
            'max_width': mock.Mock(),
            'max_height': mock.Mock(),
        }
        edit_forms = mock.Mock()
        add_form = mock.Mock()
        add_form.widgets = {
            'id': mock.Mock(),
            'ratio_width': mock.Mock(),
            'ratio_height': mock.Mock(),
            'min_width': mock.Mock(),
            'min_height': mock.Mock(),
            'max_width': mock.Mock(),
            'max_height': mock.Mock(),
        }
        item.subforms = [edit_forms, add_form]
        edit_forms.subforms = [form]
        item.update()
        form = item.subforms[0].subforms[0]
        self.assertEqual(form.widgets['id'].size, 10)
        self.assertEqual(form.widgets['ratio_width'].size, 3)
        self.assertEqual(form.widgets['ratio_height'].size, 3)
        self.assertEqual(form.widgets['min_width'].size, 3)
        self.assertEqual(form.widgets['min_height'].size, 3)
        self.assertEqual(form.widgets['max_width'].size, 3)
        self.assertEqual(form.widgets['max_height'].size, 3)
        self.assertEqual(add_form.widgets['id'].size, 10)
        self.assertEqual(add_form.widgets['ratio_width'].size, 3)
        self.assertEqual(add_form.widgets['ratio_height'].size, 3)
        self.assertEqual(add_form.widgets['min_width'].size, 3)
        self.assertEqual(add_form.widgets['min_height'].size, 3)
        self.assertEqual(add_form.widgets['max_width'].size, 3)
        self.assertEqual(add_form.widgets['max_height'].size, 3)

    def test_CropImageIDControlPanelView(self):
        from collective.cropimage.browser.template import CropImageIDControlPanelView
        self.assertEqual(
            CropImageIDControlPanelView.__name__,
            'MyFormWrapper'
        )
        self.assertEqual(
            CropImageIDControlPanelView.form.__name__,
            'CropImageIDControlPanelForm'
        )
        filename = CropImageIDControlPanelView.index.filename.split('/')[-1]
        self.assertEqual(
            filename,
            'controlpanel.pt'
        )
