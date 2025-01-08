
IMPORT ".module/login_naver.as" AS NAVER_LOGIN



SET edge_1 = BROWSER_EDGE(BACKGROUND = FALSE, MAXIMIZE=TRUE)
SET chrome_1 = BROWSER_CHROME(BACKGROUND = FALSE, MAXIMIZE=FALSE)

SET sheetname = "Result"
SET dt = READ_EXCEL("C:\Users\User\Documents\병원 테스트_result - 네이버 완료.xlsx", SHEET_NAME = "Result")
SET naver_logined = FALSE



ON_BROWSER edge_1
    NAVIGATE "google.com"
    TYPE_INTO ${selector_id:google_search_검색창} "Test"
    

CLOSE_BROWSER