# -*- coding: utf-8 -*-
from plone.app.blob.interfaces import IBlobbable
from plone.app.blob.utils import guessMimetype
from xmlrpclib import Binary
from zope.component import adapts
from zope.interface import implementer


@implementer(IBlobbable)
class BlobbableBinary(object):
    """ adapter for xmlrpclib Binary instance to work with blobs """
    adapts(Binary)

    def __init__(self, context):
        self.context = context

    def feed(self, blob):
        """ see interface ... """
        blobfile = blob.open('w')
        blobfile.writelines(self.context.data)
        blobfile.close()

    def filename(self):
        """ see interface ... """
        return getattr(self.context, 'filename', None)

    def mimetype(self):
        """ see interface ... """
        return guessMimetype(self.context.data, self.filename())
