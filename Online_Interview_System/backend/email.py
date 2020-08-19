from django.core.mail import send_mail
from .models import Interviewee

TIME_OPTIONS = [
    '周六上午9:30-10:30',
    '周六下午2:30-3:30',
    '周日上午9:30-10:30'
]

EMAIL_FROM = "jobs@interview.ustc.edu.cn"
ITVE_SUBJECT = "面试通知"
ITVE_MESSAGE = "\
尊敬的{}：\n\
    您好！欢迎您参加interview.com公司的在线面试，面试时间为{}，届时请点击以下链接进入面试页面：\n\n{}"
ITVE_URL_PAT = "http://106.14.227.202/#/interviewee/{}/"

ITVR_SUBJECT = "新面试安排"
ITVR_MESSAGE = "\
尊敬的面试官：\n\
    刚刚为您新增了面试安排。面试编号为{}，时间为{}，请查收。"

def room_send_email(itve, itvr, roomid, time):
    """
    Send notification emails to interviewer & interviewee
    """
    itve_url = ITVE_URL_PAT.format(roomid)
    itve_name = Interviewee.objects.get(pk=itve)
    itve_msg = ITVE_MESSAGE.format(itve_name, TIME_OPTIONS[time], itve_url)
    send_mail(ITVE_SUBJECT, itve_msg, EMAIL_FROM, [itve], fail_silently=False)

    itvr_msg = ITVR_MESSAGE.format(roomid, TIME_OPTIONS[time])
    send_mail(ITVR_SUBJECT, itvr_msg, EMAIL_FROM, [itvr], fail_silently=False)