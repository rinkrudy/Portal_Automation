*** Settings ***
Library    OperatingSystem
Library    Collections
*** Variables ***
${URL}      https://map.naver.com/p?c=15.00,0,0,0,dh
${Location_Start}    //label[contains(text(),'출발지')]/following-sibling::input
${Location_End}    //label[contains(text(),'도착지')]/following-sibling::input
${Dict_XPath}    길찾기=//span[text()='길찾기']    다시입력=//button[text()='다시입력']
${Dict_Ui_Info}    ${None}


*** Keywords ***
Initialize Module
    [Arguments]    ${ui_info_json}
    Set Global Variable    ${Dict_Ui_Info}    ${ui_info_json["Naver"]["Map"]["ui"]}

    
Open Browser To Naver Map
    Open Browser    ${URL}    browser=Chrome
    Log    ${Dict_Ui_Info}
    Sleep    3s

Input Location
    [Arguments]     ${type}    ${text}
    ${ui_input}    Set Variable    없음
    IF    '${type}' == '출발지'
        ${ui_input}=    Set Variable    ${Location_Start}
    ELSE IF    '${type}' == '도착지'
        ${ui_input}=    Set Variable    ${Location_End}
    ELSE
        Fatal Error
    END
    Input Text    ${ui_input}    ${text}
    Sleep    3s

Click Naver ui
    [Arguments]    ${ui_name}
    Click Element    xpath=${Dict_Ui_Info['${ui_name}']['value']}
    Sleep    3s

Move To '길찾기'
    Click Element    xpath=//span[text()='길찾기']
    Sleep    3s

Click Button
    Click Element    xpath=//button[text()='다시입력']]
    Sleep    3s

Initialize Location
    Click Element    xpath=//button[text()='다시입력']]
    Sleep    3s

Click Find Path
    Click Element    xpath=//span[text()='길찾기']
    Sleep    3s


