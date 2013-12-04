collective.clipboardupload   
==========================


.. image:: https://travis-ci.org/quintagroup/collective.clipboardupload.png
       :target: https://travis-ci.org/quintagroup/collective.clipboardupload

Introduction
------------

Quintagroup has developed a collective.clipboardupload tool that essentially allows you to copy images and past them directly  into TinyMCE visual editor.

.. image:: http://quintagroup.com/services/plone-development/products/collective.clipboardupload/clipboardupload.png
       :target: http://www.youtube.com/watch?v=V3-z4M8M74g

Compatibility
-------------

* Plone 4.0
* Plone 4.1
* Plone 4.3

Know browser issues: Ctrl+V does not always work for me in Firefox (MacOSX 10.8), so menu Edit -> Paste to the rescue. 
Safari works same way. Chrome fails 100%. Works in Windows.

Installation
------------

In your buildout.cfg add the following::
    
 [buildout]
   ....
 
    eggs =
        ...
        collective.clipboardupload

It will engage automatically after buildout is rebuilt and instance started.

Usage
-----

*Collective.clipboardupload*, developed to simplify the process of inserting images into TinyMCE without the need to upload the image, with simple Copy/Paste operation.

Open an image in, for example, Preview.app select an area and copy it to clipboard. Switch to Plone TinyMCE and Paste. Use your browser menu Edit -> Paste in case Ctrl+V fails.

The picture will be automatically uploaded to the edited page containing folder and stored as an Plone Image. Upon save the Image path is converted to *resolveuid* link.

Authors
-------

* Maksym Shalenyi


