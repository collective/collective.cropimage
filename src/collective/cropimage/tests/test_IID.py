import unittest


class TestIID(unittest.TestCase):

    def test_subclass(self):
        from collective.cropimage.interfaces import IAddID
        from collective.cropimage.interfaces import IID
        self.assertTrue(issubclass(IID, IAddID))

    def test_id__instance(self):
        from zope.schema import ASCIILine
        from collective.cropimage.interfaces import IID
        self.assertIsInstance(IID.get('id'), ASCIILine)

    def test_id__title(self):
        from collective.cropimage.interfaces import IID
        self.assertEqual(IID.get('id').title, u'ID')

    def test_id_readonly(self):
        from collective.cropimage.interfaces import IID
        self.assertTrue(IID.get('id').readonly)
