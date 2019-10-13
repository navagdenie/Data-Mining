import requests as r
from getpass import getpass

username = input('Введите имя пользователя')
password = getpass()

req = r.get('https://easybacklog.com/api/', auth=(username, password))

with open('easybacklog_text.html', 'w') as f:
    f.write(req.text)
