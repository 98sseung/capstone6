from selenium import webdriver
from selenium.common.exceptions import UnexpectedAlertPresentException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
import urllib.request
import time
import sys
from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger
from fpdf import FPDF
from bs4 import BeautifulSoup
import datetime
import requests
from selenium.webdriver.chrome.options import Options
import os
import pyotp
import smtplib
from email.mime.text import MIMEText

url = input("진단할 url 입력: ")
email = input("사용자 email 입력: ")

def user_OTP() :
    secret = pyotp.random_base32()
    totp = pyotp.TOTP(secret, interval=60)
    otp = totp.now()  

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login('otpcapstone6@gmail.com', 'huranoxbyilklwae')
    msg = MIMEText('OTP를 입력해주세요: '+ otp)
    msg['Subject'] = 'OTP 인증번호'
    s.sendmail("otpcapstone6@gmail.com",email, msg.as_string())
    s.quit()
    otp_auth = int(input('이메일을 확인하여 60초 이내에 OTP를 입력해주세요 : '))
    while True:
        if otp_auth != int(otp):
            print("OTP를 다시 입력해주세요: ")
            otp_auth = int(input())
            continue
        break
    print('인증 완료')

user_OTP()

driver = webdriver.Chrome(ChromeDriverManager().install())


report = PdfFileReader(open("./Guide(web).pdf", 'rb'))
writer = PdfFileWriter()
writer.addPage(report.getPage(0))
writer.addPage(report.getPage(1))

def LI(domain): #LDAP Injection(3)
    Inspection_Items = "LDAP Injection(3)"
    contents = ""
    cve = "Safety"

    urls = domain+"/login.php"

    XPATH_id = "/html/body/div/form/p[1]/input"
    XPATH_pw = "/html/body/div/form/p[2]/input"
    XPATH_click = "/html/body/div/form/input"

    lines = [
            "*",
            "admin)(&))",
            "*)(&",
            ")(cn=*))",
            "*()|&'",
            "*(|(objectclass=*))",
            "*)(uid=*))(|(uid=*",
            "admin*)((|userpassword=*)"
            ]

    count = 0
    for payload in lines:
        driver.get(urls)
        input_box = driver.find_element(By.XPATH, XPATH_id)
        input_box.send_keys(payload)
        input_box2 = driver.find_element(By.XPATH, XPATH_pw)
        input_box2.send_keys("admin")
        driver.find_element(By.XPATH, XPATH_click).click()
        alert = driver.switch_to.alert
        alert_text = alert.text
        alert.accept()
        if "되셨습니다" in alert_text:
            count += 1
    if count > 0:
        writer.addPage(report.getPage(8))
        writer.addPage(report.getPage(9))
        cve = "Risk"
        print("LDAP Injection 취약")
        contents = urls
        return (Inspection_Items, contents.strip(), cve)
    else:
        print("LDAP Injection 안전")
        contents = "This website is \"SAFETY\" from LDAP Injection"
        return (Inspection_Items, contents.strip(), cve)

def SI(domain): # SQLi(5)
    Inspection_Items = "SQL Injection(5)"
    contents = ""
    cve = "Safety"

    urls = domain+"/login.php"

    XPATH_id = "/html/body/div/form/p[1]/input"
    XPATH_pw = "/html/body/div/form/p[2]/input"
    XPATH_click = "/html/body/div/form/input"

    lines = ["'or 1 = 1 -- '",
            "‘ or 1 = 1 - -’",
            "‘ or 1 = 1 - -",
            "‘ or ’1’=1’",
            "‘ or 1 =’1"]
    count = 0
    for payload in lines:
        driver.get(urls)
        input_box = driver.find_element(By.XPATH, XPATH_id)
        input_box.send_keys("admin")
        input_box2 = driver.find_element(By.XPATH, XPATH_pw)
        input_box2.send_keys(payload)
        driver.find_element(By.XPATH, XPATH_click).click()
        alert = driver.switch_to.alert
        alert_text = alert.text
        alert.accept()
        if "성공" in alert_text:
            count += 1
    if count > 0:
        cve = "Risk"
        writer.addPage(report.getPage(10))
        writer.addPage(report.getPage(11))
        writer.addPage(report.getPage(12))
        writer.addPage(report.getPage(13))
        writer.addPage(report.getPage(14))
        writer.addPage(report.getPage(15))
        print("SQL Injection 취약")
        contents = urls
        return (Inspection_Items, contents.strip(), cve)
    else:
        print("SQL Injection 안전")
        contents = "This website is \"SAFETY\" from SQL Injection"
        return (Inspection_Items, contents.strip(), cve)

