from collective.cropimage.interfaces import IID
from zope.interface import implements


class ID(object):

    implements(IID)

    def __init__(self, id, **kwargs):
        self.id = id
        for key in kwargs.keys():
            setattr(self, key, kwargs[key])
