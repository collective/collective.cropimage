from Products.CMFCore.utils import getToolByName
from collective.cropimage.tests.base import IntegrationTestCase

import logging
import mock

OLD_IDS = [{
    'id': 'feed',
    'ratio_width': 17.0,
    'ratio_height': 15.0,
    'min_width': 170.0,
    'min_height': 150.0,
    'max_width': 170.0,
    'max_height': 150.0,
}]

IDS = {'feed': {
    'ratio_width': 17.0,
    'ratio_height': 15.0,
    'min_width': 170.0,
    'min_height': 150.0,
    'max_width': 170.0,
    'max_height': 150.0,
}}


class TestUpgrades(IntegrationTestCase):
    """Upgrades Test Case."""

    def setUp(self):
        self.portal = self.layer['portal']
        self.setup = getToolByName(self.portal, 'portal_setup')
        self.logger = logging.getLogger(__name__)

    def test__reinstall_profiles(self):
        from collective.cropimage.upgrades import reinstall_profiles
        from plone.registry.interfaces import IRegistry
        from zope.component import getUtility
        registry = getUtility(IRegistry)
        registry['collective.cropimage.ids'] = IDS
        reinstall_profiles(self.setup, self.logger)
        self.assertEqual(registry['collective.cropimage.ids'], IDS)

    @mock.patch('collective.cropimage.upgrades.reinstall_profiles')
    def test_upgarade_1_to_2__with_logger(self, reinstall_profiles):
        from collective.cropimage.upgrades import upgrade_1_to_2
        upgrade_1_to_2(self.setup, self.logger)
        reinstall_profiles.assert_called_with(self.setup, self.logger)

    @mock.patch('collective.cropimage.upgrades.logging')
    @mock.patch('collective.cropimage.upgrades.reinstall_profiles')
    def test_upgarade_1_to_2__without_logger(self, reinstall_profiles, logging):
        from collective.cropimage.upgrades import upgrade_1_to_2
        upgrade_1_to_2(self.setup)
        reinstall_profiles.assert_called_with(self.setup, logging.getLogger())

    def test_convert_old_ids_to_new_ids(self):
        from collective.cropimage.upgrades import convert_old_ids_to_new_ids
        self.assertEqual(convert_old_ids_to_new_ids(OLD_IDS), IDS)
