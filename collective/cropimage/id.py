from collective.cropimage import _
from zope.interface import Interface
from zope.interface import implements
from zope.schema import Float
from zope.schema import TextLine


class IID(Interface):

    id = TextLine(
        title=_(u'ID'),
    )

    ratio_width = Float(
        title=_(u'Ratio Width'),
        description=_(u'Keep this field 0.0 if you do not need to set width/height ratio.'),
        default=0.0,
    )

    ratio_height = Float(
        title=_(u'Ratio Height'),
        description=_(u'Keep this field 0.0 if you do not need to set width/height ratio.'),
        default=0.0,
    )

    min_width = Float(
        title=_(u'Minimum Width'),
        description=_(u'Keep this field 0.0 if you do not need to set minimum width.'),
        default=0.0,
    )

    min_height = Float(
        title=_(u'Minimum Height'),
        description=_(u'Keep this field 0.0 if you do not need to set minimum height.'),
        default=0.0,
    )

    max_width = Float(
        title=_(u'Maximum Width'),
        description=_(u'Keep this field 0.0 if you do not need to set maximum width.'),
        default=0.0,
    )

    max_height = Float(
        title=_(u'Maximum Height'),
        description=_(u'Keep this field 0.0 if you do not need to set maximum height.'),
        default=0.0,
    )


class ID(object):

    implements(IID)

    def __init__(self, id, **kwargs):
        self.id = id
        for key in kwargs.keys():
            setattr(self, key, kwargs[key])

    def __repr__(self):
        return '<ID with id={id!r}>'.format(
            id=self.id,
        )
