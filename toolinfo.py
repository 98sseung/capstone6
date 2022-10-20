print("해당 도구는 주요정보통신기반시설 웹 취약점 분석 및 평가 가이드를 기반으로, ")
print("웹 취약점 항목을 자동으로 진단해주며, 진단 결과를 PDF 보고서로 작성해주는 기능을 하고있습니다.")
print("\n<점검 항목>  \n")
print("1 - LDAP Injection : LDAP 인젝션")
print("    웹페이지 내 LDAP 인젝션 취약점을 점검합니다.\n")
print("2 - SQL Injection : SQL 인젝션")
print("     웹페이지 내 SQL 인젝션 취약점 존재 여부를 점검합니다.\n")
print("3 - XPath Injection : XPath 인젝션")
print("    웹페이지 내 조작된 XPath 쿼리 공격 가능성을 점검합니다.\n")
print("4 - XSS : 크로스사이트 스크립팅")
print("    웹 사이트 내 크로스사이트 스크립팅 취약점 존재 여부를 점검합니다.\n")
print("5 - BF : 약한 문자열 강도")
print("    웹페이지 내 로그인 폼 등에 약한 강도의 문자열 사용 여부를 점검합니다.\n")
print("6 - IA : 불충분한 인증")
print("    중요 페이지 접근 시 추가 인증 요구 여부를 점검합니다.\n")
print("7 - IN :  불충분한 인가")
print("    민감한 데이터 또는 기능에 접근 및 수정 시 통제 여부를 점검합니다.\n")
print("8 - SF : 세션 고정")
print("    사용자 로그인 시 항상 일정하게 고정된 세션 ID 값을 발행하는지 여부를 확인합니다.\n")
print("9 - Auto Attack : 자동화 공격")
print("    웹 애플리케이션의 특정 프로세스(로그인 시도, 게시글 등록, SMS 발송등)에 대한 반복적인 요청 시 통제 여부를 확인합니다.\n")
print("10 - PV : 프로세스 검증 누락")
print("    인증이 필요한 웹 사이트의 중요(관리자 페이지, 회원변경 페이지 등)페이지에 대한 접근제어 설정 여부를 확인합니다.\n")
print("11 - File Download : 파일 다운로드")
print("    웹 사이트에서 파일 다운로드 시 허용된 경로 외 다른 경로의 파일 접근이 가능한지 여부를 점검합니다.\n")
print("12 - Admin Page Exposure : 관리자 페이지 노출")
print("    유추하기 쉬운 URL로 관리자 페이지 및 메뉴 접근의 가능 여부를 점검합니다.\n")