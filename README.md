collective.clipboardupload   
==========================


[![Build Status](https://travis-ci.org/quintagroup/collective.clipboardupload.png?branch=master)](https://travis-ci.org/quintagroup/collective.clipboardupload)


Introduction
------------

Quintagroup has developed a collective.clipboardupload tool that essentially allows you to copy images and past them directly  into TinyMCE visual editor.

Compatibility
-------------

* Plone 4.x

Installation
------------

In your buildout.cfg add the following::
    
 [buildout]
   ....
 
    eggs =
        ...
        collective.clipboardupload

Usage
-----

*Collective.clipboardupload* is a Python package, developed to simplify the  process of inserting images into visual editor without the need to upload the image.

 
After you have installed the product, activate it via Site Setup -> Add-ons section. Now you can copy any image from your computer or some web source and then click "Paste" on your visual editor or by key combination. Those pictures will be automatically uploaded to the folder that contains a page and stored as an image content type. Furthermore the path to the image itself upon saving in TinyMCE  is rendered as *resolveuid* link. 

Authors
-------

* Joe Schmoe, Original Author
* Bob Slob, contributed monkey patches
* Jane Main, wrote flibberty module
* Maksym Shalenyy


