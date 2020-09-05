from .models import Interviewee
from email.mime.text import MIMEText
import smtplib, ssl

port = 465  # For SSL
smtp_server = "email-smtp.ap-northeast-1.amazonaws.com"
sender_email = "fandahao17@mail.ustc.edu.cn"  # Enter your address
username = 'AKIAX3SUJJO7YMLKVPWI'
password = 'BEuwtJ6h20pdOLVZ//9Qh+h7xK5OyVKL4UyHiat6s3jy'


TIME_OPTIONS = [
    '周六上午9:30-10:30',
    '周六下午2:30-3:30',
    '周日上午9:30-10:30'
]

ITVE_SUBJECT = "面试通知"
ITVE_MESSAGE = "\
尊敬的{}：\n\n\
    您好！欢迎您参加interview.com公司的在线面试，面试时间为{}，届时请点击以下链接进入面试页面：\n\n{}"
ITVE_URL_PAT = "http://106.14.227.202/#/interviewee/{}/"

def room_send_email(itve, itvr, roomid, time):
    """
    Send notification emails to interviewer & interviewee
    """
    # print("---email, type:{}, number:{}".format(type(time), time))
    url = ITVE_URL_PAT.format(roomid)
    name = Interviewee.objects.get(pk=itve)
    msg = MIMEText(ITVE_MESSAGE.format(name, TIME_OPTIONS[int(time)], url), 'plain', 'utf-8')
    msg['Subject'] = ITVE_SUBJECT
    msg['From'] = 'Jobs <fandahao17@mail.ustc.edu.cn>'
    msg['To'] = itve

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(username, password)
        server.sendmail(sender_email, [itve], msg.as_string())
