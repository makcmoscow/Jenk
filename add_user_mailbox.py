#!/usr/bin/python3.6
import requests
import argparse
import random
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
parser = argparse.ArgumentParser()
parser.add_argument('-d', '--domain', type = str, default = "m-production.tv", help = 'choose domain name')
parser.add_argument('list_of_logins', type = str, help = 'Перечень имен в кавычках через запятую')
parser.add_argument('-m', '--mail', type = str, default = "mproduction.tv@gmail.com", help = 'enter mailbox to send created boxes credentials')
args = parser.parse_args()
list_of_logins = args.list_of_logins.split(',')
log_in_cred = {'fUsername':'alexander@m-production.tv', 'fPassword' : '565ts89%w()32'}
domain = args.domain


def get_session(log_in_cred):
    with requests.Session() as session:
        log_in = session.post('https://mail.m-pr.tv/postfixadmin/login.php', data = log_in_cred)
        return session
def get_token(session):
    r = session.get('https://mail.m-pr.tv/postfixadmin/edit.php?table=mailbox')
    page = str(r.content)
    token = (page.split('token')[1].replace('"', '').split()[0].replace('value=', ''))
    return token

def create_mailbox(session, token, login, domain, password):
    time.sleep(1)
    form_data ={'table': 'mailbox', 'token': token, 'value[local_part]': login, 'value[domain]': domain, 'value[password]':\
        password, 'value[password2]': password, 'value[active]': '1', 'value[welcome_mail]': '1', 'submit': 'Создать ящик'}
    rr = session.post('https://mail.m-pr.tv/postfixadmin/edit.php?table=mailbox&domain=abp-finances.ru', data = form_data)


#def get_domains(session):
#    domain_list = session.get('https://mail.m-pr.tv/postfixadmin/list.php?table=domain')
#    domain_list = str(domain_list.content.decode()).split('domain=')
#    domains = {}
#    for y, x in enumerate(domain_list):
#        if not y==0:
#            domains[y]=(x.split("\'")[0])
#    return domains

def create_password():
    chars = {1:'+-/*!&$#?=@<>', 2:'abcdefghijkopqrstuvwxyz', 3:'ABCDEFGHIJKLMNPQRSTUVWXYZ1234567890'}
    password = ''
    for _ in range(8):
        char = random.choice(chars[random.randint(1, 3)])
        password+=char
    return password

def mail(args, list_of_logins, new_mailboxes):
    addr_from = "testmprtv@mail.ru" # Адресат
    addr_to = args.mail # Получатель
    password = "565ts89%w()32" # Пароль
    msg = MIMEMultipart() # Создаем сообщение
    msg['From'] = addr_from # Адресат
    msg['To'] = addr_to # Получатель
    msg['Subject'] = 'Пароли для почтовых ящиков {}'.format(args.list_of_logins) # Тема сообщения
    body = new_mailboxes
    msg.attach(MIMEText(body, 'plain')) # Добавляем в сообщение текст
    server = smtplib.SMTP('smtp.mail.ru', 587) # Создаем объект SMTP
    #server.set_debuglevel(True) # Включаем режим отладки - если отчет не нужен, строку можно закомментировать
    server.starttls() # Начинаем шифрованный обмен по TLS
    server.login(addr_from, password) # Получаем доступ
    server.send_message(msg) # Отправляем сообщение
    server.quit() # Выходим


if __name__ == '__main__':

    session = get_session(log_in_cred)
    new_mailboxes = ''
    #domains = get_domains(session)
    #for key in domains:
    #    print(key, ' ', domains[key])

    #domain = domains[int(input('Enter domain number'))]
    for login in list_of_logins:
        login = login.strip()
        password = create_password()
        token = get_token(session)
        create_mailbox(session=session, token=token, login=login, domain=domain, password=password)
        new_mailboxes += (login+'@'+domain + ' ' + password+ '\n')
    mail(args, list_of_logins, new_mailboxes)
