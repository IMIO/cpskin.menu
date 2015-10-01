*** Settings ***

Resource  plone/app/robotframework/keywords.robot

Test Setup  Run keywords  Open test browser
Test Teardown  Close all browsers


*** Variables ***


*** Test Cases ***

Test menu
    Click LOISIRS Menu
    Location Should Be  http://localhost:55001/plone/loisirs


*** Keywords ***

Click LOISIRS Menu
    Element Should Be Visible  css=li#portaltab-loisirs a
    Click Element              css=li#portaltab-loisirs a
