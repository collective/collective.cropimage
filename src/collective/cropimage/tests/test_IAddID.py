import unittest


class TestIAddID(unittest.TestCase):

    def test_id(self):
        from zope.schema import ASCIILine as FIELD
        from collective.cropimage.interfaces import IAddID
        field = IAddID.get('id')
        self.assertTrue(isinstance(field, FIELD))
        self.assertEqual(field.title, u'ID')

    def test_ratio_width(self):
        from zope.schema import Float as FIELD
        from collective.cropimage.interfaces import IAddID
        field = IAddID.get('ratio_width')
        self.assertTrue(isinstance(field, FIELD))
        self.assertEqual(field.title, u'Ratio Width')
        self.assertEqual(
            field.description,
            u'Keep this field 0.0 if you do not need to set width/height ratio.'
        )
        self.assertEqual(field.default, 0.0)

    def test_ratio_height(self):
        from zope.schema import Float as FIELD
        from collective.cropimage.interfaces import IAddID
        field = IAddID.get('ratio_height')
        self.assertTrue(isinstance(field, FIELD))
        self.assertEqual(field.title, u'Ratio Height')
        self.assertEqual(
            field.description,
            u'Keep this field 0.0 if you do not need to set width/height ratio.'
        )
        self.assertEqual(field.default, 0.0)

    def test_min_width(self):
        from zope.schema import Float as FIELD
        from collective.cropimage.interfaces import IAddID
        field = IAddID.get('min_width')
        self.assertTrue(isinstance(field, FIELD))
        self.assertEqual(field.title, u'Minimum Width')
        self.assertEqual(
            field.description,
            u'Keep this field 0.0 if you do not need to set minimum width.'
        )
        self.assertEqual(field.default, 0.0)

    def test_min_height(self):
        from zope.schema import Float as FIELD
        from collective.cropimage.interfaces import IAddID
        field = IAddID.get('min_height')
        self.assertTrue(isinstance(field, FIELD))
        self.assertEqual(field.title, u'Minimum Height')
        self.assertEqual(
            field.description,
            u'Keep this field 0.0 if you do not need to set minimum height.'
        )
        self.assertEqual(field.default, 0.0)

    def test_max_width(self):
        from zope.schema import Float as FIELD
        from collective.cropimage.interfaces import IAddID
        field = IAddID.get('max_width')
        self.assertTrue(isinstance(field, FIELD))
        self.assertEqual(field.title, u'Maximum Width')
        self.assertEqual(
            field.description,
            u'Keep this field 0.0 if you do not need to set maximum width.'
        )
        self.assertEqual(field.default, 0.0)

    def test_max_height(self):
        from zope.schema import Float as FIELD
        from collective.cropimage.interfaces import IAddID
        field = IAddID.get('max_height')
        self.assertTrue(isinstance(field, FIELD))
        self.assertEqual(field.title, u'Maximum Height')
        self.assertEqual(
            field.description,
            u'Keep this field 0.0 if you do not need to set maximum height.'
        )
        self.assertEqual(field.default, 0.0)
