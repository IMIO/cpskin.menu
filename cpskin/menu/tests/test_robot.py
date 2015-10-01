# -*- coding: utf-8 -*-
from plone.testing import layered
from cpskin.menu.testing import CPSKIN_MENU_ROBOT_TESTING, CPSKIN_MENU_ROBOT_TESTING_LOAD_PAGE

import os
import robotsuite
import unittest


def test_suite():
    suite = unittest.TestSuite()
    current_dir = os.path.abspath(os.path.dirname(__file__))
    robot_dir = os.path.join(current_dir, 'robot')
    robot_files = [
        os.path.join('robot', doc) for doc in os.listdir(robot_dir) if doc.endswith('.robot')
    ]
    load_page_robot_test = "robot/test_js_menu_with_load_page.robot"
    lp_index = robot_files.index(load_page_robot_test)
    del robot_files[lp_index]

    for robot_file in robot_files:
        rts = robotsuite.RobotTestSuite(robot_file)
        suite.addTests([
            layered(
                rts,
                layer=CPSKIN_MENU_ROBOT_TESTING
            )
        ])

    # Use another test layer for load_page tests
    rts = robotsuite.RobotTestSuite(load_page_robot_test)
    suite.addTests([
        layered(
            rts,
            layer=CPSKIN_MENU_ROBOT_TESTING_LOAD_PAGE
        )
    ])
    return suite
