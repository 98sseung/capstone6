import sys
import subprocess
import time
from termcolor import cprint

import os
#os.system("mode con cols=81 lines=42")
print_red = lambda x: cprint(x, 'red')
print_yellow = lambda x: cprint(x, 'yellow')
print_green = lambda x: cprint(x, 'green')
print_blue = lambda x: cprint(x, 'blue')
print_magenta = lambda x : cprint(x, "magenta")
print_cyan = lambda x : cprint(x, "cyan")
print_grey = lambda x : cprint(x, "grey")
print_white = lambda x : cprint(x, "white")

def fun1():
    print("\n=> 진단을 시작합니다.\n") 
    time.sleep(1)
    subprocess.call("python web_diagnostic.py",shell=True)
    print("=> 진단이 완료되었습니다.\n\n")

def fun2():
    a=input("\n=> 이메일로 진단 보고서를 전송 하시겠습니까? (y/n)")
    if(a=="y"):
        subprocess.call("python post.py",shell=True)
        print("=> 보고서가 전송되었습니다.\n\n")
    else :
        print("=> 메뉴 화면으로 돌아갑니다.\n\n")

def fun3():
    print("\n=> 제작자 소개 메뉴입니다.\n")
    subprocess.call("python teaminfo.py",shell=True)

def fun4():
    print_blue("\n=> 웹 취약점 진단 시스템 소개 페이지 입니다.\n")
    subprocess.call("python toolinfo.py",shell=True)
    
def fun5():
    print("=>help")
    subprocess.call("python help.py", shell=True)
    


if __name__ == '__main__':

    print_blue(" \n===================================================================================================================  ")
    print_blue("  ________  ________  ________  ________  _________  ________  ________   _______                 ________              ")
    print_blue(" |\   ____\|\   __  \|\   __  \|\   ____\|\___   ___\\\\   __  \|\   ___  \|\  ___ \               |\   ____\           ")
    print_blue(" \ \  \___|\ \  \|\  \ \  \|\  \ \  \___|\|___ \  \_\ \  \|\  \ \  \\\\ \  \ \   __/|              \ \  \___|           ")
    print_blue("  \ \  \    \ \   __  \ \   ____\ \_____  \   \ \  \ \ \  \\\\\  \ \  \\\\ \  \ \  \_|/_              \ \  \____        ")
    print_blue("   \ \  \____\ \  \ \  \ \  \___|\|____|\  \   \ \  \ \ \  \\\\\  \ \  \\\\ \  \ \  \_|\    __________ \ \  ___  \      ")
    print_blue("    \ \_______\ \__\ \__\ \__\     ____\_\  \   \ \__\ \ \_______\ \__\\\\ \__\ \_______ |\_________\ \ \_______\       ")
    print_blue("     \|_______|\|__|\|__|\|__|    |\_________\   \|__|  \|_______|\|__| \|__|\|_______|\|_________|  \|_______|         ")
    print_blue("                                  \|_________|                                                                          ")
    print_blue("                                                                   중부대학교 정보보호학과 team.저희가할수있겠조          ")
    print_blue(" \n====================================================================================================================\n")
    print_red("\n                                                        ※  주 의  ※\n")
    print_red("                           해당 도구는 취약점 진단 도구로 허가된 사용자만 사용이 가능합니다.")
    print_red("               또한, 허가받은 URL을 제외한 다른 URL에 해당 도구 사용시 법적임 책임은 사용자에게 있습니다.\n\n")
    while True:
        print("\n __________     웹 취약점 진단 서비스     __________")
        print("|                                                   |")
        print("|                1. 진단하기                        |")
        print("|                                                   |")
        print("|                2. 결과조회                        |")
        print("|                                                   |")
        print("|                3. Team 저희가할수있겠조           |")   
        print("|                                                   |")
        print("|                4. 도구 소개                       |")
        print("|                                                   |")
        print("|                5. Help                            |")
        print("|                                                   |")
        print("|                0. 종료                            |")
        print("|___________________________________________________|\n")
        menu=int(input("선택: "))

        if menu==0:
            print("\n\n=>웹 취약점 진단 서비스를 종료합니다.")
            time.sleep(1)
            sys.exit()
        elif menu==1:
            fun1()
            time.sleep(1)
        elif menu==2:
            fun2()
            time.sleep(1)
        elif menu==3:
            fun3()
            time.sleep(1)
        elif menu==4:
            fun4()
            time.sleep(1)
        elif menu==5:
            fun5()
            time.sleep(1)
        else:
            print("잘못된 입력입니다.")
