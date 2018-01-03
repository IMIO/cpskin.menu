# -*- coding: utf-8 -*-
from Acquisition import aq_chain
from cpskin.menu.browser.menu import invalidate_menu
from plone import api
from plone.uuid.interfaces import IUUID
from Products.CMFCore.WorkflowCore import WorkflowException
from zope.component.hooks import getSite


def content_has_id(content):
    try:
        content.getId()
    except AttributeError:
        return False
    else:
        return True


def object_is_wrapped(content):
    return len(aq_chain(content)) > 1


def content_modified(content, event):
    if not content_has_id(content):
        return
    if not object_is_wrapped(content):
        return
    try:
        state = api.content.get_state(content)
    except WorkflowException:
        return
    if state != 'published_and_shown':
        return
    portal_properties = api.portal.get_tool('portal_properties')
    navtree_properties = portal_properties.get('navtree_properties', None)
    if navtree_properties:
        metaTypesNotToList = list(navtree_properties.metaTypesNotToList)
        if getattr(content, 'portal_type', None) in metaTypesNotToList:
            return
    if IUUID(getSite(), None) is not None:
        invalidate_menu(content)
