import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def my_send_mail(msg_to, token):
    msg_from = '1007591290@qq.com'  # 发送方邮箱
    passwd = 'ciuwoerrvbjrbcge'
    
    #设置邮件内容
    #MIMEMultipart类可以放任何内容
    msg = MIMEMultipart()
    #设置邮件主题
    msg['Subject']="CSC4001 Verification"

    content="这个是字符串"
    #把内容加进去
    msg.attach(MIMEText(content,'plain','utf-8'))
    
    #发送方信息
    msg['From']=msg_from
    
    #开始发送
    
    #通过SSL方式发送，服务器地址和端口
    s = smtplib.SMTP_SSL("smtp.qq.com", 25)
    # 登录邮箱
    s.login(msg_from, passwd)
    #开始发送
    s.sendmail(msg_from, msg_to, msg.as_string())
    print("邮件发送成功")

# source: https://blog.csdn.net/MATLAB_matlab/article/details/106240424