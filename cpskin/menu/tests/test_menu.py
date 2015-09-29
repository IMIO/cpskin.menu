# -*- coding: utf-8 -*-
import unittest2 as unittest
from zope.component import getUtility, queryUtility
from zope.ramcache.interfaces.ram import IRAMCache
from plone.uuid.interfaces import IUUID
from plone import api
from cpskin.menu.testing import CPSKIN_MENU_INTEGRATION_TESTING
from cpskin.menu.browser.menu import (CpskinMenuViewlet, cache_key,
                                      invalidate_menu)
from plone.memoize.interfaces import ICacheChooser
from cpskin.menu.browser.menu import cache_key_desktop


def cache_exist(viewlet):
    # Si j utilise cache exist ici c'est bon
    adapter = queryUtility(ICacheChooser)('cpskin.menu.browser.menu.superfish_portal_tabs')
    key = cache_key_desktop(None, viewlet)
    return adapter.get(key) and True or False


def get_cache_miss(viewlet):
    storage = getUtility(IRAMCache)._getStorage()
    return storage._misses.get('cpskin.menu.browser.menu.superfish_portal_tabs', 0)


def empty_cache():
    adapter = queryUtility(ICacheChooser)('cpskin.menu.browser.menu.superfish_portal_tabs')
    adapter.client.invalidateAll()


class TestMenu(unittest.TestCase):

    layer = CPSKIN_MENU_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        empty_cache()

    def tearDown(self):
        empty_cache()

    def test_menu_portal_tabs(self):
        viewlet = CpskinMenuViewlet(self.portal, self.request, None, None)
        viewlet.update()
        self.assertTrue(viewlet.is_homepage)
        menus = viewlet.superfish_portal_tabs()
        self.assertEqual(len(menus), 2)

    def test_menu_cache_key_on_root(self):
        viewlet = CpskinMenuViewlet(self.portal, self.request, None, None)
        viewlet.update()
        key = cache_key(viewlet.superfish_portal_tabs, viewlet)
        self.assertTrue(key.startswith('menu.'))
        self.assertTrue(key.endswith(IUUID(self.portal)))

    def test_menu_cache_key_on_communes(self):
        communes = getattr(self.portal, 'commune')
        viewlet = CpskinMenuViewlet(communes, self.request, None, None)
        viewlet.update()
        key = cache_key(viewlet.superfish_portal_tabs, viewlet)
        self.assertTrue(key.startswith('menu.'))
        self.assertTrue(key.endswith(IUUID(self.portal)))

    def test_menu_cache_key_on_communes_subitem(self):
        item = self.portal.restrictedTraverse('commune/services_communaux')
        communes = getattr(self.portal, 'commune')
        viewlet = CpskinMenuViewlet(item, self.request, None, None)
        viewlet.update()
        key = cache_key(viewlet.superfish_portal_tabs, viewlet)
        self.assertTrue(key.startswith('menu.'))
        self.assertTrue(key.endswith(IUUID(self.portal)))

    def test_menu_cache_usage_test_fail(self):
        item = self.portal.restrictedTraverse('commune/services_communaux')
        viewlet = CpskinMenuViewlet(item, self.request, None, None)
        viewlet.update()
        self.assertEqual(cache_exist(viewlet), False)
        viewlet.superfish_portal_tabs()
        self.assertEqual(cache_exist(viewlet), True)

    def test_menu_cache_usage_different_context(self):
        item = self.portal.restrictedTraverse('commune/services_communaux')
        viewlet1 = CpskinMenuViewlet(item, self.request, None, None)
        viewlet1.update()
        self.assertEqual(cache_exist(viewlet1), False)
        viewlet1.superfish_portal_tabs()
        self.assertEqual(cache_exist(viewlet1), True)

        item = self.portal.restrictedTraverse('commune')
        viewlet2 = CpskinMenuViewlet(item, self.request, None, None)
        viewlet2.update()
        self.assertEqual(cache_exist(viewlet2), False)
        viewlet2.superfish_portal_tabs()
        self.assertEqual(cache_exist(viewlet2), True)

        item = self.portal.restrictedTraverse('loisirs')
        viewlet3 = CpskinMenuViewlet(item, self.request, None, None)
        viewlet3.update()
        self.assertEqual(cache_exist(viewlet3), False)
        viewlet3.superfish_portal_tabs()
        self.assertEqual(cache_exist(viewlet3), True)

    def test_menu_cache_invalidation(self):
        item = self.portal.restrictedTraverse('commune/services_communaux')
        viewlet = CpskinMenuViewlet(item, self.request, None, None)
        viewlet.update()
        self.assertEqual(cache_exist(viewlet), False)
        viewlet.superfish_portal_tabs()
        self.assertEqual(cache_exist(viewlet), True)
        # XXX l'invalidation ne se fait pas. je ne comprends pas pourquoi.
        # CF jfroche, peut etre un probleme avec le notify(event) ?
#         api.content.move(item, self.portal)
        # Le move() lance bien invalidate_menu, mais celui ci ne fonctionne pas
        invalidate_menu(item)
        self.assertEqual(cache_exist(viewlet), False)

    def test_menu_cache_invalidate_another_menu(self):
        item = self.portal.restrictedTraverse('commune/services_communaux')
        commune = self.portal.restrictedTraverse('commune/services_communaux')
        viewlet = CpskinMenuViewlet(item, self.request, None, None)
        viewlet.update()

