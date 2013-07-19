# -*- coding: utf-8 -*-
import unittest
import doctest
from collective.clipboardupload import imageupload


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests(doctest.DocTestSuite(imageupload))
    return suite