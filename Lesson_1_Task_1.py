import requests as r
import json
from getpass import getpass

username = input('Введите имя пользователя')
password = getpass()

req = r.get('https://api.github.com/user/repos', auth=(username, password))
data = json.loads(req.text)

for i in range(len(data)):
    print(data[i]['name'])

#with open(username + '_repos.json', 'w') as f:
#   json.dump(data, f)
