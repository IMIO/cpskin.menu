*** Settings ***

Resource  plone/app/robotframework/keywords.robot

Suite Setup  Run keywords  Open test browser
Suite Teardown  Close all browsers


*** Variables ***


*** Test Cases ***
When accessing homepage, menu is not shown
    On homepage
    No menu

When accessing page in navigation, level 2 menu is shown
    On each page
    Menu level 2 shown with corresponding content
    Other levels are not shown

When accessing page not in navigation, menu is not shown
    On each page not in navigation
    No menu

When clicking home, homepage is reloaded
    On each page
    Click home in level 1
    Homepage is loaded

When clicking level 1, other page is loaded
    On each page 
    Click level 1
    Item page is loaded
    Menu level 2 shown with corresponding content
#    Click outside menu
#    Menu is not hidden.


*** Keywords ***

On Homepage
    Go to  ${PLONE_URL}

No menu
    Element should not be visible  css=.portal-globalnav-cpskinmenu.navTreeLevel0

On each page 
    Go to  ${PLONE_URL}/subfolder-1
    Set suite variable  ${ORIGINAL_URL}  Log location
    Set suite variable  ${CURRENT_ID}  subfolder-1

On each page not in navigation
    Go to  ${PLONE_URL}/Members

Menu level 2 shown with corresponding content
    Wait until element is visible  css=#portal-globalnav-cpskinmenu-${CURRENT_ID}

Other levels are not shown
    Element should not be visible  css=.portal-globalnav-cpskinmenu.navTreeLevel1
    Element should not be visible  css=.portal-globalnav-cpskinmenu.navTreeLevel2
    Element should not be visible  css=.portal-globalnav-cpskinmenu.navTreeLevel3

Click home in level 1
    Click element  css=#portaltab-index_html a

Homepage is loaded
    ${CURRENT_URL} =  Log location
    Should not be equal  ${ORIGINAL_URL}  ${CURRENT_URL}
    Location should be  ${PLONE_URL}

Click level 1
    Click element  css=#portaltab-other-1 a

Item page is loaded
    ${CURRENT_URL} =  Log location
    Should not be equal  ${ORIGINAL_URL}  ${CURRENT_URL}
    Location should be  ${PLONE_URL}/other-1
    Set suite variable  ${CURRENT_ID}  other-1

