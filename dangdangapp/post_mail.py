import os
from django.core.mail import send_mail, EmailMultiAlternatives

os.environ['DJANGO_SETTINGS_MODULE'] = 'dangdangapp.settings'

if __name__ == '__main__':

    subject, from_email, to = '注册验证', 'gethopett@sina.com', '13003838091@163.com'
    text_content = '欢迎访问注册当当，祝贺你收到了我的邮件，有幸收到我的邮件说明你及其幸运'
    html_content = '<p>感谢注册当当，<a href="http://{}/confirm/?code={}" target=blank>点我</a>，就能验证你的个人信息了，验证结束你就可以登录了！</p>'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()