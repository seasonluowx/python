from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr(( \
        Header(name, 'utf-8').encode(), \
        addr.encode('utf-8') if isinstance(addr, unicode) else addr))

from_addr = 'seasonluowx@126.com'
password = 'baobao871027'
to_addr = '262737197@qq.com'
smtp_server = 'smtp.126.com'

msg = MIMEText('hello, send by Python...', 'plain', 'utf-8')
msg['From'] = _format_addr(u'Python爱好者 <%s>' % from_addr)
msg['To'] = _format_addr(u'管理员 <%s>' % to_addr)
msg['Subject'] = Header(u'来自smtp……', 'utf-8').encode()

server = smtplib.SMTP(smtp_server, 25)
server.set_debuglevel(1)
server.login(from_addr, password)
server.sendmail(from_addr, [to_addr], msg.as_string())
server.quit()

# from email.mime.text import MIMEText
# import smtplib
#
# msg = MIMEText('hello, send by Python...', 'plain', 'utf-8')
# from_addr = 'seasonluowx@126.com'
# password = 'baobao871027'
# # 输入SMTP服务器地址:
# smtp_server = 'smtp.126.com'
# # 输入收件人地址:
# to_addr = '262737197@qq.com'
# server = smtplib.SMTP(smtp_server, 25) # SMTP协议默认端口是25
# server.set_debuglevel(1)
# server.login(from_addr, password)
# server.sendmail(from_addr, [to_addr], msg.as_string())
# server.quit()