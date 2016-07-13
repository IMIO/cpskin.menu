# -*- coding: utf-8 -*-
from plone.testing import layered
from plone.app.testing import ROBOT_TEST_LEVEL
from cpskin.menu.testing_robot import CPSKIN_LOAD_PAGE_ROBOT

import os
import robotsuite
import unittest


def test_suite():
    suite = unittest.TestSuite()
    load_page_robot_test = "robot/test_load_page.robot"
    rts = robotsuite.RobotTestSuite(load_page_robot_test)
    rts.level = ROBOT_TEST_LEVEL
    suite.addTests([
        layered(
            rts,
            layer=CPSKIN_LOAD_PAGE_ROBOT
        )
    ])
    return suite
