# ============================================================================
# ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s cpskin.menu -t test_mobile.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path cpskin cpskin.menu.testing.CPSKIN_MENU_ROBOT_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot cpskin/menu/tests/robot/test_mobile.robot [-i current]
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings ***

Resource  plone/app/robotframework/keywords.robot

Test Setup  Run keywords  Open test browser
Test Teardown  Close all browsers


*** Variables ***
${FF_PROFILE_DIR}  ${CURDIR}/firefoxmobileprofile


*** Test cases ***

Test desktop menu not visible
    Element Should Not Be Visible  css=ul#portal-globalnav li#portaltab-commune

Test menu mobile
    Element should not be visible  css=ul.submenu-level-1
    Click Element       id=mobnav-btn
    Location Should Be  ${PLONE_URL}
    Wait until element is visible  css=ul.submenu-level-1
    Wait until element is not visible  css=ul.submenu-level-2
    Click Loisirs in menu
    Location Should Be  ${PLONE_URL}
    Wait until element is visible  css=ul.submenu-level-2
    Wait until element is not visible  css=ul.submenu-level-3
    Click Element       css=ul.submenu-level-2 li:nth-child(2)
    Location Should Be  ${PLONE_URL}
    Wait until element is visible  css=ul.submenu-level-3
    Wait until element is not visible  css=ul.submenu-level-4
    Click Element       css=ul.submenu-level-3 li:nth-child(2)
    Location Should Be  ${PLONE_URL}
    Wait until element is visible  css=ul.submenu-level-4
    Click Element       css=ul.submenu-level-4 li:nth-child(1)
    Location Should Be  ${PLONE_URL}/loisirs/art_et_culture/artistes/tata

Test loading with 3 levels
    [tags]  current
    Click Element       id=mobnav-btn
    Click Loisirs in menu
    Location Should Be  ${PLONE_URL}
    Click Element       css=ul.submenu-level-2 li:nth-child(2)
    Location Should Be  ${PLONE_URL}
    Click Element       css=ul.submenu-level-3 li:nth-child(1)
    Location Should Be  ${PLONE_URL}/loisirs/art_et_culture/bibliotheques

Test direct access link
    Click Element  id=mobnav-btn
    Click Loisirs in menu
    Location Should Be  ${PLONE_URL}
    Click Element  css=ul.submenu-level-2 li:nth-child(2)
    Location Should Be  ${PLONE_URL}
    Click Element  css=ul.submenu-level-3 li:nth-child(4)
    Location Should Be  ${PLONE_URL}/loisirs/art_et_culture/artistes/rockers/john_lennon

Test menu after access from URL root
    Go to  ${PLONE_URL}
    Element should not be visible  css=#title-level-1
    Element should not be visible  css=#title-level-2
    Element should not be visible  css=#title-level-3
    Element should not be visible  css=#title-level-4

Test menu after access from URL loisirs
    Go to  ${PLONE_URL}/loisirs
    Element should not be visible  css=#title-level-1
    Element should be visible  css=#title-level-2
    Element should not be visible  css=#title-level-3
    Element should not be visible  css=#title-level-4

Test menu after access from URL art_et_culture
    Go to  ${PLONE_URL}/loisirs/art_et_culture
    Element should not be visible  css=#title-level-1
    Element should be visible  css=#title-level-2
    Element should be visible  css=#title-level-3
    Element should not be visible  css=#title-level-4

Test menu after access from URL artistes
    Go to  ${PLONE_URL}/loisirs/art_et_culture/artistes
    Element should not be visible  css=#title-level-1
    Element should be visible  css=#title-level-2
    Element should be visible  css=#title-level-3
    Element should be visible  css=#title-level-4

Test menu after access from URL abba
    Go to  ${PLONE_URL}/loisirs/art_et_culture/artistes/abba
    Element should not be visible  css=#title-level-1
    Element should be visible  css=#title-level-2
    Element should be visible  css=#title-level-3
    Element should be visible  css=#title-level-4

*** Keywords ***

Click Loisirs in menu
    Wait until element is visible  css=ul.submenu-level-1 li:nth-child(7)
    Click Element  css=ul.submenu-level-1 li:nth-child(7)
