from Products.CMFCore.utils import getToolByName
from plone.testing import z2
from plone.app.testing import PloneWithPackageLayer
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE
from plone.app.testing import PLONE_FIXTURE
from zope.configuration import xmlconfig

#import collective.clipboardupload

class ClipboarduploadtLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import collective.clipboardupload
        xmlconfig.file(
            'configure.zcml',
            collective.clipboardupload,
            context=configurationContext
        )

    def setUpPloneSite(self, portal):
        workflowTool = getToolByName(portal, 'portal_workflow')
        workflowTool.setDefaultChain('simple_publication_workflow')

COLLECTIVE_CLIPBOARDUPLOAD_FIXTURE = ClipboarduploadtLayer()
COLLECTIVE_CLIPBOARDUPLOAD_ROBOT_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_CLIPBOARDUPLOAD_FIXTURE, AUTOLOGIN_LIBRARY_FIXTURE, z2.ZSERVER),
    name="collective.clipboardupload:Robot")
