*** Settings ***

Resource  plone/app/robotframework/keywords.robot

Suite Setup  Run keywords  Open test browser
Suite Teardown  Close all browsers


*** Variables ***

#${BROWSER}  Firefox
#${SELENIUM_TIMEOUT}  5

*** Test Cases ***
When accessing homepage, menu is not shown
    On homepage
    No menu

When accessing page in navigation, level 2 menu is shown
    On each page
    Menu level 2 shown with corresponding content
    Other levels are not shown
    Click outside menu
    Menu is not hidden

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
    Click outside menu
    Menu is not hidden

Test menu level 2 structure
    On each page
    Menu level 2 shown with corresponding content
    In level 2 menu, Folder with subcontent is shown as access to submenu
    In level 2 menu, Folder with subcontent and with default view is shown as access to submenu
    In level 2 menu, Folder with default view and no other subcontent is shown as direct link
    In level 2 menu, Content element is shown as direct link
    In level 2 menu, Folder without subcontent is shown as direct link

Test direct link in level 2
    On each page
    Menu level 2 shown with corresponding content
    Click direct link in level 2
    Direct link page is loaded

Test submenu in level 2
    On each page
    Menu level 2 shown with corresponding content
    Click submenu in level 2
    Menu level 3 shown
    No page is loaded

Test menu level 3 structure
    [tags]  current
    On each page
    Menu level 2 shown with corresponding content
    Click submenu in level 2
    Menu level 3 shown
    No page is loaded
    In level 3 menu, Folder with subcontent is shown as access to submenu
    In level 3 menu, Folder with subcontent and with default view is shown as access to submenu
    In level 3 menu, Folder with default view and no other subcontent is shown as direct link
    In level 3 menu, Content element is shown as direct link
    In level 3 menu, Folder without subcontent is shown as direct link

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

Click outside menu
    Click element  css=#parent-fieldname-title

Menu is not hidden
    Menu level 2 shown with corresponding content
    
In level 2 menu, Folder with subcontent is shown as access to submenu
    Page should contain element  css=#portal-globalnav-cpskinmenu-subfolder-1-subfolder-1-subfolder-2 .sf-sub-indicator
    
In level 2 menu, Folder with subcontent and with default view is shown as access to submenu
    Page should contain element  css=#portal-globalnav-cpskinmenu-subfolder-1-subfolder-1-default-view-subcontent-in-2 .sf-sub-indicator

In level 2 menu, Folder with default view and no other subcontent is shown as direct link
    Page should contain element  css=#portal-globalnav-cpskinmenu-subfolder-1-subfolder-1-default-view-empty-in-2
    Page should not contain element  css=#portal-globalnav-cpskinmenu-subfolder-1-subfolder-1-default-view-empty-in-2 .sf-sub-indicator

In level 2 menu, Content element is shown as direct link
    Page should contain element  css=#portal-globalnav-cpskinmenu-subfolder-1-subfolder-1-direct-link-in-2
    Page should not contain element  css=#portal-globalnav-cpskinmenu-subfolder-1-subfolder-1-direct-link-in-2 .sf-sub-indicator

In level 2 menu, Folder without subcontent is shown as direct link
    Page should contain element  css=#portal-globalnav-cpskinmenu-subfolder-1-subfolder-1-empty-in-2
    Page should not contain element  css=#portal-globalnav-cpskinmenu-subfolder-1-subfolder-1-empty-in-2 .sf-sub-indicator
    
Click direct link in level 2
    Click element  css=#portal-globalnav-cpskinmenu-subfolder-1-subfolder-1-direct-link-in-2 a

Direct link page is loaded
    ${CURRENT_URL} =  Log location
    Should not be equal  ${ORIGINAL_URL}  ${CURRENT_URL}
    Location should be  ${PLONE_URL}/subfolder-1/direct-link-in-2
    Set suite variable  ${CURRENT_ID}  direct-link-in-2
    
Click submenu in level 2
    ${EL} =  Set variable  css=#portal-globalnav-cpskinmenu-subfolder-1-subfolder-1-subfolder-2 > span > a
    Locator Should Match X Times  ${EL}  1
    Wait until element is visible  ${EL}
    Wait until page does not contain element  jquery=:animated
    Click element  ${EL}

No page is loaded
    ${CURRENT_URL} =  Log location
    Should not be equal  ${ORIGINAL_URL}  ${CURRENT_URL}

Menu level 3 shown
    Wait until page does not contain element  jquery=:animated
    Wait until element is visible  css=#subfolder-1-subfolder-2-empty-in-3
    Element should be visible  css=#subfolder-1-subfolder-2-empty-in-3

In level 3 menu, Folder with subcontent is shown as access to submenu
    Page should contain element  css=#portal-globalnav-cpskinmenu-subfolder-1-subfolder-1-subfolder-2-subfolder-3 .sf-sub-indicator
    
In level 3 menu, Folder with subcontent and with default view is shown as access to submenu
    Page should contain element  css=#portal-globalnav-cpskinmenu-subfolder-1-subfolder-1-subfolder-2-default-view-subcontent-in-3 .sf-sub-indicator

In level 3 menu, Folder with default view and no other subcontent is shown as direct link
    ${EL} =  Set variable  css=#portal-globalnav-cpskinmenu-subfolder-1-subfolder-1-subfolder-2-default-view-empty-in-3
    Page should contain element  ${EL}
    Page should not contain element  ${EL} .sf-sub-indicator

In level 3 menu, Content element is shown as direct link
    ${EL} =  Set variable  css=#portal-globalnav-cpskinmenu-subfolder-1-subfolder-1-subfolder-2-direct-link-in-3
    Page should contain element  ${EL}
    Page should not contain element  ${EL} .sf-sub-indicator

In level 3 menu, Folder without subcontent is shown as direct link
    ${EL} =  Set variable  css=#portal-globalnav-cpskinmenu-subfolder-1-subfolder-1-subfolder-2-empty-in-3
    Page should contain element  ${EL}
    Page should not contain element  ${EL} .sf-sub-indicator
