# -*- coding: utf-8 -*-
"""
This module is responsible for searching image tags that contain image data
inside them and saving it like an Image object. Also each image tag that
contains image data will be replaced with the link to the created Images object
    >>> DateTime.strftime = lambda x,y: 'UniqueId'
    >>> class Image():
    ...     def __init__(self, uid):
    ...         self.uid = uid
    ...     def UID(self):
    ...         return self.uid
    ...     def setImage(self, data):
    ...         print data
    >>> class Context(dict):
    ...     id_count = 0
    ...     text = ""
    ...     def generateUniqueId(self):
    ...         return "UniqueId"
    ...     def invokeFactory(self, type_name='Image', id='uid'):
    ...         self.id_count += 1
    ...         uid = "%s%s"%(id, self.id_count)
    ...         self[uid] = Image(uid)
    ...         return uid
    ...     def getRawText(self):
    ...         return self.text
    ...     def setText(self, data):
    ...         print data
    ...     def getParentNode(self):
    ...         return self
    >>> transaction.commit = lambda : None
    >>> context = Context()

    Image with link:
    >>> context.text = '<img src="http://abc.com/image.png"/>'
    >>> extract_image_data_from_body(context, None)
    <img src="http://abc.com/image.png"/>

    Image without src:
    >>> context.text = '<img alt="http://abc.com/image.png"/>'
    >>> extract_image_data_from_body(context, None)
    <img alt="http://abc.com/image.png"/>

    Image with data:
    >>> context.text = '<img  class="class" src="data:image/jpeg;base64,VGhp'\
                       'cyBpcyByYXcgaW1hZ2UgZGF0YQ=="  alt="alt" />'
    >>> extract_image_data_from_body(context, None)
    This is raw image data
    <img alt="alt" class="class" src="resolveuid/Clipboard_image_UniqueId1"/>

    Single quotes notation:
    >>> context.text = "<img  class='class' src='data:image/jpeg;base64,VGhp"\
                       "cyBpcyByYXcgaW1hZ2UgZGF0YQ=='  alt='alt' />"
    >>> extract_image_data_from_body(context, None)
    This is raw image data
    <img alt="alt" class="class" src="resolveuid/Clipboard_image_UniqueId2"/>

    No quotes notation:
    >>> context.text = "<img  class=class src=data:image/jpeg;base64,VGhpcy"\
                       "BpcyByYXcgaW1hZ2UgZGF0YQ==  />"
    >>> extract_image_data_from_body(context, None)
    This is raw image data
    <img class="class" src="resolveuid/Clipboard_image_UniqueId3"/>

    Image with tricky attrs:
    >>> context.text = " <img alt=' /> ' src='data:image/jpeg;base64,VGhpcyB"\
                       "pcyByYXcgaW1hZ2UgZGF0YQ=='  />"
    >>> extract_image_data_from_body(context, None)
    This is raw image data
    <img alt=" /&gt; " src="resolveuid/Clipboard_image_UniqueId4"/>

    Image inside other tags:
    >>> context.text = " <div><img src='data:image/jpeg;base64,VGhpcyBpcyB"\
                       "yYXcgaW1hZ2UgZGF0YQ=='  /></div><div><p><img src='"\
                       "data:image/jpeg;base64,VGhpcyBpcyByYXcgaW1hZ2UgZGF0"\
                       "YQ=='  /><img src='data:image/jpeg;base64,VGhpcyBpc"\
                       "yByYXcgaW1hZ2UgZGF0YQ=='  /></p></div>"\
                       "&lt;img class='class' src='data:image/tiff;base64,"\
                       "VGhpcyBpcyByYXcgaW1hZ2UgZGF0YQ==' />"
    >>> extract_image_data_from_body(context, None)
    This is raw image data
    This is raw image data
    This is raw image data
    <div><img src="resolveuid/Clipboard_image_UniqueId5"/></div><div><p><img src="resolveuid/Clipboard_image_UniqueId6"/><img src="resolveuid/Clipboard_image_UniqueId7"/></p></div>&lt;img class='class' src='data:image/tiff;base64,VGhpcyBpcyByYXcgaW1hZ2UgZGF0YQ==' /&gt;

"""
import base64
import re
import transaction
import operator
from itertools import ifilter
from DateTime import DateTime
from bs4 import BeautifulSoup
from zope.event import notify

RE_IMAGE_DATA = re.compile(r'data:image/\w{2,5};base64,(.+)')


def generate_image_object(context, data):
    """
    Creates Image object on given context and returns its resolved UID

    """
    uid = 'Clipboard_image_%s' % DateTime().strftime("%Y-%m-%d-%H%M.%f")
    name = context.invokeFactory(type_name='Image', id=uid)
    obj = context[name]
    obj.setImage(base64.b64decode(data))
    from Products.Archetypes.event import ObjectInitializedEvent
    notify(ObjectInitializedEvent(obj))
    transaction.commit()
    return obj.UID()


def extract_image_data_from_body(context, event):
    """
    EditedEvent event handler that creates Image objects from images data
    inside Document text and replaces that data with
    links to the created Images objects.
    """
    text = context.getRawText()
    soup = BeautifulSoup(text)
    # we need collect both BS image objects and images data returned by RE
    images = ((i, RE_IMAGE_DATA.search(i.get('src', ''))) \
               for i in soup.findAll('img'))
    for image, data in ifilter(operator.itemgetter(1), images):
        resolved_uid = generate_image_object(context, data.group(1))
        image['src'] = 'resolveuid/%s' % resolved_uid
    context.setText(str(soup.html.body)[6:-7])  # just body without <body> tags
