*** Settings ***

Resource  plone/app/robotframework/selenium.robot

Library  Remote  ${PLONE_URL}/RobotRemote
Library  OperatingSystem

Test Setup  Open test browser
Test Teardown  Close all browsers

*** Test Cases ***

After the document creation pasted images should be saved into separate files
    Log in as a 'Site Administrator'
    Go to 'create a new document' form
    Paste image from clipboard
    Save the form
    As the result - link of the created image will replace the image data

After the document editing pasted images should be saved into separate files
    Log in as a 'Site Administrator'
    Go to 'Edit Document' form
    Paste image from clipboard
    Save the form
    As the result - link of the created image will replace the image data


*** Keywords ***

Log in as a '${ROLE}'
    Enable autologin as  ${ROLE}
    Go to  ${PLONE_URL}

Go to 'create a new document' form
    go to   ${PLONE_URL}/createObject?type_name=Document
    Input Text  title   ${document_name}

Paste image from clipboard
    ${data}=  Get Binary File   ${CURDIR}/owl.jpg.base64
    Wait Until Page Contains Element   text_ifr    30
    Select Frame    text_ifr
    Execute JavaScript  img=window.document.createElement("img");img.src="data:image/jpeg;base64,${data}";window.document.getElementsByTagName('body')[0].appendChild(img)
    Unselect Frame

Save the form
    Click Element  xpath=//input[@value="Save"]

Go to 'Edit Document' form
    Go to 'create a new document' form
    Select Frame    text_ifr
    Execute JavaScript  p=window.document.createElement("p");window.document.getElementsByTagName('body')[0].appendChild(p)
    Unselect Frame
    save the form
    go to   ${PLONE_URL}/${document_name}/edit

As the result - link of the created image will replace the image data
    [Arguments]         ${images num}=1
    ${data}=  Get Binary File   ${CURDIR}/owl.jpg.base64
    Xpath Should Match X Times  //div[@id="content-core"]//img   ${images num}
    Page Should Not Contain Image   //img[@src="data:image/jpeg;base64,${data}"]

*** Variables ***
${document_name}  test_document