def XI(domain): # XPath 인젝션(7)
    Inspection_Items = "XPath Injection(7)"
    contents = ""
    cve = "Safety"
    
    urls = domain+"/login.php"

    XPATH_id = "/html/body/div/form/p[1]/input"
    XPATH_pw = "/html/body/div/form/p[2]/input"
    XPATH_click = "/html/body/div/form/input"

    lines_id = ["'and'a'='a", "and 1=1"]
    lines_pw = ["'and'a'='b", "and 1=2"]
    lines_err= ["‘ or count(parent::*[position()=1])=0 or ‘a’='b",
                "‘ or count(parent::*[position()=1])>0 or ‘a’='b",
                "1 or count(parent::*[position()=1])=0",
                "1 or count(parent::*[position()=1])>0"]
    content = []
    count = 0

    for i in range(0,2):
        try:
            driver.get(urls)
            input_box = driver.find_element(By.XPATH, XPATH_id)
            input_box.send_keys(lines_id[i])
            input_box2 = driver.find_element(By.XPATH, XPATH_pw)
            input_box2.send_keys(lines_pw[i])
            driver.find_element(By.XPATH, XPATH_click).click()
            alert = driver.switch_to.alert
            alert_text = alert.text
            content.append(alert_text)
            alert.dismiss()
        except UnexpectedAlertPresentException:
            time.sleep(1)
    if content[0] != content[1]:
        count += 1

    for line in lines_err:
        try:
            driver.get(urls)
            input_box = driver.find_element(By.XPATH, XPATH_id)
            input_box.send_keys(line)
            input_box2 = driver.find_element(By.XPATH, XPATH_pw)
            input_box2.send_keys(line)
            driver.find_element(By.XPATH, XPATH_click).click()
            alert = driver.switch_to.alert
            alert_text = alert.text
            content.append(alert_text)
            alert.dismiss()
        except UnexpectedAlertPresentException:
            time.sleep(1)
            if "실패" or "성공" in alert_text:
                count += 1
    if count != 0:
        cve = "Risk"
        writer.addPage(report.getPage(18))
        writer.addPage(report.getPage(19))
        print("XPath Injection 취약")
        contents = urls
        return (Inspection_Items, contents.strip(), cve)
    else:
        print("XPath Injection 안전")    
        contents = "This website is \"SAFETY\" from XPath Injection"
        return (Inspection_Items, contents.strip(), cve)

def XS(domain): # XSS(11)
    Inspection_Items = "XSS(11)"
    contents = ""
    cve = "Safety"

    urls = domain+"/board.php"
    lines = ["<script>alert('XSS Risk')</script>",
             '"><script>alert(XSS Risk)</script>']
    count = len(lines)
    for payload in lines:
        try:
            driver.get(urls)
            input_box = driver.find_element(By.NAME, "search")
            input_box.send_keys(payload)
            driver.find_element(By.XPATH, '/html/body/div/form/button').click()
        except UnexpectedAlertPresentException:
            time.sleep(2)
            count -= 1
    if count > 0:
        cve = "Risk"
        writer.addPage(report.getPage(30))
        writer.addPage(report.getPage(31))
        writer.addPage(report.getPage(32))
        writer.addPage(report.getPage(33))
        writer.addPage(report.getPage(34))
        contents = urls
        print("XSS 취약")
        return (Inspection_Items, contents.strip(), cve)
    else:
        print("XSS 안전")
        contents = "This website is \"SAFETY\" from Cross Site Scripting"
        return (Inspection_Items, contents.strip(), cve)


