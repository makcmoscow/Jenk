#!/usr/bin/python3.6
import requests
import argparse
import random
import time
parser = argparse.ArgumentParser()
#parser.add_argument('-d', type = int, default = 6, help = 'choose domain name')
parser.add_argument('list_of_logins', type = str, help = 'Перечень имен в кавычках через запятую')
args = parser.parse_args()
list_of_logins = args.list_of_logins.split(',')
log_in_cred = {'fUsername':'alexander@m-production.tv', 'fPassword' : '565ts89%w()32'}


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

def get_domains(session):
    domain_list = session.get('https://mail.m-pr.tv/postfixadmin/list.php?table=domain')
    domain_list = str(domain_list.content.decode()).split('domain=')
    domains = {}
    for y, x in enumerate(domain_list):
        if not y==0:
            domains[y]=(x.split("\'")[0])
    return domains

def create_password():
    chars = {1:'+-/*!&$#?=@<>', 2:'abcdefghijkopqrstuvwxyz', 3:'ABCDEFGHIJKLMNPQRSTUVWXYZ1234567890'}
    password = ''
    for _ in range(8):
        char = random.choice(chars[random.randint(1, 3)])
        password+=char
    return password


session = get_session(log_in_cred)
domains = get_domains(session)
for key in domains:
    print(key, ' ', domains[key])

domain = domains[int(input('Enter domain number'))]

for login in list_of_logins:
    login = login.strip()
    password = create_password()
    token = get_token(session)
    create_mailbox(session=session, token=token, login=login, domain=domain, password=password)
    print(login+'@'+domain, ' ', password)
