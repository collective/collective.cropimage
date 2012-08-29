import unittest


class TestID(unittest.TestCase):

    def createInstance(self):
        from collective.cropimage.id import ID
        return ID('id01')

    def test_instance(self):
        item = self.createInstance()
        from collective.cropimage.id import ID
        self.assertTrue(isinstance(item, ID))
        from collective.cropimage.id import IID
        self.assertTrue(IID.providedBy(item))
