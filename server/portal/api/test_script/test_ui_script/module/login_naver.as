ARGUMENTS
    IN driver:${driver}
    IN id:string
    IN pw:string
    OUT successful:boolean

ON_BROWSER driver
    DELAY 00:05
    CLICK_ELEMENT ${selector_id:naver_home_login_button}
    TYPE_INTO ${selector_id:naver_login_page_id_editbox} id
    TYPE_PASSWORD ${selector_id:naver_login_page_id_password} pw
    CLICK_ELEMENT ${selector_id:naver_login_page_submit}
    DELAY 00:05

successful = TRUE