def BF(domain): # 약한 문자열 강도(12)
    Inspection_Items = "BF(12)"
    contents = ""
    cve = "Safety"

    urls = domain+"/login.php"

    XPATH_id = "/html/body/div/form/p[1]/input"
    XPATH_pw = "/html/body/div/form/p[2]/input"
    XPATH_click = "/html/body/div/form/input"

    idz = ["adminstrator", "manager","guest", "admin", "test"]

    passwds = ["Abcd",
            "aaaa",
            "admin",
            "test",
            "1234",
            "1111",
            "password"]

    for i in idz:
        driver.get(urls)
        input_box = driver.find_element(By.XPATH, XPATH_id)
        input_box.send_keys(i)

        for payload in passwds:    
            input_box2 = driver.find_element(By.XPATH, XPATH_pw)
            input_box2.send_keys(payload)
            driver.find_element(By.XPATH, XPATH_click).click()
            alert = driver.switch_to.alert
            alert_text = alert.text
            alert.accept()
            if "되었습니다" in alert_text:
                cve = "Risk"
                writer.addPage(report.getPage(35))
                writer.addPage(report.getPage(36))
                print("약한 문자열 강도 취약")
                contents = urls
                return (Inspection_Items, contents.strip(), cve)
            else:
                input_box2.clear()
    print("약한 문자열 강도 안전")
    contents = "This website is \"SAFETY\" from BF"
    return (Inspection_Items, contents.strip(), cve)

def IA(domain): # 불충분한 인증(13)
    Inspection_Items = "IA(13)"
    contents = ""
    cve = "Safety"

    urls = domain+"/login.php"

    XPATH_id = "/html/body/div/form/p[1]/input"
    XPATH_pw = "/html/body/div/form/p[2]/input"
    XPATH_click = "/html/body/div/form/input"
    XPATH_Mypage = '//*[@id="collapsibleNavbar"]/ul/li[6]/div/a[4]'
    X = '//*[@id="navbarDropdown"]'
    count = 0

    driver.get(urls)
    input_box = driver.find_element(By.XPATH, XPATH_id)
    input_box.send_keys("admin")
    input_box2 = driver.find_element(By.XPATH, XPATH_pw)
    input_box2.send_keys("admin")
    driver.find_element(By.XPATH, XPATH_click).click()

    try:
        driver.find_element(By.XPATH, X).click()
        driver.find_element(By.XPATH, XPATH_Mypage).click()

    except UnexpectedAlertPresentException:
        time.sleep(1)
        count += 1

    if count > 0:
        cve = "Risk"
        writer.addPage(report.getPage(37))
        writer.addPage(report.getPage(38))
        print("불충분한 인증 취약")
        contents = urls
        return (Inspection_Items, contents.strip(), cve)
    else:
        print("불충분한 인증 안전")
        contents = "This website is \"SAFETY\" from IA"
        return (Inspection_Items, contents.strip(), cve)

def IN(domain): #불충분한 인가(17)
    Inspection_Items = "IN(17)"
    contents = "This Website \"Risk\" from IN"
    cve = "Risk"
    msg = "불충분한 인가 취약"

    urls = domain+"/board.php"
    sourcecode = urllib.request.urlopen(urls).read()
    soup = BeautifulSoup(sourcecode, "html.parser")
    li=[0 for i in range(3)]

    for href in soup.find("tr", class_="even").find_all("tbody"):
        attr = href.find("a")["href"]
        if "number" in attr:
            num = li.split('=')
            li.append(num[1])

    if li[0] == li[0]+1:
        msg = "불충분한 인가 취약"
        cve = "Risk"
        contents = "This website is \"Risk\" from IN"
        writer.addPage(report.getPage(45))
        writer.addPage(report.getPage(46))
        print(msg)
        return (Inspection_Items, contents.strip(), cve)
    try:
        driver.get(urls)
        writer.addPage(report.getPage(45))
        writer.addPage(report.getPage(46))
        print(msg)
        return (Inspection_Items, contents.strip(), cve)
    except UnexpectedAlertPresentException:
        time.sleep(1)
        msg = "불충분한 인가 안전"
        cve = "Safety"
        contents = "This website is \"SAFETY\" from IN"
        print(msg)
    return (Inspection_Items, contents.strip(), cve)


