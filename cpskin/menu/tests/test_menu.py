# -*- coding: utf-8 -*-
import unittest2 as unittest
from zope.component import queryUtility
from plone.uuid.interfaces import IUUID
from plone import api
from cpskin.menu.testing import CPSKIN_MENU_INTEGRATION_TESTING
from cpskin.menu.browser.menu import (CpskinMenuViewlet,
                                      invalidate_menu)
from plone.memoize.interfaces import ICacheChooser
from cpskin.menu.browser.menu import cache_key_desktop


def cache_exist(viewlet):
    # Si j utilise cache exist ici c'est bon
    adapter = queryUtility(ICacheChooser)('cpskin.menu.browser.menu.superfish_portal_tabs')
    key = cache_key_desktop(None, viewlet)
    return adapter.get(key) and True or False


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
        self.assertEqual(len(menus), 4754)

    def test_menu_cache_key_on_root(self):
        viewlet = CpskinMenuViewlet(self.portal, self.request, None, None)
        viewlet.update()
        key = cache_key_desktop(viewlet.superfish_portal_tabs, viewlet)
        self.assertTrue(key.startswith('menu-'))
        self.assertTrue(key.endswith(IUUID(viewlet._get_real_context())))

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
        self.assertEqual(cache_exist(viewlet2), True)
        viewlet2.superfish_portal_tabs()
        self.assertEqual(cache_exist(viewlet2), True)

        item = self.portal.restrictedTraverse('loisirs')
        viewlet3 = CpskinMenuViewlet(item, self.request, None, None)
        viewlet3.update()
        self.assertEqual(cache_exist(viewlet3), True)
        viewlet3.superfish_portal_tabs()
        self.assertEqual(cache_exist(viewlet3), True)

    def test_menu_cache_invalidation(self):
        item = self.portal.restrictedTraverse('commune/services_communaux')
        viewlet = CpskinMenuViewlet(item, self.request, None, None)
        viewlet.update()
        self.assertEqual(cache_exist(viewlet), False)
        viewlet.superfish_portal_tabs()
        self.assertEqual(cache_exist(viewlet), True)
        invalidate_menu(item)
        self.assertEqual(cache_exist(viewlet), False)

    def test_menu_cache_invalidate_another_menu(self):
        item = self.portal.restrictedTraverse('commune/services_communaux')
        commune = self.portal.restrictedTraverse('commune/services_communaux')
        viewlet = CpskinMenuViewlet(item, self.request, None, None)
        viewlet.update()

        self.assertEqual(cache_exist(viewlet), False)
        viewlet.superfish_portal_tabs()
        self.assertEqual(cache_exist(viewlet), True)

        loisirs = self.portal.restrictedTraverse('loisirs')
        invalidate_menu(loisirs)
        viewlet.superfish_portal_tabs()
        self.assertEqual(cache_exist(viewlet), True)

        viewlet.superfish_portal_tabs()
        invalidate_menu(commune)
        self.assertEqual(cache_exist(viewlet), False)

    def test_objet_modification_invalidates_menu(self):
        item = self.portal.restrictedTraverse('commune/services_communaux')
        viewlet = CpskinMenuViewlet(item, self.request, None, None)
        viewlet.update()

        self.assertEqual(cache_exist(viewlet), False)
        viewlet.superfish_portal_tabs()
        self.assertEqual(cache_exist(viewlet), True)
        viewlet.superfish_portal_tabs()
        self.assertEqual(cache_exist(viewlet), True)
        item.setTitle('Test Cache Invalidation')
        item.processForm()
        self.assertEqual(cache_exist(viewlet), False)
        viewlet.superfish_portal_tabs()
        self.assertEqual(cache_exist(viewlet), True)

    def test_object_creation_invalidates_menu(self):
        item = self.portal.restrictedTraverse('commune/services_communaux')
        viewlet = CpskinMenuViewlet(item, self.request, None, None)
        viewlet.update()
        self.assertEqual(cache_exist(viewlet), False)
        viewlet.superfish_portal_tabs()
        self.assertEqual(cache_exist(viewlet), True)
        api.content.create(item, 'Folder', 'foo')
        self.assertEqual(cache_exist(viewlet), False)

    def test_object_publication_invalidates_menu(self):
        item = self.portal.restrictedTraverse('commune/services_communaux')
        viewlet = CpskinMenuViewlet(item, self.request, None, None)
        viewlet.update()
        self.assertEqual(cache_exist(viewlet), False)
        viewlet.superfish_portal_tabs()
        self.assertEqual(cache_exist(viewlet), True)
        api.content.transition(item, 'publish')
        self.assertEqual(cache_exist(viewlet), False)
        viewlet.superfish_portal_tabs()
        self.assertEqual(cache_exist(viewlet), True)

    def test_object_removed_invalidates_menu(self):
        item = self.portal.restrictedTraverse('commune/services_communaux')
        commune = self.portal.restrictedTraverse('commune')
        viewlet = CpskinMenuViewlet(commune, self.request, None, None)
        viewlet.update()
        self.assertEqual(cache_exist(viewlet), False)
        viewlet.superfish_portal_tabs()
        self.assertEqual(cache_exist(viewlet), True)
        api.content.delete(item)
        self.assertEqual(cache_exist(viewlet), False)
        viewlet.update()
        self.assertEqual(cache_exist(viewlet), False)
        viewlet.superfish_portal_tabs()
        self.assertEqual(cache_exist(viewlet), True)

    def test_object_moved_invalidates_menus(self):
        item = self.portal.restrictedTraverse('commune/services_communaux')
        commune = self.portal.restrictedTraverse('commune')
        loisirs = self.portal.restrictedTraverse('loisirs')
        viewlet = CpskinMenuViewlet(commune, self.request, None, None)
        viewlet.update()
        self.assertEqual(cache_exist(viewlet), False)
        viewlet.superfish_portal_tabs()
        self.assertEqual(cache_exist(viewlet), True)
        viewlet_loisirs = CpskinMenuViewlet(loisirs, self.request, None, None)
        viewlet_loisirs.update()
        self.assertEqual(cache_exist(viewlet), True)
        self.assertEqual(cache_exist(viewlet_loisirs), True)
        api.content.move(item, loisirs)
        self.assertEqual(cache_exist(viewlet), False)
        self.assertEqual(cache_exist(viewlet_loisirs), False)
        viewlet.update()
        viewlet_loisirs.update()
        self.assertEqual(cache_exist(viewlet), False)
        self.assertEqual(cache_exist(viewlet_loisirs), False)
        viewlet_loisirs.superfish_portal_tabs()
        self.assertEqual(cache_exist(viewlet), True)
        self.assertEqual(cache_exist(viewlet_loisirs), True)

    def test_object_rename_invalidates_menu(self):
        item = self.portal.restrictedTraverse('commune/services_communaux')
        commune = self.portal.restrictedTraverse('commune')
        viewlet = CpskinMenuViewlet(commune, self.request, None, None)
        viewlet.update()
        self.assertEqual(cache_exist(viewlet), False)
        viewlet.superfish_portal_tabs()
        self.assertEqual(cache_exist(viewlet), True)
        viewlet.superfish_portal_tabs()
        self.assertEqual(cache_exist(viewlet), True)
        api.content.rename(item, new_id='sc')
        viewlet.update()
        self.assertEqual(cache_exist(viewlet), False)
        viewlet.superfish_portal_tabs()
        self.assertEqual(cache_exist(viewlet), True)