#         self.assertEqual(cache_exist(viewlet), 0)
        viewlet.superfish_portal_tabs()
        self.assertEqual(cache_exist(viewlet), 1)

        loisirs = self.portal.restrictedTraverse('loisirs')
        invalidate_menu(loisirs)
        viewlet.superfish_portal_tabs()
        self.assertEqual(cache_exist(viewlet), 2)

        invalidate_menu(commune)
        viewlet.superfish_portal_tabs()
        self.assertEqual(cache_exist(viewlet), 3)

    def test_objet_modification_invalidates_menu(self):
        item = self.portal.restrictedTraverse('commune/services_communaux')
        viewlet = CpskinMenuViewlet(item, self.request, None, None)
        viewlet.update()
        self.assertEqual(cache_exist(), 0)
        viewlet.superfish_portal_tabs()
        self.assertEqual(cache_exist(), 1)
        viewlet.superfish_portal_tabs()
        self.assertEqual(cache_exist(), 1)
        item.setTitle('Test Cache Invalidation')
        item.processForm()
        viewlet.superfish_portal_tabs()
        self.assertEqual(cache_exist(), 2)

    def test_object_creation_invalidates_menu(self):
        item = self.portal.restrictedTraverse('commune/services_communaux')
        viewlet = CpskinMenuViewlet(item, self.request, None, None)
        viewlet.update()
        self.assertEqual(cache_exist(), 0)
        viewlet.superfish_portal_tabs()
        self.assertEqual(cache_exist(), 1)
        viewlet.superfish_portal_tabs()
        self.assertEqual(cache_exist(), 1)
        api.content.create(item, 'Folder', 'foo')
        viewlet.superfish_portal_tabs()
        self.assertEqual(cache_exist(), 2)

    def test_object_publication_invalidates_menu(self):
        item = self.portal.restrictedTraverse('commune/services_communaux')
        viewlet = CpskinMenuViewlet(item, self.request, None, None)
        viewlet.update()
        self.assertEqual(cache_exist(), 0)
        viewlet.superfish_portal_tabs()
        self.assertEqual(cache_exist(), 1)
        viewlet.superfish_portal_tabs()
        self.assertEqual(cache_exist(), 1)
        api.content.transition(item, 'publish')
        viewlet.superfish_portal_tabs()
        self.assertEqual(cache_exist(), 2)

    def test_object_removed_invalidates_menu(self):
        item = self.portal.restrictedTraverse('commune/services_communaux')
        commune = self.portal.restrictedTraverse('commune')
        viewlet = CpskinMenuViewlet(commune, self.request, None, None)
        viewlet.update()
        self.assertEqual(cache_exist(), 0)
        viewlet.superfish_portal_tabs()
        self.assertEqual(cache_exist(), 1)
        viewlet.superfish_portal_tabs()
        self.assertEqual(cache_exist(), 1)
        api.content.delete(item)
        viewlet.update()
        viewlet.superfish_portal_tabs()
        self.assertEqual(cache_exist(), 2)

    def test_object_moved_invalidates_menus(self):
        item = self.portal.restrictedTraverse('commune/services_communaux')
        commune = self.portal.restrictedTraverse('commune')
        loisirs = self.portal.restrictedTraverse('loisirs')
        viewlet = CpskinMenuViewlet(commune, self.request, None, None)
        viewlet.update()
        self.assertEqual(cache_exist(), 0)
        viewlet.superfish_portal_tabs()
        self.assertEqual(cache_exist(), 1)
        viewlet.superfish_portal_tabs()
        self.assertEqual(cache_exist(), 1)
        viewlet_loisirs = CpskinMenuViewlet(loisirs, self.request, None, None)
        viewlet_loisirs.update()
        self.assertEqual(cache_exist(), 1)
        viewlet_loisirs.superfish_portal_tabs()
        self.assertEqual(cache_exist(), 1)
        viewlet_loisirs.superfish_portal_tabs()
        self.assertEqual(cache_exist(), 1)
        api.content.move(item, loisirs)
        viewlet.update()
        viewlet_loisirs.update()
        self.assertEqual(cache_exist(), 1)
        viewlet_loisirs.superfish_portal_tabs()
        self.assertEqual(cache_exist(), 2)
        viewlet.superfish_portal_tabs()
        self.assertEqual(cache_exist(), 2)

    def test_object_rename_invalidates_menu(self):
        item = self.portal.restrictedTraverse('commune/services_communaux')
        commune = self.portal.restrictedTraverse('commune')
        viewlet = CpskinMenuViewlet(commune, self.request, None, None)
        viewlet.update()
        self.assertEqual(cache_exist(), 0)
        viewlet.superfish_portal_tabs()
        self.assertEqual(cache_exist(), 1)
        viewlet.superfish_portal_tabs()
        self.assertEqual(cache_exist(), 1)
        api.content.rename(item, new_id='sc')
        viewlet.update()
        viewlet.superfish_portal_tabs()
        self.assertEqual(cache_exist(), 2)