def SF(domain): # 세션 고정(19)
    Inspection_Items = "SF(19)"
    contents = "This website is \"SAFETY\" from SF"
    cve = "Safety"

    urls = domain+"/login.php"

    XPATH_id = "/html/body/div/form/p[1]/input"
    XPATH_pw = "/html/body/div/form/p[2]/input"
    XPATH_click = "/html/body/div/form/input"
    XPATH_nav = '//*[@id="navbarDropdown"]'
    XPATH_logout = '//*[@id="collapsibleNavbar"]/ul/li[5]/div/a[1]'

    driver.get(urls)
    driver.maximize_window()
    input_box = driver.find_element(By.XPATH, XPATH_id)
    input_box.send_keys('test')
    input_box2 = driver.find_element(By.XPATH, XPATH_pw)
    input_box2.send_keys('test')
    driver.find_element(By.XPATH, XPATH_click).click()
    alert = driver.switch_to.alert
    alert.accept()

    for cookie in driver.get_cookies():
        c = {cookie['name'] : cookie['value']}

    driver.find_element(By.XPATH, XPATH_nav).click()
    driver.find_element(By.XPATH, XPATH_logout).click()

    driver.get(urls)
    driver.maximize_window()
    input_box = driver.find_element(By.XPATH, XPATH_id)
    input_box.send_keys('test')
    input_box2 = driver.find_element(By.XPATH, XPATH_pw)
    input_box2.send_keys('test')
    driver.find_element(By.XPATH, XPATH_click).click()
    alert = driver.switch_to.alert
    alert.accept()

    for cookie in driver.get_cookies():
        a = {cookie['name'] : cookie['value']}

    if c == a:
        cve = "Risk"
        writer.addPage(report.getPage(50))
        print("세션 고정 취약")
        contents = urls
        return (Inspection_Items, contents.strip(), cve)
    else:
        print("세션 고정 안전")
        return (Inspection_Items, contents.strip(), cve)

def AU(domain): # 자동화 공격(20)
    Inspection_Items = "Auto Attack(20)"
    contents = "This Website is \"SAFETY\" from Auto Attack"
    cve = "Safety"

    urls = domain+"/login.php"

    XPATH_id = "/html/body/div/form/p[1]/input"
    XPATH_pw = "/html/body/div/form/p[2]/input"
    XPATH_click = "/html/body/div/form/input"
    count = 0
    for payload in range(5):
        driver.get(urls)
        input_box = driver.find_element(By.XPATH, XPATH_id)
        input_box.send_keys("admin")
        input_box2 = driver.find_element(By.XPATH, XPATH_pw)
        input_box2.send_keys('aaaa1234!@')
        driver.find_element(By.XPATH, XPATH_click).click()
        alert = driver.switch_to.alert
        alert_text = alert.text
        alert.accept()
        if "확인해주세요" in alert_text:
            count += 1
    if count >= 5:
        cve = "Risk"
        writer.addPage(report.getPage(51))
        writer.addPage(report.getPage(52))
        print("자동화 공격 취약")
        contents = urls
        return (Inspection_Items, contents.strip(), cve)
    else:
        print("자동화 공격 안전")
        return (Inspection_Items, contents.strip(), cve)


