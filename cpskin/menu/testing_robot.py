# -*- coding: utf-8 -*-

from zope.component import queryUtility
from zope.interface import alsoProvides
from Products.CMFCore.utils import getToolByName

from plone import api
from plone.testing import z2
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.app.testing import PloneWithPackageLayer
from plone.app.testing import applyProfile
from plone.app.testing import (login,
                               TEST_USER_NAME,
                               setRoles,
                               TEST_USER_ID)
from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE
from plone.registry.interfaces import IRegistry
from plone.memoize.interfaces import ICacheChooser

from affinitic.caching.memcached import MemcacheAdapter
from affinitic.caching.testing import NO_MEMCACHED

from cpskin.menu.interfaces import IFourthLevelNavigation, IDirectAccess

import cpskin.menu
from cpskin.menu.testing import memcached_launched


def setupContent(context):
    if context.readDataFile('cpskin.menu.content.txt') is None:
        return
    portal = context.getSite()
    for id in ['Members', 'visuel.png', 'cpskinlogo.png', 'footer-static',
            'banner.jpg']:
        exclude = portal[id]
        exclude.setExcludeFromNav(True)
        exclude.reindexObject()
    subfolder1 = setupSubContent(portal, 1)
    subfolder2 = setupSubContent(subfolder1, 2)
    subfolder3 = setupSubContent(subfolder2, 3)
    alsoProvides(subfolder3, IFourthLevelNavigation)
    subfolder4 = setupSubContent(subfolder3, 4)


def setupSubContent(container, index):
    suffix = str(index)
    id = 'subfolder-' + suffix
    sub = api.content.create(
        type='Folder',
        title=id,
        id=id,
        container=container)
    id = 'other-' + suffix
    other = api.content.create(
        type='Folder',
        title=id,
        id=id,
        container=container)
    suffix = str(index+1)
    id = 'empty-in-' + suffix
    api.content.create(
        type='Folder',
        title=id,
        id=id,
        container=sub)
    id = 'direct-link-in-' + suffix
    api.content.create(
        type='Document',
        title=id,
        id=id,
        container=sub)
    id = 'direct-link-in-' + suffix
    api.content.create(
        type='Document',
        title=id,
        id=id,
        container=other)
    id = 'default-view-subcontent-in-'+ suffix
    subsub = api.content.create(
        type='Folder',
        title=id,
        id=id,
        container=sub)
    id = 'default-view'
    api.content.create(
        type='Document',
        title=id,
        id=id,
        container=subsub)
    subsub.setDefaultPage(id)
    id = 'content-1'
    api.content.create(
        type='Document',
        title=id,
        id=id,
        container=subsub)
    id = 'content-2'
    api.content.create(
        type='Document',
        title=id,
        id=id,
        container=subsub)
    id = 'default-view-empty-in-'+ suffix
    subsub = api.content.create(
        type='Folder',
        title=id,
        id=id,
        container=sub)
    id = 'default-view'
    api.content.create(
        type='Document',
        title=id,
        id=id,
        container=subsub)
    subsub.setDefaultPage(id)
    return sub


CPSKIN_NO_PERSISTENCE_FIXTURE = PloneWithPackageLayer(
    name="CPSKIN_MENU_FIXTURE",
    zcml_filename="testing.zcml",
    zcml_package=cpskin.menu,
    gs_profile_id="cpskin.menu:testing_no_persistence")

CPSKIN_NO_PERSISTENCE_ROBOT = FunctionalTesting(
    bases=(CPSKIN_NO_PERSISTENCE_FIXTURE, AUTOLOGIN_LIBRARY_FIXTURE,
           z2.ZSERVER_FIXTURE),
    name="cpskin.menu:Robot")


CPSKIN_PERSISTENCE_FIXTURE = PloneWithPackageLayer(
    name="CPSKIN_MENU_FIXTURE",
    zcml_filename="testing.zcml",
    zcml_package=cpskin.menu,
    gs_profile_id="cpskin.menu:testing_persistence")

CPSKIN_PERSISTENCE_ROBOT = FunctionalTesting(
    bases=(CPSKIN_PERSISTENCE_FIXTURE, AUTOLOGIN_LIBRARY_FIXTURE,
           z2.ZSERVER_FIXTURE),
    name="cpskin.menu:Robot")


CPSKIN_LOAD_PAGE_FIXTURE = PloneWithPackageLayer(
    name="CPSKIN_MENU_FIXTURE",
    zcml_filename="testing.zcml",
    zcml_package=cpskin.menu,
    gs_profile_id="cpskin.menu:testing_load_page")

CPSKIN_LOAD_PAGE_ROBOT = FunctionalTesting(
    bases=(CPSKIN_LOAD_PAGE_FIXTURE, AUTOLOGIN_LIBRARY_FIXTURE,
           z2.ZSERVER_FIXTURE),
    name="cpskin.menu:Robot")
