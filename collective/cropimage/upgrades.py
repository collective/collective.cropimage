from Products.CMFCore.utils import getToolByName
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

import logging

PROFILE_ID = 'profile-collective.cropimage:default'


def reinstall_profiles(context, logger):
    registry = getUtility(IRegistry)
    ids = registry['collective.cropimage.ids']
    setup = getToolByName(context, 'portal_setup')
    logger.info('Reinstalling collective.cropimage.')
    setup.runAllImportStepsFromProfile(
        'profile-collective.cropimage:default',
        purge_old=False
    )
    logger.info('Reinstalled collective.cropimage.')
    logger.info('Setting collective.cropimage.ids')
    registry['collective.cropimage.ids'] = ids
    logger.info('Set collective.cropimage.ids')


def upgrade_1_to_2(context, logger=None):
    """Update JSregistry."""
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger(__name__)
    reinstall_profiles(context, logger)