def PV(): #프로세스 검증 누락(21)
    Inspection_Items = "PV(21)"
    contents = "This Website is \"SAFETY\" from PV"
    cve = "Safety"

    f = open("./payload/url.txt",'r')
    line = f.readlines()
    length = []
    i = 0
    cnt = 0
    for u in line:
        line[i] = line[i].strip('\n')
        i=i+1

    for url in line:
        response = requests.get(url = url)
        status = response.status_code
        res = response.text
        length.append(len(res))

    for le in length:
        if length.count(le) == 1 :
            cve = "Risk"
            writer.addPage(report.getPage(53))
            writer.addPage(report.getPage(54))
            writer.addPage(report.getPage(55))
            print("프로세스 검증 누락 취약","(", line[length.index(le)] ,")" )
            contents = "This Website \"Risk\" from PV"
            contents = line[length.index(le)]
            return (Inspection_Items, contents.strip(), cve)
        else : 
            print("프로세스 검증 누락 안전")
            return (Inspection_Items, contents.strip(), cve)


def FD(domain): #파일 다운로드(23)
    Inspection_Items = "File Download(23)"
    contents = "This Website is \"SAFETY\" from File Downloads"
    cve = "Safety"

    urls = domain+"/board.php"
    driver.get(urls)
    a_tag = driver.find_element(By.TAG_NAME, "a")
    href_text = a_tag.get_attribute('href')
    urls2 = href_text
    driver.get(urls2)
    a = driver.find_element(By.TAG_NAME, "a")
    href = a.get_attribute('href')

    down_url = href[:-1]
    down_url2 = down_url + "../../../../../../../../etc/passwd"
    driver.get(down_url2)
    time.sleep(1)

    #/Downloads를 다운로드된 경로로 바꿔주기
    if os.path.isfile("/Downloads/_.._.._.._.._.._.._.._etc_passwd") is True :
        cve = "Risk"
        writer.addPage(report.getPage(64))
        writer.addPage(report.getPage(65))
        writer.addPage(report.getPage(66))
        writer.addPage(report.getPage(67))
        print("파일 다운로드 취약")
        contents = urls
        return (Inspection_Items, contents.strip(), cve)
    else :
        print("파일 다운로드 안전")
        return (Inspection_Items, contents.strip(), cve)

def AE(domain): # 관리자 페이지 노출(24)
    Inspection_Items = "Admin Page Exposure(24)"
    contents = "This Website is \"SAFETY\" from Admin Page Exposure"
    cve = "Safety"

    page= ["/admin", "/manager", "/master", "/system", "/administart", "/admin/admin.php"]
    urls = domain
    for pages in page:
        try:
            res = urlopen(urls+pages)
            if res.status == 200 :
                cve = "Risk"
                writer.addPage(report.getPage(68))
                writer.addPage(report.getPage(69))
                writer.addPage(report.getPage(70))
                print("Admin_Page 경로 취약 --> ", pages)
                contents = urls
                return (Inspection_Items, contents.strip(), cve)
            else : 
                print("Admin_Page 경로 안전")
                return (Inspection_Items, contents.strip(), cve)
        except HTTPError as e:
            err = e.read()
            code = e.getcode()
            if code != 200 : continue #print(code) ## 404

def capstone(url):
    results = []
    results.append(LI(url)) # LDAP 인젝션(3)
    results.append(SI(url)) # SQL 인젝션(5)
    results.append(XI(url)) # XPath 인젝션(7)
    results.append(XS(url)) # 크로스사이트 스크립팅(11)
    results.append(BF(url)) # 약한 문자열 강도(12)
    results.append(IA(url)) # 불충분한 인증(13)
    results.append(IN(url)) # 불충분한 인가(17)
    results.append(SF(url)) # 세션 고정(19)
    results.append(AU(url)) # 자동화 공격(20)
    results.append(PV()) # 프로세스 검증 누락(21)
    results.append(FD(url)) # 파일 다운로드(23)
    results.append(AE(url)) # 관리자 페이지 노출(24)
    return results

