import os
import smtplib
from email.encoders import encode_base64
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate

file_list = os.listdir("./output")

email=input("전송받을 이메일 입력: ")
msg = MIMEMultipart()

msg['From'] = 'otpcapstone6@gmail.com'
msg['To'] = email
msg['Date'] = formatdate(localtime=True)
msg['Subject'] = Header(s='capstone6<웹 취약점 진단 서비스>', charset='utf-8')
body = MIMEText('capstone6<웹 취약점 진단 보고서> 첨부된 파일 2개를 확인해 주세요.', _charset='utf-8')
msg.attach(body)

files = list()
files.append("./output/"+file_list[0])
files.append("./output/"+file_list[1])

for f in files:
    part = MIMEBase('application', "octet-stream")
    part.set_payload(open(f, "rb").read())
    encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
    msg.attach(part)

mailServer = smtplib.SMTP_SSL('smtp.gmail.com', 465)
mailServer.login('otpcapstone6@gmail.com', 'huranoxbyilklwae')  # 본인 계정과 비밀번호 사용.
mailServer.send_message(msg)
mailServer.quit()