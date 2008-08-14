from AccessControl import ClassSecurityInfo
from ComputedAttribute import ComputedAttribute
from Products.CMFCore.permissions import View, ModifyPortalContent
from Products.Archetypes.Field import ImageField
from Products.ATContentTypes.lib.imagetransform import ATCTImageTransform

from plone.app.imaging.interfaces import IImageScaleHandler


class ImageFieldMixin(ImageField):
    """ mixin class for methods needed for image field """

    security  = ClassSecurityInfo()

    security.declareProtected(View, 'getSize')
    def getSize(self, instance, scale=None):
        """ get size of scale or original """
        handler = IImageScaleHandler(self, None)
        if handler is not None:
            image = handler.getScale(instance, scale)
            if image is not None:
                return image.width, image.height
        return 0, 0

    security.declareProtected(View, 'getScale')
    def getScale(self, instance, scale=None, **kwargs):
        """ get scale by name or original """
        if scale is None:
            return self.get(instance, **kwargs)
        handler = IImageScaleHandler(self, None)
        if handler is not None:
            return handler.getScale(instance, scale)
        return None


class ImageMixin(ATCTImageTransform):
    """ mixin class for methods needed for image content """

    security = ClassSecurityInfo()

    # accessor and mutator methods

    security.declareProtected(View, 'getImage')
    def getImage(self, **kwargs):
        """ archetypes.schemaextender (wisely) doesn't mess with classes,
            so we have to provide our own accessor """
        return self.getBlobWrapper()

    security.declareProtected(ModifyPortalContent, 'setImage')
    def setImage(self, value, **kwargs):
        """ set image contents and possibly also the id """
        mutator = self.getField('image').getMutator(self)
        mutator(value, **kwargs)

    # methods from ATImage

    security.declareProtected(View, 'tag')
    def tag(self, **kwargs):
        """ generate image tag using the api of the ImageField """
        return self.getField('image').tag(self, **kwargs)

    security.declareProtected(View, 'getSize')
    def getSize(self, scale=None):
        field = self.getField('image')
        return field.getSize(self, scale=scale)

    security.declareProtected(View, 'getWidth')
    def getWidth(self, scale=None):
        return self.getSize(scale)[0]

    security.declareProtected(View, 'getHeight')
    def getHeight(self, scale=None):
        return self.getSize(scale)[1]

    width = ComputedAttribute(getWidth, 1)
    height = ComputedAttribute(getHeight, 1)

