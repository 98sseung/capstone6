from termcolor import cprint

print_blue = lambda x : cprint(x, "blue")
print_blue("Select 1: 진단하기")
print("        → 진단할 URL 입력 (ex : https://google.com)\n")
print_blue("Select 2: 결과 조회")
print("        → 진단 결과 보고서 이메일로 받기 선택 시 사용자 Email 입력(ex : capstone6@naver.com )\n")
print_blue("Select 3: 도구 제작자 소개\n")
print_blue("Select 4: 도구 소개\n")
print_blue("Select 5: 도움말 보기\n")
print_blue("Select 0: 종료\n")