data = []

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", size=20)
        self.cell(200, 20, txt="Capstone - Web Vulnerability Diagnostic Results Report", ln=1, align="C")
        self.set_text_color(46,138,204)
        self.cell(20, 20, txt="Scan Information", ln=1)
        self.set_line_width(1)
        self.set_draw_color(255, 0, 0)
        self.line(10, 45, 200, 45)
        self.set_line_width(1)
        self.set_draw_color(0, 0, 0)
        self.set_text_color(0,0,0)
        self.set_font("Arial", size=11) 
        self.cell(20, 5, txt="Website URL = "+url, ln=1) 
        self.cell(10,5,txt="Start Time = "+str(start_t), ln=1) 
        self.cell(10,5,txt="Finish Time = "+str(end_t), ln=1) 
        self.cell(10,5,txt="Scan duration = "+str(duration), ln=1)

    def footer(self):
        self.set_y(-15) 
        self.set_font('Arial', 'I', 8) 
        self.set_text_color(128) 
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')
    
    def chapter_title(self, num, label):
        self.set_font('Arial', '', 12) 
        self.set_fill_color(200, 220, 255) 
        self.cell(0, 6, 'Chapter %d : %s' % (num, label), 0, 1, 'L', 1) 
        self.ln(4)

    def chapter_body(self, spacing=2):
        global data
        self.cell(10, 20, ln=1, align="c")
        self.set_font("Arial", 'B', size=24) 
        self.cell(10, 20, txt="List of tests performed (12/12)",ln=1 ,align="L")
        self.set_font("Arial", 'B', size=15) 
        self.set_draw_color(0, 0, 0) 
        self.set_line_width(0.5) 
        col_width = self.w / 3.3
        row_height = self.font_size
        header = ('Type', 'Contents', 'Resulte')
        
        cellwidth = 110
        cellHeight= 5
        self.cell(40, cellHeight*3, txt=header[0], border=1, align="C") 
        self.cell(cellwidth, cellHeight*3, txt=header[1], border=1, align="C") 
        self.cell(40, cellHeight*3, txt=header[2], border=1, ln=1, align="C") 
        self.set_font("Arial", size=10)

        for i in range(12): #capstone(url) results 풀면 범위 늘려줘야함.
            line =1
            if self.get_string_width(data[i][1]) < cellwidth:
                line =1

            else:
                textLength=len(data[i][1])
                errMargin = 44
                startChar = 0
                maxChar = 0
                textArray = []
                tmpString=""
                st = data[i][1]
                while (startChar < textLength):
                    while (self.get_string_width(tmpString) < (cellwidth - errMargin) and (startChar+maxChar) < textLength):
                        maxChar +=1
                        tmpString = st[startChar : maxChar]
                    
                    startChar= startChar + maxChar
                    textArray.append(tmpString)
                    line +=1
                    maxChar=0
                    tmpString=""

            self.cell(40, line*cellHeight, txt=data[i][0], border=1, ln=0,align = "C")
            x = self.get_x()
            y = self.get_y()
            self.multi_cell(cellwidth, cellHeight, txt=data[i][1], border=1)
            self.set_xy(x+cellwidth, y)
            self.cell(40, line*cellHeight, txt=data[i][2], border=1, ln=1,align = "C")

    def print_chapter(self, num, title, name):
        self.add_page()
        self.chapter_title(num, title)
        self.chapter_body(name)


if __name__ == '__main__':

    start_t = datetime.datetime.now()
    R_filename = "Analysis Results Report"+f"({start_t.strftime('%H-%M-%S')})"+".pdf" #Result
    G_filename = "Action Method Guide"+f"({start_t.strftime('%H-%M-%S')})" #Guide

    data.extend(capstone(url))
    driver.quit()

    end_t = datetime.datetime.now()
    duration = end_t - start_t

    writer.write(open("./output/"+G_filename+".pdf", "wb"))

title = 'Web Scan Report'

pdf = PDF()
pdf.set_title(title)
pdf.add_page()
pdf.chapter_body()
pdf.output(f"./output/{R_filename}", 'F')