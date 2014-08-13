from Products.CMFCore.utils import getToolByName
from collective.cropimage.tests.base import IntegrationTestCase


class TestCase(IntegrationTestCase):
    """TestCase for Plone setup."""

    def setUp(self):
        self.portal = self.layer['portal']

    def test_is_collective_cropimage_installed(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.failUnless(installer.isProductInstalled('collective.cropimage'))

    # registry.xml
    def test_ids_registry(self):
        """Test if collective.cropimage.ids is properly registered."""
        from zope.component import getUtility
        from plone.registry.interfaces import IRegistry
        registry = getUtility(IRegistry)
        self.assertEqual(len(registry['collective.cropimage.ids']), 0)
        field = registry.records['collective.cropimage.ids'].field
        self.assertEqual(field.title, u'Identifications')
        self.assertEqual(field.description, u'ID for styling, etc.')
        from plone.registry.field import Dict
        isinstance(field.value_type, Dict)

    # controlpanel.xml
    def test_controlpanel(self):
        controlpanel = getToolByName(self.portal, 'portal_controlpanel')
        action = [
            action for action in controlpanel.listActions() if action.id == 'crop_image_registry'
        ][0]
        self.assertEqual(action.title, 'Crop Image Registry')
        self.assertEqual(action.appId, 'collective.cropimage')
        self.assertEqual(action.action.text, 'string:${portal_url}/@@crop-image-controlpanel')
        self.assertEqual(action.icon_expr.text, 'string:$portal_url/cut_icon.png')
        self.assertTrue(action.visible)
        self.assertEqual(action.permissions, ('Manage portal',))

    # actions.xml
    def test_crop_image(self):
        actions = getToolByName(self.portal, 'portal_actions')
        action = actions.object_buttons.crop_image
        self.assertEqual('Crop Image', action.getProperty('title'))
        self.assertEqual(
            'string:${globals_view/getCurrentObjectUrl}/@@crop-image',
            action.getProperty('url_expr')
        )
        self.assertEqual(
            'python: object.restrictedTraverse("has-image")()',
            action.getProperty('available_expr')
        )
        self.assertEqual(('Modify portal content',), action.getProperty('permissions'))
        self.assertEqual(True, action.getProperty('visible'))

    # jsregistry.xml
    def test_jsregistry(self):
        javascripts = getToolByName(self.portal, 'portal_javascripts')
        res = '++resource++collective.cropimage.javascripts/jquery.Jcrop.js'
        self.assertTrue(res in javascripts.getResourceIds())
        item = javascripts.getResource(res)
        self.assertEqual(item.getCompression(), 'none')

    # cssregistry.xml
    def test_cssregistry(self):
        css = getToolByName(self.portal, 'portal_css')
        res = '++resource++collective.cropimage.stylesheets/main.css'
        self.assertTrue(res in css.getResourceIds())

    def test_browserlayer(self):
        from collective.cropimage.browser.interfaces import ICollectiveCropimageLayer
        from plone.browserlayer import utils
        self.failUnless(ICollectiveCropimageLayer in utils.registered_layers())

    def test_metadata__version(self):
        setup = getToolByName(self.portal, 'portal_setup')
        self.assertEqual(
            setup.getVersionForProfile('profile-collective.cropimage:default'),
            u'3')

    def test_uninstall__package(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        installer.uninstallProducts(['collective.cropimage'])
        self.failIf(installer.isProductInstalled('collective.cropimage'))

    def test_uninstall__registry__collective_cropimage_ids(self):
        setup_tool = getToolByName(self.portal, 'portal_setup')
        setup_tool.runAllImportStepsFromProfile(
            'profile-collective.cropimage:uninstall'
        )
        from zope.component import getUtility
        from plone.registry.interfaces import IRegistry
        registry = getUtility(IRegistry)
        # collective.cropimage.banks should be uninstalled form registry.
        self.assertRaises(KeyError, lambda: registry['collective.cropimage.ids'])

    def test_uninstall__controlpanel(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        installer.uninstallProducts(['collective.cropimage'])
        controlpanel = getToolByName(self.portal, 'portal_controlpanel')
        ids = [action.id for action in controlpanel.listActions()]
        # crop_image_registry configlet should be uninstalled from controlpanel
        self.assertTrue('crop_image_registry' not in ids)

    def test_uninstall__actions(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        installer.uninstallProducts(['collective.cropimage'])
        # crop_image should be uninstalled from actions
        actions = getToolByName(self.portal, 'portal_actions')
        self.assertFalse(hasattr(actions.object_buttons, 'crop_image'))

    def test_uninstall__jsregistry(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        installer.uninstallProducts(['collective.cropimage'])
        # jsregisty.xml should be uninstalled.
        javascripts = getToolByName(self.portal, 'portal_javascripts')
        res = '++resource++collective.cropimage.javascripts/jquery.Jcrop.js'
        self.assertFalse(res in javascripts.getResourceIds())

    def test_uninstall__cssregistry(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        installer.uninstallProducts(['collective.cropimage'])
        # cssregistry.xml should be uninstalled.
        css = getToolByName(self.portal, 'portal_css')
        res = '++resource++collective.cropimage.stylesheets/main.css'
        self.assertFalse(res in css.getResourceIds())

    def test_uninstall__browserlayer(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        installer.uninstallProducts(['collective.cropimage'])
        from collective.cropimage.browser.interfaces import ICollectiveCropimageLayer
        from plone.browserlayer import utils
        self.failIf(ICollectiveCropimageLayer in utils.registered_layers())
